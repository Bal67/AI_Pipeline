# Architecture Document: Bedrock Orchestrated AI Pipeline

## Overview
This system allows users to submit prompts via Streamlit, which are processed through a Prefect-orchestrated workflow using AWS Bedrock models.

## Components
- **Streamlit UI**: User interface to submit prompts
- **FastAPI Backend**: Accepts prompt submissions and triggers Prefect flow
- **Prefect Flow**:
  - Load prompt(s)
  - Call AWS Bedrock with retry and logging
  - Save results to JSON

## Monitoring
- Managed via Prefect UI
- Each task is observable with log and retry detail

## AWS Integration
- Uses `prefect_aws.AwsCredentials` block
- Calls Bedrock's runtime API

## Retry Mechanism
- Load & Bedrock call tasks have 2 retries with delay
- Failures and retries are logged and visible in Prefect UI
