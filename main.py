from speech_to_text import speech_to_text
from text_to_summary import text_to_summary
from video_to_speech import video_to_speech

res = "video.mp4"
res = video_to_speech(res)
res = speech_to_text(res)
res = text_to_summary(res)

print("this is your marvellous summary: ", res)