from flask import Flask, render_template, request, jsonify
from src.translate import translate

app = Flask(__name__)

messages = []


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/send", methods=["POST"])
def send_message():
    global messages
    message = request.json.get("message")
    if message:
        messages.append({"user": "User", "text": message})
        messages.append({"user": "Translate", "text": translate(message)})
    return jsonify(messages)


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)


if __name__ == "__main__":
    app.run(debug=True)
