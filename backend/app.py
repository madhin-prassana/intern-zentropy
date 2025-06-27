import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from chat_azure import ask_question, set_pdf_context
from amalgamation import (
    LlamaParser, MarkerParser, DoclingParser,
    MarkitdownParser, OCRParser, HybridParser
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output_data"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files or 'parser' not in request.form:
        return jsonify({"error": "Missing file or parser selection"}), 400

    file = request.files['file']
    parser_choice = request.form['parser']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    parser_map = {
        "1": (LlamaParser(), "amalgamation(llama).md"),
        "2": (MarkerParser(), "amalgamation(marker).md"),
        "3": (DoclingParser(), "amalgamation(docling).md"),
        "4": (MarkitdownParser(), "amalgamation(markitdown).md"),
        "5": (OCRParser(), "amalgamation(ocr).md"),
        "6": (HybridParser(), "amalgamation(hybrid).md"),
    }

    if parser_choice not in parser_map:
        return jsonify({"error": "Invalid parser choice"}), 400

    parser, output_file = parser_map[parser_choice]
    output_path = os.path.join(OUTPUT_FOLDER, output_file)

    try:
        parser.parse(file_path, output_path)
        set_pdf_context(output_path)
        return jsonify({"message": "PDF parsed and context set."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = ask_question(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5001)