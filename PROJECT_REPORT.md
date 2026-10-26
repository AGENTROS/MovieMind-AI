# MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning
**JSPM's Rajarshi Shahu College of Engineering, Tathawade, Pune-33**  
**Department of Computer Engineering**  
*Class: TY Div C | Course: Machine Learning | Academic Year 2026-27 (Semester-I)*

---

## 1. Title
**MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning**

## 2. Abstract
With the rapid proliferation of on-demand digital streaming services, catalog sizes have exploded into tens of thousands of titles. Consequently, users encounter severe choice overload and decision fatigue. This project develops **MovieMind AI**, an intelligent hybrid movie recommendation system built in Python using Machine Learning. The system synthesizes **Content-Based Filtering** (TF-IDF Vectorization and Cosine Similarity) and **Collaborative Filtering** (user-item rating matrices with user mean-centering). Its measured hybrid Hit Rate@5 is 13.33% across 30 held-out evaluation users; these values are dataset-specific and do not imply that the hybrid model always beats each baseline. A responsive Streamlit dashboard provides paginated TMDB discovery and OMDb-linked movie details.

## 3. Introduction
Recommendation systems represent one of the most commercially impactful applications of Machine Learning. Unlike search engines that necessitate proactive keyword queries, recommender systems anticipate consumer desire by analyzing implicit and explicit behavioral patterns.
1. **Content-Based Filtering**: Leverages item metadata (genres, titles, keywords) to identify close mathematical vectors.
2. **Collaborative Filtering**: Exploits collective rating histories across the user base to predict preferences for unseen items.
3. **Hybrid Architecture**: Melds both approaches to balance accuracy, novelty, and robustness against data sparsity.

## 4. Problem Statement
Traditional discovery mechanisms suffer from generic popularity bias or uncurated search results. Content-Based models suffer from narrow overspecialization (e.g. recommending only space movies to someone who liked Interstellar). Conversely, Collaborative Filtering falters when new items or users enter the system with zero historical ratings (the Cold-Start problem). MovieMind AI combines both signals and provides live browsing, while live titles remain outside the MovieLens-trained models.

## 5. Objectives
1. Clean, preprocess, and enrich the MovieLens 100k dataset.
2. Implement Content-Based Filtering using TF-IDF and Cosine Similarity.
3. Implement User-Based Collaborative Filtering using user-item rating matrices and deviation-from-mean predictions.
4. Construct a weighted Hybrid Recommender engine ($Score_{Hybrid} = \alpha S_{CB} + (1-\alpha) S_{CF}$).
5. Evaluate models using Precision@K, Recall@K, Hit Rate@K, and RMSE.
6. Provide an interactive web dashboard in Streamlit with real-time ratings and TMDB API poster integration.

## 6. Dataset and Libraries Required
- **Dataset**: GroupLens MovieLens Latest Small (9,742 movies, 100,836 ratings, 610 users, 3,683 tags).
- **Libraries**: `python` 3.10+, `pandas`, `numpy`, `scikit-learn`, `streamlit`, `requests`, `python-docx`.

## 7. Approach / Methodology
- **TF-IDF & Cosine Similarity**:
  $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
- **User-Based Collaborative Filtering**:
  $$\hat{r}_{u, i} = \bar{r}_u + \frac{\sum_{v \in N(u)} sim(u, v) \cdot (r_{v, i} - \bar{r}_v)}{\sum_{v \in N(u)} |sim(u, v)|}$$
- **Hybrid Fusion**:
  $$Score_{Hybrid} = \alpha \cdot Score_{Content} + (1 - \alpha) \cdot Score_{Collaborative}$$

## 8. Implementation
- `data_loader.py`: Preprocessing, year extraction, tag aggregation, rating stats.
- `content_based.py`: TF-IDF matrix computation and cosine distance ranking.
- `collaborative.py`: Pivot matrix, user mean-centering, and live guest user rating projection.
- `hybrid.py`: Dynamic linear fusion model.
- `evaluation.py`: Train-test evaluation benchmarking.
- `tmdb_api.py`: TMDB v3 API client, paginated discovery and metadata caching.
- `movie_sources.py`: OMDb details by IMDb ID and local API-key configuration.
- `movie_filters.py`: Strict local catalog filter implementation.
- `app.py`: Streamlit dark-mode web application.

## 9. Results and Evaluation
| Model | Precision@5 | Recall@5 | Hit Rate@5 | RMSE |
|---|---|---|---|---|
| Content-Based Filtering | 3.33% | 0.13% | 16.67% | N/A |
| Collaborative Filtering | 4.67% | 0.24% | 20.00% | 1.208 |
| Hybrid Model (α = 0.5) | 3.33% | 0.19% | 13.33% | N/A |

## 10. Conclusion
The system combines content-based filtering and collaborative user signals, then reports held-out metrics from the actual recommendation implementations. Results are dataset- and evaluation-sample-specific; new TMDB movies can be browsed but are not added to the MovieLens training data.
