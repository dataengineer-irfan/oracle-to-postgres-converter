import asyncio
from api.rag_engine import get_rag_engine

engine = get_rag_engine()
prompt = 'Delete the record from p_lic_cert_tb where the license number is LIC-9999'
relevant_tables = engine.retrieve_context(prompt)
schema_context = engine.retrieve_schema_context(relevant_tables)
context_hint = f'\nRelevant tables based on your keywords: ' + ', '.join(relevant_tables)
if schema_context: context_hint += f'\n{schema_context}'
system_prompt = "You are an expert PostgreSQL Database Administrator. Your job is to translate the user's natural language request into a single, valid PostgreSQL SQL statement. Do not include any explanations, markdown formatting, or SQL block backticks. Output ONLY the raw SQL string ending with a semicolon. Example output: UPDATE p_dtl_tb SET p_dba_nam = 'testname' WHERE p_sys_id = 3163961;" + context_hint
full_prompt = system_prompt + '\n\nUser Request: ' + prompt

print(f'Total length of prompt: {len(full_prompt)} characters')
print('=== EXACT PROMPT ===')
print(full_prompt)
