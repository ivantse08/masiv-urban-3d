import requests
import re
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are a helpful assistant that extracts filters about building properties from user queries.
    Here is the user query: "{query}"
    Choose the most relevant filter based on these options:
    - height
    - area
    - perimeter
    - stage
    - obscured
    - struct_id
    - building_type
    - building_code

    Respond ONLY using this format: attribute operator value
    Example: height > 30
    If a string value is needed (like stage or obscured), put it in quotes: stage = "Constructed"
    Only respond with one line. No explanations.
    """
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )
    try:
        generated = response.json()[0]['generated_text']
        print("Generated:", generated)

        # Match using regex
        match = re.match(r'(\w+)\s*(=|>|<)\s*("?[\w\s]+"?)', generated)
        if match:
            attr, op, val = match.groups()

            # Remove quotes if value is a string like stage = "Constructed"
            val = val.strip('"') if '"' in val else val

            return {
                "attribute": attr.strip(),
                "operator": op.strip(),
                "value": val.strip()
            }

    except Exception as e:
        print("LLM parsing error:", e)
        print("Raw output:", response.text)

    return {}  # fallback