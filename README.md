# 🎬 MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning

An end-to-end, production-grade Movie Recommendation System built with **Machine Learning**, **Python**, **Streamlit**, and **The Movie Database (TMDB) API**.

---

## 🌟 Key Features
1. **Hybrid Recommendation Engine**:
   - Blends **Content-Based Filtering** (TF-IDF + Cosine Similarity) and **Collaborative Filtering** (User-Item Interaction Matrix).
   - Dynamic weight adjustment slider ($\alpha$) to balance content similarity vs crowd rating patterns.
2. **Interactive Live Rating & Personalization**:
   - Users can rate movies (0.5 to 5 stars) in real-time.
   - The Collaborative Filtering model dynamically projects custom guest user ratings into the latent user matrix to deliver instantaneous personalized recommendations.
3. **Live Movie Catalog & Metadata**:
   - Searches and discovers current releases from TMDB, including paginated catalog results.
   - Applies genre, year, rating, runtime and Indian streaming-provider filters through live discovery.
   - Enriches IMDb-linked details with OMDb runtime, plot, cast and rating data when configured.
   - The MovieLens training data remains available offline; live browsing requires a TMDB key.
4. **Comprehensive ML Evaluation & Analytics**:
   - Benchmarked on the **MovieLens 100k dataset** (9,742 movies, 100,836 ratings, 610 users).
   - Evaluation metrics are calculated from held-out ratings and the actual recommendation models.
5. **Academic Project Report & Viva Voce**:
   - Full 10-section report conforming to university templates (JSPM's RSCOE format).
   - Generates both Microsoft Word (`.docx`) and Markdown (`.md`) reports.
   - 10 comprehensive Viva questions and model answers embedded directly in the app.

---

## 📂 Project Structure
```
ML MINI PROJECT/
├── app.py                      # Main Streamlit web application & dark-themed dashboard
├── content_based.py            # TF-IDF vectorizer & Cosine Similarity engine
├── collaborative.py            # User-item rating matrix & User-Based CF
├── hybrid.py                   # Weighted hybrid recommendation fusion engine
├── evaluation.py               # Precision@K, Recall@K, Hit Rate@K & RMSE evaluation
├── tmdb_api.py                 # TMDB v3 API client, image caching & offline fallbacks
├── movie_sources.py            # OMDb details and local environment configuration
├── movie_filters.py            # Strict local catalog filtering
├── data_loader.py              # Preprocessing, year extraction, tag aggregation
├── download_dataset.py         # Automated MovieLens dataset downloader
├── report_generator.py         # Automated DOCX and Markdown report generator
├── MovieMind_AI_Project_Report.docx # Formatted academic report for college submission
├── PROJECT_REPORT.md           # Full project documentation in Markdown
├── requirements.txt            # Python dependencies
├── tests/                      # Filter, metadata source and recommender tests
└── data/                       # MovieLens CSV dataset files
    ├── movies.csv
    ├── ratings.csv
    ├── tags.csv
    ├── links.csv
    └── evaluation_metrics.json
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API keys (optional)
Copy `.env.example` to `.env` and add your own TMDB and OMDb API keys:
```env
TMDB_API_KEY=your_tmdb_v3_api_key
TMDB_READ_ACCESS_TOKEN=your_tmdb_read_access_token
OMDB_API_KEY=your_omdb_api_key
```
The keys can also be entered under **Settings**. `.env` is excluded from Git; never commit API keys. TMDB discovery supports up to 500 pages per query, not literally unlimited. OMDb provides details by IMDb ID; it does not provide a current-release discovery feed.

**Security:** Revoke and replace any API key shared in a screenshot, URL, chat, or public repository before using it.

### 3. Launch the Web Application
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run focused checks
```bash
python -m unittest discover -s tests
```

---

## 🧠 Machine Learning Algorithms Explained

### 1. Content-Based Filtering
- **Feature Extraction**: Combines movie title, genres, and user tags into an enriched text metadata soup.
- **TF-IDF Vectorization**: Converts terms into numerical weights reflecting their uniqueness and relevance.
- **Cosine Similarity**: Computes the cosine angle between target movie vector $A$ and catalog vector $B$:
  $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

### 2. Collaborative Filtering
- **User-Item Matrix**: Rows represent users, columns represent movies, entries contain ratings ($0.5$ to $5.0$).
- **Mean-Centering**: Normalizes user ratings by subtracting user average rating to eliminate personal bias.
- **Neighbor-Weighted Prediction**:
  $$\hat{r}_{u, i} = \bar{r}_u + \frac{\sum_{v \in N(u)} sim(u, v) \cdot (r_{v, i} - \bar{r}_v)}{\sum_{v \in N(u)} |sim(u, v)|}$$

### 3. Weighted Hybrid Fusion
- Combines normalized scores from both engines with parameter $\alpha \in [0, 1]$:
  $$\text{Score}_{\text{Hybrid}} = \alpha \cdot \text{Score}_{\text{Content}} + (1 - \alpha) \cdot \text{Score}_{\text{Collab}}$$
- Can fall back to content or collaborative signals when one side is unavailable; new live titles remain outside the MovieLens-trained model until ratings/features are incorporated.

## Live data and filter behavior
- The random picker uses TMDB discovery when configured and applies genre, era, rating, sort and streaming-provider filters together.
- **Under 90 minutes** is strict: titles with missing runtime or runtime of 90 minutes or more are rejected. OMDb can supplement missing TMDB runtime when configured.
- If no title satisfies every selected constraint, the app reports that instead of silently widening the filters.
- New live TMDB titles can be browsed, but the recommendation models are trained on the bundled MovieLens ratings and do not yet learn from live titles.
