from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "https://fruit-front-end.vercel.app/",  # Your frontend URL
    "methods": ["GET", "POST", "PUT", "DELETE"],  # Allow these methods
    "headers": ["Content-Type", "Authorization"],  # Allow these headers
}})


# In-memory storage for FAQs (for demonstration purposes)
faqs = [
    {"id": 1, "question": "What is Fruit.ai?", "answer": "Fruit.ai is an AI-powered platform for managing your health by providing personalized insights about fruits, their benefits, and more."},
    {"id": 2, "question": "How does the chatbot work?", "answer": "The chatbot is designed to answer your questions regarding fruits, their health benefits, and provide other useful information."},
    {"id": 3, "question": "How do I use the Translator?", "answer": "The translator allows you to translate names of fruits or other health-related terms into regional languages."},
    {"id": 4, "question": "Can I get detailed information on specific fruits?", "answer": "Yes, you can browse detailed information about specific fruits including their nutritional value, health benefits, and more."},
    {"id": 5, "question": "Is there a mobile app version available?", "answer": "Currently, Fruit.ai is accessible through the web, but we are working on launching a mobile app version soon."}
]

# Helper function to find an FAQ by ID
def find_faq_by_id(faq_id):
    return next((faq for faq in faqs if faq["id"] == faq_id), None)

# Create a new FAQ
@app.route('/api/faqs', methods=['POST'])
def create_faq():
    data = request.get_json()
    new_id = max(faq["id"] for faq in faqs) + 1 if faqs else 1
    new_faq = {"id": new_id, "question": data["question"], "answer": data["answer"]}
    faqs.append(new_faq)
    return jsonify(new_faq), 201

# Get all FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs)

# Get a specific FAQ
@app.route('/api/faqs/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    faq = find_faq_by_id(faq_id)
    if faq:
        return jsonify(faq)
    else:
        return jsonify({"error": "FAQ not found"}), 404

# Update an existing FAQ
@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    data = request.get_json()
    faq = find_faq_by_id(faq_id)
    if faq:
        faq["question"] = data.get("question", faq["question"])
        faq["answer"] = data.get("answer", faq["answer"])
        return jsonify(faq)
    else:
        return jsonify({"error": "FAQ not found"}), 404

# Delete an FAQ
@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    global faqs
    faqs = [faq for faq in faqs if faq["id"] != faq_id]
    return jsonify({"message": "FAQ deleted"}), 200

# Root route
@app.route('/')
def home():
    return "Welcome to the Fruit API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
