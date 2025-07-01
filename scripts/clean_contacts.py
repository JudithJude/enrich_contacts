import pandas as pd

print(">>> Running clean_contacts.py...")

try:
    print(">>> Reading data/contacts_raw.csv...")
    df = pd.read_csv('data/contacts_raw.csv')
    print(f">>> Loaded {df.shape[0]} rows")
    print("Columns as loaded:", df.columns.tolist())
except FileNotFoundError:
    print("⚠️ ERROR: contacts_raw.csv not found! Please check data/ folder.")
    exit()

# Strip whitespace from all column names
df.columns = [col.strip() for col in df.columns]
print("Columns after strip():", df.columns.tolist())

# Try to rename the columns
df = df.rename(columns={
    'Record ID': 'id',
    'First Name': 'first_name',
    'Last Name': 'last_name',
    'Company Name': 'company_name',
    'Phone Number': 'phone_number',
    'Mobile Phone Number': 'mobile_number'
})
print("Columns after renaming:", df.columns.tolist())

# Add person_name
df['person_name'] = df['first_name'].fillna('') + ' ' + df['last_name'].fillna('')
print("Columns after adding person_name:", df.columns.tolist())

# Now, right before selecting columns, print all columns
print("All columns right before selection:", df.columns.tolist())

# Try to select columns
try:
    df = df[['id', 'person_name', 'company_name', 'phone_number', 'mobile_number']]
    print("SUCCESS! Selected columns.")
except Exception as e:
    print("FAILED to select columns:", e)
    print("Final available columns:", df.columns.tolist())
    exit(1)

# Continue as normal
df = df.drop_duplicates(subset=['id'])
df = df.dropna(subset=['person_name', 'company_name'])
df = df.reset_index(drop=True)

df.to_csv('data/contacts_cleaned.csv', index=False)
print(f">>> Saved contacts_cleaned.csv with {df.shape[0]} rows")
