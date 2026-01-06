# =============================================================================
# 02_profile_report.py
# Purpose: Generate automated data profiling report using ydata-profiling
# Phase: Discovery / Source System Analysis
# =============================================================================

import pandas as pd
from ydata_profiling import ProfileReport

# =============================================================================
# CONFIGURATION - Update these variables for your project
# =============================================================================

# TODO: Update with your source file path
INPUT_FILE = "your_source_file.csv"

# TODO: Update with a descriptive title for your report
REPORT_TITLE = "Data Profile Report - [Your Project Name]"

# TODO: Update with desired output file name
OUTPUT_FILE = "data_profile_report.html"

# Report mode: True = faster/minimal, False = comprehensive/slower
MINIMAL_MODE = True

# =============================================================================
# LOAD DATA
# =============================================================================

print("Loading data...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded: {INPUT_FILE}")
print(f"Shape: {len(df):,} rows x {len(df.columns)} columns\n")

# =============================================================================
# GENERATE PROFILE REPORT
# =============================================================================

print("Generating profile report...")
if MINIMAL_MODE:
    print("(Minimal mode - faster generation)")
else:
    print("(Comprehensive mode - this may take several minutes)")

profile = ProfileReport(
    df,
    title=REPORT_TITLE,
    minimal=MINIMAL_MODE
)

# =============================================================================
# SAVE REPORT
# =============================================================================

profile.to_file(OUTPUT_FILE)

print("\n" + "=" * 60)
print("PROFILE REPORT COMPLETE")
print("=" * 60)
print(f"Report saved to: {OUTPUT_FILE}")
print(f"Open this file in your browser to view the report.")
print("=" * 60)
