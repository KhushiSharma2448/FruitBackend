from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import translate_v2 as translate

app = Flask(__name__)


CORS(app, resources={r"/api/*": {
    "origins": "https://fruit-front-end.vercel.app",  # Your frontend URL
    "methods": ["GET", "POST", "PUT", "DELETE","OPTIONS"],  # Allow these methods
    "headers": ["Content-Type", "Authorization"],  # Allow these headers
}})


# Initialize Google Translate client
translate_client = translate.Client()
@app.route('/api/translate', methods=['POST', 'OPTIONS'])
def translate_text():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({"message": "CORS preflight successful"})
        response.status_code = 200
        response.headers.add('Access-Control-Allow-Origin', 'https://fruit-front-end.vercel.app')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response
    
    # Handle POST request for translation
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language')
    
    if not text or not target_language:
        return jsonify({"error": "Text and target_language are required"}), 400
    
    # Perform translation using Google Translate API
    try:
        result = translate_client.translate(text, target_language=target_language)
        return jsonify({"translated_text": result['translatedText']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
