from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_azure import ask_question

app = Flask(__name__)

# Apply CORS with full control
CORS(app, resources={r"/ask": {"origins": "*"}}, supports_credentials=True)

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        # CORS preflight response
        response = app.make_default_options_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    question = data.get("question", "")
    answer = ask_question(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5001)