import re
import streamlit as st
from streamlit_chat import message
import requests
from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-Large')
model = AutoModelWithLMHead.from_pretrained("./models/checkpoint-2000")

st.set_page_config(
    page_title="COVID Doctor using DialoGPT",
    page_icon=":robot:"
)

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-Large"
headers = {"Authorization": st.secrets['api_key']}

st.header("COVID Doctor using DialoGPT")
st.markdown("[Based on Rushi's work!](https://github.com/rushic24/DialoGPT-Finetune)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
    bot_input_ids = tokenizer.encode(payload["inputs"]["text"] + tokenizer.eos_token, return_tensors='pt')

    chat_history_ids = model.generate(
      bot_input_ids, 
      max_length=100,
      pad_token_id=tokenizer.eos_token_id,  
      no_repeat_ngram_size=4,       
      do_sample=True, 
      top_k=10, 
      top_p=0.7,
      temperature = 0.8
    )
    output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return {"generated_text": output}

def get_text():
    input_text = st.text_input("You: ", key="input")    
    return input_text 

def process_output(output_text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', output_text)
    if len(sentences) > 1:
        sentences.pop()
    return " ".join(sentences)

user_input = get_text()

if user_input:
    output = query({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },"parameters": {"repetition_penalty": 1.33},
    })
    st.session_state.past.append(user_input)
    processed_output = process_output(output["generated_text"])
    st.session_state.generated.append(processed_output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')