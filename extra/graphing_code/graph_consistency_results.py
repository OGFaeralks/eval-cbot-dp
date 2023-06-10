__author__ = '{Fabian Dacic}'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the names of your consistency files
files = ['../../results/botkit_natural_results/botkit_natural_consistency_run.csv', 
         '../../results/chatterbot_results/chatterbot_consistency.csv', 
         '../../results/dialogpt_results/dialogpt_consistency.csv']

# Specify the column names
query_group_column = 'query_group'
jaccard_similarity_column = 'jaccard_similarity'

# Set custom names for the chatbots
chatbot_labels = ['Botkit with Natural', 'ChatterBot', 'DialoGPT']

# Create an empty dataframe to store all the data
df_all = pd.DataFrame()

# Read the consistency files, store the data in df_all with an extra column for the chatbot label
for i, file in enumerate(files):
    df = pd.read_csv(file)
    df['Chatbot'] = chatbot_labels[i]  # add a new column for the chatbot label
    df_all = pd.concat([df_all, df])  # add this dataframe to df_all

# Print out descriptive statistics for each chatbot
for label in chatbot_labels:
    print(f"Descriptive statistics for {label}:")
    print(df_all.loc[df_all['Chatbot'] == label, jaccard_similarity_column].describe())
    print('\n')

# Create a boxplot for the combined dataframe
plt.figure(figsize=(10, 7))
sns.boxplot(x='Chatbot', y=jaccard_similarity_column, data=df_all)

# Set y-label and title
plt.ylabel('Jaccard Similarity')
plt.title('The average consistency of all chatbots')
# Save the figure as an image with white background and tight layout
plt.savefig('../../results/average_consistency_of_all_three.png')
# Show the plot
plt.show()