# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import bedrock_flow

class Prompt(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/api/bedrock")
def run_prompt(payload: Prompt):
    with open("prompts.txt", "w") as f:
        f.write(payload.prompt)
    result = bedrock_flow()
    return {"result": result[payload.prompt]}
