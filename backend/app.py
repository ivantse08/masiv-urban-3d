from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import process_query
from data_loader import get_buildings, filter_buildings
import os

app = Flask(__name__)
CORS(app)

@app.route("/api/buildings", methods=["GET"])
def get_buildings_endpoint():
    buildings = get_buildings()
    return jsonify(buildings)

@app.route("/api/query", methods=["POST"])
def query():
    data = request.json
    query_text = data.get("query", "")
    
    filter_instruction = process_query(query_text)
    print("LLM Filter:", filter_instruction)

    # Example filtering logic (replace with your real data logic)
    buildings = get_buildings()  # Load buildings from wherever you're storing them
    filtered = filter_buildings(buildings, filter_instruction)

    return jsonify(filtered)

# Health check route
@app.route("/healthz")
def health_check():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
