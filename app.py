# app.py
import streamlit as st
import requests

st.title("Bedrock AI Prompt Runner")

prompt = st.text_area("Enter your prompt:", height=200)
if st.button("Submit to Bedrock"):
    if prompt:
        with st.spinner("Sending prompt..."):
            res = requests.post("http://localhost:8000/api/bedrock", json={"prompt": prompt})
            if res.status_code == 200:
                st.success("Bedrock response:")
                st.write(res.json()["result"])
            else:
                st.error("Failed to get response.")
