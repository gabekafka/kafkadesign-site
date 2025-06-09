#!/usr/bin/env python3
import os
import pandas as pd

# —— CONFIG ——
TEMPLATE_CSV = 'mc-member-data.csv'
EXCEL_FILE   = 'aisc-shapes-database-v15.0 (4).xlsx'
OUTPUT_CSV   = 'aisc-shapes-formatted.csv'

# Zero-based row index where your real headers live
# e.g. if your headers are on the 5th line of the sheet, use HEADER_ROW = 4
HEADER_ROW = 4

# —— DIAGNOSTICS ——
print("Working dir: ", os.getcwd())
print("Files here:  ", os.listdir())

# —— LOAD TEMPLATE SCHEMA ——
df_template = pd.read_csv(TEMPLATE_CSV)
print(f"Loaded template: {df_template.shape[0]} rows × {df_template.shape[1]} cols")

# —— LOAD AISC EXCEL ——
df_xlsx = pd.read_excel(
    EXCEL_FILE,
    sheet_name=0,
    header=HEADER_ROW
)
print(f"Loaded Excel:   {df_xlsx.shape[0]} rows × {df_xlsx.shape[1]} cols")
print("Excel columns:", df_xlsx.columns.tolist())

# —— FILTER & REFORMAT —— 
# Keep only columns that appear in both files
common_cols = [c for c in df_template.columns if c in df_xlsx.columns]
print("Common columns:", common_cols)

# Build new DataFrame
df_new = df_xlsx[common_cols].copy()

# Add any missing template columns as empty
for col in df_template.columns:
    if col not in df_new.columns:
        df_new[col] = pd.NA

# Reorder to match template exactly
df_new = df_new[df_template.columns]

# —— WRITE OUTPUT —— 
df_new.to_csv(OUTPUT_CSV, index=False)
print(f"Saved formatted data → {OUTPUT_CSV}")