import duckdb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

print("1. Loading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("2. Fetching Jobs...")
con = duckdb.connect("data/jobs.db")
df_jobs = con.sql("SELECT * FROM jobs").df()

if df_jobs.empty:
    print("No jobs found! Run ingest.py.")
    exit()

# --- DENSE RESUME EMBEDDING ---
# We construct a string that contains ONLY the high-signal keywords.
# This ensures the AI models what matters: Skills + Years + Domain.
structured_resume = """
Role: Data Scientist, Machine Learning Engineer, AI Engineer.
Experience: 1.5 years in End-to-End Machine Learning, Model Building, and Cloud Engineering.
Education: M.Sc. Computer Science, AI Specialization.
Core Skills: Python, Scikit-Learn, PyTorch, TensorFlow, Pandas, NumPy, SQL.
Engineering Skills: ETL Pipelines, Docker, Google Cloud Platform (GCP), Azure, CI/CD, MLOps, Airflow.
Focus: Building and deploying Predictive Models, Deep Learning, Time Series Analysis, Natural Language Processing (NLP).
Languages: English (Fluent), Italian (Native).
"""

print("3. encoding 'Dense' Resume...")
resume_vector = model.encode([structured_resume])

print("4. encoding Job Descriptions...")
# Batch encode 
job_vectors = model.encode(df_jobs['job_description'].tolist())

print("5. Matching...")
scores = cosine_similarity(resume_vector, job_vectors)[0]

df_jobs['match_score'] = scores
df_jobs = df_jobs.sort_values(by='match_score', ascending=False)

# Show Top 3 Matches
print("\n" + "="*50)
print("TOP 3 JOB MATCHES:")
print("="*50)

for index, row in df_jobs.head(3).iterrows():
    print(f"ROLE:   {row['job_title']}")
    print(f"COMPANY: {row['employer_name']}")
    print(f"SCORE:   {row['match_score']:.2f} / 1.0") # e.g. 0.85
    print("-" * 30)

# Optional: Save the best matches back to DuckDB or CSV
df_jobs.to_csv("best_matches.csv", index=False)
print("\nSaved top matches to 'best_matches.csv'")