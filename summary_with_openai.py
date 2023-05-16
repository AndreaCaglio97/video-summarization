import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def summary_with_davinci(text):
    summarized_text = openai.Completion.create(
        model="text-davinci-003",
        prompt=text + "\n\nTl;dr",
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    message = 'Summary with davinci:'
    return message, summarized_text
