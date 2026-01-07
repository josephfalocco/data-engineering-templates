# Data Engineering Templates

Reusable templates for building data warehouses using Python, PostgreSQL, and medallion architecture.

## What This Is

A collection of templates, scripts, and documentation I've developed for data warehouse projects. Covers the full lifecycle from requirements gathering through ETL development and validation.

Built for batch processing workflows with CSV/flat file sources into PostgreSQL star schema data models.

## The 4-Phase Methodology

| Phase | Focus | Deliverables |
|-------|-------|--------------|
| **Phase 1: Discovery** | Understand the problem | Requirements doc, project charter |
| **Phase 2: Source Analysis** | Explore and profile data | Data profiling reports, quality assessment |
| **Phase 3: Design** | Model the solution | ERD diagram, DDL scripts, data dictionary |
| **Phase 4: Build** | Develop and validate | ETL pipeline, validation queries |

## Repository Structure
```
├── Phase1-Discovery/
│   ├── requirements_template.md
│   └── project_charter_template.md
│
├── Phase2-Source-Analysis/
│   ├── 01_explore_data.py
│   ├── 02_profile_report.py
│   └── 03_data_quality_checks.py
│
├── Phase3-Design/
│   ├── 01_create_tables_template.sql
│   └── 02_lucidchart_erd_prompt.txt
│
└── Phase4-Build/
    ├── 01_etl_pipeline_template.py
    └── 02_validation_queries_template.sql
```

## Tech Stack

- **Python** — pandas, psycopg2, sqlalchemy
- **PostgreSQL** — database engine
- **Medallion Architecture** — bronze/silver/gold layers
- **Star Schema** — dimension and fact table modeling

## Who This Is For

- Data analysts building their first warehouse
- Freelancers/consultants needing a repeatable process
- Anyone learning data engineering fundamentals

## How to Use

1. Clone or download this repo
2. Navigate to the phase you're working on
3. Read the README in each folder
4. Copy templates to your project
5. Replace `[PLACEHOLDERS]` with your project specifics

## Architecture Pattern
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BRONZE    │ ──▶ │   SILVER    │ ──▶ │    GOLD     │
│  Raw Data   │     │   Cleaned   │     │ Star Schema │
└─────────────┘     └─────────────┘     └─────────────┘
```

- **Bronze** — Raw data, no transformations, preserves source exactly
- **Silver** — Cleaned, proper data types, standardized
- **Gold** — Star schema with dimensions and fact tables

## License

MIT — use freely, modify as needed.

---

*Templates developed through hands-on project work. Feedback welcome.*
