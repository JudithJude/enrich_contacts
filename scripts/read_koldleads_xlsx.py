# scripts/read_koldleads_xlsx.py
import pandas as pd
import glob
import os

print(">>> Running read_koldleads_xlsx.py...")

input_folder = "data/koldleads/"
output_file = "data/koldleads_combined.csv"

xlsx_files = glob.glob(os.path.join(input_folder, "*.xlsx"))
if not xlsx_files:
    print(f"⚠️ No .xlsx files found in {input_folder}")
    exit(1)

df_list = []
for file in xlsx_files:
    print(f"Reading {file} ...")
    df = pd.read_excel(file, engine='openpyxl')
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv(output_file, index=False)
print(f">>> Saved combined KoldLeads to {output_file} with {combined_df.shape[0]} rows")




