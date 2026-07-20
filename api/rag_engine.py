import yaml
import re
from pathlib import Path

class RAGEngine:
    def __init__(self, glossary_path: Path, odm_path: Path):
        self.glossary = {}
        self.odm_tables = set()
        self.ldm_to_tables = {} # Maps LDM entity name -> List of physical tables
        self.table_descriptions = {} # Maps table_name -> description
        
        # Load ODM first to build the LDM -> Table mapping
        self._load_odm(odm_path)
        self._load_glossary(glossary_path)
        
    def _load_odm(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for tbl in data.get("tables", []):
                    table_name = tbl.get("table_name", "").lower()
                    if table_name:
                        self.odm_tables.add(table_name)
                        desc = tbl.get("description", "").lower()
                        self.table_descriptions[table_name] = desc
                        
                    ldm_entity = tbl.get("maps_to_ldm_entity", "")
                    if ldm_entity:
                        ldm_lower = ldm_entity.lower()
                        if ldm_lower not in self.ldm_to_tables:
                            self.ldm_to_tables[ldm_lower] = []
                        self.ldm_to_tables[ldm_lower].append(table_name)
        except Exception:
            pass

    def _load_glossary(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                for term in data.get("terms", []):
                    term_name = term.get("term", "").lower()
                    
                    related_ldms = term.get("related_ldm_entities", [])
                    resolved_tables = []
                    for ldm in related_ldms:
                        resolved_tables.extend(self.ldm_to_tables.get(ldm.lower(), []))
                        
                    self.glossary[term_name] = resolved_tables
        except Exception:
            pass

    def retrieve_context(self, prompt: str) -> list[str]:
        prompt_lower = prompt.lower()
        matched_tables = set()
        
        # 1. Match against Business Glossary terms
        for term, tables in self.glossary.items():
            if term in prompt_lower:
                for t in tables:
                    matched_tables.add(t)
                    
        # 2. Match against Table names directly and their descriptions
        for t in self.odm_tables:
            core_name = re.sub(r"_(tb|tn|tx)$", "", t)
            core_name_spaces = core_name.replace("_", " ")
            if core_name in prompt_lower or core_name_spaces in prompt_lower:
                matched_tables.add(t)
                
            # Full text search on description as fallback
            desc = self.table_descriptions.get(t, "")
            # Only match if description contains words from prompt
            # We look for significant nouns like "address", "bank", etc.
            words = [w for w in prompt_lower.split() if len(w) > 3 and w not in ["create", "generate", "record", "records", "table", "tables", "with", "that", "this", "some"]]
            for w in words:
                if w in desc:
                    matched_tables.add(t)
                
        # Ensure deterministic order, with core tables prioritized
        matched_list = sorted(list(matched_tables))
        
        # Prioritize the core Provider table so it is chosen by the LLM or fallback
        if "p_dtl_tb" in matched_list:
            matched_list.remove("p_dtl_tb")
            matched_list.insert(0, "p_dtl_tb")
            
        return matched_list

# Singleton instance initialized lazily
_engine = None

def get_rag_engine() -> RAGEngine:
    global _engine
    if _engine is None:
        base_dir = Path(__file__).parent.parent
        _engine = RAGEngine(
            base_dir / "_Input" / "provider_business_glossary.yaml",
            base_dir / "_Input" / "provider_odm.yaml"
        )
    return _engine
