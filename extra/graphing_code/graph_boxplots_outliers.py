import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Specify the names of your csv files, this is an example for Botkit + Natural
files = ['../../results/botkit_natural_results/botkit_natural_accuracy_results_first_run.csv',
         '../../results/botkit_natural_results/botkit_natural_accuracy_results_second_run.csv',
         '../../results/botkit_natural_results/botkit_natural_accuracy_results_third_run.csv']

# Specify the columns that contain numeric data
numeric_columns = ['Jaccard', 'BLEU', 'ROUGE-1', 'ROUGE-2', 'ROUGE-L']

dfs = []

# Read in the data
for file in files:
    # Check if the file exists
    if os.path.isfile(file):
        df = pd.read_csv(file)
        dfs.append(df[numeric_columns])

# Assume that all dfs have the same number of rows and in the same order
average_df = pd.concat(dfs).groupby(level=0).mean()

# Using seaborn for better visualizations
fig, ax = plt.subplots(figsize=(10, 7))
sns.boxplot(data=average_df, ax=ax)

# Set the labels for the x-axis
ax.set_xticklabels(numeric_columns, rotation=45, ha='right')

# Set the title for the "Average Run" subplot
ax.set_title("Botkit and Natural average run")

# Save the figure as an image with white background and tight layout
plt.savefig('../../results/botkit_natural_results/botkit_natural_average_run.png', format='png', bbox_inches='tight', dpi=300)