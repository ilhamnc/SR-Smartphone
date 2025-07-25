from sklearn.metrics.pairwise import cosine_similarity

def recommend(df, vectorizer, tfidf_matrix, user_keywords, top_n=10):
    # Vectorizer tidak perlu di-fit lagi, hanya transform input user
    user_vec = vectorizer.transform([' '.join(user_keywords)])
    
    # Hitung similarity terhadap matrix yang sudah ada
    cosine_similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    df['Cosine Similarity'] = cosine_similarities
    recommendations = df.sort_values(by='Cosine Similarity', ascending=False).head(top_n)

    return recommendations[['model', 'sim', 'processor', 'RAM', 'ROM', 'battery', 'display', 'camera', 'card', 'harga(string)', 'Cosine Similarity']]