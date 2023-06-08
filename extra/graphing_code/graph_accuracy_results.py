import matplotlib.pyplot as plt
import numpy as np

chatbots_scores = {
    'DialoGPT-based': {'Jaccard': 0.640, 'BLEU': 0.0185, 'ROUGE-1': 0.180, 'ROUGE-2' : 0.0374, 'ROUGE-L' : 0.169},
    'Chatterbot': {'Jaccard': 0.566, 'BLEU': 0, 'ROUGE-1': 0.0857, 'ROUGE-2' : 0.00193, 'ROUGE-L' : 0.0703},
    'Botkit and Natural': {'Jaccard': 0.090, 'BLEU': 0.0224, 'ROUGE-1': 0.156, 'ROUGE-2' : 0.0288, 'ROUGE-L' : 0.145}
}

# Calculate average ROUGE score
for bot in chatbots_scores:
    rouge_avg = (chatbots_scores[bot]['ROUGE-1'] + chatbots_scores[bot]['ROUGE-2'] + chatbots_scores[bot]['ROUGE-L']) / 3
    chatbots_scores[bot]['ROUGE'] = rouge_avg

labels = list(chatbots_scores.keys())
jaccard_scores = [chatbots_scores[bot]['Jaccard'] for bot in labels]
bleu_scores = [chatbots_scores[bot]['BLEU'] for bot in labels]
rouge_scores = [chatbots_scores[bot]['ROUGE'] for bot in labels]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, jaccard_scores, width, label='Jaccard score')
rects2 = ax.bar(x, bleu_scores, width, label='BLEU')
rects3 = ax.bar(x + width, rouge_scores, width, label='Average ROUGE')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Average scores of metrics for the chatbots')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()