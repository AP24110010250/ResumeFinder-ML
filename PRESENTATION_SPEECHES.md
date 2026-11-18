# PROJECT PRESENTATION & VIVA GUIDE
## ML-Based Resume Screening and Candidate Ranking System
### Team Roles, Presentation Speeches, Folders & Files to Demonstrate

---

# MEMBER 1: Problem Statement, Solution, Dataset Analysis & Feature Engineering

### 1. Folders & Files to Take Care Of:
- **Folder:** `data/`
- **Configuration File:** `utils/config.py`
- **Core Dataset File:** `data/Rupa_dataset.csv`

### 2. Files to Open & Show When Explaining:
1. **Show `data/Rupa_dataset.csv`**: Show the 3,000 candidate records and highlight columns (`Skills`, `Experience`, `CGPA`, `Job Role`, `Final Decision`).
2. **Show `utils/config.py`**: Point to lines containing `EXCLUDED_COLUMNS` and `FEATURE_COLUMNS` to prove how leaky columns were systematically removed and how the 11 candidate features were defined.

---

### 3. Speech to be Spoken (Word-for-Word):

> "Respected evaluators and professors, good morning. 
>
> Today, our team is presenting our project: an **ML-Based Resume Screening and Candidate Ranking System**.
>
> In modern recruitment, companies and HR recruiters receive hundreds of applicant resumes for every single job opening. Manually screening and evaluating each resume is extremely slow, tedious, prone to human error, and subjective. On the other hand, traditional keyword search tools like basic Ctrl+F fail because they only look for exact character matches, ignoring candidate seniority, experience progression, and overall role suitability.
>
> To solve this problem, we developed an intelligent, automated system. It allows HR to enter specific job requirements, upload multiple candidate PDF resumes, extract their qualifications using NLP, and evaluate them using a Machine Learning pipeline trained on historical hiring patterns. It then predicts the candidate's Hire probability, ranks them from highest to lowest, and highlights any missing skills or unmet requirements.
>
> Now, looking at the dataset that powers our machine learning model:
> *(Point to `Rupa_dataset.csv`)*
>
> We used `Rupa_dataset.csv`, which contains exactly 3,000 historical candidate records. Our target variable is `Final Decision`, which consists of 1,969 Hire records (approximately 65.6%) and 1,031 Reject records (approximately 34.4%). In terms of data quality, the dataset has only 166 missing values, all localized to `Previous Job Title`. We handle these missing entries cleanly via imputation without fabricating any synthetic data.
>
> One of our most important contributions was **Target Leakage Prevention**:
> *(Point to `utils/config.py`)*
>
> The raw dataset contained columns like `Skill Match Score`, `Role Match Score`, and `LinkedIn Score`. Including these columns would artificially inflate accuracy on paper, but it is considered data leakage because when a real candidate uploads a raw PDF resume, these precalculated scores do not exist. Therefore, we strictly excluded them, along with candidate IDs and names.
>
> After auditing and cleaning, we engineered and selected **11 core features**:
> - **1 Text Feature:** `Skills` (which feeds directly into TF-IDF vectorization).
> - **6 Numerical Features:** `Experience (Years)`, `CGPA`, `Certifications Count`, `Project Count`, `Internship Experience`, and `Years Since Graduation`.
> - **4 Categorical Features:** `Education Level`, `Previous Job Title`, `Job Role`, and `Job Type`.
>
> These 11 features align identically between what our model was trained on and what our parser extracts from uploaded PDF resumes.
>
> Now, Member 2 will explain our Machine Learning architecture, model training, and ranking logic."

---

# MEMBER 2: Machine Learning Architecture, Training & Ranking Logic

### 1. Folders & Files to Take Care Of:
- **Folder:** `ml/`
- **Model Training File:** `ml/train_model.py`
- **Prediction File:** `ml/prediction.py`
- **Ranking File:** `ml/ranking.py`
- **Saved Model Pipeline:** `ml/model_pipeline.joblib`
- **Unit Test File:** `tests/test_ranking.py`

### 2. Files to Open & Show When Explaining:
1. **Show `ml/train_model.py`**: 
   - Point to `split_dataset()`: Show the 70/15/15 stratified train-val-test split.
   - Point to `build_pipeline()`: Show the `ColumnTransformer` (median imputer, one-hot encoder, TF-IDF vectorizer, and `RandomForestClassifier`).
