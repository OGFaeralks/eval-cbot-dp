import pandas as pd
import matplotlib.pyplot as plt
import os

# Specify the names of your csv files
files = ['./graphing_results/botkit_natural_accuracy_results_first_run.csv - results_accuracy_bleu_rouge.csv.csv',
         './graphing_results/botkit_natural_accuracy_results_second_run - results_accuracy_bleu_rouge_2.csv.csv',
         './graphing_results/botkit_natural_accuracy_results_third_run - results_accuracy_bleu_rouge_3.csv.csv']

# Specify the columns that contain numeric data
numeric_columns = ['Jaccard Similarity', 'BLEU', 'ROUGE-1', 'ROUGE-2', 'ROUGE-L']

dfs = []

# Read in the data
for file in files:
    # Check if the file exists
    if os.path.isfile(file):
        df = pd.read_csv(file)
        dfs.append(df[numeric_columns])

# Remove outliers from all runs
dfs_no_outliers = [df[~df.isin(df.quantile(0.95))].dropna() for df in dfs]

# Calculate the average of each metric for all runs without outliers
average_df = pd.concat(dfs_no_outliers)

# Define colors for each metric
colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'darkred']

# Create a figure and axes for the boxplot
fig, ax = plt.subplots(figsize=(10, 7))

# Plot the boxplot for the "Average Run" without outliers
boxplot = ax.boxplot(average_df.values, patch_artist=True)

# Set facecolor of the boxes for each metric
for j, patch in enumerate(boxplot['boxes']):
    patch.set_facecolor(colors[j])

# Set the labels for the x-axis
ax.set_xticklabels(numeric_columns, rotation=45, ha='right')

# Change color and linewidth of the medians
for median in boxplot['medians']:
    median.set(color='black', linewidth=2)

# Set the title for the "Average Run" subplot
ax.set_title("Botkit and Natural average run (with combined outliers)")

# Save the figure as an image with white background and tight layout
plt.savefig('botkit_natural_average_run.png', format='png', bbox_inches='tight', dpi=300)