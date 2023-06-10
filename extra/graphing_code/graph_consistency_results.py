import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the names of your consistency files
files = ['../../results/botkit_natural_results/', 
         './graphing_results/chatterbot_consistency.csv - chatterbot_consistency.csv.csv', 
         './graphing_results/dialogpt_consistency.csv - dialogpt_consistency.csv.csv']

# Specify the column names
query_group_column = 'query_group'
jaccard_similarity_column = 'jaccard_similarity'

# Set custom names for the chatbots
chatbot_labels = ['Botkit with Natural', 'ChatterBot', 'DialoGPT']

# Read the consistency files and store the data in a list
dfs = []
for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# Print out descriptive statistics for each chatbot
for i, df in enumerate(dfs):
    print(f"Descriptive statistics for {chatbot_labels[i]}:")
    print(df[jaccard_similarity_column].describe())
    print('\n')

# Create a new figure for the boxplots
plt.figure(figsize=(10, 7))

# Add a boxplot for each dataframe
for i, df in enumerate(dfs):
    sns.boxplot(y=df[jaccard_similarity_column], label=chatbot_labels[i])

# Set y-label and title
plt.ylabel('Jaccard Similarity')
plt.title('The average consistency of all chatbots')

# Add legend
plt.legend(chatbot_labels)

# Show the plot
plt.show()