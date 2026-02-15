import duckdb
import json
import os

print("Starting ingestion with Advanced Filters...")

# 1. Safety Check: Is the file empty?
file_path = 'data/raw_jobs.json'
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
        if not data:
            print("⚠️ Warning: data/raw_jobs.json is empty. No jobs found to ingest.")
            exit()
except Exception as e:
    print(f"❌ Error reading JSON: {e}")
    exit()

con = duckdb.connect("data/jobs.db")

# 2. Ingest raw data
con.sql("CREATE OR REPLACE TABLE jobs_unfiltered AS SELECT * FROM read_json_auto('data/raw_jobs.json')")

count_before = con.sql("SELECT COUNT(*) FROM jobs_unfiltered").fetchone()[0]
print(f"Total Jobs Before Filtering: {count_before}")

# 3. Apply Strict Filters (Experience, Language, Seniority)
query = """
    CREATE OR REPLACE TABLE jobs AS 
    SELECT 
        job_id,
        job_title,
        employer_name,
        COALESCE(job_city, job_country, 'Remote/Netherlands') as job_location,
        job_description,
        job_apply_link
    FROM (
        SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY job_title, employer_name ORDER BY job_posted_at_timestamp DESC) as rn
        FROM jobs_unfiltered
    )
    WHERE rn = 1
    -- FILTER: Seniority
    AND LOWER(job_title) NOT LIKE '%senior%'
    AND LOWER(job_title) NOT LIKE '%sr.%'
    AND LOWER(job_title) NOT LIKE '%sr %'
    AND LOWER(job_title) NOT LIKE '%staff%'
    AND LOWER(job_title) NOT LIKE '%lead%'
    AND LOWER(job_title) NOT LIKE '%principal%'
    AND LOWER(job_title) NOT LIKE '%manager%'
    AND LOWER(job_title) NOT LIKE '%head of%'
    
    -- FILTER: Dutch Language
    AND LOWER(job_title) NOT LIKE '%dutch%'
    AND LOWER(job_description) NOT LIKE '%dutch required%'
    AND LOWER(job_description) NOT LIKE '%vloeiend nederlands%'
    AND LOWER(job_description) NOT LIKE '%beheersing van de nederlandse%'
    AND LOWER(job_description) NOT LIKE '% het %'
    AND LOWER(job_description) NOT LIKE '% een %'
    AND LOWER(job_description) NOT LIKE '% en %'
    
    -- FILTER: Experience > 3 Years (Regex)
    AND NOT REGEXP_MATCHES(job_description, '([4-9]|[1-9][0-9])\+?\s*(years|year|jaar|jaren)')
;
"""

con.sql(query)
con.sql("DROP TABLE jobs_unfiltered")

print("✅ Database updated with Language & Experience filters.")

count_after = con.sql("SELECT COUNT(*) FROM jobs").fetchone()[0]
print(f"Total Jobs After Filtering: {count_after}")
print(f"Jobs Removed: {count_before - count_after}")