import requests
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"Extract the filter from this query: '{query}'. Return a JSON object with 'attribute', 'operator', and 'value'."
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )
    result = response.json()
    try:
        return eval(result[0]['generated_text'])
    except Exception as e:
        print("LLM parsing error:", e)
        return {}
