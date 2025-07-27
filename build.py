import pandas as pd
import pickle
from app.preprocessing import preprocess_data 
from sklearn.feature_extraction.text import TfidfVectorizer

print("Memulai proses build...")

df = pd.read_csv('smartphones.csv')
processed_df = preprocess_data(df)

# Buat dan latih TfidfVectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_df['features'])

# Simpan dataframe yang sudah bersih sebagai file JSON
processed_df.to_json('app/data/smartphones_processed.json', orient='records')

# Simpan vectorizer dan matrix TF-IDF menggunakan pickle
with open('app/data/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('app/data/tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)

print("Proses build selesai. File data dan model telah disimpan.")