2. **Show `ml/prediction.py`**: Point to `get_hire_class_index()` and `predict_proba()`.
3. **Show `ml/ranking.py`**: Point to `rank_candidates()` sorting candidates by predicted probability.

---

### 3. Speech to be Spoken (Word-for-Word):

> "Good morning, professors. I was responsible for the Machine Learning architecture, model training, and candidate ranking logic.
>
> Following our strict project requirements, we implemented exactly one classification algorithm: a single **Random Forest Classifier**. We did not mix in multiple classifiers or artificial cosine similarity ranking.
>
> *(Point to `ml/train_model.py` -> `split_dataset`)*
>
> To ensure scientific rigor and prevent data snooping, we implemented an exact **70% Training, 15% Validation, and 15% Test stratified split** with a fixed random seed of 42:
> - **Training Set (70%):** 2,100 records
> - **Validation Set (15%):** 450 records
> - **Untouched Test Set (15%):** 450 records
>
> Stratification ensured that both Hire and Reject class proportions were maintained identically across all three partitions.
>
> *(Point to `ml/train_model.py` -> `build_pipeline`)*
>
> We built a clean, leak-free Scikit-learn `ColumnTransformer` preprocessing pipeline:
> 1. Numerical features (`Experience`, `CGPA`, etc.) are processed using `SimpleImputer` with the median strategy.
> 2. Categorical features (`Job Role`, `Job Type`, `Education Level`, `Previous Job Title`) are imputed and transformed using `OneHotEncoder(handle_unknown='ignore')`.
> 3. The `Skills` text is vectorized directly using `TfidfVectorizer(max_features=150)` with token boundary patterns that preserve technical characters like C++ and CI/CD.
>
> *(Point to `ml/train_model.py` -> `RandomForestClassifier`)*
>
> We tuned the Random Forest using 200 estimators (`n_estimators=200`) and a feature sampling ratio of 30% (`max_features=0.3`). We trained on the training partition, tuned against the validation partition, retrained on the combined 2,550 train-and-validation records, and evaluated the final pipeline **once on the untouched 450-record test set**.
>
> Our final test results achieved:
> - **Test Accuracy:** **74.22%**
> - **Hire Recall:** **87%** (The model successfully identified 258 out of 295 genuine hires)
> - **Hire F1-Score:** **0.82**
>
> In our viva, examiners often ask why accuracy is 74% and not 95%. The answer is that real-world hiring has inherent feature overlap. Candidates with identical experience and CGPA can have different hiring outcomes. 74.22% represents the true, non-leaked predictive capability of the data. Achieving 95% without leaky columns would simply mean overfitting to noise.
>
> *(Point to `ml/prediction.py` and `ml/ranking.py`)*
>
> During inference, our prediction module dynamically locates the index of the `'Hire'` class in `model.classes_` and extracts the probability using `predict_proba()`. In `ml/ranking.py`, candidates are sorted strictly by descending Hire probability, assigning Rank 1 to the candidate with the highest statistical likelihood of being hired.
>
> Member 3 will now explain our backend text parsing, NLP extraction, and SQLite database."

---

# MEMBER 3: Backend Processing, NLP & Database Architecture

### 1. Folders & Files to Take Care Of:
- **Folder:** `backend/`
- **Folder:** `database/`
- **PDF Parser File:** `backend/resume_parser.py`
- **NLP Preprocessor:** `backend/text_preprocessor.py`
- **Skill Extractor:** `backend/skill_extractor.py`
- **Candidate Feature Extractor:** `backend/candidate_features.py`
- **Duplicate Detector:** `backend/candidate_manager.py`
- **Database File:** `backend/database.py` and `database/candidates.db`
- **Test Files:** `tests/test_parser.py` and `tests/test_features.py`

### 2. Files to Open & Show When Explaining:
1. **Show `backend/resume_parser.py`**: Point to `extract_pdf_text()` showing PyMuPDF (`fitz`) reading text and catching empty/scanned PDFs.
2. **Show `backend/skill_extractor.py`**: Point to `SKILL_DICTIONARY` and `extract_skills()` showing regex boundary matching (`(?<![a-zA-Z0-9])...`).
3. **Show `backend/candidate_features.py`**: Point to `calculate_requirement_checks()` showing transparent rule-based checks.
4. **Show `backend/database.py`**: Point to SQLite `CREATE TABLE IF NOT EXISTS jobs` and `candidates`.

