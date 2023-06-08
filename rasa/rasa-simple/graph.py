import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
def QuerysizeVsResponseTime():
  df = pd.read_csv("response_times.csv")

  # Create a figure and axis
  fig, ax = plt.subplots()

  # Plot the average response time
  ax.scatter(df["Query Size"], df["Average Time (ms)"], label="Average Time")

  # Plot the maximum response time
  # ax.scatter(df["Query Size"], df["Highest Time (ms)"], label="Highest Time")

  # Set labels and title
  ax.set_xlabel("Query Size")
  ax.set_ylabel("Response Time (ms)")
  ax.set_title("Query Size vs Response Time")

  # Add legend
  ax.legend()

  # Show the plot
  plt.show()

def barplotAveTime():
  df = pd.read_csv("response_times.csv")
  average_time = df['Average Time (ms)'].mean() / 1000  # Convert average time to seconds
  highest_time = df['Highest Time (ms)'].max() / 1000  # Convert highest time to seconds
  plt.bar(['Average Time', 'Highest Time'], [average_time, highest_time])
  plt.ylabel('Time (seconds)')  # Update y-axis label
  plt.title('Rasa response times')
  plt.show()


# barplotAveTime()
QuerysizeVsResponseTime()