import os
# 1. Silence HuggingFace warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import duckdb
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from datetime import date  # <--- NEW IMPORT

# Helper function to remove emojis/weird characters
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

print("Loading model and data...")
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

model = SentenceTransformer('all-MiniLM-L6-v2')
con = duckdb.connect("data/jobs.db")
df_jobs = con.sql("SELECT job_title, employer_name, job_description FROM jobs").df()

if df_jobs.empty:
    print("No jobs to visualize!")
    exit()

# Clean titles for the plot
df_jobs['clean_title'] = df_jobs['job_title'].apply(clean_text)

print("Calculating vectors...")

# --- NOTE: For consistency with match.py, you might want to use the structured string here too.
# But for now, we stick to reading the file as you requested.
try:
    with open("resume.txt", "r") as f:
        resume_text = f.read()
except FileNotFoundError:
    print("resume.txt not found! Using placeholder.")
    resume_text = "Data Scientist Machine Learning Engineer Python SQL"

resume_vector = model.encode([resume_text])
job_vectors = model.encode(df_jobs['job_description'].tolist())

all_vectors = np.vstack([resume_vector, job_vectors])

print("Squashing dimensions...")
pca = PCA(n_components=2)
reduced_vectors = pca.fit_transform(all_vectors)

my_coords = reduced_vectors[0]
job_coords = reduced_vectors[1:]

# --- PLOTTING ---
plt.figure(figsize=(12, 8))

# Plot YOU
plt.scatter(my_coords[0], my_coords[1], c='red', s=300, marker='*', label='My Resume')
plt.text(my_coords[0]+0.02, my_coords[1]+0.02, "YOU", fontsize=12, fontweight='bold', color='red')

# Plot JOBS
plt.scatter(job_coords[:, 0], job_coords[:, 1], c='blue', s=100, alpha=0.6, label='Jobs')

# Add Labels
for i, txt in enumerate(df_jobs['clean_title']):
    plt.text(job_coords[i, 0]+0.02, job_coords[i, 1], txt, fontsize=9, alpha=0.8)

plt.title(f'Job Market Map: {date.today()}', fontsize=16)
plt.xlabel('Dimension 1', fontsize=10)
plt.ylabel('Dimension 2', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# --- NEW SAVING LOGIC ---
# 1. Define the folder
save_folder = "daily_plots"

# 2. Create it if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 3. Create unique filename with date
today_str = date.today().strftime("%Y-%m-%d")
filename = f"{save_folder}/job_radar_{today_str}.png"

# 4. Save
plt.savefig(filename)
print(f"✅ Success! Saved plot to {filename}")

# --- DECODING THE AXES ---
df_coords = pd.DataFrame({
    'job_title': df_jobs['clean_title'],
    'x': job_coords[:, 0],
    'y': job_coords[:, 1]
})

print("\n--- WHAT DO THE AXES MEAN? ---")
print(f"LEFT   (Min X): {df_coords.sort_values('x').iloc[0]['job_title']}")
print(f"RIGHT  (Max X): {df_coords.sort_values('x', ascending=False).iloc[0]['job_title']}")
print(f"BOTTOM (Min Y): {df_coords.sort_values('y').iloc[0]['job_title']}")
print(f"TOP    (Max Y): {df_coords.sort_values('y', ascending=False).iloc[0]['job_title']}")