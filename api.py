from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import translate_v2 as translate

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://fruit-front-end.vercel.app"])


# Initialize Google Translate client
translate_client = translate.Client()

@app.route('/api/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language')
    
    if not text or not target_language:
        return jsonify({"error": "Text and target_language are required"}), 400
    
    # Perform translation
    try:
        result = translate_client.translate(text, target_language=target_language)
        return jsonify({"translated_text": result['translatedText']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
