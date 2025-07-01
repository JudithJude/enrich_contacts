import pandas as pd

print(">>> Running enrich_contacts.py...")

# Load contacts
df_contacts = pd.read_csv('data/contacts_with_linkedin_search.csv')
df_koldleads = pd.read_csv('data/koldleads_combined.csv', low_memory=False)
print("Columns in koldleads_combined.csv:", df_koldleads.columns.tolist())

# Make matching columns (lowercased)
df_contacts['person_name_lc'] = df_contacts['person_name'].str.strip().str.lower()
df_contacts['company_name_lc'] = df_contacts['company_name'].str.strip().str.lower()
df_koldleads['person_name'] = (
    df_koldleads['First Name'].fillna('') + ' ' + df_koldleads['Last Name'].fillna('')
)
df_koldleads['person_name_lc'] = df_koldleads['person_name'].str.strip().str.lower()
df_koldleads['company_name_lc'] = df_koldleads['Company Name'].str.strip().str.lower()

# Merge!
df_merged = pd.merge(
    df_contacts,
    df_koldleads,
    how="left",
    on=["person_name_lc", "company_name_lc"],
    suffixes=('', '_koldleads')
)

# Extract columns
output_cols = list(df_contacts.columns) + [
    'Email', 'Phone', 'Web Address', 'Title', 'Revenue', 'Employee'
]

# Add LinkedIn URL if present
df_merged['LinkedIn URL'] = df_merged['Web Address'].where(
    df_merged['Web Address'].str.contains("linkedin.com", case=False, na=False), "")

df_merged = df_merged[output_cols + ['LinkedIn URL']]

output_file = 'data/contacts_enriched.csv'
df_merged.to_csv(output_file, index=False)
print(f">>> Enriched contacts saved to {output_file} ({len(df_merged)} rows)")




















# import pandas as pd

# print(">>> Running enrich_contacts.py...")

# # 1. Load contacts with LinkedIn search
# try:
#     df_contacts = pd.read_csv('data/contacts_with_linkedin_search.csv')
#     print(f">>> Loaded {len(df_contacts)} contacts")
# except Exception as e:
#     print(f"⚠️ ERROR: contacts_with_linkedin_search.csv not found or unreadable: {e}")
#     exit(1)

# # 2. Load KoldLeads
# try:
#     df_koldleads = pd.read_csv('data/koldleads_combined.csv', low_memory=False)
#     print(f">>> Loaded {len(df_koldleads)} KoldLeads rows")
#     print("Columns in koldleads_combined.csv:", df_koldleads.columns.tolist())
# except Exception as e:
#     print(f"⚠️ ERROR: koldleads_combined.csv not found or unreadable: {e}")
#     exit(1)

# # 3. Make sure person_name exists in KoldLeads
# if 'person_name' not in df_koldleads.columns:
#     if 'First Name' in df_koldleads.columns and 'Last Name' in df_koldleads.columns:
#         df_koldleads['person_name'] = (
#             df_koldleads['First Name'].fillna('') + ' ' + df_koldleads['Last Name'].fillna('')
#         )
#     else:
#         print("ERROR: 'First Name' and/or 'Last Name' columns missing from KoldLeads data.")
#         exit(1)

# # Optional: Clean up whitespace and lower-case for matching
# df_contacts['person_name_lc'] = df_contacts['person_name'].str.strip().str.lower()
# df_contacts['company_name_lc'] = df_contacts['company_name'].str.strip().str.lower()
# df_koldleads['person_name_lc'] = df_koldleads['person_name'].str.strip().str.lower()
# if 'Company Name' in df_koldleads.columns:
#     df_koldleads['company_name_lc'] = df_koldleads['Company Name'].str.strip().str.lower()
# else:
#     print("ERROR: 'Company Name' column missing in KoldLeads data.")
#     exit(1)

# # Columns to extract
# cols_to_extract = [
#     'Email',
#     'Phone',
#     'Web Address',
#     'Title',
#     'Revenue',
#     'Employee'
# ]

# # 4. Match and enrich
# enriched_rows = []
# for idx, row in df_contacts.iterrows():
#     mask = (
#         (df_koldleads['person_name_lc'] == row['person_name_lc']) &
#         (df_koldleads['company_name_lc'] == row['company_name_lc'])
#     )
#     match = df_koldleads[mask]
#     if not match.empty:
#         # Take the first matching row
#         info = match.iloc[0]
#         enriched = row.to_dict()
#         for col in cols_to_extract:
#             enriched[col] = info.get(col, "")
#         # Add LinkedIn URL column if 'Web Address' includes a LinkedIn profile
#         web_addr = info.get('Web Address', "")
#         if pd.notna(web_addr) and "linkedin.com" in str(web_addr).lower():
#             enriched['LinkedIn URL'] = web_addr
#         else:
#             enriched['LinkedIn URL'] = ""
#     else:
#         enriched = row.to_dict()
#         for col in cols_to_extract:
#             enriched[col] = ""
#         enriched['LinkedIn URL'] = ""
#     enriched_rows.append(enriched)

# # 5. Save final enriched contacts
# df_enriched = pd.DataFrame(enriched_rows)
# output_file = 'data/contacts_enriched.csv'
# df_enriched.to_csv(output_file, index=False)
# print(f">>> Enriched contacts saved to {output_file} ({len(df_enriched)} rows)")





















