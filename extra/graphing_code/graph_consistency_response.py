__author__ = '{Fabian Dacic}'

import matplotlib.pyplot as plt
import pandas as pd
import os

# Specify the names and the locations of your csv files in the order of the corresponding bot
file_groups = [
    (
        'DialoGPT',
        [
            '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_1.csv',
            '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_2.csv',
            '../../results/dialogpt_results/accuracy_results/dialogpt_accuracy_results_run_3.csv',
        ]
    ),
    (
        'Chatterbot',
        [
            '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_1.csv',
            '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_2.csv',
            '../../results/chatterbot_results/accuracy_results/chatterbot_accuracy_results_run_3.csv',
        ]
    ),
    (
        'Botkit and Natural',
        [
            '../../results/botkit_natural_results/accuracy_results_new/newest_results_accuracy_run_1.csv',
            '../../results/botkit_natural_results/accuracy_results_new/newest_results_accuracy_run_2.csv',
            '../../results/botkit_natural_results/accuracy_results_new/newest_results_accuracy_run_3.csv',
        ]
    ),
]

# Bot names and their respective response times
bot_names = []
response_times = []

# Iterate over each file group
for bot_name, files in file_groups:
    # Set conversion factor for time depending on the bot
    time_conversion_factor = 0.001 if bot_name == 'Botkit and Natural' else 1
    for file in files:
        if os.path.isfile(file):  # Check if file exists
            df = pd.read_csv(file)  # Read the CSV file

            # Extract response time, add to the list
            if 'Response Time' in df.columns:
                average_time = df['Response Time'].mean() * time_conversion_factor
                print(f"Average response time for {bot_name} in file {file} is: {average_time} seconds")

            bot_names.append(bot_name)
            response_times.append(average_time)


# Add hard-coded value for Rasa
bot_names.append('Rasa')
response_times.append(2.1)

# Create a new figure for the bar plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Response Time Data
ax.bar(bot_names, response_times, color='r')
ax.set_title('Average Response Time Per Query')
ax.set_ylabel('Response Time (seconds)')

# Show the plot
plt.tight_layout()
plt.savefig('../../results/average_response_time_for_three.png')

plt.show()