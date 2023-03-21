from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")


def translate(input_text, input_language="en", output_language="it"):
    tokenizer.src_lang = input_language
    encoded_input = tokenizer(input_text, return_tensors="pt")
    generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(output_language))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)



if __name__ == '__main__':
    print(translate("Hello world!"))
    print(translate("In this video I'm going to tell you about some things that I want to do to increase the number of "
              "subscribers on my YouTube channel."))