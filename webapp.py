from flask import Flask
from flask import request
from flask import jsonify
import os
import tempfile

from speech_to_text import speech_to_text_translated
from text_to_italian import translate
from text_to_summary import text_to_summary
from video_to_speech import video_to_speech

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/speech_to_text_translated", methods=["POST"])
def speech_to_text_translated_api():
    file = request.files['file']
    if not file:
        return "bad request"
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        filename = file.filename
        input_file_path = os.path.join(tmpdirname, filename)
        output_file_path = os.path.join(tmpdirname, 'audio.mp3')
        file.save(input_file_path)
        video_to_speech(input_file_path, output_file_path)
        res = speech_to_text_translated(output_file_path)
        return jsonify(res)


@app.route("/text_to_summary", methods=["POST"])
def text_to_summary_api():
    input_ = request.get_json()['input']
    res = text_to_summary(input_)
    return jsonify(res)


@app.route("/translate", methods=["POST"])
def translate_api():
    input_ = request.get_json()['input']
    res = translate(input_)
    return jsonify(res)


@app.route("/summarize", methods=["POST"])
def summarize():
    file = request.files['file']
    if not file:
        return "bad request"
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        filename = file.filename
        input_file_path = os.path.join(tmpdirname, filename)
        output_file_path = os.path.join(tmpdirname, 'audio.mp3')
        file.save(input_file_path)
        video_to_speech(input_file_path, output_file_path)
        [_, transcription] = speech_to_text_translated(output_file_path)
        [_, summary] = text_to_summary(transcription)
        [_, res] = translate(summary)
        return jsonify(res)
