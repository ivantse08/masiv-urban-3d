import requests
import json
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are an AI that extracts filters from natural language queries.

    Input: "{query}"

    Output format:
    {{
    "attribute": "...",
    "operator": "...",
    "value": ...
    }}

    Only return the JSON. No explanations, no extra text.
    """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
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
