import os
import psycopg2

def load_schemas():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="password"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Creating schemas...")
    cur.execute("CREATE SCHEMA IF NOT EXISTS provider;")
    cur.execute("CREATE SCHEMA IF NOT EXISTS common;")
    
    ddl_dir = r"C:\Users\affra\Documents\Oracle to Postgre\oracle_to_postgres\output\ddl"
    
    # 1. Execute all table creations
    for file in os.listdir(ddl_dir):
        if file.endswith(".sql") and file != "all_fk_constraints.sql":
            print(f"Executing {file}...")
            with open(os.path.join(ddl_dir, file), "r", encoding="utf-8") as f:
                sql = f.read()
                try:
                    cur.execute(sql)
                except Exception as e:
                    print(f"Error executing {file}: {e}")
                    
    # 2. Execute foreign keys
    fk_file = os.path.join(ddl_dir, "all_fk_constraints.sql")
    if os.path.exists(fk_file):
        print(f"Executing {os.path.basename(fk_file)}...")
        with open(fk_file, "r", encoding="utf-8") as f:
            sql = f.read()
            try:
                cur.execute(sql)
            except Exception as e:
                print(f"Error executing FK constraints: {e}")
                
    cur.close()
    conn.close()
    print("Schema load complete!")

if __name__ == "__main__":
    load_schemas()
