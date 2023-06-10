__author__ = '{Fabian Dacic}'

import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Specify the names of your csv files, this is an example for Botkit+Natural
files = ['../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_run_1.csv',
         '../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_run_2.csv',
         '../../results/botkit_natural_results/accuracy_results/botkit_natural_accuracy_run_3.csv']

# Specify the columns that contain numeric data
numeric_columns = ['Jaccard Similarity', 'BLEU', 'ROUGE-1', 'ROUGE-2', 'ROUGE-L']

dfs = []

# Read in the data
for file in files:
    # Check if the file exists
    if os.path.isfile(file):
        df = pd.read_csv(file)
        dfs.append(df[numeric_columns])

# Assume that all dfs have the same number of rows and in the same order
average_df = pd.concat(dfs).groupby(level=0).mean()

# Adding average df to the list of dfs
dfs.append(average_df)

# Creating a 2x2 plot grid
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 14))

# Flattening axes for easy iterating
axes = axes.flatten()

# Plotting each dataframe in a subplot
for i, df in enumerate(dfs):
    sns.boxplot(data=df, ax=axes[i])
    axes[i].set_xticklabels(numeric_columns, rotation=45, ha='right')
    if i < len(dfs) - 1:
        axes[i].set_title(f"Botkit and Natural Run {i+1}")
    else:
        axes[i].set_title(f"Botkit and Natural Average Run")

plt.tight_layout()

# Save the figure as an image with white background and tight layout
plt.savefig('../../results/botkit_natural_results/img/botkit_natural_runs_and_average.png', 
    format='png', 
        bbox_inches='tight', 
            dpi=300)