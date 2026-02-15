import requests
import json
import os
import time
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("RAPIDAPI_KEY")

# --- CONFIGURATION ---
SEARCH_MODE = "country" 
TARGET_CITY = "Amsterdam"
JOB_TITLES = ["Data jobs", "Data Scientist", "Machine Learning Engineer", "AI Engineer"] 
# ---------------------

all_jobs = []
seen_ids = set()

print(f"🔎 Starting Search ...")

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

for title in JOB_TITLES:
    if SEARCH_MODE == "city":
        query_text = f"{title} in {TARGET_CITY}, Netherlands"
    else:
        query_text = f"{title} in Netherlands"
        
    print(f"   Fetching: {title}...")

    querystring = {
        "query": query_text,
        "num_pages": "5",
        "country": "nl",         
        "date_posted": "week",  # Only recent jobs --> all, today, 3days, week, month
        # BROKEN --> "job_requirements": "under_3_years_experience" # Junior/Medior only    
        }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('data', [])
            
            new_count = 0
            for job in jobs:
                job_id = job.get('job_id')
                if job_id not in seen_ids:
                    all_jobs.append(job)
                    seen_ids.add(job_id)
                    new_count += 1
            
            print(f"     Found {len(jobs)} results, {new_count} unique new ones.")
        else:
            print(f"     ❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"     ❌ Exception: {e}")

    time.sleep(1) 

print(f"\n✅ Total Jobs Collected: {len(all_jobs)}")

# Save to file
output_path = 'data/raw_jobs.json'
with open(output_path, 'w') as f:
    json.dump(all_jobs, f, indent=4)
print(f"Saved to {output_path}")