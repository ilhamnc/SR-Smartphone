from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend(df, user_keywords, top_n=10):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['features'])

    user_vec = vectorizer.transform([' '.join(user_keywords)])
    cosine_similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    df['Cosine Similarity'] = cosine_similarities
    recommendations = df.sort_values(by='Cosine Similarity', ascending=False).head(top_n)

    # Tentukan kolom output seperti original 
    return recommendations[['model', 'sim', 'processor', 'RAM', 'ROM', 'battery', 'display', 'camera', 'card', 'harga(string)', 'Cosine Similarity']]
