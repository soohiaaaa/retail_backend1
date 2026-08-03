
import duckdb

DB_FILE = "retail_warehouse.duckdb"
KAGGLE_CSV = "kaggle_retail_data.csv" # Your downloaded Kaggle file

def load_kaggle_to_duckdb():
    conn = duckdb.connect(DB_FILE)
    conn.execute("DROP TABLE IF EXISTS retail_sales;")
    
    print("Ingesting Kaggle dataset directly into warehouse database...")
    # DuckDB automatically samples the CSV schema and streams it seamlessly
    conn.execute(f"""
        CREATE TABLE retail_sales AS 
        SELECT * FROM read_csv_auto('{KAGGLE_CSV}');
    """)
    
    print(f"Loaded {conn.execute('SELECT COUNT(*) FROM retail_sales;').fetchone()[0]} rows!")
    conn.close()

if __name__ == "__main__":
    load_kaggle_to_duckdb()
