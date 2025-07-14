from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_similarity_score(vec1, vec2):
    return float(cosine_similarity([vec1], [vec2])[0][0]) * 100
