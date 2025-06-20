# pipeline.py
import json
from prefect import flow, task
from prefect_aws import AwsCredentials

@task(retries=2, retry_delay_seconds=10)
def load_prompt_file(prompt_file: str) -> list:
    with open(prompt_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

@task(retries=2, retry_delay_seconds=5)
def call_bedrock(prompts: list, model_id: str, aws_creds_block: str):
    session = AwsCredentials.load(aws_creds_block).get_boto3_session()
    client = session.client("bedrock-runtime")
    
    results = {}
    for prompt in prompts:
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": 0.7,
                "topP": 0.9,
                "maxTokenCount": 512
            }
        })
        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        results[prompt] = json.loads(response["body"].read())["results"][0]["outputText"]
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
    results = call_bedrock(prompts, model_id, aws_creds_block)
    save_output(results, output_file)
    return results
