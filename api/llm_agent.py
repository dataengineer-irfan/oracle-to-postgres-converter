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
        "format": "json",
        "options": {
            "temperature": 0.0,
            "num_predict": 100,
            "top_k": 10
        }
    }
    
    # Try Docker host first, fallback to localhost. Support full ngrok URLs if provided.
    if OLLAMA_HOST.startswith("http"):
        primary_url = f"{OLLAMA_HOST.rstrip('/')}/api/generate" if not OLLAMA_HOST.endswith("generate") else OLLAMA_HOST
    else:
        primary_url = f"http://{OLLAMA_HOST}:11434/api/generate"
        
    urls_to_try = [
        primary_url,
        "http://localhost:11434/api/generate",
        "http://127.0.0.1:11434/api/generate"
    ]
    
    for url in urls_to_try:
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                headers = {"ngrok-skip-browser-warning": "true"}
                response = await client.post(url, json=payload, headers=headers)
                
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

async def generate_sql_from_intent(prompt: str, schema_context: str = "") -> str:
    """
    Calls the local Ollama API to translate natural language into a valid PostgreSQL statement.
    """
    engine = get_rag_engine()
    relevant_tables = engine.retrieve_context(prompt)
    
    context_hint = ""
    if relevant_tables:
        context_hint = f"\nRelevant tables based on your keywords: {', '.join(relevant_tables)}"
        if schema_context:
            context_hint += f"\n{schema_context}"
            
        join_context = engine.retrieve_join_context(relevant_tables)
        if join_context:
            context_hint += f"\n{join_context}"
        
    system_prompt = (
        "You are an expert PostgreSQL Database Administrator. "
        "Your job is to translate the user's natural language request into a single, valid PostgreSQL SQL statement. "
        "CRITICAL INSTRUCTIONS: "
        "1. Do not include any explanations, greetings, or markdown formatting (no ```sql). "
        "2. NEVER ask for more information, clarification, or follow-up questions. "
        "3. ALWAYS prefix EVERY table name with the 'provider.' schema (e.g., provider.p_mcare_tb). "
        "4. NEVER invent or hallucinate column names. ONLY use the exact column names provided in the context below. "
        "5. If the user's request is vague or missing details, MAKE YOUR BEST GUESS and write a generic SQL query anyway. "
        "6. Output ONLY the raw SQL string ending with a semicolon. If you output anything other than SQL, the system will crash."
        "Example output: UPDATE provider.p_dtl_tb SET p_dba_nam = 'testname' WHERE p_sys_id = 3163961;"
        f"{context_hint}"
    )
    
    payload = {
        "model": "qwen2.5:3b",
        "prompt": system_prompt + "\n\nUser Request: " + prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 300,
            "top_k": 10
        }
    }
    

    if OLLAMA_HOST.startswith("http"):
        primary_url = f"{OLLAMA_HOST.rstrip('/')}/api/generate" if not OLLAMA_HOST.endswith("generate") else OLLAMA_HOST
    else:
        primary_url = f"http://{OLLAMA_HOST}:11434/api/generate"
        
    urls_to_try = [
        primary_url,
        "http://localhost:11434/api/generate",
        "http://127.0.0.1:11434/api/generate"
    ]
    
    for url in urls_to_try:
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                headers = {"ngrok-skip-browser-warning": "true"}
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    sql_text = data.get("response", "").strip()
                    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
                    if sql_text:
                        return sql_text
                    else:
                        print(f"LLM returned empty string for URL: {url}")
                else:
                    print(f"LLM returned status {response.status_code} for URL: {url}")
        except Exception as e:
            print(f"LLM connection error for {url}: {e}")
            continue
            
    return "-- Error: Could not generate SQL from the AI service."
