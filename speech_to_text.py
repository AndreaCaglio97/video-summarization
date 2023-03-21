import whisper

model = whisper.load_model("base")


def speech_to_text(audio_file="audio.mp3"):
    # load audio and pad/trim it to fit 30 seconds
    # audio = whisper.load_audio(audio_file)
    # audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(language="en", without_timestamps=False, task="translate")
    result = model.transcribe(audio_file, options)
    print(result)
    return result["text"]
    # print(result["text"])


# run if this file is called directly
if __name__ == '__main__':
    speech_to_text("audio.mp3")
