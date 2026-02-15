# 🎯 AI Job Sniper
> *An automated, AI-powered headhunter that hunts for jobs while I sleep.*

![Job Market Visualization](plots/job_radar.png)

## 💡 What is this?
Finding the perfect job is a data problem. Instead of doom-scrolling LinkedIn, I built an **ETL pipeline** that:
1.  **Extracts** fresh job postings daily from the web (via JSearch API).
2.  **Transforms** and filters data using SQL (DuckDB) to remove noise (e.g., non-English roles, high seniority).
3.  **Loads** clean data into a local OLAP database.
4.  **Matches** candidates using **Semantic Vector Search** (SBERT + Cosine Similarity) rather than simple keyword matching.
5.  **Notifies** me via email with a daily briefing of top matches.

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Database:** DuckDB (SQL-based OLAP)
* **AI/ML:** `sentence-transformers` (all-MiniLM-L6-v2), `scikit-learn` (PCA, Cosine Similarity)
* **Visualization:** Matplotlib (Dimensionality reduction plots)
* **Automation:** Windows Task Scheduler

## 🚀 How it Works

### 1. Extraction (`extract.py`)
Fetches "Machine Learning" and "Data Science" roles from the Netherlands.
* *Optimization:* Uses a `while` loop to handle pagination automatically.
* *API:* JSearch (RapidAPI).

### 2. Ingestion & Cleaning (`ingest.py`)
Ingests raw JSON into DuckDB and applies strict SQL filters:
* **Deduplication:** Uses Window Functions (`ROW_NUMBER()`) to remove duplicate listings across platforms.
* **Filtering:** Regex-based filtering to exclude roles requiring >3 years experience or Dutch fluency.

### 3. Vector Matching (`match.py`)
Instead of keyword matching, I use **Semantic Search**:
1.  Embeds my resume into a 384-dimensional vector.
2.  Embeds every job description into the same vector space.
3.  Calculates **Cosine Similarity** to find the mathematical "nearest neighbors" to my ideal role.

### 4. Visualization (`visualize.py`)
Uses **PCA (Principal Component Analysis)** to reduce the 384 dimensions down to 2D, plotting the "Job Market Map" to visually see where my profile sits relative to open positions.

## 📊 Setup
1.  Clone the repo:
    ```bash
    git clone [https://github.com/yourusername/job-sniper.git](https://github.com/yourusername/job-sniper.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file with your API keys:
    ```env
    RAPIDAPI_KEY=your_key_here
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_app_password
    ```
4.  Run the pipeline:
    ```bash
    python run_daily.py
    ```

## 📈 Future Improvements
* [ ] Add a Streamlit dashboard for interactive filtering.
* [ ] Integrate LLM (GPT-4) to generate custom cover letters for top matches.
* [ ] Deploy to AWS Lambda for cloud automation.

---
*Built by Giacomo Mossio*