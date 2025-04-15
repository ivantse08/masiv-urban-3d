import requests
import json
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are a helpful assistant that extracts filters from user queries.
    Here is the user query: "{query}"
    Choose the most relevant filter based off these options: height, area, length, stage of construction
    """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-xxl",
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
