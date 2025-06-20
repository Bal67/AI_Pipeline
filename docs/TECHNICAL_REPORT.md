# Technical Report: AI Pipeline with AWS Bedrock & Prefect

## 1. Project Overview

This project implements an AI-powered pipeline that takes user-submitted prompts, sends them to Amazon Bedrock’s Claude 3 model, and returns the generated responses. It uses Prefect to orchestrate tasks and Streamlit for an interactive UI. The pipeline includes retry mechanisms, monitoring via the Prefect UI, and supports logging for debugging and observability.

---

## 2. Problem Statement

AI model inference workflows often lack:
- Scalable orchestration
- Integrated observability and monitoring
- Error resilience and retries
- An accessible user interface

This project solves those issues by integrating Prefect (orchestration), AWS Bedrock (inference), and Streamlit (UI).

---

## 3. System Architecture

### Components:
- **Streamlit**: For prompt submission and response display.
- **Prefect**: Manages flow orchestration, task retries, and logging.
- **AWS Bedrock**: Hosts Claude 3 model for prompt completion.
- **Tests**: Use `pytest` and `coverage` for test assurance.

### Flow:
1. User enters a prompt via the Streamlit UI.
2. Prompt is written to a text file.
3. Prefect flow reads the prompt and sends it to Claude 3 via the Bedrock API.
4. Response is displayed to the user.
5. Run logs and metadata are recorded and accessible.

---

## 4. Technical Stack

| Layer        | Technology                 |
|--------------|----------------------------|
| Frontend     | Streamlit                  |
| Workflow     | Prefect (with retry logic) |
| AI Inference | AWS Bedrock (Claude 3)     |
| Testing      | Pytest + Coverage          |
| Logging      | Prefect Logs + Streamlit   |

---

## 5. Retry and Error Handling

- `load_prompt_file` and `call_bedrock` are decorated with:
  ```python
  @task(retries=2, retry_delay_seconds=10)
  ```
- Errors during Bedrock invocation will trigger retries automatically.
- Logs for each attempt are captured and viewable in the Prefect UI.

---

## 6. Monitoring and Logging

- Flow runs are visible in Prefect UI.
- The Streamlit app shows:
  - Last run logs
  - Recent run history
- Each flow run can be traced with a unique ID.

---

## 7. Testing and Coverage

- Tests located in `tests/` folder.
- Example tested: prompt file loading.
- Run coverage with:
  ```bash
  coverage run -m pytest
  coverage report -m > coverage.txt
  ```
- Results show < 90% coverage for core pipeline modules.


