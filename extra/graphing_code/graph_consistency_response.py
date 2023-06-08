import matplotlib.pyplot as plt

# Jaccard Similarity Data
jaccard_bot_names = ['DialoGPT-based', 'Chatterbot', 'Botkit and Natural']
jaccard_scores = [0.130, 0.690, 0.445]

# Response Time Data
response_bot_names = ['DialoGPT-based', 'Chatterbot', 'Botkit and Natural', 'Rasa']
response_times = [14.3, 0.785, 0.01, 2.1]

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot Jaccard Similarity Data
ax1.bar(jaccard_bot_names, jaccard_scores, color='b')
ax1.set_title('Jaccard Similarity for Consistency')
ax1.set_ylabel('Jaccard Similarity')

# Plot Response Time Data
ax2.bar(response_bot_names, response_times, color='r')
ax2.set_title('Average response Time')
ax2.set_ylabel('Response Time (seconds)')

# Show plots
plt.tight_layout()
plt.show()