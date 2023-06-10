__author__ = '{Fabian Dacic}'

import pandas as pd

# This program is more to generate a csv file of the average of all runs for accuracy,
# that file can then be plugged in for use in shiny.chemgrid for plotting

# List of your csv files, this is an example for the Botkit + Natural measurements
files = ['../../results/botkit_natural_results/accuracy_refined_results/newest_botkit_results_run_1 - Sheet1.csv', 
         '../../results/botkit_natural_results/accuracy_refined_results/newest_botkit_results_run_2 - Sheet1.csv', 
         '../../results/botkit_natural_results/accuracy_refined_results/newest_botkit_results_run_3 - Sheet1.csv']

# Read them in
frames = [pd.read_csv(f) for f in files]

# Assuming that all frames have the same number of rows and in the same order
average_frame = pd.concat(frames).groupby(level=0).mean()

# Save the mean to a new csv
average_frame.to_csv('botkit_accuracy_average.csv', index=False)