from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
from typing import List, Tuple
import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.response_selection import get_most_frequent_response
import requests
from bs4 import BeautifulSoup

file_path_medical = "../../training/train_data.json"

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

# Create and train the ChatterBot instance
bot = ChatBot(
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

bot.storage.drop()  # Clean the database before training

# Use the ChatterBotCorpusTrainer to train the bot with the English corpus
corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train("chatterbot.corpus.english.greetings")

conversations = load_data_from_json(file_path_medical)
train_bot(bot, conversations)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))


if __name__ == "__main__":
    app.run()
