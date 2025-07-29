from sklearn.metrics.pairwise import cosine_similarity

def recommend(df, vectorizer, tfidf_matrix, user_keywords):
    # Mengekstrak input user menjadi matrix TF-IDF dengan campuran kosakata dari dokumen(kumpulan dataset)
    user_vec = vectorizer.transform([' '.join(user_keywords)])
    
    # Hitung similarity terhadap matrix yang sudah ada (matrix diubah menjadi vector menggunakan flatten())
    cosine_similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    
    df['Cosine Similarity'] = cosine_similarities
    recommendations = df.sort_values(by='Cosine Similarity', ascending=False).head(10)

    return recommendations[['model', 'sim', 'processor', 'RAM', 'ROM', 'battery', 'display', 'camera', 'card', 'harga(string)', 'Cosine Similarity']]