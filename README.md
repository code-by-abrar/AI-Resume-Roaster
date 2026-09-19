# 🔥 AI Resume Roaster — Brutal AI Feedback & Resume Improver

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq LLaMA 3](https://img.shields.io/badge/LLM-Groq%20LLaMA%203-F55036.svg?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C.svg?style=for-the-badge)](https://langchain.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

**Get hilariously brutal, brutally honest AI-powered resume roasting and high-impact improvement suggestions in seconds.**

[Key Features](#-key-features) • [Project Structure](#-project-structure) • [Quick Start](#-quick-start) • [License](#-license)

</div>

---

## 📌 Overview

Most resumes fail the **6-second recruiter glance** and get rejected by Applicant Tracking Systems (ATS). 

**AI Resume Roaster** parses resumes using PDF extractors, identifies cringey corporate buzzwords, mercilessly roasts formatting flaws, and provides structured, metric-driven recommendations alongside a live editor to rewrite weak bullets into winning achievements.

---

## ⚡ Key Features

- 🔥 **Brutal Roast Engine**: Hilarious, no-filter critique pointing out cliché buzzwords, vague summaries, and formatting fails.
- 🛠️ **Resume Improver (`improver.py`)**: Generates actionable, metric-oriented bullet rewrites using the STAR methodology.
- 📄 **Multi-Engine PDF Extraction**: Employs `pdfplumber` and `PyPDF2` for accurate, layout-preserving text parsing.
- ⚡ **Near-Instant Groq Inference**: Powered by `langchain-groq` for ultra-fast, high-throughput responses.
- 💻 **Interactive Web Frontend**: Includes an interactive resume upload dashboard (`index.html`) and live resume editor (`editor.html`).
- 🛡️ **Robust JSON Repair**: Utilizes `json_repair` to guarantee structured API responses without LLM parsing errors.

---

## 📂 Project Structure

```text
AI_Resume_Roaster/
├── backend/
│   ├── app.py               # FastAPI REST API endpoints & CORS setup
│   ├── improver.py          # Resume optimization & bullet rewrite logic
│   ├── prompts.py           # Structured system prompts & roast templates
│   ├── resume_parser.py     # PDF parsing via pdfplumber & PyPDF2
│   └── resume_roaster.py    # Groq-powered roast generator
├── frontend/
│   ├── index.html           # Main upload dashboard
│   └── editor.html          # Interactive resume editor
├── .env.example             # Environment template
├── .gitignore               # Excludes secrets, uploads, and venvs
├── requirements.txt         # Clean dependencies
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/code-by-abrar/AI_Resume_Roaster.git
cd AI_Resume_Roaster
```

### 2. Setup Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Inside `.env`, add your Groq API Key ([get a free key here](https://console.groq.com/keys)):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 5. Launch the Backend Server
```bash
uvicorn backend.app:app --reload --port 8000
```
*Or using the FastAPI CLI:*
```bash
fastapi dev backend/app.py
```

### 6. Open Frontend
Open `frontend/index.html` in your browser to start roasting resumes!

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.