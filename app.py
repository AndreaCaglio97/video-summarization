import gradio as gr
from gradio.mix import Parallel

title = "Text Summarizer"
description = "Past an article text or other text. Submit the text and the machine will create four summaries based on words in the text. Which sentences in the text are the most important for the summaries? Which summaries are better for your case?"

io1 = gr.Interface.load('huggingface/sshleifer/distilbart-cnn-12-6')
io2 = gr.Interface.load("huggingface/facebook/bart-large-cnn")
io3 = gr.Interface.load("huggingface/csebuetnlp/mT5_multilingual_XLSum")
io4 = gr.Interface.load("huggingface/google/pegasus-xsum")

iface = Parallel(io1, io2, io3, io4,
                 theme='huggingface',
                 inputs=gr.inputs.Textbox(lines=10, label="Text"), title=title, description=description)

iface.launch(share=False)
