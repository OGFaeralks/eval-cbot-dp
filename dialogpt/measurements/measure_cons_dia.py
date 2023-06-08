import timeit
import datetime
import csv
import json
from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-Large')
model = AutoModelWithLMHead.from_pretrained("../models/checkpoint-2000")

def jaccard_similarity(response1, response2):
    score = len(set(response1).intersection(response2)) / len(set(response1).union(response2))
    return score

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

queries = [
    ["I'm experiencing lung pain and discomfort, but it's not constant or in the same place. I don't have a fever, and I only cough or sneeze once a day. Should I get tested for COVID-19?",
     "My lungs feel uncomfortable and painful, but the location keeps changing and it's not in both lungs at the same time. I have no fever, and I sneeze and cough infrequently. Do I need a coronavirus test?",
     "I have some lung discomfort and pain that moves around and isn't simultaneous in both lungs. I don't have a high temperature, and I only cough and sneeze occasionally. Is it necessary for me to get tested for COVID-19?"],
    ["Should I get tested for COVID-19 if I have a blocked nose and recently returned from a high-risk country?",
     "I just came back from a country with a high COVID-19 risk, and my nose is congested. Do I need a coronavirus test?",
     "If I have nasal congestion and have traveled from a high-risk area, should I be tested for COVID-19?"],
    ["I've had a dry cough and a sore throat for a week, which seems to be worsening. I don't have a runny nose or fever but sometimes experience headaches. Do I need a COVID-19 test?",
     "My dry cough and sore throat have been persisting for a week and are getting worse. There's no fever or runny nose, but I occasionally have headaches. Should I get tested for COVID-19?",
     "I've been dealing with a worsening dry cough and sore throat for the past week. I don't have a fever or runny nose, but I do get headaches from time to time. Is it necessary to test for COVID-19?"],
    ["Can COVID-19 symptoms vary in severity, with some people experiencing mild symptoms like fatigue and a low-grade fever, while others have more extreme symptoms?",
     "Is it possible for coronavirus symptoms to be mild in some cases, such as only having fatigue and a low fever, rather than severe symptoms like difficulty breathing?",
     "Can the symptoms of COVID-19 be different for each person, with some having mild symptoms like tiredness and a low fever, while others experience more severe symptoms?"],
    ["I've been self-quarantining after a flight on March 8th and have experienced headaches and a sore throat. With only two days left in my quarantine, should my symptoms be worse by now?",
     "Since my flight on March 8th, I've been in self-quarantine and have had a sore throat and headaches. As my quarantine is almost over, should my symptoms have worsened by now?",
     "I've been self-isolating after a plane journey on March 8th, and I've had a runny throat and headaches. With only two days left in my self-quarantine, should I expect more severe symptoms by now?"]
]

# Open a CSV file to write the results
with open('dialogpt_consistency.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["query_group", "response1", "response2", "jaccard_similarity"])

    for i, query_group in enumerate(queries):
        responses = []
        for question in query_group:
            response = query({
                "inputs": {
                    "past_user_inputs": [],
                    "generated_responses": [],
                    "text": question,
                }
            })
            responses.append(response["generated_text"])
        
        # Calculate consistency (Jaccard Similarity) for each pair of responses
        for j in range(len(responses)):
            for k in range(j+1, len(responses)):
                consistency_score = jaccard_similarity(responses[j], responses[k])
                writer.writerow([i + 1, responses[j], responses[k], consistency_score])