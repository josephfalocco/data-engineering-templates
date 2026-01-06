# =============================================================================
# 01_explore_data.py
# Purpose: Initial exploration of source data for data warehouse project
# Phase: Discovery / Source System Analysis
# =============================================================================

import pandas as pd

# =============================================================================
# CONFIGURATION - Update these variables for your project
# =============================================================================

# TODO: Update with your source file path
INPUT_FILE = "your_source_file.csv"

# TODO: Update with a key categorical column to analyze unique values
# Examples: "Account", "Category", "Customer_ID", "Product_Name"
KEY_COLUMN = "your_key_column"

# Number of rows to preview
PREVIEW_ROWS = 10

# =============================================================================
# LOAD DATA
# =============================================================================

print("Loading data...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded: {INPUT_FILE}\n")

# =============================================================================
# BASIC INFO
# =============================================================================
print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\n\nCOLUMN NAMES:")
print("-" * 40)
for col in df.columns:
    print(f"  - {col}")

# =============================================================================
# DATA TYPES
# =============================================================================
print("\n\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

# =============================================================================
# PREVIEW DATA
# =============================================================================
print("\n\n" + "=" * 60)
print(f"FIRST {PREVIEW_ROWS} ROWS")
print("=" * 60)
print(df.head(PREVIEW_ROWS))

# =============================================================================
# UNIQUE VALUES IN KEY COLUMN
# =============================================================================
print("\n\n" + "=" * 60)
print(f"UNIQUE VALUES IN: {KEY_COLUMN}")
print("=" * 60)

if KEY_COLUMN in df.columns:
    for value in sorted(df[KEY_COLUMN].dropna().unique()):
        print(f"  {value}")
    print(f"\nTotal unique values: {df[KEY_COLUMN].nunique()}")
    print(f"Null values: {df[KEY_COLUMN].isna().sum()}")
else:
    print(f"WARNING: Column '{KEY_COLUMN}' not found in dataset!")
    print(f"Available columns: {list(df.columns)}")

# =============================================================================
# SUMMARY STATISTICS (Numeric Columns)
# =============================================================================
print("\n\n" + "=" * 60)
print("NUMERIC COLUMN STATISTICS")
print("=" * 60)
print(df.describe())

# =============================================================================
# MISSING VALUES SUMMARY
# =============================================================================
print("\n\n" + "=" * 60)
print("MISSING VALUES BY COLUMN")
print("=" * 60)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

if missing.sum() == 0:
    print("No missing values found!")

print("\n" + "=" * 60)
print("EXPLORATION COMPLETE")
print("=" * 60)
