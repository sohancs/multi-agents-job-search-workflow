# 🤖 Multi-Agent Job Search Workflow

An intelligent, fully automated job search pipeline powered by **LangGraph** and **OpenAI**. This system scrapes job listings from LinkedIn, filters and re-ranks them against your resume using AI, and automatically drafts personalized application emails via Gmail — all with zero manual effort.

---

## ✨ Features

- 🔍 **LinkedIn Job Scraper** — Fetches job listings based on configurable search queries and location using the Apify LinkedIn scraper
- 🧹 **Duplicate Filter** — Removes duplicate job postings before processing
- 🧠 **AI Resume Selector** — Automatically picks the best-matching resume (AI-focused or Backend-focused) for each job using an LLM
- 📊 **AI Job Re-Ranker** — Scores each job against your resume (1–10 relevance), highlights matching & missing skills, and filters out low-relevance jobs (score < 6)
- ✉️ **AI Email Writer** — Drafts personalized, human-sounding cold emails tailored to each job's description and your resume
- 📬 **Gmail Integration** — Automatically saves drafted emails to your Gmail Drafts folder via the Gmail API
- 🗄️ **SQLite Persistence** — Stores all matched jobs, scores, email statuses, and metadata in a local SQLite database

---

## 🏗️ Architecture

The workflow is built as a **directed graph** using [LangGraph](https://github.com/langchain-ai/langgraph):

```
START
  │
  ▼
scrap_jobs          ← Scrapes LinkedIn via Apify
  │
  ▼
filter_jobs         ← Deduplicates job listings
  │
  ▼
resume_selector     ← LLM picks the best resume per job
  │
  ▼
rerank_jobs         ← LLM scores relevance, filters score < 6
  │
  ├──────────────────────────────────┐
  ▼                                  ▼
db_writter_fn       ← Saves to DB   write_email_agent_fn  ← Writes email per job
  │                                  │
  ▼                                  ▼
 END                            draft_email_node_fn   ← Saves to Gmail Drafts
                                     │
                                     ▼
                               update_job_status      ← Updates DB status
                                     │
                                     ▼
                                    END
```

---

## 📁 Project Structure

```
MultiAgentJobSearchWorkflow/
│
├── main.py                      # Entry point — initializes DB and runs the workflow
├── job_workflow.py              # Builds the LangGraph state graph
├── state.py                     # AgentState TypedDict (shared state across all nodes)
├── configs.py                   # Config loader from app.env
├── app.env                      # Environment variables (API keys, candidate info, etc.)
├── requirements.txt             # Python dependencies
│
├── agents/                      # LLM-powered agents
│   ├── reranker_agent.py        # Scores and ranks jobs against resume
│   ├── resume_selector_agent.py # Selects the right resume per job
│   └── email_writter_agent.py   # Drafts personalized outreach emails
│
├── nodes/                       # Graph nodes (pure workflow steps)
│   ├── scrapper_node.py         # Triggers the LinkedIn scraper tool
│   ├── filter_node.py           # Deduplicates raw job listings
│   ├── load_resume_node.py      # Pre-loads resume PDFs from disk
│   ├── db_writter_node.py       # Writes/updates jobs in SQLite
│   └── draft_email_node.py      # Saves email drafts via Gmail API
│
├── tools/
│   └── scrapper_tools.py        # LangChain tool wrapping the Apify LinkedIn scraper
│
├── db/
│   └── init_db.py               # SQLite schema creation and path resolution
│
├── resumes/                     # Place your resume PDFs here
│   ├── <your-ai-resume>.pdf
│   └── <your-backend-resume>.pdf
│
└── secrets/                     # OAuth credentials (gitignored)
    ├── credentials.json         # Google OAuth client credentials
    └── token.json               # Auto-generated Gmail access token
```

---

## ⚙️ Configuration

All configuration is managed via **`app.env`**. Create this file in the project root:

```env
# --- API Keys ---
APIFY_API_TOKEN=your_apify_api_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini          # or gpt-4o, gpt-3.5-turbo, etc.

# --- Job Search Settings ---
JOB_SEARCH_QUERIES=Senior Backend Developer, AI Engineer
LOCATION=Dubai, United Arab Emirates
SEACH_JOB_COUNT=10
JOB_POSTED_FILTER_IN_SEC=r86400   # r86400 = last 24 hours

# --- Candidate Info (used in email drafts) ---
CANDIDATE_NAME=Your Full Name
CANDIDATE_EMAIL=you@gmail.com
CANDIDATE_LINKEDIN_URL=https://linkedin.com/in/yourprofile
CANDIDATE_GITHUB_URL=https://github.com/yourusername
CANDIDATE_MOB_NO=+1234567890
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/MultiAgentJobSearchWorkflow.git
cd MultiAgentJobSearchWorkflow
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy and fill in your values:

```bash
cp app.env.example app.env      # or create app.env manually
```

### 5. Add your resumes

Place your resume PDFs in the `resumes/` directory and update the file mappings in `nodes/load_resume_node.py`:

```python
files = {
    "AI":      "resumes/your-ai-resume.pdf",
    "Backend": "resumes/your-backend-resume.pdf"
}
```

### 6. Set up Gmail API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **Gmail API**
3. Create **OAuth 2.0 Client ID** credentials (Desktop App type)
4. Download the JSON and save it as `secrets/credentials.json`
5. On first run, a browser window will open for you to authorize Gmail access — a `token.json` will be auto-saved

### 7. Run the workflow

```bash
python main.py
```

---

## 🧩 Key Components

### Agents (LLM-powered)

| Agent | Description |
|---|---|
| `resume_selector_agent` | Classifies each job as `AI`, `Backend`, or `NONE` to pick the right resume |
| `reranker_agent` | Scores job–resume fit (1–10), extracts matching/missing skills, filters out jobs below score 6 |
| `email_writter_agent` | Generates a personalized cold email with subject line, concise body, and signature |

### Nodes (Workflow Steps)

| Node | Description |
|---|---|
| `scrapper_node` | Invokes the Apify LinkedIn scraper LangChain tool |
| `filter_node` | Deduplicates jobs by URL |
| `load_resume_node` | Pre-loads PDF resumes using `PyPDFLoader` |
| `db_writter_node` | Persists ranked jobs to SQLite; updates email status after drafting |
| `draft_email_node` | Authenticates with Gmail and saves emails to Drafts |

---

## 🗄️ Database Schema

Jobs are persisted in a local SQLite database at `db/jobs.db`:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Auto-incremented primary key |
| `date_scraped` | TEXT | Timestamp of when the job was scraped |
| `company_name` | TEXT | Company posting the job |
| `job_title` | TEXT | Job title |
| `source` | TEXT | Job source (e.g., LinkedIn) |
| `job_description` | TEXT | Full job description text |
| `job_link` | TEXT (UNIQUE) | Job posting URL (prevents duplicates) |
| `location` | TEXT | Job location |
| `recruiter_name` | TEXT | Recruiter's name (if available) |
| `recruiter_email` | TEXT | Recruiter's email (if available) |
| `resume_used` | TEXT | Which resume was selected (`AI` or `Backend`) |
| `match_score` | INTEGER | AI relevance score (1–10) |
| `status` | TEXT | `NEW`, `SUCCESS`, or `FAILURE` |
| `notes` | TEXT | LLM reasoning for the match score |
| `matching_skills` | TEXT | Comma-separated matching skills |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `langgraph` | Multi-agent workflow graph orchestration |
| `langchain`, `langchain-openai` | LLM chains, prompts, and OpenAI integration |
| `langchain-community` | PyPDFLoader for resume ingestion |
| `openai` | OpenAI API client |
| `apify-client` | LinkedIn job scraping via Apify |
| `pypdf` | PDF parsing |
| `pydantic` | Data validation for LLM output parsing |
| `python-dotenv` | `.env` file loading |
| `google-auth-oauthlib` | Gmail OAuth flow |
| `google-auth-httplib2` | Gmail HTTP transport |
| `google-api-python-client` | Gmail API client |

---

## 🔒 Security Notes

- **`secrets/`** is gitignored — never commit `credentials.json` or `token.json`
- **`app.env`** contains sensitive API keys — add it to `.gitignore` if sharing publicly
- The Gmail scope used is `gmail.compose` (draft-only) — the app cannot read or send emails on your behalf

---

## 🛣️ Roadmap

- [ ] Support for multiple job portals (Indeed, Glassdoor, Naukri)
- [ ] Scheduled cron runs (e.g., daily at 8 AM)
- [ ] Web dashboard to review and approve email drafts before saving
- [ ] Slack / WhatsApp notifications for high-scoring matches
- [ ] Support for more resume types / more fine-grained resume selection

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a PR or issue.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
