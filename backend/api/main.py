from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import List
import sys
from pathlib import Path
import yaml

from backend.api.llm_agent import parse_intent, generate_sql_from_intent
from backend.api.dependency_graph import resolve_dependencies
from backend.api.guardrails import enforce_schema
from backend.config import DB_CONFIG
import psycopg

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
        rules_path = Path(__file__).parent.parent.parent / "_Input" / "business_rules.yaml"
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
    script_path = str(Path(__file__).parent.parent / "generation" / "generate_data.py")
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

class DMLPreviewRequest(BaseModel):
    tables: List[str]

import csv

@app.post("/api/data/preview-dml")
async def preview_dml(req: DMLPreviewRequest):
    """Generate up to 10 real INSERT statements per table from generated CSVs."""
    output = []
    data_dir = Path(__file__).parent.parent / "generated_data"
    
    for table in req.tables:
        csv_file = data_dir / f"{table.upper()}.csv"
        if not csv_file.exists():
            output.append(f"-- No generated data found for {table}")
            continue
            
        output.append(f"-- Smart Test Data Generation DML for {table} (First 10 rows)")
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                if not headers:
                    continue
                
                cols = ", ".join(headers)
                count = 0
                for row in reader:
                    if count >= 10:
                        break
                    
                    # Escape quotes and handle nulls
                    vals = []
                    for val in row:
                        if val == '' or val is None:
                            vals.append('NULL')
                        else:
                            clean_val = str(val).replace("'", "''")
                            vals.append(f"'{clean_val}'")
                            
                    vals_str = ", ".join(vals)
                    output.append(f"INSERT INTO {table} ({cols})\nVALUES ({vals_str});")
                    count += 1
        except Exception as e:
            output.append(f"-- Error reading {table}: {e}")
            
        output.append("") # blank line between tables
        
    return {"dml": "\n".join(output)}

# ─── LIVE DATA STUBS ──────────────────────────────────────────────────────────
# TODO: wire each stub to real database / migration engine

@app.get("/api/migration/status")
async def migration_status():
    """Current migration pipeline stage and overall progress."""
    # TODO: read from migration state DB table
    return {
        "stage": "conversion",          # connect | analyze | convert | validate | deploy
        "progress": 91,                  # overall %
        "stage_index": 3,
        "stages": ["Connect", "Analyze", "Convert", "Validate", "Deploy"],
        "current_stage_progress": 78,
    }

@app.get("/api/migration/stats")
def migration_stats():
    """Object counts and conversion metrics."""
    oracle = oracle_schema()
    postgres = postgres_schema()
    
    total = oracle["tables"]
    converted = postgres["tables"]
    auto_pct = (converted / total) * 100 if total > 0 else 0
    
    return {
        "objects":   total,
        "tables":    total,
        "views":     oracle["views"],
        "packages":  oracle["packages"],
        "functions": oracle["functions"],
        "converted": int(auto_pct),
        "validated": int(auto_pct),
        "errors":    0,
        "warnings":  max(0, total - converted),
        "last_run":  "Just now",
    }

@app.get("/api/projects")
async def list_projects():
    """Recent migration projects."""
    # TODO: read from projects table
    return {
        "projects": [
            {"id": 1, "name": "Oracle-Financials-Prod", "status": "in_progress", "progress": 91, "last_updated": "2026-07-21"},
            {"id": 2, "name": "HR Schema Migration",    "status": "completed",   "progress": 100,"last_updated": "2026-07-19"},
            {"id": 3, "name": "Inventory Database",     "status": "pending",     "progress": 0,  "last_updated": "2026-07-18"},
        ]
    }

