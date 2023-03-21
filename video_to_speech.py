import ffmpeg


def video_to_speech(input_file_name='video.mp4'):
    output_file_path = 'audio.mp3'

    stream = ffmpeg.input(input_file_name)
    audio_stream = stream.audio
    audio_stream = ffmpeg.output(audio_stream, output_file_path)
    ffmpeg.run(audio_stream)
    return output_file_path


# run only if this file is called directly
if __name__ == '__main__':
    video_to_speech()
