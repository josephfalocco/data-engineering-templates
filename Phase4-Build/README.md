# Phase 4: Build Templates

Templates for ETL pipeline development and post-load validation.

## Contents

| File | Purpose |
|------|---------|
| 01_etl_pipeline_template.py | Python ETL pipeline skeleton (bronze → silver → gold) |
| 02_validation_queries_template.sql | Post-ETL data quality checks |

## How to Use

### Step 1: Set Up ETL Pipeline
1. Copy `01_etl_pipeline_template.py` to your project folder
2. Rename to `etl_pipeline.py`
3. Update the configuration section at the top:
   - Database connection details
   - Source file path
   - Table names
4. Customize transformations in the silver layer section for your data

### Step 2: Run the Pipeline
1. Run bronze layer first — verify raw data loaded correctly
2. Run silver layer — verify transformations applied
3. Run gold layer — verify dimensions populated before fact table

### Step 3: Validate the Load
1. Open `02_validation_queries_template.sql`
2. Replace placeholders with your table/column names
3. Run each validation query after ETL completes
4. Investigate any failures before moving forward

## Placeholder Reference

| Placeholder | Replace With | Examples |
|-------------|--------------|----------|
| [SOURCE_FILE.csv] | Your source data file | "orders_export.csv", "employees.csv" |
| [DATABASE_NAME] | PostgreSQL database name | "sales_dwh", "hr_analytics" |
| [YOUR_PASSWORD] | Database password | (your password) |
| [TABLE_NAME] | Target table name | "raw_orders", "dim_customer" |
| [COLUMNS] | Column list for validation | "order_id, customer_id, amount" |
| [PRIMARY_KEY] | Primary key column | "order_id", "employee_id" |
| [DATE_COLUMN] | Date field to validate | "order_date", "hire_date" |
| [FOREIGN_KEY] | Foreign key column | "customer_key", "product_key" |

## ETL Pattern
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BRONZE    │ ──▶│   SILVER    │ ──▶ │    GOLD     │
│  Raw Data   │     │  Cleaned    │     │ Star Schema │
└─────────────┘     └─────────────┘     └─────────────┘
```

| Layer | What Happens | Key Principle |
|-------|--------------|---------------|
| Bronze | Load raw data as-is | No transformations — preserve source exactly |
| Silver | Clean, cast types, filter | Fix data quality issues, standardize formats |
| Gold | Build star schema | Dimensions first, then fact tables |

## Validation Checks Explained

| Check | What It Catches |
|-------|-----------------|
| Row count comparison | Data lost during load |
| Primary key duplicates | ETL created duplicate records |
| Null checks on required fields | Missing critical data |
| Foreign key orphans | Fact records pointing to non-existent dimensions |
| Date range validation | Data outside expected time boundaries |
| Aggregate comparisons | Transformation errors (source sum ≠ target sum) |

## Common Issues & Fixes

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Row count mismatch | Filter too aggressive, load failed midway | Check WHERE clauses, verify full load |
| Duplicate PKs | Missing DISTINCT, bad join logic | Add deduplication in silver layer |
| Null FKs in fact table | Dimension missing records | Load dimensions first, check join keys |
| Type conversion errors | Bad source data format | Add error handling, clean in silver layer |
| Slow performance | No indexes, large single transaction | Add indexes, batch the loads |

## Best Practices

- **Always load dimensions before facts** — foreign key dependencies
- **Validate after each layer** — don't wait until gold to find bronze issues
- **Log row counts** — print counts after each step for debugging
- **Use transactions** — rollback on failure to avoid partial loads
- **Test with small data first** — use LIMIT during development
