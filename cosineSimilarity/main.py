import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
os.chdir('..')
from functions import querySong

# Load the first 1000 songs in the dataset
df = pd.read_csv('dataset/partial.csv')
feature_vectors = []

# Only select several columns
columns = [8, 9, 11, 12, 13, 14, 15, 16, 17]
for row in range(len(df)):
    temp = []
    for column in columns:
        temp.append(df.iloc[row][column])
    feature_vectors.append(temp)

# Calculate cosine similarity matrix
cosine_sim_matrix = cosine_similarity(feature_vectors)

# Get song based on the ID
query_song = [querySong('0bC7GKnxh9W9JIvJ6HVWxc')]

# Calculate cosine similarity between the query song and all other songs
cosine_similarities = cosine_similarity(query_song, feature_vectors)

# Get the most similar song index
most_similar_song_index = np.argmax(cosine_similarities)

# # Print the most similar song index and its corresponding similarity score
# print("Most similar song index:", most_similar_song_index)
# print("Similarity score:", cosine_similarities[0, most_similar_song_index])

print(df.iloc[most_similar_song_index])