"""
ETL Pipeline Template
Medallion Architecture: Bronze → Silver → Gold

Replace all [PLACEHOLDERS] with project-specific values
"""

import pandas as pd
import psycopg2

# ============================================
# CONFIGURATION
# ============================================

CSV_FILE = "[SOURCE_FILE.csv]"

DB_HOST = "localhost"
DB_NAME = "[DATABASE_NAME]"
DB_USER = "postgres"
DB_PASSWORD = "[YOUR_PASSWORD]"

# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# ============================================
# STEP 1: LOAD BRONZE (RAW DATA)
# ============================================

def load_bronze(csv_path):
    """Load raw CSV data to bronze layer"""
    
    # TODO: Update column list based on source file
    df = pd.read_csv(csv_path)
    
    # TODO: Select and rename columns for bronze table
    # df = df[['col1', 'col2', 'col3']]
    # df.columns = ['bronze_col1', 'bronze_col2', 'bronze_col3']
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("TRUNCATE TABLE bronze.[TABLE_NAME];")
    
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO bronze.[TABLE_NAME] ([COLUMNS])
            VALUES ([PLACEHOLDERS])
        """, (tuple(row)))
    
    conn.commit()
    row_count = len(df)
    cur.close()
    conn.close()
    
    print(f"✓ Bronze layer loaded: {row_count} rows")
    return row_count

# ============================================
# STEP 2: TRANSFORM BRONZE TO SILVER
# ============================================

def transform_silver():
    """Transform bronze data and load to silver layer"""
    
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM bronze.[TABLE_NAME]", conn)
    
    # TODO: Add transformations
    # - Data cleaning
    # - Type conversions
    # - Column splitting/parsing
    # - Filtering
    
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE silver.[TABLE_NAME];")
    
    # TODO: Insert transformed data
    
    conn.commit()
    row_count = len(df)
    cur.close()
    conn.close()
    
    print(f"✓ Silver layer loaded: {row_count} rows")
    return row_count

# ============================================
# STEP 3: POPULATE GOLD LAYER (STAR SCHEMA)
# ============================================

def populate_gold():
    """Populate dimension and fact tables from silver layer"""
    
    conn = get_connection()
    cur = conn.cursor()
    
    df = pd.read_sql("SELECT * FROM silver.[TABLE_NAME]", conn)
    
    # TODO: Populate each dimension table
    # TODO: Build lookup dictionaries for foreign keys
    # TODO: Populate fact table with foreign key lookups
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("✓ Gold layer populated")

# ============================================
# RUN PIPELINE
# ============================================

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✓ Connected to PostgreSQL successfully!")
        conn.close()
        
        load_bronze(CSV_FILE)
        transform_silver()
        populate_gold()
        
        print("\n✓ ETL Pipeline complete!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
