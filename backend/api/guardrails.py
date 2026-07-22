import Levenshtein
from typing import List
from backend.api.rag_engine import get_rag_engine

def enforce_schema(predicted_tables: List[str]) -> List[str]:
    """
    Takes the raw list of tables from the LLM and uses fuzzy matching
    to guarantee they exist in the actual schema, preventing hallucinations
    instantly without an LLM loop.
    """
    engine = get_rag_engine()
    actual_tables = engine.odm_tables
    
    if not actual_tables:
        # Fallback if ODM couldn't load, just return as-is
        return predicted_tables

    validated = set()
    for pt in predicted_tables:
        pt_lower = pt.lower()
        if pt_lower in actual_tables:
            validated.add(pt_lower)
        else:
            # Fuzzy match
            best_match = None
            best_dist = float('inf')
            
            for at in actual_tables:
                dist = Levenshtein.distance(pt_lower, at)
                if dist < best_dist:
                    best_dist = dist
                    best_match = at
            
            # If it's a reasonably close match (e.g. they forgot _tb or a vowel)
            if best_match and best_dist <= 5:
                validated.add(best_match)
                
    return list(validated)
