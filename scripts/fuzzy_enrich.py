import pandas as pd
from rapidfuzz import process, fuzz

THRESHOLD = 60  #this is the similarity score

contacts = pd.read_csv("data/contacts_with_linkedin_search.csv")
leads    = pd.read_csv("data/koldleads_combined.csv",
                       usecols=["Company Name", "Email"])
leads["Company Name"] = leads["Company Name"].str.lower()

lookup = dict(zip(leads["Company Name"], leads["Email"]))

matches = []
for i, row in contacts.iterrows():
    name = row["company_name"].lower()
    best = process.extractOne(
        query=name,
        choices=lookup.keys(),
        scorer=fuzz.token_sort_ratio
    )
    if best and best[1] >= THRESHOLD:
        matches.append({
            **row,
            "matched_company": best[0],
            "matched_email":   lookup[best[0]],
            "sim":             round(best[1] / 100, 2)
        })
    if (i+1) % 200 == 0:
        print(f"   Processed {i+1:,} contacts")

pd.DataFrame(matches).to_csv("data/contacts_enriched_fuzzy.csv", index=False)
print("✅  Saved contacts_enriched_fuzzy.csv")
