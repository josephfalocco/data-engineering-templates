# Phase 3: Design Templates

Templates for database design phase using medallion architecture and star schema.

## Contents

| File | Purpose |
|------|---------|
| 01_create_tables_template.sql | DDL script with medallion schemas + star schema tables |
| 02_lucidchart_erd_prompt.txt | AI prompt for generating ERD in Lucidchart |

## How to Use

### Step 1: ERD Diagram
1. Open Lucidchart → New → Templates → Search "ERD" → Select "Database ER diagram (crow's foot)"
2. Open `02_lucidchart_erd_prompt.txt`
3. Replace all `[PLACEHOLDERS]` with your project specifics
4. Paste into Lucid AI prompt box
5. Adjust layout as needed

### Step 2: Data Dictionary
1. Create Notion page titled "Data Dictionary"
2. Add Overview section with table list
3. For each table, add:
   - Table name as heading
   - Description paragraph
   - Table with columns: Column Name | Data Type | Nullable | Description

### Step 3: DDL Scripts
1. Copy `01_create_tables_template.sql` to your project folder
2. Rename to `create_tables.sql`
3. Replace all `[PLACEHOLDERS]` with your project specifics
4. Execute in pgAdmin:
   - Step 1: Create schemas
   - Steps 2-3: Create bronze/silver tables
   - Steps 4-5: Create dimensions, then fact table (order matters for foreign keys)

## Placeholder Reference

| Placeholder | Replace With | Examples |
|-------------|--------------|----------|
| [PROJECT_NAME] | Your project name | "Sales Analytics", "HR Metrics", "Inventory Tracker" |
| [DATE] | Creation date | "January 2025" |
| [SOURCE_SYSTEM] | Data source name | "Salesforce", "SAP", "CSV Export", "Shopify" |
| [SOURCE_NAME] | Short source identifier | "orders", "employees", "products" |
| [DIMENSION_1] | First dimension name | "customer", "product", "employee", "location" |
| [DIMENSION_2] | Second dimension name | "region", "category", "department", "vendor" |
| [FACT_NAME] | Fact table subject | "sales", "shipments", "timesheets", "inventory" |

## Notes

- Always create dimension tables BEFORE fact tables (foreign key dependencies)
- Bronze layer: all VARCHAR columns (preserve raw data)
- Silver layer: proper data types applied
- Gold layer: star schema with surrogate keys
- dim_date is reusable across most projects — keep as-is
