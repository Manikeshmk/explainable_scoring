# ExplainGrade — Complete System Documentation

> **AI-powered short answer grading that explains itself — in plain English.**

---

## Table of Contents

1. **System Overview**
2. **Architecture Diagram**
3. **Local Running (Python Backend)**
4. **Website Running (Web Frontend)**
5. **Data Flow & Processing Pipeline**
6. **File Structure & Purposes**
7. **Troubleshooting & Common Issues**

---

## 1. System Overview

### What is ExplainGrade?

ExplainGrade is an **Automated Short Answer Grading (ASAG)** system designed to:

- ✅ **Score** student text responses (0-5 or custom max)
- ✅ **Explain** exactly why a student received that score
- ✅ **Provide actionable feedback** in plain English anyone can understand
- ✅ **Run without any server** (browser-based option) or **locally** (for better accuracy)

### Key Components

| Component              | Purpose                        | Technology                                |
| ---------------------- | ------------------------------ | ----------------------------------------- |
| **Backend (Local)**    | High-accuracy grading with NLP | Python 3.9+, sentence-transformers, spaCy |
| **Frontend (Website)** | Browser-based instant grading  | Plain JavaScript, no frameworks           |
| **Data Source**        | Training dataset               | Mohler Dataset (2,200+ student responses) |
| **Deployment**         | Live website                   | GitHub Pages (static hosting)             |

### Two Ways to Use

#### 🌐 Browser Version (Zero Install)

