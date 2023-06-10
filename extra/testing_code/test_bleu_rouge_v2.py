"""
Description: Considering that there really isn't a JavaScript library for BLEU, I had to make a Python file to 
pretty much take the accuracy csv files and feed them to the functions here in order to get them. The results are
then sent over back to the botkit_natural_results
"""
__author__ = '{Fabian Dacic}'

import pandas as pd
import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge 

def calculate_bleu(reference, candidate):
    reference = nltk.word_tokenize(reference.lower())
    candidate = nltk.word_tokenize(candidate.lower())
    return sentence_bleu([reference], candidate)

def calculate_rouge(reference, candidate):
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    return scores[0]

# This is just an example, please do change the name to the original Botkit and Natural generated file in order for it to work!
df = pd.read_csv("../../results/botkit_natural_results/accuracy_results_new/newest_results_accuracy_run_3.csv")

bleu_scores = []
rouge_1_scores = []
rouge_2_scores = []
rouge_l_scores = []

for index, row in df.iterrows():
    bleu = calculate_bleu(row['Actual Answer'], row['Generated Answer'])
    rouge_scores = calculate_rouge(row['Actual Answer'], row['Generated Answer'])
    
    bleu_scores.append(bleu)
    rouge_1_scores.append(rouge_scores['rouge-1']['f'])
    rouge_2_scores.append(rouge_scores['rouge-2']['f'])
    rouge_l_scores.append(rouge_scores['rouge-l']['f'])

df['BLEU'] = bleu_scores
df['ROUGE-1'] = rouge_1_scores
df['ROUGE-2'] = rouge_2_scores
df['ROUGE-L'] = rouge_l_scores

df.to_csv("../../results/botkit_natural_results/accuracy_refined_results/bn_acc_ref_new_3.csv", index=False)