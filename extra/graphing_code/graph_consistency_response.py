__author__ = '{Fabian Dacic}'

import matplotlib.pyplot as plt
import pandas as pd
import os

# Specify the names and the locations of your csv files
files = [
    '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_1.csv', 
    '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_2.csv', 
    '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_3.csv', 
    '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_1.csv',
    '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_2.csv',
    '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_3.csv',
    '../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_results_run_1.csv',
    '../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_results_run_2',
    '../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_results_run_3.csv'
]

# Bot names
bot_names = ['DialoGPT-based', 'Chatterbot', 'Botkit and Natural', 'Rasa']

# Create a list with the hard-coded value for Rasa
response_times = [None, None, None, 2.1]

# Iterate over each file
for i, file in enumerate(files):
    if os.path.isfile(file): # Check if file exists
        df = pd.read_csv(file) # Read the CSV file

        # Check for column name and extract response time, add to the list
        if 'Response Time' in df.columns:
            response_times[i] = df['Response Time'].mean()
        elif 'Response Time (s)' in df.columns:
            response_times[i] = df['Response Time (s)'].mean()

# Create a new figure for the bar plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Response Time Data
ax.bar(bot_names, response_times, color='r')
ax.set_title('Average Response Time')
ax.set_ylabel('Response Time (seconds)')

# Show the plot
plt.tight_layout()
plt.show()