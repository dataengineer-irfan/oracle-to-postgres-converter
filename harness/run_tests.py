import asyncio
import json
import csv
import time
from pathlib import Path
import httpx
import websockets

API_URL = "http://localhost:8080"
WS_URL = "ws://localhost:8080/ws/logs"

async def wait_for_completion():
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                msg = await ws.recv()
                if "Pipeline finished" in msg:
                    return True
                if "Failed" in msg and "Error" in msg:
                    return False
    except Exception as e:
        print(f"  [!] WebSocket error: {e}")
        return False

async def run_test_harness():
    harness_dir = Path(__file__).parent
    questions_file = harness_dir / "questions.json"
    results_file = harness_dir / "test_results.csv"
    
    with open(questions_file, "r") as f:
        questions = json.load(f)

    results = []
    
    print(f"Starting automated test harness for {len(questions)} questions...\n")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, prompt in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] Testing: '{prompt}'")
            start_time = time.time()
            
            # Step 1: Parse Intent
            try:
                parse_resp = await client.post(f"{API_URL}/parse-intent", json={"prompt": prompt})
                parse_resp.raise_for_status()
                data = parse_resp.json()
                tables = data.get("plan", [])
                print(f"  -> Identified {len(tables)} tables: {tables[:3]}{'...' if len(tables) > 3 else ''}")
            except Exception as e:
                print(f"  -> [ERROR] Parsing failed: {e}")
                results.append({
                    "Question": prompt,
                    "Status": "Failed (Parsing)",
                    "Tables": "",
                    "Duration(s)": round(time.time() - start_time, 2)
                })
                continue
                
            if not tables:
                print("  -> [SKIP] No tables identified.")
                results.append({
                    "Question": prompt,
                    "Status": "Skipped (No tables)",
                    "Tables": "None",
                    "Duration(s)": round(time.time() - start_time, 2)
                })
                continue
                
            # Step 2: Execute Pipeline (generate exactly 2 rows for speed)
            try:
                exec_resp = await client.post(f"{API_URL}/execute", json={"tables": tables, "rows": 2})
                exec_resp.raise_for_status()
                
                # Wait for WebSocket to signal completion
                success = await asyncio.wait_for(wait_for_completion(), timeout=120.0)
                
                duration = round(time.time() - start_time, 2)
                status = "Success" if success else "Failed (Generation)"
                print(f"  -> {status} in {duration}s")
                
                results.append({
                    "Question": prompt,
                    "Status": status,
                    "Tables": ", ".join(tables),
                    "Duration(s)": duration
                })
            except Exception as e:
                print(f"  -> [ERROR] Execution failed: {e}")
                results.append({
                    "Question": prompt,
                    "Status": "Failed (Timeout/Error)",
                    "Tables": ", ".join(tables),
                    "Duration(s)": round(time.time() - start_time, 2)
                })
                
    # Save Results
    with open(results_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Question", "Status", "Tables", "Duration(s)"])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n✅ Test harness completed! Results saved to {results_file}")

if __name__ == "__main__":
    asyncio.run(run_test_harness())
