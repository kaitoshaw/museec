import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example dataset (feature vectors for 4 songs)
# Replace this with your actual dataset
feature_vectors = np.array([
    [0.8, 0.2, 0.4],  # Index 0
    [0.5, 0.7, 0.9],  # Index 1
    [0.3, 0.1, 0.6],  # Index 2
    [0.2, 0.4, 0.5]   # Index 3
])

# Calculate cosine similarity matrix
cosine_sim_matrix = cosine_similarity(feature_vectors)

print(cosine_sim_matrix)

# Example query song (feature vector)
# Replace this with the feature vector of the song you want to find similar songs for
query_song = np.array([[0.3, 0.1, 0.8]])

# Calculate cosine similarity between the query song and all other songs
cosine_similarities = cosine_similarity(query_song, feature_vectors)
print(cosine_similarities)

# Get the most similar song index
most_similar_song_index = np.argmax(cosine_similarities)

# Print the most similar song index and its corresponding similarity score
print("Most similar song index:", most_similar_song_index)
print("Similarity score:", cosine_similarities[0, most_similar_song_index])

