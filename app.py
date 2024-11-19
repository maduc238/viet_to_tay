from flask import Flask, render_template, request
from src.translate import translate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        processed_text = translate(input_text)
        return render_template("index.html", input_text=input_text, processed_text=processed_text)
    return render_template("index.html", input_text="", processed_text="")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
