import re
import en_core_web_lg
import torch
from transformers import pipeline


def chunk_clean_text(text):
    """Chunk text longer than 500 tokens"""
    article = nlp(text)
    sentences = [i.text for i in list(article.sents)]

    current_chunk = 0
    chunks = []

    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(" ")) <= 500:
                chunks[current_chunk].extend(sentence.split(" "))
            else:
                current_chunk += 1
                chunks.append(sentence.split(" "))
        else:
            chunks.append(sentence.split(" "))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = " ".join(chunks[chunk_id])

    return chunks


def preprocess_plain_text(x):
    x = x.encode("ascii", "ignore").decode()  # unicode
    x = re.sub(r"https*\S+", " ", x)  # url
    x = re.sub(r"@\S+", " ", x)  # mentions
    x = re.sub(r"#\S+", " ", x)  # hastags
    x = re.sub(r"\s{2,}", " ", x)  # over spaces
    x = re.sub("[^.,!?A-Za-z0-9]+", " ", x)  # special charachters except .,!?

    return x


def clean_text(text):
    """Return clean text from the various input sources"""
    return chunk_clean_text(preprocess_plain_text(text))


def get_spacy():
    nlp = en_core_web_lg.load()
    return nlp


def google_model():
    model_name = 'google/pegasus-large'
    summarizer = pipeline('summarization', model=model_name, tokenizer=model_name,
                          device=0 if torch.cuda.is_available() else -1)
    return summarizer


nlp = get_spacy()

model_type = "Google-Pegasus"

max_len = 100
min_len = 50

plain_text = "The app supports extractive summarization which aims to identify the salient information that is then extracted and grouped together to form a concise summary. For documents or text that is more than 500 words long, the app will divide the text into chunks and summarize each chunk. Please note when using the sidebar slider, those values represent the min/max text length per chunk of text to be summarized. If your article to be summarized is 1000 words, it will be divided into two chunks of 500 words first then the default max length of 100 words is applied per chunk, resulting in a summarized text with 200 words maximum"

summarizer_model = google_model()


def text_to_summary(text):
    text_to_summarize = clean_text(text)
    summarized_text = summarizer_model(text_to_summarize, max_length=max_len, min_length=min_len,
                                       clean_up_tokenization_spaces=True, no_repeat_ngram_size=4)
    summarized_text = ' '.join([summ['summary_text'] for summ in summarized_text])
    print(summarized_text)
    return summarized_text


# eexecute if importe
if __name__ == '__main__':
    text_to_summary(plain_text)
