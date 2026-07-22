import os
import csv
from pathlib import Path
from db.db import DatabaseManager
from config import DB_CONFIG
import re

def main():
    db = DatabaseManager(DB_CONFIG)
    conn = db.connect()
    
    print("Creating reference schema...")
    db.execute("DROP SCHEMA IF EXISTS reference CASCADE;")
    db.execute("CREATE SCHEMA reference;")
    
    print("Loading and modifying DDL...")
    ddl_path = Path("_Input/referance_ddl/provider_system_reference_ddl.sql")
    with open(ddl_path, "r", encoding="utf-8") as f:
        ddl_content = f.read()
        
    # Replace provider schema with reference schema
    ddl_content = re.sub(r'SET search_path TO provider;', 'SET search_path TO reference;', ddl_content, flags=re.IGNORECASE)
    ddl_content = re.sub(r'CREATE TABLE provider\.', 'CREATE TABLE reference.', ddl_content, flags=re.IGNORECASE)
    
    print("Executing DDL...")
    db.execute(ddl_content)
    
    data_dir = Path("_Input/referance_data")
    for csv_file in data_dir.glob("*.csv"):
        # Extract table name from filename e.g. provider_r_vv_tb.csv -> r_vv_tb
        table_name = csv_file.stem
        if table_name.startswith("provider_"):
            table_name = table_name[len("provider_"):]
            
        print(f"Loading data into reference.{table_name} from {csv_file.name}...")
        
        with open(csv_file, "r", encoding="windows-1252") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                continue
                
            rows = list(reader)
            if not rows:
                continue
                
            cols = ", ".join([h.lower() for h in headers])
            placeholders = ", ".join(["%s"] * len(headers))
            
            insert_sql = f"INSERT INTO reference.{table_name} ({cols}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
            
            value_rows = []
            for row in rows:
                val_tuple = tuple(None if row[h] == '' else row[h] for h in headers)
                value_rows.append(val_tuple)
                
            with conn.cursor() as cur:
                cur.executemany(insert_sql, value_rows)
            conn.commit()
            
        print(f"Loaded {len(rows)} rows into reference.{table_name}.")
        
    print("Done loading reference data.")

if __name__ == "__main__":
    main()