---

### 3. Speech to be Spoken (Word-for-Word):

> "Good morning, professors. I was responsible for backend processing, NLP information extraction, and database persistence.
>
> *(Point to `backend/resume_parser.py`)*
>
> Our resume extraction is powered by **PyMuPDF (`fitz`)**. When an HR recruiter uploads multiple PDF files, our parser inspects the raw file bytes in memory. It verifies that the file is not empty or corrupted, iterates through every page, and extracts selectable digital text. If a user uploads a scanned image PDF that contains zero selectable text, our system immediately warns them that OCR is deliberately excluded and requests a digital PDF.
>
> *(Point to `backend/text_preprocessor.py`)*
>
> Once raw text is extracted, our NLP module cleans and normalizes it. It converts text to lowercase and removes web URLs, email addresses, and noisy punctuation. However, our regex cleaning specifically preserves symbols like `+`, `#`, `-`, and `/` so that vital technical keywords such as `C++`, `C#`, and `CI/CD` are not destroyed.
>
> *(Point to `backend/skill_extractor.py`)*
>
> For skill identification, we built a canonical dictionary covering all 60 technical and professional skills in the dataset plus industry synonyms. To prevent false positives, we implemented regex non-alphanumeric boundary matching:
> ```regex
> (?<![a-zA-Z0-9])skill(?![a-zA-Z0-9])
> ```
> This boundary check ensures that single-letter or short skills like `'C'` or `'R'` are never falsely detected inside words like `'Customer'`, `'Company'`, or `'Research'`. The extractor then compares candidate skills against recruiter requirements, computing **Matched Skills**, **Missing Skills**, and **Skill Match Percentage**.
>
> *(Point to `backend/candidate_features.py`)*
>
> In `candidate_features.py`, we extract years of professional experience, education level (`Bachelor's`, `Master's`, `PhD`), CGPA, and project counts. We then map these attributes directly into the 11-feature dictionary expected by Member 2's Random Forest.
>
> Importantly, we separate ML prediction from **Rule-Based Requirement Checks**. The Random Forest was not trained on recruiter job descriptions, so we do not pretend the model learned custom requirements. Instead, our backend performs transparent rule checks: verifying whether candidate experience $\ge$ minimum experience, and verifying education degree hierarchy.
>
> *(Point to `backend/candidate_manager.py` and `backend/database.py`)*
>
> Finally, we built SHA-256 cryptographic hashing in `candidate_manager.py` to identify duplicate resumes in batch uploads. All data is persisted in a relational **SQLite database** (`candidates.db`), containing two tables: `jobs` (storing HR requirement criteria) and `candidates` (storing candidate metadata, predicted probabilities, ranks, and recruitment statuses).
>
> Member 4 will now demonstrate our frontend GUI, dashboard visualizations, and user workflows."

---

# MEMBER 4: Frontend GUI Architecture, User Experience & Reporting

### 1. Folders & Files to Take Care Of:
- **Root Entry Point:** `app.py`
- **Folder:** `frontend/`
- **Dashboard File:** `frontend/dashboard.py`
- **Job Form File:** `frontend/job_form.py`
- **Resume Upload File:** `frontend/resume_upload.py`
- **Results File:** `frontend/results.py`
- **Comparison File:** `frontend/comparison.py`
- **Shortlisting File:** `frontend/shortlisting.py`
- **Theme Configuration:** `.streamlit/config.toml`

### 2. Files to Open & Show When Explaining:
1. **Show the Live Web App in Browser (`http://localhost:8501`)**:
   - Show the **Top Segmented Navigation Bar** and the green pulsating **"Random Forest Ready"** live badge.
2. **Show Page 1 (`Dashboard`)**: Show the KPI metric cards, the Plotly candidate ranking distribution chart, and the **Top 10 Feature Importances** chart.
3. **Show Page 2 (`Requirements`) & Page 3 (`Upload`)**: Show the input form and demonstrate uploading sample PDFs.
4. **Show Page 4 (`Results`) & Page 5 (`Compare`)**: Show ranked candidate cards, missing skills, and the side-by-side comparison table.
5. **Show Page 6 (`Shortlist`)**: Show status modification (`Pending`, `Shortlisted`), click **Save to SQLite**, and click **Export to Excel (.xlsx)** to download the spreadsheet.

