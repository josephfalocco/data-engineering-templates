-- ============================================
-- VALIDATION QUERIES TEMPLATE
-- Run after each ETL to confirm data integrity
-- Replace [PLACEHOLDERS] with actual table/column names
-- ============================================

-- -----------------------------------------
-- 1. ROW COUNTS BY LAYER
-- -----------------------------------------
SELECT 'bronze.[TABLE]' as table_name, COUNT(*) as row_count 
FROM bronze.[TABLE]
UNION ALL
SELECT 'silver.[TABLE]', COUNT(*) 
FROM silver.[TABLE]
UNION ALL
SELECT 'gold.fact_[NAME]', COUNT(*) 
FROM gold.fact_[NAME]
UNION ALL
SELECT 'gold.dim_[NAME]', COUNT(*) 
FROM gold.dim_[NAME];


-- -----------------------------------------
-- 2. ORPHAN CHECK - FACT TABLE
-- All foreign keys should match (expect zeros)
-- -----------------------------------------
SELECT 'Missing [dimension]_key' as issue, COUNT(*) as count
FROM gold.fact_[NAME] f
LEFT JOIN gold.dim_[NAME] d ON f.[key] = d.[key]
WHERE d.[key] IS NULL;


-- -----------------------------------------
-- 3. DATE RANGE CHECK
-- -----------------------------------------
SELECT 
    MIN(full_date) as earliest_date,
    MAX(full_date) as latest_date,
    COUNT(DISTINCT full_date) as unique_dates
FROM gold.dim_date;


-- -----------------------------------------
-- 4. NULL CHECK ON REQUIRED FIELDS
-- -----------------------------------------
SELECT '[column_name] nulls' as issue, COUNT(*) as count
FROM gold.fact_[NAME]
WHERE [column_name] IS NULL;


-- -----------------------------------------
-- 5. SUMMARY BY KEY DIMENSION
-- Sanity check the numbers make sense
-- -----------------------------------------
SELECT 
    d.[group_column],
    COUNT(*) as record_count,
    SUM(f.[measure]) as total
FROM gold.fact_[NAME] f
JOIN gold.dim_[NAME] d ON f.[key] = d.[key]
GROUP BY d.[group_column]
ORDER BY total DESC;
