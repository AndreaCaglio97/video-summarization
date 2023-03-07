import streamlit as st
import os

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
from transformers import pipeline
from transformers import set_seed

debug = False

MODELS = [
    "ARTeLab/mbart-summarization-fanpage",
    "ARTeLab/mbart-summarization-ilpost",
    "ARTeLab/mbart-summarization-mlsum",
    "ARTeLab/it5-summarization-mlsum",
    "ARTeLab/it5-summarization-ilpost",
    "ARTeLab/it5-summarization-fanpage"
]

DEFAULT_TEXT: str = """(Fanpage) Dopo oltre mezzo secolo, il mistero della Natività di Caravaggio resta intatto. L'opera, intitolata la "Natività con i Santi Lorenzo e Francesco d'Assisi", fu trafugata la notte tra il 17 e il 18 ottobre 1969 dall'Oratorio di San Lorenzo a Palermo e tuttora non è stata ancora recuperata. L'olio su tela realizzato da Caravaggio, inserito dagli investigatori nella top ten mondiale delle opere d'arte trafugate e mai più ritrovate, ha un valore di mercato che si aggirerebbe oggi intorno ai 20 milioni di dollari secondo l'FBI. La sua storia è avvolta nel mistero e dopo cinquantuno anni ancora non è stata risolta, dopo il furto della mafia nel 1969 e forse ormai distrutta. L'unica certezza è che nemmeno questo Natale potremo ammirare l'opera raffigurante la nascita di Cristo del grande genio pittorico italiano. E forse, secondo i più pessimisti, non ci riusciremo mai più. Nella notte tra il 17 e il 18 ottobre, nel cuore di Palermo, i boss di Cosa Nostra si intrufolarono nell'Oratorio di San Lorenzo e arrotolarono la "Natività con i Santi Lorenzo e Francesco d'Assisi" di Caravaggio in malo modo, facendo sgranare la tela. Una delle più alte testimonianza dell'arte di ogni tempo fu distrutta così. Ma come facciamo a sapere oggi che la tela è andata distrutta? Fu il pentito Francesco Marino Mannoia, durante il processo Andreotti nel 1996 a raccontare del presunto disastro di un gioiello arrotolato in fretta e portato via in segno di sfregio. Ma questa versione stride con quella di un altro pentito che ricorda il quadro affisso ai summit di mafia, come un trofeo, mentre sui giornali si sussurrava di losche ma non provate trattative da 60 miliardi di vecchie lire fra mediatori e trafficanti. Nel 2017, il mafioso Gaetano Grado asserisce che la tela sarebbe stata nascosta, ma all'estero: nel 1970 il boss Badalamenti l'avrebbe trasferita in Svizzera in cambio di una notevole somma di franchi ad un antiquario svizzero, giunto a Palermo per definire l'affare. Grado riferisce anche che Badalamenti gli avrebbe detto che il quadro era stato scomposto per essere venduto sul mercato clandestino."""


class TextSummarizer:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.model_loaded = None
        set_seed(42)

    def load(self, model_name):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.generator = pipeline(
            "text2text-generation", model=self.model, tokenizer=self.tokenizer
        )
        self.model_loaded = model_name

    def summarize(self, model_name, input_text, generate_kwargs) -> str:
        if not self.generator or self.model_loaded != model_name:
            with st.spinner("meanwhile: downloading/loading selected model...please don't go :("):
                self.load(model_name)
        return self.generator(
            input_text, return_tensors=False, return_text=True, **generate_kwargs
        )[0].get("generated_text")


@st.cache(allow_output_mutation=True)
def instantiate_generator():
    summarizer = TextSummarizer()
    return summarizer


def main():
    st.set_page_config(  # Alternate names: setup_page, page, layout
        page_title="ARTeLab SummIT",
        layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
        initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
        page_icon="📰",  # String, anything supported by st.image, or None.
    )

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    generator = instantiate_generator()

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 500px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("""# ARTeLab SummIT""")
    #st.sidebar.image("fl.png", width=220)
    st.sidebar.markdown(
        """
        * Create summaries of Italian news articles.
        * Copy paste any Italian news text and press the Generate Summary botton.
        """
    )
    st.sidebar.title("Parameters:")

    MODEL = st.sidebar.selectbox("Choose model", index=1, options=MODELS)

    min_length = st.sidebar.number_input(
        "Min length", min_value=10, max_value=150, value=40
    )
    max_length = st.sidebar.number_input(
        "Max length", min_value=20, max_value=250, value=142
    )
    no_repeat_ngram_size = st.sidebar.number_input(
        "No repeat NGram size", min_value=1, max_value=5, value=3
    )

    if sampling_mode := st.sidebar.selectbox(
        "select a Mode", index=0, options=["Beam Search", "Top-k Sampling"]
    ):
        if sampling_mode == "Beam Search":
            num_beams = st.sidebar.number_input(
                "Num beams", min_value=1, max_value=10, value=4
            )
            length_penalty = st.sidebar.number_input(
                "Length penalty", min_value=0.0, max_value=5.0, value=1.5, step=0.1
            )
            params = {
                "min_length": min_length,
                "max_length": max_length,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "num_beams": num_beams,
                "early_stopping": True,
                "length_penalty": length_penalty,
                "num_return_sequences": 1,
            }
        else:
            top_k = st.sidebar.number_input(
                "Top K", min_value=0, max_value=100, value=50
            )
            top_p = st.sidebar.number_input(
                "Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.05
            )
            temperature = st.sidebar.number_input(
                "Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.05
            )
            params = {
                "min_length": min_length,
                "max_length": max_length,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "do_sample": True,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "num_return_sequences": 1,
            }

    input_text = st.text_area("Enter an Italian news text", DEFAULT_TEXT, height=450)

    if st.button("Generate summary"):

        with st.spinner("Generating summary ..."):
        
            response = generator.summarize(MODEL, input_text, params)

            st.header("Summary:")
            st.markdown(response)


if __name__ == "__main__":
    main()