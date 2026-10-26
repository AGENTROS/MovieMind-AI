import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from evaluation import get_cached_or_default_metrics

REPORT_DOCX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MovieMind_AI_Project_Report.docx')
REPORT_MD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PROJECT_REPORT.md')

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def generate_docx_report():
    metrics = get_cached_or_default_metrics()
    doc = Document()

    # Set standard margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ----------------- COVER PAGE (JSPM RSCOE Format) -----------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("JSPM's\nRAJARSHI SHAHU COLLEGE OF ENGINEERING\nTATHAWADE, PUNE-33\n")
    run_inst.font.name = 'Arial'
    run_inst.font.size = Pt(13)
    run_inst.bold = True
    run_inst.font.color.rgb = RGBColor(30, 41, 59)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_dept = p_dept.add_run("DEPARTMENT OF COMPUTER ENGINEERING\n")
    run_dept.font.name = 'Arial'
    run_dept.font.size = Pt(12)
    run_dept.bold = True
    run_dept.font.color.rgb = RGBColor(59, 130, 246)

    doc.add_paragraph("\n")

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_proj = p_proj.add_run("Mini Project\non\n")
    run_proj.font.name = 'Arial'
    run_proj.font.size = Pt(14)
    run_proj.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("“MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning”\n")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(16)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph("\n")

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("-Submitted by-\n")
    run_sub.font.size = Pt(11)
    run_sub.italic = True

    p_students = doc.add_paragraph()
    p_students.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_students.add_run(
        "1. Name of Student: ___________________  Roll No: _________\n"
        "2. Name of Student: ___________________  Roll No: _________\n"
        "3. Name of Student: ___________________  Roll No: _________\n"
    )
    r_s.font.size = Pt(11)

    doc.add_paragraph("\n")

    p_class = doc.add_paragraph()
    p_class.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_class.add_run(
        "Class and Division: TY Div C\n"
        "Course: Machine Learning\n"
        "Academic Year 2026-27\n"
        "(Semester-I)"
    )
    r_c.font.size = Pt(11)
    r_c.bold = True

    doc.add_page_break()

    # ----------------- HELPER FOR HEADINGS -----------------
    def add_section_heading(num_str, title_str):
        h = doc.add_heading(level=1)
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.name = 'Arial'
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        return p

    # 1. TITLE
    add_section_heading("1", "Title")
    p = doc.add_paragraph(
        "MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning"
    )
    p.runs[0].bold = True

    # 2. ABSTRACT
    add_section_heading("2", "Abstract")
    doc.add_paragraph(
        "With the explosive growth of digital streaming platforms, users are overwhelmed with thousands of movie choices, "
        "leading to decision fatigue. Recommendation systems have emerged as an indispensable technology to filter and discover "
        "relevant content tailored to individual tastes. This project presents MovieMind AI, a hybrid movie recommendation system "
        "engineered using Python and Machine Learning. The system integrates two core paradigms: Content-Based Filtering via "
        "TF-IDF Vectorization and Cosine Similarity, and Collaborative Filtering using User-Item rating matrices and user-user similarity. "
        "To mitigate individual algorithmic shortcomings—such as overspecialization in content-based methods and the cold-start problem "
        "in collaborative filtering—a weighted hybrid engine is developed. The system is benchmarked on the MovieLens 100k dataset "
        "utilizing Precision@K, Recall@K, Hit Rate@K, and Root Mean Squared Error (RMSE). A production-ready, dark-themed interactive "
        "dashboard built with Streamlit provides live movie search, dynamic user rating submission, live TMDB API poster integration, "
        "and real-time recommendation updates."
    )

    # 3. INTRODUCTION
    add_section_heading("3", "Introduction")
    doc.add_paragraph(
        "Recommendation systems play a pivotal role in modern digital consumption, powering platforms such as Netflix, Amazon Prime, "
        "Spotify, and YouTube. In traditional e-commerce or streaming environments, users often struggle to find media that matches "
        "their nuanced preferences. Information retrieval alone is insufficient because search engines require users to formulate exact "
        "queries, whereas recommendation systems proactively suggest relevant media.\n\n"
        "Machine Learning recommendation algorithms are categorized primarily into:\n"
        "1. Content-Based Filtering: Analyzes item attributes (genres, plot summaries, user tags) to compute vector similarities.\n"
        "2. Collaborative Filtering: Analyzes historical rating interactions across a user community to identify correlated taste profiles.\n"
        "3. Hybrid Recommendation Systems: Combines both paradigms to achieve superior recommendation accuracy and eliminate individual algorithmic weaknesses."
    )

    # 4. PROBLEM STATEMENT
    add_section_heading("4", "Problem Statement")
    doc.add_paragraph(
        "Traditional movie discovery mechanisms rely either on generic popularity rankings or rigid search queries, which fail "
        "to deliver personalized cinematic experiences. Furthermore, standalone Content-Based Filtering models suffer from "
        "overspecialization (recommending only identical genres), while standalone Collaborative Filtering models suffer from the "
        "notorious Cold-Start Problem when new users or unrated movies enter the system. The objective of this project is to design, "
        "implement, and evaluate a comprehensive Hybrid Movie Recommendation System that simultaneously addresses cold-start limitations, "
        "provides transparent ML evaluation metrics, and offers a modern interactive user interface."
    )

    # 5. OBJECTIVES
    add_section_heading("5", "Objectives")
    doc.add_paragraph(
        "The primary objectives of the MovieMind AI project are:\n"
        "1. To preprocess and analyze the MovieLens dataset (9,742 movies, 100,836 ratings, 610 users).\n"
        "2. To implement Content-Based Filtering utilizing Term Frequency-Inverse Document Frequency (TF-IDF) and Cosine Similarity.\n"
        "3. To implement User-Based Collaborative Filtering using Mean-Centered User-Item interaction matrices and Pearson/Cosine similarity.\n"
        "4. To develop a weighted Hybrid Recommendation Engine that synergistically combines Content and Collaborative signals.\n"
        "5. To rigorously evaluate and compare both approaches using Precision@K, Recall@K, Hit Rate@K, and RMSE.\n"
        "6. To construct an interactive, modern dark-themed web application utilizing Streamlit with live movie search, custom user rating inputs, and TMDB API poster integration."
    )

    # 6. DATASET AND LIBRARIES REQUIRED
    add_section_heading("6", "Dataset and Libraries Required")
    doc.add_paragraph(
        "Dataset Description:\n"
        "The project utilizes the official MovieLens Latest Small dataset provided by GroupLens Research at the University of Minnesota. "
        "The dataset consists of:\n"
        "• movies.csv: 9,742 movies with attributes `movieId`, `title`, and pipe-separated `genres`.\n"
        "• ratings.csv: 100,836 ratings applied on a 5-star scale (0.5 to 5.0) across 610 unique users.\n"
        "• tags.csv: 3,683 user-generated textual tags associated with movies.\n"
        "• links.csv: Cross-reference identifiers mapping `movieId` to external `imdbId` and `tmdbId`."
    )
    
    # Table of Libraries
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].text = "Library / Tool"
    hdr[1].text = "Version"
    hdr[2].text = "Purpose in Project"
    for cell in hdr:
        set_cell_background(cell, "1E3A8A")
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

    libs = [
        ("Python", "3.10+", "Core programming language"),
        ("Pandas & NumPy", "Latest", "Matrix manipulation, data preprocessing, and vectorized calculations"),
        ("Scikit-Learn", "Latest", "TF-IDF Vectorization, Cosine Similarity, and train-test splitting"),
        ("Streamlit", "1.30+", "Interactive dark-theme web dashboard and reactive UI components"),
        ("TMDB API & Requests", "v3", "Dynamic fetching of live high-definition posters, backdrops, and YouTube trailers"),
        ("Python-Docx", "1.0+", "Automated generation of IEEE/college academic documentation")
    ]
    for lib, ver, purp in libs:
        row = table.add_row().cells
        row[0].text = lib
        row[1].text = ver
        row[2].text = purp

    doc.add_paragraph("\n")

    # 7. APPROACH / METHODOLOGY
    add_section_heading("7", "Approach / Methodology")
    doc.add_paragraph(
        "The architecture of MovieMind AI is organized into three sequential modules:\n\n"
        "A. Feature Engineering & Content-Based Filtering:\n"
        "Movie genres, cleaned titles, and user-generated tags are concatenated into an enriched content soup. "
        "TF-IDF vectorizer extracts n-gram frequency matrices representing semantic features. "
        "Cosine similarity measures the angle between movie vector A and candidate vector B:\n"
        "   Cosine Similarity(A, B) = (A · B) / (||A|| ||B||)\n\n"
        "B. User-Based Collaborative Filtering:\n"
        "A User-Item matrix is constructed where rows represent users and columns represent movies. "
        "To mitigate user rating bias (some users systematically rate higher than others), user ratings are normalized by mean-centering: "
        "s_{u, i} = r_{u, i} - r̄_u. Cosine similarity determines user neighborhood N(u). "
        "Predicted rating for unseen movie i is computed via similarity-weighted deviation:\n"
        "   r̂_{u, i} = r̄_u + [ Σ_{v ∈ N(u)} sim(u, v) * (r_{v, i} - r̄_v) ] / [ Σ_{v ∈ N(u)} |sim(u, v)| ]\n\n"
        "C. Weighted Hybrid Fusion:\n"
        "Scores from Content similarity (S_CB ∈ [0, 1]) and Collaborative predicted rating (normalized S_CF ∈ [0, 1]) "
        "are fused via a tunable hyperparameter α (default 0.5):\n"
        "   Score_Hybrid = α * S_CB + (1 - α) * S_CF\n"
        "This formulation guarantees reliable recommendations even when a user has no prior ratings (α defaults to 1.0) "
        "or when a movie has no tags (α shifts toward CF)."
    )

    # 8. IMPLEMENTATION
    add_section_heading("8", "Implementation")
    doc.add_paragraph(
        "The project is structured modularly for maintainability and scalability:\n"
        "• data_loader.py: Cleans titles, aggregates tags, computes aggregate rating stats, and loads CSV files.\n"
        "• content_based.py: Implements TF-IDF vectorization and cosine similarity retrieval.\n"
        "• collaborative.py: Implements User-Item matrix generation, user mean-centering, and dynamic guest user rating vectors.\n"
        "• hybrid.py: Integrates Content and Collaborative scores with linear weighting.\n"
        "• evaluation.py: Splits ratings into 80% train / 20% test sets and computes Precision@K, Recall@K, Hit Rate@K, and RMSE.\n"
        "• tmdb_api.py: Handles TMDB v3 API communication with local disk caching and curated offline image fallbacks.\n"
        "• app.py: Streamlit frontend featuring 6 dedicated views matching modern streaming UI designs:\n"
        "  1. Home Dashboard with hero banner and genre filtering\n"
        "  2. Search & Explore with live filters\n"
        "  3. Movie Details with high-res posters, overviews, and YouTube trailers\n"
        "  4. Personalized Recommendations (Content, Collaborative, and Hybrid tabs)\n"
        "  5. Interactive My Ratings system with live rating analytics\n"
        "  6. Model Analytics & Comparison dashboard"
    )

    # 9. RESULTS
    add_section_heading("9", "Results and Evaluation")
    doc.add_paragraph(
        "The system was evaluated using an 80/20 train-test split over active MovieLens users. "
        f"The table reports measured Precision@{metrics['k']}, Recall@{metrics['k']}, "
        "Hit Rate, and rating-prediction error; results are specific to this dataset and sample."
    )

    # Results Table
    res_table = doc.add_table(rows=1, cols=5)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_hdr = res_table.rows[0].cells
    r_hdr[0].text = "Approach"
    r_hdr[1].text = f"Precision@{metrics['k']}"
    r_hdr[2].text = f"Recall@{metrics['k']}"
    r_hdr[3].text = f"Hit Rate@{metrics['k']}"
    r_hdr[4].text = "RMSE"
    for cell in r_hdr:
        set_cell_background(cell, "1E3A8A")
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

    evaluation_rows = [
        ("Content-Based Filtering", metrics["content_based"]),
        ("Collaborative Filtering", metrics["collaborative"]),
        ("Hybrid Model (α = 0.5)", metrics["hybrid"]),
    ]
    for model_name, model_metrics in evaluation_rows:
        row = res_table.add_row().cells
        row[0].text = model_name
        row[1].text = f"{model_metrics['precision']:.2f}%"
        row[2].text = f"{model_metrics['recall']:.2f}%"
        row[3].text = f"{model_metrics['hit_rate']:.2f}%"
        row[4].text = (
            f"{model_metrics['rmse']:.3f}"
            if model_metrics.get("rmse") is not None else "N/A"
        )

    doc.add_paragraph(
        "\nObservations:\n"
        "1. Content-Based Filtering finds movies with similar metadata, though it can produce homogeneous genre suggestions. "
        "It does not add live TMDB movies to the MovieLens-trained models.\n"
        "2. Collaborative Filtering captures latent user preferences and predicts ratings for unseen movies.\n"
        f"3. These measured results use {metrics['sample_users_evaluated']} users and the implemented held-out evaluation; "
        "they should be interpreted as dataset-specific measurements rather than a guarantee that the hybrid model outperforms every baseline."
    )

    # 10. CONCLUSION
    add_section_heading("10", "Conclusion")
    doc.add_paragraph(
        "In this project, MovieMind AI—a hybrid movie recommendation system—was successfully designed, implemented, and evaluated. "
        "By fusing Content-Based Filtering (TF-IDF + Cosine Similarity) with User-Based Collaborative Filtering (Mean-Centered Rating "
        "Matrices), the system can use either signal when the other is unavailable, but it does not eliminate cold-start limitations. "
        f"Empirical evaluation on the MovieLens dataset measured a {metrics['hybrid']['hit_rate']:.2f}% "
        f"Hit Rate@{metrics['k']} for the hybrid engine across {metrics['sample_users_evaluated']} users. "
        "The modern Streamlit dashboard with TMDB API integration delivers an intuitive and visually compelling interface suitable "
        "for real-world streaming environments.\n\n"
        "Future Scope:\n"
        "• Deep Learning Embeddings: Implementing Matrix Factorization using Neural Collaborative Filtering (NCF) or Autoencoders.\n"
        "• Context-Aware Recommendations: Incorporating temporal features such as time of day, day of week, or mood.\n"
        "• Scalable Cloud Deployment: Deploying the recommendation microservice on AWS / Google Cloud Run with distributed Redis caching."
    )

    doc.save(REPORT_DOCX_PATH)
    print(f"Project Report successfully created at {REPORT_DOCX_PATH}")

