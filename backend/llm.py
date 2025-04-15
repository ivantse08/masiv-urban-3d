import requests
import json
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are a helpful assistant that extracts filters about building properties from user queries.
    Here is the user query: "{query}"
    Choose the most relevant filter based off these options: height, area, perimeter, stage of construction, obstructed, building id, building type and building code 
    and provide a value it should be greater than or less than or equal to.
    Example query: "Show all buildings above 30 feet", then your response should be "height > 30"
    Example query2: "Show all buildings that are constructed", then your response should "stage = Constructed"
    All your responses should be based of this format with "filter sign value"
    """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )
    print("ResponseText", response.text)
    result = response.json()
    try:
        # Safely parse JSON-like string
        generated = result[0]['generated_text']
        return json.loads(generated)
    except Exception as e:
        print("LLM parsing error:", e)
        print("Raw LLM output:", result)
        return {}