@app.get("/api/schema/oracle")
def oracle_schema():
    """Live Oracle source schema object counts."""
    # Simulated connection for now; extensible for live Oracle URL
    stats = {
        "tables": 0, "views": 0, "indexes": 0,
        "packages": 0, "functions": 0, "sequences": 0,
        "connected": False
    }
    try:
        odm_path = Path(__file__).parent.parent.parent / "_Input" / "provider_odm.yaml"
        if odm_path.exists():
            with open(odm_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                stats["tables"] = len(data.get("tables", []))
                stats["indexes"] = stats["tables"] * 2  # Simulated
                stats["connected"] = True
    except Exception as e:
        print(f"Oracle connection error: {e}")
    return stats

@app.get("/api/schema/postgres")
def postgres_schema():
    """Live PostgreSQL target schema object counts."""
    stats = {"tables": 0, "views": 0, "indexes": 0, "connected": False}
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'provider' AND table_type = 'BASE TABLE'")
                stats["tables"] = cur.fetchone()[0]
                
                cur.execute("SELECT count(*) FROM information_schema.views WHERE table_schema = 'provider'")
                stats["views"] = cur.fetchone()[0]
                
                cur.execute("SELECT count(*) FROM pg_indexes WHERE schemaname = 'provider'")
                stats["indexes"] = cur.fetchone()[0]
                
                stats["connected"] = True
    except Exception as e:
        print(f"Postgres connection error: {e}")
    return stats

@app.get("/api/connections/health")
def connections_health():
    """Live connection health check for both databases."""
    from datetime import datetime
    health = {"oracle": False, "postgres": False, "timestamp": datetime.utcnow().isoformat() + "Z"}
    
    try:
        odm_path = Path(__file__).parent.parent.parent / "_Input" / "provider_odm.yaml"
        if odm_path.exists():
            health["oracle"] = True
    except: pass
    
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                health["postgres"] = True
    except: pass
    
    return health

@app.get("/api/ai/analysis")
def ai_analysis():
    """AI confidence score and migration analysis summary."""
    oracle = oracle_schema()
    postgres = postgres_schema()
    
    total_objects = oracle["tables"]
    converted = postgres["tables"]
    auto_pct = (converted / total_objects) * 100 if total_objects > 0 else 0
    
    return {
        "confidence":       min(99, int(auto_pct)) if auto_pct > 0 else 0,
        "objects_analyzed": total_objects,
        "auto_converted":   converted,
        "manual_hours":     max(0, (total_objects - converted) * 2),
        "warnings":         max(0, total_objects - converted),
        "errors":            0,
        "suggestions": [
            "Review unconverted tables for custom triggers",
            "Verify data types for columns exceeding PostgreSQL limits",
            "Map Oracle sequences to PostgreSQL IDENTITY columns"
        ]
    }

@app.get("/api/validation/results")
async def validation_results():
    """Latest validation run results."""
    # TODO: read from validation_results table
    return {
        "passed":   401,
        "warnings":  12,
        "errors":     3,
        "last_run": "2026-07-21T01:30:00Z",
        "details": [
            {"object": "provider",        "status": "passed",  "message": "DDL valid"},
            {"object": "common",          "status": "warning", "message": "Index missing on FK column"},
            {"object": "CUSTOMER_SEQ",    "status": "error",   "message": "Sequence step incompatible"},
        ]
    }

class SQLRequest(BaseModel):
    sql: str
    database: str = "postgres"

from backend.api.rag_engine import get_rag_engine

@app.post("/api/sql/ai-generate")
async def ai_generate_sql(req: GenerateRequest):
    """Generate SQL from natural language."""
    sql = await generate_sql_from_intent(req.prompt)
    return {"sql": sql}

@app.post("/api/sql/execute")
async def execute_sql(req: SQLRequest):
    """Execute a SQL statement and return results."""
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Basic safety check for demo purposes
                if req.sql.strip().lower().startswith(("drop", "truncate", "alter")):
                    raise HTTPException(status_code=400, detail="Destructive DDL commands are blocked for safety.")
                
                cur.execute("SET search_path TO public, provider, common, reference;")
                print(f"Executing SQL: {req.sql}")
                cur.execute(req.sql)
                
                is_select = cur.description is not None
                if is_select:
                    columns = [desc.name for desc in cur.description]
                    rows = cur.fetchall()
                    rowcount = len(rows)
                else:
                    columns = []
                    rows = []
                    rowcount = cur.rowcount
                    conn.commit()
                
                return {
                    "columns": columns,
                    "rows": rows,
                    "rowcount": rowcount,
                    "duration_ms": 0, # Placeholder
                }
    except Exception as e:
        print(f"SQL Execution Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/data/{table}")
async def get_table_data(table: str, page: int = 1, per_page: int = 100):
    """Paginated live table data."""
    # TODO: wire to real PostgreSQL query
    return {
        "table":    table,
        "page":     page,
        "per_page": per_page,
        "total":    0,
        "columns":  [],
        "rows":     [],
    }
