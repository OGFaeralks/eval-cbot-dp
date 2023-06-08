# Import necessary library
import pandas as pd

# Specify the names of your consistency files
files = ['./graphing_results/botkit_natural_consistency_run.csv - botkit_natural_consistency_run.csv.csv', 
         './graphing_results/chatterbot_consistency.csv - chatterbot_consistency.csv.csv', 
         './graphing_results/dialogpt_consistency.csv - dialogpt_consistency.csv.csv']

# Specify the column names
query_group_column = 'query_group'
jaccard_similarity_column = 'jaccard_similarity'

# Read the consistency files and store the data in a list
dfs = []
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# Set custom names for the chatbots
chatbot_labels = ['Botkit with Natural', 'ChatterBot', 'DialoGPT']

# Print out descriptive statistics for each chatbot
for i, df in enumerate(dfs):
    print(f"Descriptive statistics for {chatbot_labels[i]}:")
    print(df[jaccard_similarity_column].describe())
    print('\n')