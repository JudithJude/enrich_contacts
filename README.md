# Contacts Enrichment Pipeline  
*Python + RapidFuzz + Postgres + Metabase*

This repo cleans a HubSpot contact export, merges a 5 M-row KoldLeads dataset, fuzzy-matches company names to pull e-mails, and surfaces everything in Postgres + Metabase.

---

## 🚀 Quick Start (5 min)

```bash
git clone https://github.com/JudithJude/contacts_enrich.git.git
cd contacts_enrich

# Spin up Postgres + Metabase + Pgadmin
docker compose up -d          # ports 5432 / 3000 & / 8080

# Python env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# Drop Source Files
data/contacts_raw.csv                # HubSpot export
data/koldleads/                      # place all six XLSX lead files here

#Run the Pipeline
bash run_pipeline.sh

Output:

data/contacts_enriched_fuzzy.csv (10 cols, 4 159 rows)

Postgres table contacts_enriched_fuzzy

🖥️ Metabase
URL → http://localhost:3000

First-run: create admin user → add DB contacts_enrich

host postgres, user/pass metabase, db contacts_enrich

Import metabase_dashboard.json (Admin → Templates)

KPI cards, similarity histogram, top domains, low-confidence & unmatched tables are pre-built.


🔄 Refresh Workflow
Replace data/contacts_raw.csv with a new export.

bash run_pipeline.sh – cleans, matches, and COPYs to Postgres.

Metabase auto-updates (or click Sync schema).



🐍 Scripts Overview
Script	Purpose
clean_contacts.py	Standardises headers, dedupes, writes contacts_cleaned.csv.
generate_linkedin_search_urls.py	Adds linkedin_search_url column.
read_koldleads_xlsx.py	Reads every XLSX in data/koldleads/, writes koldleads_combined.csv.
fuzzy_enrich.py	RapidFuzz match (threshold ≥ 0.60) → contacts_enriched_fuzzy.csv.


❓ FAQ
Q How long does the fuzzy-match run?
A ≈ 4 h 45 m on a 4-core laptop (4 k contacts vs 5.1 M leads).

Q Can I add more lead files?
Yes – drop any extra XLSX into data/koldleads/ and rerun run_pipeline.sh.

Q How can I tweak the similarity threshold?
Edit THRESHOLD at the top of scripts/fuzzy_enrich.py, rerun the script.

Q Disk space is huge – tips?
gzip koldleads_raw.csv shrinks 1.1 GB → ~180 MB. All large files are in .gitignore.

Q Metabase doesn’t see my new table.
Admin → Databases → contacts_enrich → Sync schema (or wait for auto-sync).