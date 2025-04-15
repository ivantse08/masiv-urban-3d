from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import process_query
from data_loader import get_buildings, filter_buildings

app = Flask(__name__)
CORS(app)

@app.route("/api/buildings", methods=["GET"])
def get_buildings_endpoint():
    buildings = get_buildings()
    return jsonify(buildings)

@app.route("/api/query", methods=["POST"])
def query():
    query_text = request.json.get("query")
    filter_instruction = process_query(query_text)
    filtered = filter_buildings(get_buildings(), filter_instruction)
    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)
