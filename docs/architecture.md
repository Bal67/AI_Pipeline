# Architecture Document: Bedrock-Orchestrated AI Pipeline

## Overview
This system allows users to submit prompts via a Streamlit web UI. Submitted prompts are processed through a Prefect-orchestrated pipeline that invokes AWS Bedrock Claude models to generate responses. Results are stored and displayed in the UI, and the entire process is observable and retry-safe.

---

## Architecture Components

### 1. **Streamlit Frontend**
- Provides a simple interface for:
  - Submitting prompts
  - Viewing Claude responses
  - Displaying recent run history and logs
- Communicates directly with the Prefect flow (no FastAPI in current implementation)

### 2. **Prefect Orchestration**
- Main orchestration engine responsible for:
  - Loading the prompt from a text file
  - Invoking the Claude model via AWS Bedrock
  - Returning the result to the UI

#### Tasks in the Flow:
- `load_prompt_file()`: Loads the prompt content from `prompts.txt`
- `call_bedrock()`: Sends the prompt to Bedrock and returns the Claude response
- `bedrock_flow()`: Main flow to run the above tasks in sequence

### 3. **AWS Integration**
- Uses `prefect_aws.AwsCredentials` block for secure AWS access
- Calls `bedrock-runtime` client via `boto3` inside Prefect task
- Claude model used: `anthropic.claude-3-sonnet-20240229-v1:0`

---

## Monitoring and Observability

### 1. **Prefect UI**
- Flow and task runs are tracked automatically
- Logs and retry attempts are accessible in the Prefect dashboard
- Recent runs and logs are viewable directly in the Streamlit app

### 2. **Streamlit Integration**
- Displays real-time logs from last flow run
- Lists recent run history with status and timestamps

---

## Retry Mechanisms

- Both `load_prompt_file()` and `call_bedrock()` tasks:
  - Use Prefect’s built-in retry logic
  - Configured for `retries=2`, `retry_delay_seconds=5–10`
- Failures are gracefully retried and tracked in the UI

---

## Data Flow Diagram

```text
[User]
   │
   ▼
[Streamlit UI] ──> [prompts.txt]
   │                   │
   ▼                   ▼
[Prefect Flow] ──> [Claude via Bedrock]
   │
   ▼
[Streamlit Display / Logs]
