import httpx
import json
import os
from api.rag_engine import get_rag_engine

# Determine if running in Docker to reach host machine's Ollama
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "host.docker.internal")

async def parse_intent(prompt: str) -> list[str]:
    """
    Calls the local Ollama API (qwen2.5:3b) to parse natural language into a list of tables.
    Uses RAG to inject relevant context to help the small model.
    """
    engine = get_rag_engine()
    relevant_tables = engine.retrieve_context(prompt)
    
    context_hint = ""
    if relevant_tables:
        context_hint = f"\nRelevant tables based on your keywords: {', '.join(relevant_tables)}"
        
    system_prompt = (
        "You are an enterprise data architect assistant. "
        "Your only job is to extract the EXACT core database table names from the user's prompt. "
        "Do not return all tables from the context, ONLY return the primary tables the user explicitly requested. "
        "Return ONLY a valid JSON list of strings representing the table names. "
        "Do not include markdown blocks, explanations, or conversational text. "
        "Example: [\"p_dtl_tb\"]"
        f"{context_hint}"
    )
    
    payload = {
        "model": "qwen2.5:3b",
        "prompt": system_prompt + "\n\nUser Prompt: " + prompt,
        "stream": False,
        "format": "json"
    }
    
    # Try Docker host first, fallback to localhost
    urls_to_try = [
        f"http://{OLLAMA_HOST}:11434/api/generate",
        "http://localhost:11434/api/generate",
        "http://127.0.0.1:11434/api/generate"
    ]
    
    for url in urls_to_try:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "[]")
                    try:
                        tables = json.loads(response_text)
                        if isinstance(tables, list) and len(tables) > 0:
                            return tables
                    except json.JSONDecodeError:
                        pass
        except Exception:
            continue
            
    # Deterministic fallback: just pick the first most likely table if LLM completely fails
    return [relevant_tables[0]] if relevant_tables else []
