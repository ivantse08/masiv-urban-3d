import requests
import re
import os

HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

def process_query(query):
    prompt = f"""
    You are a helpful assistant that extracts building filter conditions from natural language.

    Available attributes:
    - height
    - area
    - perimeter
    - stage
    - obscured
    - struct_id
    - building_type
    - building_code

    For the query below, respond with exactly one condition in the format:
    attribute operator value
    Query: "{query}"
    Examples:
    "Show buildings taller than 50m" → height > 50  
    "Only constructed buildings" → stage = "Constructed"  
    "Obscured buildings" → obscured = "Y"
    "Hide obscured buildings" → obscured = "N"
    "Find buildings with an area over 1000 square meters" -> area > 1000
    "List buildings with perimeter less than 300 meters" → perimeter < 300
    "Show building with struct ID 12345" → struct_id = 12345
    "Show only commercial buildings" → building_type = "Commercial"
    "Find buildings with code 4" → building_code = 4

    Always return exactly one condition in this format and nothing else.
    Query: "{query}"
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