print(">>> Running generate_linkedin_search_urls.py...")

import pandas as pd
import urllib.parse

try:
    df = pd.read_csv('data/contacts_cleaned.csv')
    print(f">>> Loaded {df.shape[0]} cleaned contacts")
except FileNotFoundError:
    print("⚠️ ERROR: contacts_cleaned.csv not found! Please run clean_contacts.py first.")
    exit()

df['email'] = ''
df['linkedin_url'] = ''
df['final_phone_number'] = df['mobile_number'].fillna(df['phone_number'])
df['linkedin_search_url'] = ''

for idx, row in df.iterrows():
    person_name = row['person_name']
    company_name = row['company_name']
    search_query = f"{person_name} {company_name} LinkedIn"
    encoded_query = urllib.parse.quote(search_query)
    google_search_url = f"https://www.google.com/search?q={encoded_query}"
    df.at[idx, 'linkedin_search_url'] = google_search_url

df.to_csv('data/contacts_with_linkedin_search.csv', index=False)
print(f">>> Saved contacts_with_linkedin_search.csv with {df.shape[0]} rows")



