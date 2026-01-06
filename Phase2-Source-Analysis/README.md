# Phase 2: Source System Analysis Templates

## Purpose
Scripts for exploring and profiling raw data before designing the database.

## Scripts

### 01_explore_data.py
**What it does:** Quick overview of dataset structure - row counts, columns, data types, unique values in key fields.

**When to use:** First script you run on any new data source.

**What to change:**
- Line 9: Update filename in `pd.read_csv('your_file.csv')`
- Line 38: Update column name in `df['Your Key Column'].unique()` to whatever field you want to inspect

**What to look for:**
- [ ] How many rows? Does it match what the source said?
- [ ] Column names - any surprises? Weird characters?
- [ ] Data types - are dates showing as 'object' (string)? Numbers as strings?
- [ ] Key columns - do the unique values make sense?

---

### 02_profile_report.py
**What it does:** Generates comprehensive HTML report with statistics, distributions, missing values, correlations.

**When to use:** After initial exploration, before design phase.

**What to change:**
- Line 9: Update filename in `pd.read_csv('your_file.csv')`
- Line 14: Update report title
- Line 19: Update output filename if desired

**What to look for:**
- [ ] Missing values - which columns have gaps? Is that expected?
- [ ] High cardinality - columns with tons of unique values (potential dimensions)
- [ ] Low cardinality - columns with few values (good for categorical grouping)
- [ ] Zeros vs nulls - are blanks stored as 0 or actually null?
- [ ] Date formats - consistent? Parseable?

---

### 03_data_quality_checks.py
**What it does:** Runs specific data quality checks based on issues identified during profiling. Tests date formats, number formats, key relationships, and null values.

**When to use:** After profiling reveals potential issues. Customize checks based on what you found.

**What to change:**
- Line 9: Update filename in `pd.read_csv('your_file.csv')`
- Line 17: Update date column name and expected format
- Line 24: Update numeric column name and expected pattern
- Line 32: Update the grouping column for relationship checks
- Line 44: Update column name for category/type distribution
- Line 51: Update the list of key columns for null checks

**What to look for:**

*Date Format:*
- [ ] All dates follow same format?
- [ ] Any unexpected characters or patterns?

*Numeric Format:*
- [ ] Consistent formatting (decimals, thousands separators)?
- [ ] Any unexpected characters or symbols?

*Relationship Verification:*
- [ ] Expected number of rows per group?
- [ ] Any orphan records or unexpected groupings?

*Category Distribution:*
- [ ] All categories recognized? No NULLs or unexpected values?
- [ ] Distribution makes sense for the data?

*Null Checks:*
- [ ] All key columns have zero nulls?
- [ ] If nulls exist, is it expected (like optional fields)?

**Common red flags this script catches:**
- Mixed date formats that will break ETL
- Inconsistent number formatting
- Broken relationships (orphan records)
- Unexpected categories or values
- Missing data in critical fields