---

### 3. Speech to be Spoken (Word-for-Word):

> "Good morning, professors. I designed and developed the frontend user interface, data visualizations, and reporting features using **Streamlit** and custom CSS.
>
> *(Show browser window -> Top Navigation Bar)*
>
> Rather than using a generic or cluttered sidebar, we built an innovative **Top Segmented Pill Navigation Bar** with a unified **Electric Cobalt Blue (`#2563EB`)** editorial theme. On the left is our system branding, in the center are our horizontal pill tab switchers, and on the right is an animated live pulse dot confirming that the Random Forest pipeline is active and ready.
>
> Let me walk you through our 6 core pages:
>
> *(Click on 📊 Dashboard)*
>
> **Page 1: System Dashboard & Analytics**
> Here, recruiters see high-level KPI cards tracking resumes uploaded, analyzed, shortlisted, and average Hire probabilities. We integrated interactive **Plotly charts** displaying:
> 1. The Candidate Ranking Distribution in descending order.
> 2. The **Top 10 Feature Importances** extracted from the Random Forest. Notice that `Experience (Years)` is #1 at ~15% importance, followed by `Years Since Graduation` and `CGPA`. This mathematically explains why experience had the highest Gini impurity decrease during tree splitting.
>
> *(Click on ⚙️ Requirements)*
>
> **Page 2: HR Job Requirements Form**
> This allows the recruiter to specify the Job Title, required technical skills, minimum experience, and education requirements. Dropdowns for `Job Role` and `Job Type` are populated strictly from verified dataset categories to ensure seamless model alignment.
>
> *(Click on 📂 Upload)*
>
> **Page 3: Resume Upload & Ingestion**
> Here, recruiters can drag-and-drop multiple digital PDF resumes. The system validates file sizes and formats. When we click the **'Analyze Resumes'** button, it triggers Member 3's PyMuPDF parser and Member 2's Random Forest inference in real-time.
>
> *(Click on 🏆 Results)*
>
> **Page 4: Candidate Screening & Ranking Leaderboard**
> Candidates are displayed in expandable cards sorted strictly by their predicted Hire probability. Each card displays:
> - Predicted decision and probability badge.
> - Candidate experience, education, CGPA, and project count.
> - Transparent rule checks showing whether the candidate meets minimum experience.
> - **Matched Skills** and **Missing Skills** highlighted in clear alert badges.
>
> *(Click on ⚖️ Compare)*
>
> **Page 5: Candidate Side-by-Side Comparison**
> Recruiters can select 2 or 3 candidates from a dropdown to compare them side-by-side across all attributes in an intuitive comparison matrix.
>
> *(Click on 🎯 Shortlist)*
>
> **Page 6: Decision Management & Excel Export**
> Recruiters can change candidate statuses from `Pending` to `Shortlisted` or `Not Shortlisted`. With one click, they can save all records to the SQLite database, or click **'Export to Excel (.xlsx)'**, which uses **OpenPyXL** to generate a complete, formatted spreadsheet report.
>
> This concludes our presentation. We are now open for your questions."

---

# QUICK CHEAT SHEET FOR THE PRESENTATION

| Member | Topic | Key Files to Keep Open | One Sentence Summary |
| :--- | :--- | :--- | :--- |
| **Member 1** | Problem, Solution, Dataset, Features | `data/Rupa_dataset.csv`<br>`utils/config.py` | "I explain why manual screening fails, audit the 3,000 dataset records, and prove why we removed leaky score columns." |
| **Member 2** | ML Training, Random Forest, Metrics | `ml/train_model.py`<br>`ml/prediction.py`<br>`ml/ranking.py` | "I explain the 70/15/15 stratified split, ColumnTransformer, 74.22% accuracy, and probability ranking." |
| **Member 3** | PyMuPDF, NLP, Rules, SQLite | `backend/resume_parser.py`<br>`backend/skill_extractor.py`<br>`backend/database.py` | "I explain digital PDF parsing, boundary-safe skill regex, requirement checks, and SQLite storage." |
| **Member 4** | GUI, Dashboard, Compare, Excel | `app.py`<br>Live Web App (`http://localhost:8501`) | "I demonstrate the top segmented navigation, Plotly charts, candidate comparison matrix, and Excel export." |
