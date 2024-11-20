from flask import Flask, render_template, request, jsonify
from src.translate import translate_with_subtitle

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    input_text = data.get("input_text", "")
    translated_text, processed_text = translate_with_subtitle(input_text)
    return jsonify({"processed_text": processed_text, "translated_text": translated_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run(host='0.0.0.0', port=443, ssl_context="adhoc")
