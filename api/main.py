from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import List
import sys
from pathlib import Path

from api.llm_agent import parse_intent
from api.dependency_graph import resolve_dependencies
from api.guardrails import enforce_schema

app = FastAPI(title="Smart Test Data Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

class ExecutionRequest(BaseModel):
    tables: List[str]
    rows: int = 50

execution_logs = []

import yaml

def apply_business_rules(tables: set[str]) -> set[str]:
    expanded_tables = set(tables)
    try:
        rules_path = Path(__file__).parent.parent / "_Input" / "business_rules.yaml"
        if rules_path.exists():
            with open(rules_path, "r", encoding="utf-8") as f:
                rules = yaml.safe_load(f)
                required_children = rules.get("required_children", {})
                
                for table in tables:
                    children = required_children.get(table, [])
                    for child in children:
                        expanded_tables.add(child)
    except Exception as e:
        print(f"Error loading business rules: {e}")
    return expanded_tables

@app.post("/parse-intent")
async def parse_intent_endpoint(req: GenerateRequest):
    raw_tables = await parse_intent(req.prompt)
    validated_tables = enforce_schema(raw_tables)
    
    # Apply Business Rules to inject required children (e.g., Addresses for Providers)
    expanded_tables = apply_business_rules(validated_tables)
    
    final_plan = resolve_dependencies(expanded_tables)
    return {"plan": final_plan}

async def run_data_generator(tables: List[str], rows: int):
    global execution_logs
    execution_logs.clear()
    execution_logs.append(f"Starting data generation pipeline for {len(tables)} tables...")
    
    # Run generate_data.py inside the container natively
    script_path = str(Path(__file__).parent.parent / "generate_data.py")
    tables_arg = ",".join(tables)
    
    import random
    dynamic_seed = str(random.randint(1, 999999))
    
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, script_path, "--rows", str(rows), "--tables", tables_arg, "--no-truncate", "--seed", dynamic_seed,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            text = line.decode('utf-8').rstrip()
            if text:
                execution_logs.append(text)
                
        await process.wait()
        execution_logs.append(f"Pipeline finished with code {process.returncode}")
    except Exception as e:
        execution_logs.append(f"Execution Error: {str(e)}")
        execution_logs.append("Pipeline finished with code 1")

@app.post("/execute")
async def execute_generation(req: ExecutionRequest):
    asyncio.create_task(run_data_generator(req.tables, req.rows))
    return {"status": "started", "tables_to_generate": req.tables, "target_rows": req.rows}

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    last_idx = 0
    try:
        while True:
            if last_idx < len(execution_logs):
                new_logs = execution_logs[last_idx:]
                for log in new_logs:
                    await websocket.send_text(log)
                last_idx = len(execution_logs)
            await asyncio.sleep(0.5)
    except:
        pass
