from functools import reduce
from speech_to_text import speech_to_text
from summary_with_openai import summary_with_davinci
from video_to_speech import video_to_speech

video_file_name = 'video.mp4'
# speech = video_to_speech(video_file_name)
# text = speech_to_text_translated(speech)
# summary = text_to_summary(text)
# translate(summary)


steps = [video_to_speech, speech_to_text, summary_with_davinci]


def main():
    def elaborate(prev, func):
        message, intermediate_result = func(prev)
        print(message, intermediate_result)
        return intermediate_result

    reduce(elaborate, steps, video_file_name)


if __name__ == '__main__':
    main()


