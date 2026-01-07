# Phase 4: Build Templates

Templates for ETL pipeline development and post-load validation using Python and PostgreSQL.

## Contents

| File | Purpose |
|------|---------|
| 01_etl_pipeline_template.py | Python ETL pipeline using medallion architecture (bronze → silver → gold) |
| 02_validation_queries_template.sql | Post-ETL data quality checks |

## Dependencies

Install required packages before running the ETL pipeline:
```bash
pip install pandas psycopg2-binary sqlalchemy --break-system-packages
```

| Package | Purpose |
|---------|---------|
| pandas | Data manipulation and CSV loading |
| psycopg2-binary | PostgreSQL database connection |
| sqlalchemy | Enables pandas to write directly to database tables |

## How to Use

### Step 1: Configure the Pipeline
1. Copy `01_etl_pipeline_template.py` to your project folder
2. Rename to `etl_pipeline.py`
3. Update the configuration section at the top:
   - `CSV_FILE` — path to your source data
   - `DB_NAME` — your PostgreSQL database name
   - `DB_PASSWORD` — your database password
4. Replace all `[PLACEHOLDERS]` in table names and column references

### Step 2: Customize Transformations
1. **Bronze section**: Update column selections if needed (raw load, minimal changes)
2. **Silver section**: Add your data cleaning logic:
   - Strip whitespace
   - Convert data types
   - Filter invalid rows
   - Standardize text values
3. **Gold section**: Configure dimension and fact table logic:
   - Define dimension columns
   - Set up surrogate keys
   - Build fact table with foreign key lookups

### Step 3: Run the Pipeline
```bash
python etl_pipeline.py
```

Run in order — the script handles sequencing automatically:
1. Bronze layer loads first (raw data)
2. Silver layer transforms bronze data
3. Gold layer builds star schema (dimensions before fact)

### Step 4: Validate the Load
1. Open `02_validation_queries_template.sql` in pgAdmin
2. Replace all `[PLACEHOLDERS]` with your actual table/column names
3. Run each validation query after ETL completes
4. Investigate any non-zero counts before proceeding

## Placeholder Reference

| Placeholder | Replace With | Examples |
|-------------|--------------|----------|
| [SOURCE_FILE.csv] | Your source data file | "orders_export.csv", "employees.csv", "inventory.csv" |
| [DATABASE_NAME] | PostgreSQL database name | "sales_dwh", "hr_analytics", "ops_warehouse" |
| [YOUR_PASSWORD] | Database password | (your password) |
| [TABLE_NAME] | Source/staging table name | "raw_orders", "raw_employees", "raw_products" |
| [PRIMARY_KEY] | Primary key column | "order_id", "employee_id", "product_sku" |
| [DIM1_NAME] | First dimension name | "customer", "employee", "product" |
| [DIM2_NAME] | Second dimension name | "region", "department", "category" |
| [FACT_NAME] | Fact table subject | "sales", "timesheets", "shipments" |
| [MEASURE_1] | Numeric measure column | "amount", "quantity", "hours_worked" |
| [MEASURE_2] | Second measure column | "discount", "units", "overtime_hours" |
| [GROUP_COLUMN] | Dimension attribute for grouping | "category_name", "region", "department" |

## ETL Pattern
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BRONZE    │ ──▶ │   SILVER    │ ──▶ │    GOLD     │
│  Raw Data   │     │   Cleaned   │     │ Star Schema │
└─────────────┘     └─────────────┘     └─────────────┘
```

| Layer | What Happens | Key Principle |
|-------|--------------|---------------|
| Bronze | Load CSV as-is to database | No transformations — preserve source exactly |
| Silver | Clean and standardize data | Fix quality issues, cast proper data types |
| Gold | Build star schema | Dimensions first, then fact table (FK dependencies) |

## Validation Checks Explained

| Check | Query Section | What It Catches | Expected Result |
|-------|---------------|-----------------|-----------------|
| Row counts by layer | #1 | Overview of data volume | Numbers make sense |
| Bronze vs Silver | #2 | Data lost during transformation | Difference = 0 (or intentional) |
| Primary key duplicates | #3 | ETL created duplicate records | Zero rows returned |
| Foreign key orphans | #4 | Fact records missing dimension matches | All counts = 0 |
| Null checks | #5 | Missing required data | All counts = 0 |
| Date range | #6 | Dates outside expected boundaries | Reasonable min/max |
| Summary by dimension | #7 | Sanity check on aggregates | Numbers make business sense |
| Aggregate comparison | #8 | Transformation errors | Totals match across layers |

## Common Issues & Fixes

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError: sqlalchemy` | Package not installed | Run `pip install sqlalchemy --break-system-packages` |
| Row count mismatch bronze→silver | Filter too aggressive | Check WHERE clauses in silver transformation |
| Duplicate primary keys | Missing deduplication logic | Add `.drop_duplicates()` in silver layer |
| Orphan foreign keys (count > 0) | Dimension missing records | Load dimensions before fact; check join keys |
| Type conversion errors | Bad source data format | Add `errors='coerce'` to `pd.to_numeric()` |
| Aggregate totals don't match | Transformation changed values | Review silver layer logic; check for filters |
| Connection refused | PostgreSQL not running | Start PostgreSQL service; verify credentials |
| Permission denied on schema | User lacks privileges | Grant schema permissions in pgAdmin |

## Best Practices

- **Always load dimensions before facts** — foreign key dependencies require it
- **Validate after each layer** — don't wait until gold to discover bronze issues
- **Log row counts** — the template prints counts; review them each run
- **Test with small data first** — add `LIMIT 100` to reads during development
- **Use TRUNCATE, not DELETE** — faster for full refreshes
- **Keep bronze untransformed** — you'll need original data for debugging
- **Comment your transformations** — future you will thank present you

## Script Structure

### ETL Pipeline (01_etl_pipeline_template.py)
```
├── Configuration block (connection details)
├── get_connection() — database connection helper
├── load_bronze() — raw CSV to bronze schema
├── transform_silver() — cleaning and type conversion
├── populate_gold() — dimension and fact table loading
└── Main execution block with error handling
```

### Validation Queries (02_validation_queries_template.sql)
```
├── 1. Row counts by layer
├── 2. Bronze vs Silver comparison
├── 3. Primary key duplicate check
├── 4. Foreign key orphan checks
├── 5. Null checks on required fields
├── 6. Date range validation
├── 7. Summary by dimension (sanity check)
└── 8. Aggregate comparison across layers
```