- URL: [Live Demo](https://manikeshmk.github.io/Explainable_Summary_Score/)
- **Pros:** No installation, runs instantly, privacy (no server)
- **Cons:** Less accurate (TF-based approximation instead of real semantic models)
- **Best for:** Quick demos, single samples, learning the system

#### 🖥️ Local Python Version

- Command: `python local_grader.py --docx transcript.docx --xlsx summaries.xlsx`
- **Pros:** Higher accuracy (real sentence-transformers), batch processing, custom scoring
- **Cons:** Requires Python setup, slower first run (model download)
- **Best for:** Large classes, repeated use, production grading

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  BROWSER VERSION              PYTHON LOCAL VERSION           │
│  ━━━━━━━━━━━━━━━━━            ━━━━━━━━━━━━━━━━━━━━          │
│  • index.html                  • local_grader.py             │
│  • app.js                      • CLI interface               │
│  • scorer.js                   • Real ML models              │
│  • style.css                                                  │
│                                                               │
│  JSON inputs          XLSX/DOCX Read       │                 │
│  on demand            Batch Process        │                 │
│                                            ▼                 │
├─────────────────────────────────────────────────────────────┤
│              GRADING ENGINE (Two-Stage Pipeline)              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  STAGE 1: Rule-Based Floor                                   │
│  ────────────────────────────                                │
│  1. Extract technical terms from reference answer            │
│  2. Count how many appear in student answer                  │
│  3. Score = (matching keywords / total keywords) × maxScore  │
│                                                               │
│  STAGE 2: NLP Semantic Scoring                               │
│  ──────────────────────────────                              │
│  Metrics computed:                                            │
│  • Jaccard (S_j): Token-level overlap [0-1]                 │
│  • Edit Distance (S_e): Levenshtein similarity [0-1]        │
│  • TF Cosine (S_c): Word-frequency cosine [0-1]             │
│  • Word Count (S_w): Keyword density [0-1]                  │
│  • Semantic TF-IDF (S_tf): Meaning match [0-1]              │
│                                                               │
│  Formula: C_nlp = 0.15·S_j + 0.05·S_e + 0.15·S_c            │
│                   + 0.15·S_w                                  │
│           C = 0.5·S_tf + 0.5·C_nlp                           │
│           F = Special rule (see below)                        │
│           Stage2 = F × maxScore                               │
│                                                               │
│  Final Score = min(maxScore, Stage1 + Stage2)               │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                     OUTPUT LAYER                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Browser: Displays in web UI                                │
│  Local: Writes to grading_results.csv                       │
│                                                               │
│  Output includes:                                            │
│  • Final score                                               │
│  • Stage 1 & Stage 2 breakdown                               │
│  • All 5 metric values                                       │
│  • Plain English explanation                                │
│  • Student feedback                                          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Local Running (Python Backend)

### 3.1 Prerequisites

```bash
# Minimum requirements
- Python 3.9 or newer
- git (to clone repo)
- ~2 GB disk space (for models)
- ~4 GB RAM (for transformer inference)
```

### 3.2 Installation & Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/manikeshmk/Explainable_Summary_Score.git
cd Explainable_Summary_Score
```

#### Step 2: Create Virtual Environment

**Windows:**

```bash
python -m venv spacy-env
spacy-env\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv spacy-env
source spacy-env/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**

- `sentence-transformers` (2.7.0+) — Semantic similarity models
- `torch` (2.0.0+) — Deep learning framework
- `python-docx` — Read .docx files
- `openpyxl` (3.1.0+) — Read .xlsx files
- `pandas` (2.0.0+) — Data processing
- `spacy` (with en_core_web_sm) — NLP & POS tagging (optional, for better accuracy)

**First run note:** The system downloads `all-MiniLM-L6-v2` (~90 MB) on first use. This is cached locally.

### 3.3 Running the Grader

#### Basic Usage

```bash
python local_grader.py \
  --docx "path/to/transcript.docx" \
  --xlsx "path/to/summaries.xlsx"
```

#### With Custom Options

```bash
python local_grader.py \
  --docx "transcript.docx" \
  --xlsx "summaries.xlsx" \
  --max-score 10 \
  --output "my_results.csv"
```

#### Parameter Reference

| Parameter     | Required | Default               | Description                                             |
| ------------- | -------- | --------------------- | ------------------------------------------------------- |
| `--docx`      | ✅ Yes   | —                     | Path to teacher's transcript (Google Meet .docx export) |
| `--xlsx`      | ✅ Yes   | —                     | Path to student summaries spreadsheet                   |
| `--max-score` | ❌ No    | `5.0`                 | Maximum score per student                               |
| `--output`    | ❌ No    | `grading_results.csv` | Output filename                                         |

### 3.4 Input File Formats

#### .docx File (Teacher Transcript)

- Export from Google Meet as `.docx`
- Contains the reference answer / lecture transcript
- System automatically extracts text and technical terms

**Expected structure:**

```
[Paragraphs of lecture/reference content]
```

#### .xlsx File (Student Summaries)

**Required columns (flexible naming):**

| Actual Name    | Flexible Alternatives                          |
| -------------- | ---------------------------------------------- |
| `emailAddress` | `email`, `mail`                                |
| `name`         | `student_name`, `Student Name`                 |
| `summary`      | `answer`, `response`, `student_answer`, `text` |

**Example:**

```
emailAddress          | name            | summary
john.doe@school.edu  | John Doe        | The professor explained that...
jane.smith@school.edu| Jane Smith      | I learned about...
```

### 3.5 Output Format

**File created:** `grading_results.csv`

```csv
email,name,final,stage1,stage2,semantic,jaccard,note
john.doe@school.edu,John Doe,3.45,2.1,1.35,0.67,0.45,""
jane.smith@school.edu,Jane Smith,4.12,3.0,1.12,0.89,0.78,""
```

**Column explanations:**

| Column     | Type   | Range      | Meaning                           |
| ---------- | ------ | ---------- | --------------------------------- |
| `email`    | string | —          | Student email address             |
| `name`     | string | —          | Student name                      |
| `final`    | float  | 0–maxScore | **Final grade** (what to use)     |
| `stage1`   | float  | 0–maxScore | Rule-based floor score            |
| `stage2`   | float  | 0–maxScore | NLP semantic score                |
| `semantic` | float  | 0–1        | Semantic similarity metric (S_tf) |
| `jaccard`  | float  | 0–1        | Jaccard overlap (S_j)             |
| `note`     | string | —          | Error message or explanation      |

### 3.6 Processing Pipeline Line-by-Line

#### Script Entry Point: `local_grader.py`

```python
# 1. Parse command-line arguments
args = parse_args()
docx_path = args.docx
xlsx_path = args.xlsx
max_score = args.max_score

# 2. Read transcript & summaries
transcript = read_docx(docx_path)        # Extract raw text from .docx
summaries = read_xlsx(xlsx_path)          # Read student data from .xlsx

# 3. Extract reference answer (teacher's keywords)
reference_terms = extract_technical_terms(transcript)

# 4. For each student:
for student in summaries:
    student_answer = student['summary']

    # STAGE 1: Rule-based floor
    stage1_score = compute_rule_based_floor(
        reference_terms,
        student_answer,
        max_score
    )

    # STAGE 2: NLP metrics computation
    sj = jaccard_similarity(transcript, student_answer)
    se = edit_distance_similarity(transcript, student_answer)
    sc = tf_cosine_similarity(transcript, student_answer)
    sw = word_count_normalized(reference_terms, student_answer)
    stf = semantic_tfidf_similarity(transcript, student_answer)

    # Combine Stage 2 metrics
    c_nlp = 0.15*sj + 0.05*se + 0.15*sc + 0.15*sw
    c = 0.5*stf + 0.5*c_nlp

    # Apply special confidence rule
    if stf < 0.2:
        stage2_score = 0
    elif stf >= 0.9 and sw >= 0.85:
        stage2_score = max_score
    else:
        stage2_score = c * max_score

    # FINAL SCORE
    final_score = min(max_score, stage1_score + stage2_score)

    # 5. Write to CSV
    write_row_to_csv(student, final_score, stage1, stage2, ...)

# 6. Complete
print("✅ Grading complete. Results saved to grading_results.csv")
```

### 3.7 Key Functions Explained

#### `extract_technical_terms(text: str) -> list`

**Purpose:** Identify important keywords from reference answer

**Algorithm:**

1. If spaCy is installed: Use POS tagging (extract NOUN + PROPN only)
2. If not: Use fallback (words ≥4 chars, not in stopword/verb lists)

**Returns:** `['vector', 'matrix', 'algorithm', 'data', ...]`

#### `extract_keyphrases(text: str, n: int = 25) -> list`

**Purpose:** Find multi-word important phrases using TF

**Returns:** Top n phrases sorted by frequency

#### `read_docx(path: str) -> str`

**Purpose:** Extract all text from .docx file

**Returns:** Raw concatenated text of all paragraphs

#### `read_xlsx(path: str) -> list[dict]`

**Purpose:** Parse Excel spreadsheet

**Returns:** List of row dictionaries with flexible column matching

---

## 4. Website Running (Web Frontend)

### 4.1 Architecture

The website is hosted on **GitHub Pages** and runs **100% in the browser**. No server backend.

**URL:** [manikeshmk.github.io/Explainable_Summary_Score](https://manikeshmk.github.io/Explainable_Summary_Score/)

### 4.2 Key Files

#### HTML Structure: `docs/index.html`

```html
┌─ NAVBAR │ ├─ Logo │ ├─ Nav links: Pipeline | Live Demo | Batch Grade | Chat |
Research │ └─ Theme toggle ├─ HERO SECTION │ └─ Call-to-action buttons ├─
PIPELINE SECTION │ └─ Explanation of 2-stage process ├─ DEMO SECTION (id="demo")
│ ├─ Reference answer input │ ├─ Student answer input │ ├─ Max score selector │
├─ "Compute Score" button │ └─ Results display area ├─ BATCH GRADE SECTION
(id="batch") │ ├─ CSV file upload │ ├─ Download results button │ └─ Results
table ├─ SCRIPT EVAL SECTION (id="script-eval") │ ├─ DOCX upload (transcript) │
├─ XLSX upload (summaries) │ ├─ Max score input │ └─ Grade button ├─ CHAT
ASSISTANT SECTION (id="chat") │ ├─ Chat messages area │ ├─ Input field │ └─ Send
button ├─ HOW TO USE SECTION (id="how-to-use") │ └─ Setup & usage instructions
└─ FOOTER
```

#### Styling: `docs/style.css`

**Features:**

- Dark & Light theme support (`data-theme="dark|light"`)
- Responsive design (mobile-first)
- Smooth animations and transitions
- Custom color scheme (primary, success, warning, danger)
- Chat bubble styling
- Score visualization colors

**Theme Variables:**

```css
--primary: #6366f1 /* Main brand color (Indigo) */ --surface: #f3f4f6
  /* Light backgrounds */ --text: #1f2937
  /* Text color (switches for dark mode) */;
```

### 4.3 Main JavaScript Files

#### `app.js` — UI Controller

**Responsibilities:**

1. Theme management (dark/light toggle)
2. Navbar scroll behavior
3. Scroll-reveal animations
4. Toast notifications
5. Single answer scoring (demo)
6. Batch CSV grading
7. DOCX/XLSX batch grading (script eval)

**Key Functions:**

```javascript
// Theme toggle
function applyTheme(theme) { ... }

// Score computation wrapper
function computeScore() {
  const ref = document.getElementById('ref-answer').value;
  const stu = document.getElementById('stu-answer').value;
  const max = parseFloat(document.getElementById('max-score').value) || 5;

  const result = scoreStudent(ref, stu, max);
  displayResults(result);
}

// Batch CSV grading
async function processBatchCSV(file) {
  const rows = await parseCSV(file);
  const results = rows.map(row =>
    scoreStudent(row.desired_answer, row.student_answer, max_score)
  );
  downloadCSV(results);
}

// Batch DOCX/XLSX processing
async function processScriptEval() {
  const docx = await readDocxFile(docxFile);
  const xlsx = await readXlsxFile(xlsxFile);

  const ref_text = extractText(docx);
  const ref_terms = extractAnchors(ref_text);

  const results = xlsx.map(student =>
    scoreStudent(ref_text, student.summary, max_score)
  );
  downloadCSV(results);
}
```

#### `scorer.js` — Grading Engine

**The core logic for the Two-Stage Scoring Pipeline**

**Key Components:**

1. **Text Utilities**

```javascript
function tokenize(text)
// Lowercase, remove punctuation, split by whitespace
// Returns: ['the', 'professor', 'explained', 'vectors']

function tokenizeFiltered(text)
// Tokenize + remove stopwords
// Returns: ['professor', 'explained', 'vectors']
```

2. **Similarity Metrics**

```javascript
function jaccardSimilarity(text1, text2)
// Set-based token overlap
// Returns: 0.0 to 1.0

function editSimilarity(text1, text2)
// Levenshtein distance (character-level)
// Returns: 0.0 to 1.0

function tfCosineSim(text1, text2)
// TF-based cosine similarity (word frequency)
// Returns: 0.0 to 1.0
```

3. **Anchor Extraction (Technical Terms)**

```javascript
function extractTechnicalTerms(text)
// Extract 4+ char words, not in stopwords/verbs
// Used for Stage 1 floor

function extractAnchors(text, numAnchors = 5)
// Extract key phrases using TF frequencies
// Used in Stage 1 to identify reference keywords
```

4. **Two-Stage Score Computation**

```javascript
function scoreStudent(referenceAnswer, studentAnswer, maxScore) {
  // STAGE 1: Rule-based floor
  const stage1 = computeRuleBasedFloor(
    referenceAnswer,
    studentAnswer,
    maxScore,
  );

  // STAGE 2: NLP semantic scoring
  const sj = jaccardSimilarity(referenceAnswer, studentAnswer);
  const se = editSimilarity(referenceAnswer, studentAnswer);
  const sc = tfCosineSim(referenceAnswer, studentAnswer);
  const sw = normalizedWordCount(referenceAnswer, studentAnswer);
  const stf = tfCosineSim(referenceAnswer, studentAnswer); // proxy for semantic

  const cnlp = 0.15 * sj + 0.05 * se + 0.15 * sc + 0.15 * sw;
  const c = 0.5 * stf + 0.5 * cnlp;

  let stage2;
  if (stf < 0.2) {
    stage2 = 0;
  } else if (stf >= 0.9 && sw >= 0.85) {
    stage2 = maxScore;
  } else {
    stage2 = c * maxScore;
  }

  return {
    final: Math.min(maxScore, stage1 + stage2),
    stage1,
    stage2,
    metrics: { sj, se, sc, sw, stf },
  };
}
```

#### `chat.js` — Chat Assistant

**Purpose:** Answer queries about student grades and system explanations

**Two Classes:**

1. **ChatAssistant**
   - Loads `grading_results.csv`
   - Caches student data in memory
   - Methods: `findStudent()`, `getStatistics()`, `getSystemExplanation()`

2. **ChatUI**
   - Manages chat DOM elements
   - Handles input/output
   - Displays messages with formatting

**Query Pattern Matching:**

```javascript
// Example patterns
if (query includes "statistics" || "average" || "mean")
  → return getStatistics()

if (query includes "student" && "score")
  → return findStudent(name/email)

if (query includes "above" && number)
  → return findStudentsAboveScore(threshold)

if (query includes "how works" || "explain")
  → return getSystemExplanation()
```

### 4.4 Step-by-Step: Single Answer Grading

1. **User Input**

   ```
   Reference: "A vector is a mathematical object with magnitude and direction"
   Student: "Vectors have magnitude and direction"
   Max Score: 5
   ```

2. **JavaScript Event Handler (app.js)**

   ```javascript
   document.getElementById("score-btn").addEventListener("click", () => {
     const result = scoreStudent(ref, stu, 5);
     displayResults(result);
   });
   ```

3. **Scoring Process (scorer.js)**
   - Extract technical terms from reference
   - Compute all 5 metrics
   - Apply Stage 1 & Stage 2 formulas
   - Return result object

4. **Display Results (app.js)**
   ```javascript
   function displayResults(result) {
     document.getElementById("final-score").textContent =
       result.final.toFixed(2);
     document.getElementById("explanation").textContent = generateExplanation(
       result.metrics,
     );
     // Plot metrics on chart
   }
   ```

### 4.5 Step-by-Step: Batch CSV Grading

1. **User uploads CSV** with columns: `question`, `desired_answer`, `student_answer`

2. **File is read** (JavaScript FileReader API)

3. **Parse CSV**

   ```javascript
   function parseCSV(file) {
     const text = await file.text();
     const lines = text.split('\n');
     const header = lines[0].split(',');
     return lines.slice(1).map(line => {
       const values = line.split(',');
       return { question: values[0], ... };
     });
   }
   ```

4. **Score each row**

   ```javascript
   const results = rows.map((row) => ({
     ...row,
     final: scoreStudent(row.desired_answer, row.student_answer, 5).final,
   }));
   ```

5. **Generate CSV & Download**
   ```javascript
   function downloadCSV(results) {
     const csv = convertToCSV(results);
     const blob = new Blob([csv], { type: "text/csv" });
     const url = URL.createObjectURL(blob);
     const a = document.createElement("a");
     a.href = url;
     a.download = "results.csv";
     a.click();
   }
   ```

### 4.6 Step-by-Step: Batch DOCX/XLSX Grading (Script Eval)

1. **User uploads DOCX** (teacher transcript)

2. **DOCX is parsed** using `mammoth.js` library

   ```javascript
   const doc = await mammoth.convertToHtml({ arrayBuffer: docxBuffer });
   const transcript = extractPlainText(doc.value);
   ```

3. **User uploads XLSX** (student summaries)

4. **XLSX is parsed** using a CSV parsing library

   ```javascript
   const wb = await XLSX.read(xlsxFile);
   const ws = wb.Sheets[wb.SheetNames[0]];
   const data = XLSX.utils.sheet_to_json(ws);
   ```

5. **Extract reference keywords**

   ```javascript
   const referenceTerms = extractTechnicalTerms(transcript);
   ```

6. **Score each student**

   ```javascript
   const results = data.map(student => ({
     email: student.email,
     name: student.name,
     final: scoreStudent(transcript, student.summary, 5).final,
     ...
   }));
   ```

7. **Download results**

---

## 5. Data Flow & Processing Pipeline

### 5.1 Local Processing Flow

```
START
  │
  ├─ Read transcript.docx
  │  └─ Extract raw text
  │
  ├─ Read summaries.xlsx
  │  └─ Parse student records
  │
  ├─ Extract reference keywords from transcript
  │  ├─ Try spaCy POS tagging (NOUN/PROPN)
  │  └─ Fallback to keyword filter
  │
  ├─ FOR EACH STUDENT:
  │  │
  │  ├─ STAGE 1: Rule-Based Floor
  │  │  └─ Count matching keywords → floor_score
  │  │
  │  ├─ STAGE 2: NLP Metrics
  │  │  ├─ Jaccard: S_j = |A ∩ B| / |A ∪ B|
  │  │  ├─ Edit Distance: S_e = 1 - (levenshtein / max_length)
  │  │  ├─ TF Cosine: S_c = dot(tf1, tf2) / (||tf1|| * ||tf2||)
  │  │  ├─ Word Count: S_w = ref_keywords / stu_keywords
  │  │  └─ Semantic: S_tf = TF-IDF based cosine
  │  │
  │  ├─ Combine: C_nlp = 0.15·S_j + 0.05·S_e + 0.15·S_c + 0.15·S_w
  │  ├─ Blend: C = 0.5·S_tf + 0.5·C_nlp
  │  ├─ Apply rule: F = {0 if S_tf<0.2; 1 if S_tf≥0.9 and S_w≥0.85; else C}
  │  ├─ Stage 2: F × maxScore
  │  │
  │  └─ Final: min(maxScore, Stage1 + Stage2)
  │
  ├─ Write grading_results.csv
  │
  └─ END
```

### 5.2 Browser Processing Flow

```
USER INPUT
  │
  ├─ Reference answer (text)
  ├─ Student answer (text)
  └─ Max score (number)
       │
       ▼
  SCORER.JS
  ├─ Tokenize & extract anchors
  ├─ Compute 5 similarity metrics (pure JS)
  ├─ Apply Stage 1 & 2 formulas
  └─ Return: { final, stage1, stage2, metrics }
       │
       ▼
  APP.JS
  ├─ Format result for display
  ├─ Generate plain-english explanation
  ├─ Color code based on score
  └─ Render in DOM
       │
       ▼
  USER SEES RESULT
```

### 5.3 CSV Batch Flow

```
USER UPLOADS CSV
  (question | desired_answer | student_answer)
            │
            ▼
  PARSE CSV with JavaScript
            │
            ▼
  FOR EACH ROW:
    Call scoreStudent(desired_answer, student_answer, 5)
            │
            ▼
  RESULTS ARRAY:
    [{ question, desired_answer, student_answer, final, stage1, stage2, ... }]
            │
            ▼
  CONVERT TO CSV STRING
            │
            ▼
  DOWNLOAD as browser file
            │
            ▼
  USER GETS results.csv
```

---

## 6. File Structure & Purposes

```
cloud/
│
├─ 📄 README.md                          ← User guide (install, usage)
├─ 📄 IMPLEMENTATION_SUMMARY.md          ← Technical fixes & features
├─ 📄 CHAT_FEATURE.md                    ← Chat assistant documentation
│
├─ 🐍 PYTHON FILES (Local Grading)
│  ├─ local_grader.py                    ← MAIN: CLI entry point
│  ├─ anchor_extraction.py                ← Extract keyphrases using KeyBERT
│  ├─ semantic_mapping.py                 ← Compute semantic features
│  ├─ model_training.py                   ← Train ML model (historical)
│  └─ read_files.py                       ← Utility to read data files
│
├─ 📊 DATA FILES
│  ├─ mohler_dataset_edited.csv           ← Training dataset (2200+ rows)
│  ├─ grading_results.csv                 ← Output from local_grader.py
│  ├─ grading_results1.csv                ← Previous results
│  ├─ grading_results2.csv                ← Previous results
│  └─ Summary.xlsx                        ← Grading summary
│
├─ 🌐 WEBSITE (GitHub Pages: /docs/)
│  ├─ docs/
│  │  ├─ index.html                       ← Main HTML (all sections)
│  │  ├─ app.js                           ← UI controller & event handlers
│  │  ├─ scorer.js                        ← Two-stage scoring engine
│  │  ├─ chat.js                          ← Chat assistant logic
│  │  ├─ style.css                        ← All styling (dark/light)
│  │  ├─ package.json                     ← NPM dependencies (mammoth)
│  │  └─ grading_results.csv              ← CSV data loaded by chat
│  │
│  └─ docs/.gitignore                     ← Ignore node_modules, etc.
│
├─ 📦 PYTHON ENV
│  └─ spacy-env/                          ← Virtual environment
│     └─ Lib/site-packages/               ← Installed packages
│
├─ 📝 CONFIG FILES
│  ├─ requirements.txt                    ← Python dependencies
│  ├─ package.json                        ← Node.js dependencies
│  ├─ package-lock.json                   ← Lock file
│  └─ .gitignore                          ← Ignore patterns
│
└─ 🔧 BUILD/OUTPUT
   ├─ output.txt                          ← Captured stdout
   └─ __pycache__/                        ← Python cache
```

### File Purposes Quick Reference

| File                        | Type   | Purpose                                                      |
| --------------------------- | ------ | ------------------------------------------------------------ |
| `local_grader.py`           | Python | **CLI tool to grade student summaries against a transcript** |
| `anchor_extraction.py`      | Python | Extract keyphrases from text using KeyBERT                   |
| `semantic_mapping.py`       | Python | Compute similarity metrics (Jaccard, edit, semantic)         |
| `model_training.py`         | Python | (Historical) Train ML models using extracted features        |
| `index.html`                | Web    | Main HTML structure for website                              |
| `scorer.js`                 | Web    | **Core two-stage scoring algorithm in JavaScript**           |
| `app.js`                    | Web    | UI events, batch processing, results display                 |
| `chat.js`                   | Web    | Chat assistant that answers questions about grades           |
| `style.css`                 | Web    | Styling for dark/light themes, responsive design             |
| `requirements.txt`          | Config | Python package list (`pip install -r requirements.txt`)      |
| `mohler_dataset_edited.csv` | Data   | Training data (2200+ student responses with scores)          |

---

## 7. Troubleshooting & Common Issues

### 7.1 Local Running Issues

#### ❌ "ModuleNotFoundError: No module named 'python_docx'"

**Solution:**

```bash
pip install python-docx
pip install -r requirements.txt
```

#### ❌ "No spaCy model found"

**Context:** System tries to use spaCy for better accuracy, falls back gracefully if not installed.

**To enable spaCy:**

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**If not needed:** System automatically falls back to keyword filtering.

#### ❌ "XLSX file has wrong column names"

**Solution:** Check your .xlsx file has columns matching:

- `emailAddress` or `email` or `mail`
- `name` or `student_name`
- `summary` or `answer` or `response`

**Example:**

```python
df = pd.read_excel('summaries.xlsx')
print(df.columns)  # Print actual column names
```

Then rename as needed or adjust in spreadsheet.

#### ❌ "slow on first run" / "downloading model"

**This is normal:** The system downloads `all-MiniLM-L6-v2` (~90 MB) on first execution.

**To check:**

```bash
# See what's downloading
python local_grader.py --docx test.docx --xlsx test.xlsx

# Should see:
# Downloading: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/...
# [100%] Downloaded
```

This is cached after first run, so subsequent runs are instant.

### 7.2 Website Issues

#### ❌ Score shows 0 for correct answer

**Possible causes:**

1. Reference answer is very short (< 5 words) → Try longer reference
2. Student answer shares NO words with reference → Naturally gets low score
3. Browser JavaScript error → Check console (F12)

**Debugging:**

```javascript
// Open browser console (F12) and test:
scoreStudent("Python is a programming language", "Python programming", 5);
// Should return score > 0
```

#### ❌ Batch CSV upload doesn't work

**Check:**

1. CSV has correct columns: `question`, `desired_answer`, `student_answer`
2. No special characters breaking parsing
3. File size < 10 MB (browser memory limit)

**Test:**

```csv
question,desired_answer,student_answer
What is a vector?,A vector has magnitude and direction,vectors have magnitude
```

#### ❌ Chat doesn't load student data

**Reason:** `grading_results.csv` must be in `/docs/` folder

**Fix:**

1. Run `python local_grader.py ...` in main folder
2. Copy resulting `grading_results.csv` to `docs/` folder
3. Reload website

#### ❌ Dark mode doesn't persist

**This is a browser local storage issue:**

```javascript
// Check if localStorage is available:
console.log(localStorage.getItem("ess-theme"));

// If empty, browser is blocking storage (private mode?):
// Try normal browsing mode or check browser privacy settings
```

### 7.3 Performance Optimization

#### Website is slow to score

**Cause:** JavaScript scoring metrics are heavy (tokenization, TF calculation)

**Solution:**

- For batch > 100 rows: Use Python local version instead
- Browser version: OK for< 10 answers

#### Local grader is slow

**Causes & Solutions:**

| Issue                    | Cause              | Solution                           |
| ------------------------ | ------------------ | ---------------------------------- |
| **First run slow**       | Downloading models | Normal, happens once               |
| **Subsequent runs slow** | Large transcript   | Can't avoid (need to process text) |
| **Memory spike**         | All-MiniLM model   | Requires 4+ GB RAM                 |
| **Variable completion**  | Dataset size       | More students = longer process     |

**Benchmark:**

- 10 students: ~2 seconds
- 100 students: ~15 seconds
- 1000 students: ~2 minutes

---

## 8. Architecture Summary

### Two-Stage Scoring Deep Dive

#### Stage 1: Rule-Based Floor

**What:** Ensures minimum credit for actually matching key content

**Algorithm:**

1. Extract technical terms from reference answer (NOUN/PROPN POS tags)
2. Count how many appear in student answer
3. Score = (matches / total) × maxScore

**Example:**

```
Reference: "A binary tree is a tree where each node has at most 2 children"
Technical terms: [tree, node, children, binary]

Student 1: "Tree with maximum 2 children per node"
Matches: tree, children, node = 3/4 = 75%
Stage1 = 0.75 × 5 = 3.75

Student 2: "It's like a tree"
Matches: tree = 1/4 = 25%
Stage1 = 0.25 × 5 = 1.25
```

#### Stage 2: NLP Semantic

**What:** Measures semantic similarity using multiple metrics weighted by research

**Metrics** (from paper PMC12171532 & ExASAG BEA2023):

```
S_j (Jaccard):      Vocabulary overlap
                    |tokens_ref ∩ tokens_stu| / |tokens_ref ∪ tokens_stu|
                    Weight: 0.15

S_e (Edit Dist):    Character-level similarity
                    1 - (levenshtein / max_length)
                    Weight: 0.05

S_c (TF Cosine):    Word-frequency based vector similarity
                    Uses term frequencies of all tokens
                    Weight: 0.15

S_w (Word Count):   How many key keywords student used
                    ref_keywords_in_student / total_ref_keywords
                    Weight: 0.15

S_tf (Semantic TF-IDF): Semantic meaning via TF-IDF filtered tokens
                        Weights terms by importance, then cosine
                        Weight: 0.50
```

**Calculation:**

```
C_nlp = 0.15·S_j + 0.05·S_e + 0.15·S_c + 0.15·S_w

Confidence blended with semantic:
C = 0.5·S_tf + 0.5·C_nlp

Special rule (handles edge cases):
F = { 0 if S_tf < 0.2                         (too different)
    { 1 if S_tf ≥ 0.9 AND S_w ≥ 0.85       (nearly perfect)
    { C otherwise                             (normal case)

Stage2 = F × maxScore
```

**Final Score:**

```
Final = min(maxScore, Stage1 + Stage2)

Capped at maxScore to prevent over-scoring
```

### Why Two Stages?

| Stage            | Strength                                           | Weakness                   |
| ---------------- | -------------------------------------------------- | -------------------------- |
| **Rule-Based**   | Can't give unfair credit; validates actual content | Doesn't capture paraphrase |
| **NLP Semantic** | Captures meaning even if phrased differently       | Can be too lenient         |
| **Combined**     | Ensures both content AND quality of answer         | Balanced scoring           |

---

## Quick Reference Commands

### Local Grading

```bash
# Activate environment (do this every session)
spacy-env\Scripts\activate

# Basic grading
python local_grader.py --docx transcript.docx --xlsx summaries.xlsx

# Custom max score
python local_grader.py --docx transcript.docx --xlsx summaries.xlsx --max-score 10

# Custom output filename
python local_grader.py --docx transcript.docx --xlsx summaries.xlsx --output results.csv

# Check if spaCy is installed
python -m spacy info
```

### Website

```bash
# Start local web server to test website
python -m http.server 8000

# Open browser to http://localhost:8000/docs

# Check if using latest code
# Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### Git Operations

```bash
# Push changes to GitHub
git add .
git commit -m "Fixed scoring logic"
git push

# Website auto-updates from /docs folder on push
# (GitHub Pages deploys automatically)
```

---

## Summary

**ExplainGrade** is a two-part system:

1. **Local Python CLI** (`local_grader.py`)
   - High-accuracy grading using real ML models
   - Batch processing of student summaries
   - Outputs CSV with detailed scoring breakdown

2. **Browser Website** (GitHub Pages)
   - Single-answer grading in real-time
   - Batch CSV upload & grading
   - DOCX/XLSX batch processing (Script Eval)
   - Chat assistant for exploring results
   - 100% client-side, no servers

Both use the same **two-stage scoring pipeline** (Rule-based floor + NLP semantic), ensuring fair, explainable grades every time.

---

**Last Updated:** March 28, 2026  
**Version:** 2.0 (Chat & Scoring Logic Fixes)  
**Live Website:** [https://manikeshmk.github.io/Explainable_Summary_Score/](https://manikeshmk.github.io/Explainable_Summary_Score/)  
**GitHub:** [https://github.com/manikeshmk/Explainable_Summary_Score](https://github.com/manikeshmk/Explainable_Summary_Score)
