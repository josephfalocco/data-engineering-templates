-- ============================================
-- VALIDATION QUERIES TEMPLATE
-- Run after each ETL to confirm data integrity
-- Replace [PLACEHOLDERS] with actual table/column names
-- ============================================

-- -----------------------------------------
-- 1. ROW COUNTS BY LAYER
-- -----------------------------------------
SELECT 'bronze.[TABLE_NAME]' as table_name, COUNT(*) as row_count 
FROM bronze.[TABLE_NAME]
UNION ALL
SELECT 'silver.[TABLE_NAME]', COUNT(*) 
FROM silver.[TABLE_NAME]
UNION ALL
SELECT 'gold.dim_[DIM1_NAME]', COUNT(*) 
FROM gold.dim_[DIM1_NAME]
UNION ALL
SELECT 'gold.dim_[DIM2_NAME]', COUNT(*) 
FROM gold.dim_[DIM2_NAME]
UNION ALL
SELECT 'gold.fact_[FACT_NAME]', COUNT(*) 
FROM gold.fact_[FACT_NAME];


-- -----------------------------------------
-- 2. BRONZE vs SILVER ROW COUNT
-- Should match (unless filtering intentionally)
-- -----------------------------------------
SELECT 
    (SELECT COUNT(*) FROM bronze.[TABLE_NAME]) as bronze_count,
    (SELECT COUNT(*) FROM silver.[TABLE_NAME]) as silver_count,
    (SELECT COUNT(*) FROM bronze.[TABLE_NAME]) - 
    (SELECT COUNT(*) FROM silver.[TABLE_NAME]) as difference;


-- -----------------------------------------
-- 3. PRIMARY KEY DUPLICATE CHECK
-- All counts should be 1 (expect zero rows returned)
-- -----------------------------------------
SELECT '[TABLE_NAME] duplicates' as issue, [PRIMARY_KEY], COUNT(*) as count
FROM silver.[TABLE_NAME]
GROUP BY [PRIMARY_KEY]
HAVING COUNT(*) > 1;

-- Repeat for dimensions
SELECT 'dim_[DIM1_NAME] duplicates' as issue, [DIM1_NAME]_key, COUNT(*) 
FROM gold.dim_[DIM1_NAME]
GROUP BY [DIM1_NAME]_key
HAVING COUNT(*) > 1;


-- -----------------------------------------
-- 4. ORPHAN CHECK - FACT TABLE FOREIGN KEYS
-- All should return zero (no orphaned records)
-- -----------------------------------------
-- Check dimension 1
SELECT 'Missing [DIM1_NAME]_key' as issue, COUNT(*) as orphan_count
FROM gold.fact_[FACT_NAME] f
LEFT JOIN gold.dim_[DIM1_NAME] d ON f.[DIM1_NAME]_key = d.[DIM1_NAME]_key
WHERE d.[DIM1_NAME]_key IS NULL;

-- Check dimension 2
SELECT 'Missing [DIM2_NAME]_key' as issue, COUNT(*) as orphan_count
FROM gold.fact_[FACT_NAME] f
LEFT JOIN gold.dim_[DIM2_NAME] d ON f.[DIM2_NAME]_key = d.[DIM2_NAME]_key
WHERE d.[DIM2_NAME]_key IS NULL;

-- Check date dimension
SELECT 'Missing date_key' as issue, COUNT(*) as orphan_count
FROM gold.fact_[FACT_NAME] f
LEFT JOIN gold.dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL;


-- -----------------------------------------
-- 5. NULL CHECK ON REQUIRED FIELDS
-- All should return zero
-- -----------------------------------------
SELECT 'fact [MEASURE_1] nulls' as issue, COUNT(*) as null_count
FROM gold.fact_[FACT_NAME]
WHERE [MEASURE_1] IS NULL;

SELECT 'fact [MEASURE_2] nulls' as issue, COUNT(*) as null_count
FROM gold.fact_[FACT_NAME]
WHERE [MEASURE_2] IS NULL;

SELECT 'fact date_key nulls' as issue, COUNT(*) as null_count
FROM gold.fact_[FACT_NAME]
WHERE date_key IS NULL;


-- -----------------------------------------
-- 6. DATE RANGE CHECK
-- Verify dates fall within expected boundaries
-- -----------------------------------------
SELECT 
    MIN(full_date) as earliest_date,
    MAX(full_date) as latest_date,
    COUNT(*) as total_dates,
    COUNT(DISTINCT full_date) as unique_dates
FROM gold.dim_date;


-- -----------------------------------------
-- 7. FACT TABLE SUMMARY BY DIMENSION
-- Sanity check - do the numbers make sense?
-- -----------------------------------------
SELECT 
    d.[GROUP_COLUMN],
    COUNT(*) as record_count,
    SUM(f.[MEASURE_1]) as total_measure
FROM gold.fact_[FACT_NAME] f
JOIN gold.dim_[DIM1_NAME] d ON f.[DIM1_NAME]_key = d.[DIM1_NAME]_key
GROUP BY d.[GROUP_COLUMN]
ORDER BY total_measure DESC
LIMIT 10;


-- -----------------------------------------
-- 8. AGGREGATE COMPARISON (SOURCE vs TARGET)
-- Totals should match after ETL
-- -----------------------------------------
SELECT 
    'bronze' as layer, SUM(CAST([MEASURE_COLUMN] AS NUMERIC)) as total
FROM bronze.[TABLE_NAME]
UNION ALL
SELECT 
    'silver' as layer, SUM([MEASURE_COLUMN]) as total
FROM silver.[TABLE_NAME]
UNION ALL
SELECT 
    'gold' as layer, SUM([MEASURE_1]) as total
FROM gold.fact_[FACT_NAME];
