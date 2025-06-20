# pipeline.py
import json
from prefect import flow, task
from prefect_aws import AwsCredentials

@task(retries=2, retry_delay_seconds=10)
def load_prompt_file(prompt_file: str) -> list:
    with open(prompt_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

@task(retries=2, retry_delay_seconds=5)
def call_bedrock(prompts: list, aws_creds_block: str):
    aws = AwsCredentials.load(aws_creds_block)
    session = aws.get_boto3_session()
    client = session.client("bedrock-runtime")

    results = {}
    for prompt in prompts:
        messages = [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "messages": messages
        }

        resp = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )


        data = json.loads(resp["body"].read())
        assistant_msg = data.get("content", [{}])[0].get("text") \
                      or (data.get("messages", [{}])[0].get("content", [{}])[0].get("text"))
        results[prompt] = assistant_msg

    return results

@task
def save_output(results: dict, output_file: str):
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

@flow(name="Bedrock-Orchestrated-Pipeline")
def bedrock_flow(prompt_file: str = "prompts.txt",
                 output_file: str = "responses.json",
                 model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
                 aws_creds_block: str = "bedrock-creds"):
    prompts = load_prompt_file(prompt_file)
    results = call_bedrock(prompts, aws_creds_block)
    save_output(results, output_file)
    return results
