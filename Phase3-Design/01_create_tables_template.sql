-- ============================================
-- [PROJECT_NAME] Database
-- DDL Script: Create Schemas and Tables
-- Created: [DATE]
-- ============================================

-- ============================================
-- STEP 1: Create Schemas (Medallion Architecture)
-- ============================================

CREATE SCHEMA IF NOT EXISTS bronze;  -- Raw source data
CREATE SCHEMA IF NOT EXISTS silver;  -- Cleaned/transformed data
CREATE SCHEMA IF NOT EXISTS gold;    -- Star schema for analytics

-- ============================================
-- STEP 2: Create Bronze Layer Table(s)
-- ============================================

-- Raw [SOURCE_SYSTEM] data (untransformed)
-- All columns as VARCHAR to preserve raw data exactly as received
CREATE TABLE IF NOT EXISTS bronze.raw_[SOURCE_NAME] (
    -- Add columns matching your source file/system
    -- Example:
    -- column_1    VARCHAR(50),
    -- column_2    VARCHAR(100),
    -- column_3    VARCHAR(50)
);

-- ============================================
-- STEP 3: Create Silver Layer Table(s)
-- ============================================

-- Cleaned and transformed data
-- Proper data types applied, columns split/combined as needed
CREATE TABLE IF NOT EXISTS silver.cleaned_[SOURCE_NAME] (
    -- Add columns with appropriate data types
    -- Example:
    -- id              VARCHAR(50) PRIMARY KEY,
    -- event_date      DATE NOT NULL,
    -- description     VARCHAR(255),
    -- amount          DECIMAL(12,2)
);

-- ============================================
-- STEP 4: Create Dimension Tables (Gold Layer)
-- ============================================

-- dim_date: Standard date dimension for time-based analysis
CREATE TABLE IF NOT EXISTS gold.dim_date (
    date_key        INTEGER PRIMARY KEY,      -- Format: YYYYMMDD
    full_date       DATE NOT NULL,
    year            INTEGER NOT NULL,
    month           INTEGER NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    quarter         VARCHAR(2) NOT NULL
);

-- dim_[DIMENSION_1]: [DESCRIPTION]
CREATE TABLE IF NOT EXISTS gold.dim_[DIMENSION_1] (
    [dimension_1]_key    INTEGER PRIMARY KEY,
    -- Add dimension attributes
    -- Example:
    -- name               VARCHAR(100) NOT NULL,
    -- type               VARCHAR(50),
    -- category           VARCHAR(50)
);

-- dim_[DIMENSION_2]: [DESCRIPTION]
CREATE TABLE IF NOT EXISTS gold.dim_[DIMENSION_2] (
    [dimension_2]_key    INTEGER PRIMARY KEY,
    -- Add dimension attributes
);

-- ============================================
-- STEP 5: Create Fact Table (Gold Layer)
-- ============================================

-- fact_[FACT_NAME]: [DESCRIPTION]
CREATE TABLE IF NOT EXISTS gold.fact_[FACT_NAME] (
    [fact_id]           VARCHAR(50) PRIMARY KEY,
    date_key            INTEGER NOT NULL,
    [dimension_1]_key   INTEGER NOT NULL,
    [dimension_2]_key   INTEGER NOT NULL,
    -- Add measures
    -- Example:
    -- amount            DECIMAL(12,2) NOT NULL,
    -- quantity          INTEGER,
    
    -- Foreign key constraints
    CONSTRAINT fk_date 
        FOREIGN KEY (date_key) REFERENCES gold.dim_date(date_key),
    CONSTRAINT fk_[dimension_1] 
        FOREIGN KEY ([dimension_1]_key) REFERENCES gold.dim_[DIMENSION_1]([dimension_1]_key),
    CONSTRAINT fk_[dimension_2] 
        FOREIGN KEY ([dimension_2]_key) REFERENCES gold.dim_[DIMENSION_2]([dimension_2]_key)
);
