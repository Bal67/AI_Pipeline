# 🧠 AI Pipeline with AWS Bedrock & Prefect

This project implements a full-stack AI pipeline that uses **Prefect** for orchestration, **AWS Bedrock (Claude)** for text generation, and **Streamlit** as the UI. The pipeline allows users to submit prompts, trigger Claude 3 model inference, and monitor runs via logs and retry-aware workflows.

---

## 📦 Features

- ✅ Streamlit UI for prompt submission
- ✅ Prefect flow with retries and logging
- ✅ Integration with AWS Bedrock (Claude 3)
- ✅ Monitoring via Prefect UI and Streamlit
- ✅ Technical + architecture documentation
- ✅ Test coverage report

---

## 🛠️ Stack

| Layer        | Tech                     |
|--------------|--------------------------|
| UI           | Streamlit                |
| Orchestration| Prefect                  |
| AI Inference | AWS Bedrock (Claude 3)   |
| Logging      | Prefect UI, Streamlit    |
| Testing      | Pytest + Coverage        |

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/Bal67/AI_Pipeline.git
cd AI_Pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set AWS Credentials

Create a `.env` file (or set system env vars):

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
```

Also configure the Prefect `AwsCredentials` block if needed.

---

### 4. Run the App

```bash
streamlit run app.py
```

Submit a prompt, run the pipeline, and view the logs and results directly in the app.

---

## 🧪 Testing & Coverage

To run tests and generate a coverage report:

```bash
coverage run -m pytest
coverage report -m > coverage.txt
```

You can also view an HTML version:

```bash
coverage html
open htmlcov/index.html
```

---

## 📊 Monitoring

- All flow runs and task-level logs are visible in the **Prefect UI**
- Streamlit sidebar shows:
  - Recent flow runs
  - Logs from the last run
  - Claude model responses

---

## 📁 Project Structure

```
AI_Pipeline/
├── app.py                  # Streamlit frontend
├── pipeline.py             # Prefect flow and tasks
├── tests/                  # Unit tests
├── docs/                   # Architecture doc
├── .env.example
├── requirements.txt
├── README.md
├── TECHNICAL_REPORT.md
└── coverage.txt
```

---

## 📚 Docs

- [Architecture Doc](docs/architecture.md)
- [Technical Report](TECHNICAL_REPORT.md)

---

## 🔮 Future Improvements

- Integrate S3/DB for persistent storage
- Add FastAPI backend (optional)
- Stream real-time Claude output to UI
