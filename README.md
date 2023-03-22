# Video Summarization

## Console application
Starting from an Italian video, the application produces a summary of it by performing the following steps:
- video to speech (a speech in Italian is extracted from an Italian video);
- speech to text (an Italian speech is converted into an English text);
- text to summary (the English text is summarized);
- translation (the summary is translated into Italian).

#### Prerequisites:
You must have the `ffmpeg` library installed on your environment in order to use OpenAI's Whisper model.

You need to download any video you like in .mp4 format, rename it to **video.mp4**, 
and place it in the project root.

Before you can run the application, you must install all the dependencies.
To do this, you can run the following command in the terminal:

`pip install -r requirements.txt`

#### Run the app:
To run the application, you can execute the following command in the terminal:

`python main.py`

## Gradio app
#### Run the app:
To run the application, you can execute the following command in the terminal:

`gradio app.py`

## Flask app

#### Prerequisites:
Before you can run the application, you must install `en_core_web_sm`.
To do this, you can run the following command in the terminal:

`python -m spacy download en_core_web_sm`

#### Run the app:
To run the application, you can execute the following command in the terminal:

`FLASK_APP=webapp.py FLASK_ENV=development flask run`