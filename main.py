from speech_to_text import speech_to_text_translated
from text_to_summary import text_to_summary
from video_to_speech import video_to_speech

video_file_name = "video.mp4"
speech = video_to_speech(video_file_name)
text = speech_to_text_translated(speech)
summary = text_to_summary(text)
