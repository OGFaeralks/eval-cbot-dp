from typing import List, Tuple
import requests
from bs4 import BeautifulSoup

def get_faq_from_who() -> List[Tuple[str, str]]:
    url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    faqs = []

    questions = soup.find_all('div', class_='sf-accordion__trigger-panel')
    answers = soup.find_all('div', class_='sf-accordion__content')
    nluData = []
    utterData = []

    for q, a in zip(questions, answers):
        question = q.find('span', itemprop='name').get_text(strip=True)
        nluData.append(question)
        answer = a.find('div', itemprop='text').get_text(strip=True)
        utterData.append(answer)
        print("Question is: ", question, " and answer is: ", answer)
        faqs.append((question, answer))

    return faqs

get_faq_from_who()