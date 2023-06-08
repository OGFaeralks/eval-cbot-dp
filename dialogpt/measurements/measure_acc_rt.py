import timeit
import datetime
import pandas as pd
import json
from transformers import AutoModelWithLMHead, AutoTokenizer
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-Large')
model = AutoModelWithLMHead.from_pretrained("../models/checkpoint-2000")
rouge = Rouge()

def calculate_similarity_score(response, correct_answer):
    jaccard_similarity = len(set(response).intersection(correct_answer)) / len(set(response).union(correct_answer))
    bleu_score = sentence_bleu([correct_answer.split()], response.split())
    rouge_scores = rouge.get_scores(response, correct_answer)
    return jaccard_similarity, bleu_score, rouge_scores

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

# Load test data
with open("../../training/test_data.json", "r") as f:
    test_data = json.load(f)

questions = [item[0] for item in test_data]
ground_truth = [item[1] for item in test_data]

# Perform multiple runs
num_runs = 3

for run in range(num_runs):
    bot_responses = []
    response_times = []
    jaccard_similarities = []
    bleu_scores = []
    rouge_1_scores = []
    rouge_2_scores = []
    rouge_l_scores = []

    for question, correct_answer in zip(questions, ground_truth):
        start_time = timeit.default_timer()
        response = query({
            "inputs": {
                "past_user_inputs": [],
                "generated_responses": [],
                "text": question,
            }
        })
        end_time = timeit.default_timer()
        response_times.append(end_time - start_time)
        bot_responses.append(response["generated_text"])

        jaccard_similarity, bleu_score, rouge_scores = calculate_similarity_score(response["generated_text"], correct_answer)
        jaccard_similarities.append(jaccard_similarity)
        bleu_scores.append(bleu_score)
        rouge_1_scores.append(rouge_scores[0]['rouge-1']['f'])
        rouge_2_scores.append(rouge_scores[0]['rouge-2']['f'])
        rouge_l_scores.append(rouge_scores[0]['rouge-l']['f'])

    # Create a DataFrame with the results
    results = pd.DataFrame({
        "Question": questions,
        "Bot Response": bot_responses,
        "Expected Response": ground_truth,
        "Jaccard Similarity": jaccard_similarities,
        "BLEU Score": bleu_scores,
        "ROUGE-1": rouge_1_scores,
        "ROUGE-2": rouge_2_scores,
        "ROUGE-L": rouge_l_scores,
        "Response Time": response_times
    })

    # Save the results to a file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results.to_csv(f'dialogpt_accuracy_results_{timestamp}_run_{run + 1}.csv', index=False)