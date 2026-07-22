import os
import pandas as pd
import json

def analyze_data():
    data_dir = r"C:\Users\affra\Documents\Oracle to Postgre\oracle_to_postgres\temp\extracted_data\Data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    
    analysis_results = {}
    
    for file in csv_files:
        table_name = file.replace("_DATA_TABLE.csv", "").lower()
        file_path = os.path.join(data_dir, file)
        
        try:
            # Only read the first 1000 rows for quick analysis
            df = pd.read_csv(file_path, nrows=1000)
            
            table_stats = {
                "num_columns": len(df.columns),
                "columns": {}
            }
            
            for col in df.columns:
                col_name = col.lower()
                unique_values = df[col].dropna().unique()
                null_count = df[col].isnull().sum()
                
                # Check for categorical columns (few unique values relative to row count)
                # Or just collect unique values if less than 15
                if len(unique_values) > 0 and len(unique_values) <= 15:
                    table_stats["columns"][col_name] = {
                        "type": "categorical",
                        "values": unique_values.tolist(),
                        "null_ratio": float(null_count) / len(df)
                    }
            
            if table_stats["columns"]:
                analysis_results[table_name] = table_stats
                
        except Exception as e:
            print(f"Error reading {file}: {e}")
            
    with open(r"C:\Users\affra\Documents\Oracle to Postgre\oracle_to_postgres\temp\data_analysis.json", "w") as f:
        json.dump(analysis_results, f, indent=4)

if __name__ == "__main__":
    analyze_data()
