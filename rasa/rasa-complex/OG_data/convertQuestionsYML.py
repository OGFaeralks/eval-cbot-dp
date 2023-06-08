import spacy
import json

import yaml

# Open the JSON file and load the data
with open('data.json') as f:
    data = json.load(f)


patient_questions = []
doctor_answers = []


for statement in data:
    for i, person in enumerate(statement):
        if i % 2 == 0:
            patient_questions.append(person)
        else:
            doctor_answers.append(person)




nlp = spacy.load("en_core_web_sm")

def extract_symptoms(text):
    symptoms = []
    doc = nlp(text)

    for token in doc:
        if token.dep_ in ('dobj', 'attr') and token.head.lemma_ in ('have', 'suffer', 'experience'):
            symptom_phrase = ' '.join([t.text for t in token.subtree if not t.is_punct and not t.is_stop])
            symptoms.append(symptom_phrase)
    return symptoms

new_patient_questions = []



for patient in doctor_answers:
    symptoms = extract_symptoms(patient)
    temp = patient
    boolea = False
    for symptom in symptoms:    
        if not symptom.strip():
            boolea = True
            break
        # print(f"{symptom} aaaa")
        temp = temp.replace(symptom, f"[{symptom}](symptom)")
        print(temp)
    if (boolea):
        continue
    new_patient_questions.append(temp)
        
with open('output.yml', 'w') as f:
    for conversation in new_patient_questions:
        f.write('- ')
        f.write(conversation)
        f.write('\n')

# print(new_patient_questions)
