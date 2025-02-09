from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Enable CORS

# Prize pool (same prizes for everyone)
PRIZES = [
    "1 Maestro premium account for 1 month",
    "2 Maestro premium accounts for 1 week",
    "3 Maestro premium accounts for 1 week",
    "4 Maestro premium accounts for 1 week",
    "5 Maestro premium accounts for 1 week",
    "6 Maestro premium accounts for 1 week",
    "7 Maestro premium accounts for 3 days",
    "8 Maestro premium accounts for 3 days",
    "9 Maestro premium accounts for 1 day",
    "10 Maestro premium accounts for 1 day"
]

# 🔐 Store token-prize mapping
claimed_tokens = {}

@app.route('/check_token', methods=['GET'])
def check_token():
    """Check if a token has been claimed and return the assigned prize."""
    token = request.args.get('token')
    
    if not token:
        return jsonify({"error": "Missing token"}), 400

    if token in claimed_tokens:
        return jsonify({"alreadyClaimed": True, "prize": claimed_tokens[token]})
    
    return jsonify({"alreadyClaimed": False})

@app.route('/claim_token', methods=['POST'])
def claim_token():
    """Assign a prize when a token is claimed."""
    token = request.json.get('token')  # ✅ Read from JSON request body

    if not token:
        return jsonify({"error": "Missing token"}), 400

    if token in claimed_tokens:
        return jsonify({"error": "Token already claimed", "prize": claimed_tokens[token]}), 403

    # ✅ Assign a random prize once and store it
    prize = random.choice(PRIZES)
    claimed_tokens[token] = prize

    return jsonify({"status": "success", "message": "Token claimed", "prize": prize})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
