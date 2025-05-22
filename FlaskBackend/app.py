from flask import Flask, jsonify, request
from igdb_api import get_games
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173","http://localhost:5174", "http://127.0.0.1:5174"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "support_credentials": True
    }
})

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    return """<h1>Welcome to the Game Engine!</h1>

            """
     

@app.route("/games", methods=["GET"])
def games():
    try:
        query = request.args.get("search", default="")
        logger.debug(f"Received search query: {query}")

        games = get_games(query)
        logger.debug(f"Got response from IGDB: {games}")

        if isinstance(games, dict) and 'error' in games:
            return jsonify({"error": games['error']}), 500
        
        return jsonify(games)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


