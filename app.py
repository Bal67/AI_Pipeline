# app.py made with help from Claude 3.5
import streamlit as st
from pipeline import bedrock_flow
from prefect.client import get_client
from prefect.utilities.asyncutils import sync_compatible
from datetime import datetime, timedelta
from prefect.client import get_client
from prefect.server.schemas.filters import LogFilter, LogFilterFlowRunId, FlowRunFilter, FlowRunFilterStartTime
from prefect.utilities.asyncutils import sync_compatible

@sync_compatible
async def get_logs(flow_run_id: str):
    async with get_client() as client:
        log_filter = LogFilter(flow_run_id=LogFilterFlowRunId(any_=[flow_run_id]))
        return await client.read_logs(log_filter=log_filter)

@sync_compatible
async def get_recent_runs(limit: int = 5):
    async with get_client() as client:
        now = datetime.utcnow()
        start_filter = FlowRunFilterStartTime(after_=now - timedelta(days=1))
        flow_filter = FlowRunFilter(start_time=start_filter)
        runs = await client.read_flow_runs(
            flow_run_filter=flow_filter,
            limit=limit,
            sort="EXPECTED_START_TIME_DESC"

        )
        return runs

st.set_page_config(page_title="Claude 3.5 Pipeline", layout="wide")

# Sidebar
st.sidebar.title("Pipeline Monitor")
tab = st.sidebar.radio("Navigation", ["Prompt Runner", "Last Run Logs", "Run History"])

# State management
if 'last_run_id' not in st.session_state:
    st.session_state.last_run_id = None
if 'last_result' not in st.session_state:
    st.session_state.last_result = {}

# Tab 1: Prompt Runner
if tab == "Prompt Runner":
    st.title("Claude 3.5 Prompt Runner")
    st.markdown("Model: `anthropic.claude-3-sonnet-20240229-v1:0`")

    prompt = st.text_area("Enter your prompt:", height=200)
    if st.button("Run Prompt"):
        with open("prompts.txt", "w") as f:
            f.write(prompt)

        st.info("Running Bedrock flow...")
        try:
            state = bedrock_flow(
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                return_state=True
            )
            flow_run_id = state.state_details.flow_run_id
            result = state.result()

            st.session_state.last_run_id = flow_run_id
            st.session_state.last_result = result

            st.success("Claude 3.5 Response")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

# Tab 2: Logs
elif tab == "Last Run Logs":
    st.title("Logs from Most Recent Run")
    if st.session_state.last_run_id:
        logs = get_logs(st.session_state.last_run_id)
        with st.expander("View Logs"):
            for entry in logs:
                st.text(f"[{entry.timestamp}] {entry.message}")
    else:
        st.warning("No run has been executed yet.")

# Tab 3: Run History
elif tab == "Run History":
    st.title("Recent Flow Runs")
    runs = get_recent_runs()
    for run in runs:
        with st.container():
            st.markdown(f"""
            **Run ID**: `{str(run.id)[:8]}`  
            **Start Time**: {run.expected_start_time.strftime('%Y-%m-%d %H:%M:%S')}`  
            **Status**: `{run.state.name}`
            ---
            """)
