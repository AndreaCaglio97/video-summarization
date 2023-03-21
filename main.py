from speech_to_text import speech_to_text_translated
from text_to_italian import translate
from text_to_summary import text_to_summary
from video_to_speech import video_to_speech
from functools import reduce

video_file_name = 'video.mp4'
# speech = video_to_speech(video_file_name)
# text = speech_to_text_translated(speech)
# summary = text_to_summary(text)
# translate(summary)


steps = [video_to_speech, speech_to_text_translated, text_to_summary, translate]


def main():
    def elaborate(prev, func):
        message, intermediate_result = func(prev)
        print(message, intermediate_result)
        return intermediate_result

    reduce(elaborate, steps, video_file_name)


if __name__ == '__main__':
    main()


