import whisper

model = whisper.load_model("base")


def speech_to_text(audio_file="audio.mp3"):
    result = model.transcribe(audio_file)
    print(result["text"])
    return result["text"]


def speech_to_text_translated(audio_file="audio.mp3", language="en"):
    options = {
        "language": language,
        "without_timestamps": False,
        "task": "translate",
        "fp16": False
    }
    audio = whisper.load_audio(audio_file)
    result = whisper.transcribe(model, audio, **options)
    print("Original Text:", result["text"])
    return result["text"]


if __name__ == '__main__':
    speech_to_text_translated("audio.mp3")

