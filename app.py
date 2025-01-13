from flask import Flask, render_template, request, jsonify, send_file
from src.translate import translate, translate_with_subtitle, get_dict_size
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
    if len(input_text) > 0:
        # print(remove_vietnamese_accents(input_text))
        translated_text, processed_text = translate_with_subtitle(input_text)
    else:
        translated_text, processed_text = None, None
    return jsonify({"processed_text": processed_text, "translated_text": translated_text})

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    
    tts = gTTS(text=text, lang='vi')
    
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    
    return send_file(audio_stream, mimetype='audio/mpeg', as_attachment=False, download_name="output.mp3")

@app.route('/api/translate', methods=['POST'])
def transform_text():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid input, message is required'}), 400

        input_text = data['message']

        translated_text = translate(input_text)

        return jsonify({'translated': translated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
