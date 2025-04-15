import requests
import json
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are a helpful assistant that extracts filters from user queries.
    Query: "{query}"
    Once you found the filter based off the query, Respond ONLY with a JSON object in this format with attribute being the filter:
    {{"attribute": "...", "operator": "...", "value": ...}}
    """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )
    print(response.text)
    result = response.json()
    try:
        # Safely parse JSON-like string
        generated = result[0]['generated_text']
        return json.loads(generated)
    except Exception as e:
        print("LLM parsing error:", e)
        print("Raw LLM output:", result)
        return {}
