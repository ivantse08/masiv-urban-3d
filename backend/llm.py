import requests
import json
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""Extract a filter from a natural language query.

        Input: "{query}"

        Return a JSON object like:
        {{"attribute": "height", "operator": ">", "value": 100}}

        Only return the JSON object. No explanations, no comments.
        """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1",
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
