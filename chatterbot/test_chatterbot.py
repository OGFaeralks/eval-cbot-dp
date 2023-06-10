__author__ = '{Fabian Dacic}'

import string
import timeit
import json
import csv
import pandas as pd
import requests
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from datetime import datetime
from typing import Tuple, List
from chatterbot.response_selection import get_most_frequent_response
from bs4 import BeautifulSoup
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge

file_path_medical_training = "../../training/train_data.json"
file_path_medical_testing = "../../training/test_data.json"

def get_faq_from_who() -> List[Tuple[str, str]]:
    url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    faqs = []

    questions = soup.find_all('div', class_='sf-accordion__trigger-panel')
    answers = soup.find_all('div', class_='sf-accordion__content')

    for q, a in zip(questions, answers):
        question = q.find('span', itemprop='name').get_text(strip=True)
        answer = a.find('div', itemprop='text').get_text(strip=True)
        print("Question is: ", question, " and answer is: ", answer)
        faqs.append((question, answer))

    return faqs

rouge = Rouge()

def evaluate_bleu_and_rouge(ground_truth, predicted_response):
    smoothing_function = SmoothingFunction().method1
    bleu_score = sentence_bleu([ground_truth.split()], predicted_response.split(), smoothing_function=smoothing_function)
    rouge = Rouge()
    rouge_scores = rouge.get_scores(predicted_response, ground_truth, avg=True)
    return bleu_score, rouge_scores

def test_chatterbot_with_bleu_and_rouge(file_path: str, output_csv_path: str):
    print("Testing BLEU and ROUGE now...")
    with open(file_path, "r", encoding="utf-8") as file:
        test_data = json.load(file)

    total_bleu_score = 0
    total_rouge_scores = {'rouge-1': 0, 'rouge-2': 0, 'rouge-l': 0}

    for question, actual_answer in test_data:
        generated_answer = str(new_bot.get_response(question))
        bleu_score, rouge_scores = evaluate_bleu_and_rouge(actual_answer, generated_answer)

        total_bleu_score += bleu_score
        for key in total_rouge_scores:
            total_rouge_scores[key] += rouge_scores[key]['f']

        with open(output_csv_path, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["question", "generated_answer", "actual_answer", "bleu_score", "rouge-1", "rouge-2", "rouge-l"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                "question": question,
                "generated_answer": generated_answer,
                "actual_answer": actual_answer,
                "bleu_score": bleu_score,
                "rouge-1": rouge_scores['rouge-1']['f'],
                "rouge-2": rouge_scores['rouge-2']['f'],
                "rouge-l": rouge_scores['rouge-l']['f']
            })

    average_bleu_score = total_bleu_score / len(test_data)
    average_rouge_scores = {key: total_rouge_scores[key] / len(test_data) for key in total_rouge_scores}
    print("Average BLEU score for Chatterbot is: ", average_bleu_score)
    print("Average ROUGE score for Chatterbot is: ", average_rouge_scores)
    return average_bleu_score, average_rouge_scores

def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation)).lower()

def jaccard_similarity(response1, response2):
    score = len(set(response1).intersection(response2)) / len(set(response1).union(response2))
    return score

def train_bot(bot: ChatBot, sample_data: List): 
    list_trainer = ListTrainer(bot)
    
    covid_faq = get_faq_from_who()

    for tpl in covid_faq: 
        list_trainer.train(list(tpl))
    
    for lst in sample_data:
        list_trainer.train(lst)

def read_and_process_json(file_path: str) -> List[Tuple[str, str]]:
    print("Reading...")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    conversations = []
    for conversation in data:
        utterances = conversation["utterances"]
        for i in range(len(utterances) - 1):
            if utterances[i].startswith("patient:") and utterances[i + 1].startswith("doctor:"):
                question = utterances[i][len("patient:"):].strip()
                answer = utterances[i + 1][len("doctor:"):].strip()
                conversations.append((question, answer))
    return conversations

def load_data_from_json(file_path: str) -> List[Tuple[str, str]]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Create and train a new ChatterBot instance
new_bot = ChatBot(
    'TestBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///test_bot_database.sqlite3',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": get_most_frequent_response,
            "default_response": "I am not sure how to answer that since I am still learning, could you please try again?",
            "maximum_similarity_threshold": 0.5
        }
    ]
)

new_bot.storage.drop()  # Clean the database before training

corpus_trainer = ChatterBotCorpusTrainer(new_bot)
corpus_trainer.train("chatterbot.corpus.english.greetings")

conversations = load_data_from_json(file_path_medical_training)
train_bot(new_bot, conversations)

def calculate_similarity_score(response, correct_answer):
    jaccard_similarity = len(set(response).intersection(correct_answer)) / len(set(response).union(correct_answer))
    bleu_score = sentence_bleu([correct_answer.split()], response.split())
    rouge_scores = rouge.get_scores(response, correct_answer)
    return jaccard_similarity, bleu_score, rouge_scores

def test_chatterbot(file_path: str):

    with open(file_path, "r", encoding="utf-8") as file:
        test_data = json.load(file)

    for run in range(3):
        questions = []
        acc_answers = []
        responses = []
        response_times = []
        jaccard_similarities = []
        bleu_scores = []
        rouge_1_scores = []
        rouge_2_scores = []
        rouge_l_scores = []
        for question, actual_answer in test_data:
            questions.append(question)
            acc_answers.append(actual_answer)
            start_time = timeit.default_timer()
            generated_answer = str(new_bot.get_response(question))
            responses.append(generated_answer)
            end_time = timeit.default_timer()

            response_time = end_time - start_time
            response_times.append(response_time)

            js, bleu, rouge = calculate_similarity_score(generated_answer, actual_answer)
            jaccard_similarities.append(js)
            bleu_scores.append(bleu)
            rouge_1_scores.append(rouge[0]['rouge-1']['f'])
            rouge_2_scores.append(rouge[0]['rouge-2']['f'])
            rouge_l_scores.append(rouge[0]['rouge-l']['f'])

        # Create a DataFrame with the results
        results = pd.DataFrame({
            "Question": questions,
            "Bot Response": responses,
            "Expected Response": acc_answers,
            "Jaccard Similarity": jaccard_similarities,
            "BLEU Score": bleu_scores,
            "ROUGE-1": rouge_1_scores,
            "ROUGE-2": rouge_2_scores,
            "ROUGE-L": rouge_l_scores,
            "Response Time": response_times
        })

        # Save the results to a file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results.to_csv(f'rerun_chatterbot_accuracy_results_{timestamp}_run_{run + 1}.csv', index=False)


def test_chatterbot_consistency(queries):
    consistency_results = []

    # Create CSV file and write headers
    with open('chatterbot_consistency.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["query_group", "response1", "response2", "jaccard_similarity"])

        for query_group_index, query_group in enumerate(queries):
            print(f"Testing consistency for query group {query_group_index + 1}")
            responses = []
            for query in query_group:
                start_time = timeit.default_timer()
                response = str(new_bot.get_response(query))
                end_time = timeit.default_timer()
                response_time = end_time - start_time
                print(f"Query: {query}\nResponse: {response}\nResponse time: {response_time} seconds\n")
                responses.append(response)

            for i in range(len(responses)):
                for j in range(i+1, len(responses)):
                    score = jaccard_similarity(responses[i], responses[j])
                    writer.writerow([query_group_index + 1, responses[i], responses[j], score])

    return consistency_results

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
    
test_chatterbot_consistency(queries)