def generate_markdown_report():
    metrics = get_cached_or_default_metrics()
    with open(REPORT_MD_PATH, 'w', encoding='utf-8') as f:
        report = """# MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning
**JSPM's Rajarshi Shahu College of Engineering, Tathawade, Pune-33**  
**Department of Computer Engineering**  
*Class: TY Div C | Course: Machine Learning | Academic Year 2026-27 (Semester-I)*

---

## 1. Title
**MovieMind AI: A Hybrid Movie Recommendation System Using Machine Learning**

## 2. Abstract
With the rapid proliferation of on-demand digital streaming services, catalog sizes have exploded into tens of thousands of titles. Consequently, users encounter severe choice overload and decision fatigue. This project develops **MovieMind AI**, an intelligent hybrid movie recommendation system built in Python using Machine Learning. The system synthesizes **Content-Based Filtering** (TF-IDF Vectorization and Cosine Similarity) and **Collaborative Filtering** (user-item rating matrices with user mean-centering). Its measured hybrid Hit Rate@__K__ is __HYBRID_HIT__% across __USERS__ held-out evaluation users; these values are dataset-specific and do not imply that the hybrid model always beats each baseline. A responsive Streamlit dashboard provides paginated TMDB discovery and OMDb-linked movie details.

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
4. Construct a weighted Hybrid Recommender engine ($Score_{Hybrid} = \\alpha S_{CB} + (1-\\alpha) S_{CF}$).
5. Evaluate models using Precision@K, Recall@K, Hit Rate@K, and RMSE.
6. Provide an interactive web dashboard in Streamlit with real-time ratings and TMDB API poster integration.

## 6. Dataset and Libraries Required
- **Dataset**: GroupLens MovieLens Latest Small (9,742 movies, 100,836 ratings, 610 users, 3,683 tags).
- **Libraries**: `python` 3.10+, `pandas`, `numpy`, `scikit-learn`, `streamlit`, `requests`, `python-docx`.

## 7. Approach / Methodology
- **TF-IDF & Cosine Similarity**:
  $$\\text{Cosine Similarity}(A, B) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|}$$
- **User-Based Collaborative Filtering**:
  $$\\hat{r}_{u, i} = \\bar{r}_u + \\frac{\\sum_{v \\in N(u)} sim(u, v) \\cdot (r_{v, i} - \\bar{r}_v)}{\\sum_{v \\in N(u)} |sim(u, v)|}$$
- **Hybrid Fusion**:
  $$Score_{Hybrid} = \\alpha \\cdot Score_{Content} + (1 - \\alpha) \\cdot Score_{Collaborative}$$

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
__EVALUATION_TABLE__

## 10. Conclusion
The system combines content-based filtering and collaborative user signals, then reports held-out metrics from the actual recommendation implementations. Results are dataset- and evaluation-sample-specific; new TMDB movies can be browsed but are not added to the MovieLens training data.
"""
        evaluation_rows = [
            ("Content-Based Filtering", metrics["content_based"]),
            ("Collaborative Filtering", metrics["collaborative"]),
            ("Hybrid Model (α = 0.5)", metrics["hybrid"]),
        ]
        table_rows = [
            "| Model | Precision@{k} | Recall@{k} | Hit Rate@{k} | RMSE |".format(
                k=metrics["k"]
            ),
            "|---|---|---|---|---|",
        ]
        for model_name, model_metrics in evaluation_rows:
            rmse = (
                f"{model_metrics['rmse']:.3f}"
                if model_metrics.get("rmse") is not None else "N/A"
            )
            table_rows.append(
                f"| {model_name} | {model_metrics['precision']:.2f}% | "
                f"{model_metrics['recall']:.2f}% | "
                f"{model_metrics['hit_rate']:.2f}% | {rmse} |"
            )
        report = (
            report.replace("__EVALUATION_TABLE__", "\n".join(table_rows))
            .replace("__K__", str(metrics["k"]))
            .replace("__HYBRID_HIT__", f"{metrics['hybrid']['hit_rate']:.2f}")
            .replace("__USERS__", str(metrics["sample_users_evaluated"]))
        )
        f.write(report)
    print(f"Markdown report generated at {REPORT_MD_PATH}")

if __name__ == '__main__':
    generate_docx_report()
    generate_markdown_report()
