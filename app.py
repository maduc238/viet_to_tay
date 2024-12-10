from flask import Flask, render_template, request, jsonify, send_file
from src.translate import translate_with_subtitle
from gtts import gTTS
import io

app = Flask(__name__)

MAX_LENGTH = 5000

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    input_text = data.get("input_text", "")
    if len(input_text) > MAX_LENGTH:
        input_text = ""
    translated_text, processed_text = translate_with_subtitle(input_text)
    return jsonify({"processed_text": processed_text, "translated_text": translated_text})

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    
    tts = gTTS(text=text, lang='vi')
    
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    
    return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name="output.mp3")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run(host='0.0.0.0', port=443, ssl_context="adhoc")
