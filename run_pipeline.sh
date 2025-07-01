#!/usr/bin/env bash
set -e

echo "Step 1  Clean contacts…"
python scripts/clean_contacts.py

echo "Step 2  LinkedIn search URLs…"
python scripts/generate_linkedin_search_urls.py

echo "Step 3  Merge KoldLeads…"
python scripts/read_koldleads_xlsx.py

echo "Step 4  Fuzzy enrich…"
python scripts/fuzzy_enrich.py

#loading into Postgres
echo "Step 5  COPY to Postgres…"
psql -h localhost -U metabase -d contacts_enrich \
  -c "DROP TABLE IF EXISTS contacts_enriched_fuzzy;
      CREATE TABLE contacts_enriched_fuzzy (
        record_id TEXT, first_name TEXT, last_name TEXT,
        company_name TEXT, phone_number TEXT,
        mobile_phone_number TEXT, associated_note_ids TEXT,
        matched_company TEXT, matched_email TEXT, sim NUMERIC
      );"
psql -h localhost -U metabase -d contacts_enrich \
  -c "\copy contacts_enriched_fuzzy FROM 'data/contacts_enriched_fuzzy.csv' CSV HEADER"
echo "✅  Pipeline complete."