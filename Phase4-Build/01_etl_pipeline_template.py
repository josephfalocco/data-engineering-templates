"""
ETL Pipeline Template
Medallion Architecture: Bronze → Silver → Gold

Replace all [PLACEHOLDERS] with project-specific values
"""

import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# ============================================
# CONFIGURATION
# ============================================

CSV_FILE = "[SOURCE_FILE.csv]"

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "[DATABASE_NAME]"
DB_USER = "postgres"
DB_PASSWORD = "[YOUR_PASSWORD]"

# SQLAlchemy connection string (for pandas to_sql)
ENGINE = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():
    """Get psycopg2 connection for raw SQL operations"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# ============================================
# STEP 1: LOAD BRONZE (RAW DATA)
# ============================================

def load_bronze(csv_path):
    """Load raw CSV data to bronze layer - no transformations"""
    
    df = pd.read_csv(csv_path)
    
    # TODO: Select/rename columns if needed
    # df = df[['col1', 'col2', 'col3']]
    # df.columns = ['bronze_col1', 'bronze_col2', 'bronze_col3']
    
    # Clear existing data
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE bronze.[TABLE_NAME];")
        conn.commit()
    
    # Load using pandas (much faster than row-by-row)
    df.to_sql(
        name='[TABLE_NAME]',
        schema='bronze',
        con=ENGINE,
        if_exists='append',
        index=False
    )
    
    print(f"✓ Bronze layer loaded: {len(df)} rows")
    return len(df)

# ============================================
# STEP 2: TRANSFORM BRONZE TO SILVER
# ============================================

def transform_silver():
    """Transform bronze data and load to silver layer"""
    
    # Read from bronze
    df = pd.read_sql("SELECT * FROM bronze.[TABLE_NAME]", ENGINE)
    
    # ========== TRANSFORMATIONS ==========
    # TODO: Add your transformations here
    
    # Example: Clean whitespace
    # df['column_name'] = df['column_name'].str.strip()
    
    # Example: Convert data types
    # df['date_column'] = pd.to_datetime(df['date_column'])
    # df['amount_column'] = pd.to_numeric(df['amount_column'], errors='coerce')
    
    # Example: Filter invalid rows
    # df = df[df['required_column'].notna()]
    
    # Example: Standardize text
    # df['status'] = df['status'].str.upper()
    
    # ======================================
    
    # Clear and load silver
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE silver.[TABLE_NAME];")
        conn.commit()
    
    df.to_sql(
        name='[TABLE_NAME]',
        schema='silver',
        con=ENGINE,
        if_exists='append',
        index=False
    )
    
    print(f"✓ Silver layer loaded: {len(df)} rows")
    return len(df)

# ============================================
# STEP 3: POPULATE GOLD LAYER (STAR SCHEMA)
# ============================================

def populate_gold():
    """Populate dimension and fact tables from silver layer"""
    
    # Read cleaned data from silver
    df = pd.read_sql("SELECT * FROM silver.[TABLE_NAME]", ENGINE)
    
    # ========== DIMENSION 1 ==========
    # TODO: Replace with your dimension
    dim_1 = df[['[DIM1_COLUMNS]']].drop_duplicates().reset_index(drop=True)
    dim_1['[DIM1_NAME]_key'] = dim_1.index + 1  # Surrogate key
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE gold.dim_[DIM1_NAME] CASCADE;")
        conn.commit()
    
    dim_1.to_sql('dim_[DIM1_NAME]', schema='gold', con=ENGINE, if_exists='append', index=False)
    print(f"  ✓ dim_[DIM1_NAME]: {len(dim_1)} rows")
    
    # ========== DIMENSION 2 ==========
    # TODO: Repeat pattern for additional dimensions
    
    # ========== FACT TABLE ==========
    # TODO: Build fact table with foreign key lookups
    
    # Example: Merge to get surrogate keys
    # fact = df.merge(dim_1[['natural_key', 'dim1_key']], on='natural_key', how='left')
    # fact = fact[['dim1_key', 'dim2_key', 'date_key', 'measure1', 'measure2']]
    
    # with get_connection() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("TRUNCATE TABLE gold.fact_[FACT_NAME];")
    #     conn.commit()
    
    # fact.to_sql('fact_[FACT_NAME]', schema='gold', con=ENGINE, if_exists='append', index=False)
    # print(f"  ✓ fact_[FACT_NAME]: {len(fact)} rows")
    
    print("✓ Gold layer populated")

# ============================================
# RUN PIPELINE
# ============================================

if __name__ == "__main__":
    try:
        # Test connection
        with get_connection() as conn:
            print("✓ Connected to PostgreSQL successfully!\n")
        
        # Run pipeline
        load_bronze(CSV_FILE)
        transform_silver()
        populate_gold()
        
        print("\n" + "="*40)
        print("✓ ETL Pipeline complete!")
        print("="*40)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise  # Re-raise to see full traceback during development
