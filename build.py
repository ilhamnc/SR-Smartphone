import pandas as pd
import pickle
from app.preprocessing import preprocess_data # Impor fungsi preprocessing Anda
from sklearn.feature_extraction.text import TfidfVectorizer

print("Memulai proses build...")

# 1. Baca dan proses data dengan pandas (hanya di sini)
df = pd.read_csv('smartphones.csv')
processed_df = preprocess_data(df)

# 2. Buat dan latih TfidfVectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_df['features'])

# 3. Simpan objek yang dibutuhkan ke file
# Simpan dataframe yang sudah bersih sebagai file JSON (jauh lebih ringan)
processed_df.to_json('app/data/smartphones_processed.json', orient='records')

# Simpan vectorizer dan matrix TF-IDF menggunakan pickle
with open('app/data/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('app/data/tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)

print("Proses build selesai. File data dan model telah disimpan.")