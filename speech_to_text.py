import whisper

model = whisper.load_model('base')


def speech_to_text(audio_file='audio.mp3'):
    result = model.transcribe(audio_file)
    message = 'Original text:'
    return message, result['text']


def speech_to_text_translated(audio_file='audio.mp3', language='it'):
    options = {
        'language': language,
        'without_timestamps': False,
        'task': 'translate',
        'fp16': False
    }
    audio = whisper.load_audio(audio_file)
    result = whisper.transcribe(model, audio, **options)
    message = 'Original text:'
    return message, result['text']


if __name__ == '__main__':
    speech_to_text_translated('audio.mp3')

