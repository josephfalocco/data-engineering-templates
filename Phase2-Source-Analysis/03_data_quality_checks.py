# =============================================================================
# 03_data_quality_checks.py
# Purpose: Generic data quality checks applicable to any dataset
# Phase: Discovery / Source System Analysis
# =============================================================================

import pandas as pd

# =============================================================================
# CONFIGURATION - Update these variables for your project
# =============================================================================

# TODO: Update with your source file path
INPUT_FILE = "your_source_file.csv"

# TODO: Update with your primary key column(s) - should be unique per row
# Can be a single column name (string) or multiple columns (list)
# Set to None if no primary key exists
PRIMARY_KEY = "id"  # or ["col1", "col2"] for composite key

# TODO: Update with columns that should NEVER be null
REQUIRED_COLUMNS = [
    "column1",
    "column2",
    "column3"
]

# TODO: Update with date columns to check formatting
DATE_COLUMNS = [
    "date_column1",
    "date_column2"
]

# TODO: Update with numeric columns to check for outliers/ranges
NUMERIC_COLUMNS = [
    "amount",
    "quantity"
]

# TODO: Update with categorical columns to check cardinality
CATEGORICAL_COLUMNS = [
    "status",
    "category",
    "type"
]

# =============================================================================
# LOAD DATA
# =============================================================================

print("Loading data...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded: {INPUT_FILE}")
print(f"Shape: {len(df):,} rows x {len(df.columns)} columns")

print("\n" + "=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)

# =============================================================================
# CHECK 1: Primary Key Uniqueness
# =============================================================================
print("\n1. PRIMARY KEY UNIQUENESS")
print("-" * 40)

if PRIMARY_KEY:
    key_cols = [PRIMARY_KEY] if isinstance(PRIMARY_KEY, str) else PRIMARY_KEY
    
    # Verify columns exist
    missing_cols = [c for c in key_cols if c not in df.columns]
    if missing_cols:
        print(f"⚠️  Columns not found: {missing_cols}")
    else:
        total_rows = len(df)
        unique_keys = df[key_cols].drop_duplicates().shape[0]
        duplicate_count = total_rows - unique_keys
        
        if duplicate_count == 0:
            print(f"✓ Primary key is unique ({unique_keys:,} unique values)")
        else:
            print(f"⚠️  DUPLICATES FOUND: {duplicate_count:,} duplicate rows")
            print(f"   Total rows: {total_rows:,}")
            print(f"   Unique keys: {unique_keys:,}")
else:
    print("Skipped - no primary key configured")

# =============================================================================
# CHECK 2: Required Columns (Null Check)
# =============================================================================
print("\n\n2. REQUIRED COLUMNS - NULL CHECK")
print("-" * 40)

for col in REQUIRED_COLUMNS:
    if col in df.columns:
        null_count = df[col].isna().sum()
        null_pct = (null_count / len(df) * 100)
        status = "✓" if null_count == 0 else "⚠️"
        print(f"{status} {col}: {null_count:,} nulls ({null_pct:.1f}%)")
    else:
        print(f"⚠️  {col}: Column not found!")

# =============================================================================
# CHECK 3: Date Column Validation
# =============================================================================
print("\n\n3. DATE COLUMNS - FORMAT CHECK")
print("-" * 40)

for col in DATE_COLUMNS:
    if col in df.columns:
        print(f"\n{col}:")
        print(f"   Sample values: {df[col].head(5).tolist()}")
        
        # Try to parse as date
        try:
            parsed = pd.to_datetime(df[col], errors='coerce')
            unparseable = parsed.isna().sum() - df[col].isna().sum()
            if unparseable == 0:
                print(f"   ✓ All values parseable as dates")
                print(f"   Date range: {parsed.min()} to {parsed.max()}")
            else:
                print(f"   ⚠️  {unparseable:,} values could not be parsed as dates")
        except Exception as e:
            print(f"   ⚠️  Error parsing dates: {e}")
    else:
        print(f"⚠️  {col}: Column not found!")

# =============================================================================
# CHECK 4: Numeric Column Validation
# =============================================================================
print("\n\n4. NUMERIC COLUMNS - RANGE & OUTLIERS")
print("-" * 40)

for col in NUMERIC_COLUMNS:
    if col in df.columns:
        print(f"\n{col}:")
        
        # Convert to numeric if needed
        numeric_series = pd.to_numeric(df[col], errors='coerce')
        non_numeric = numeric_series.isna().sum() - df[col].isna().sum()
        
        if non_numeric > 0:
            print(f"   ⚠️  {non_numeric:,} non-numeric values found")
        
        # Basic stats
        print(f"   Min: {numeric_series.min()}")
        print(f"   Max: {numeric_series.max()}")
        print(f"   Mean: {numeric_series.mean():.2f}")
        print(f"   Median: {numeric_series.median():.2f}")
        
        # Check for negatives (may or may not be valid)
        negative_count = (numeric_series < 0).sum()
        print(f"   Negative values: {negative_count:,}")
        
        # Check for zeros
        zero_count = (numeric_series == 0).sum()
        print(f"   Zero values: {zero_count:,}")
    else:
        print(f"⚠️  {col}: Column not found!")

# =============================================================================
# CHECK 5: Categorical Column Cardinality
# =============================================================================
print("\n\n5. CATEGORICAL COLUMNS - CARDINALITY")
print("-" * 40)

for col in CATEGORICAL_COLUMNS:
    if col in df.columns:
        unique_count = df[col].nunique()
        null_count = df[col].isna().sum()
        print(f"\n{col}:")
        print(f"   Unique values: {unique_count:,}")
        print(f"   Null values: {null_count:,}")
        
        # Show value distribution (top 10)
        print(f"   Top values:")
        value_counts = df[col].value_counts().head(10)
        for val, count in value_counts.items():
            pct = count / len(df) * 100
            print(f"      {val}: {count:,} ({pct:.1f}%)")
    else:
        print(f"⚠️  {col}: Column not found!")

# =============================================================================
# CHECK 6: Duplicate Rows
# =============================================================================
print("\n\n6. DUPLICATE ROWS")
print("-" * 40)

full_duplicates = df.duplicated().sum()
print(f"Fully duplicate rows: {full_duplicates:,}")

if full_duplicates > 0:
    print(f"⚠️  {full_duplicates:,} rows are exact duplicates of other rows")
else:
    print("✓ No exact duplicate rows found")

# =============================================================================
# CHECK 7: Overall Completeness
# =============================================================================
print("\n\n7. OVERALL COMPLETENESS")
print("-" * 40)

total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isna().sum().sum()
completeness_pct = ((total_cells - missing_cells) / total_cells) * 100

print(f"Total cells: {total_cells:,}")
print(f"Missing cells: {missing_cells:,}")
print(f"Completeness: {completeness_pct:.2f}%")

# Columns with most missing values
print("\nColumns with missing values:")
missing_by_col = df.isna().sum()
missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)

if len(missing_by_col) == 0:
    print("   ✓ No missing values in any column!")
else:
    for col, count in missing_by_col.items():
        pct = count / len(df) * 100
        print(f"   {col}: {count:,} ({pct:.1f}%)")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("DATA QUALITY CHECKS COMPLETE")
print("=" * 60)
