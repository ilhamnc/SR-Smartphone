from flask import Flask
import pandas as pd 
import pickle
import json

def create_app():
    app = Flask(__name__)

    # Load data dan model yang sudah diproses saat build menggunakan pandas
    # df = pd.read_json('app/data/smartphones_processed.json', orient='records')
    
    # Load data dan model yang sudah diproses saat build tanpa pandas, gunakan modul json bawaan
    with open('app/data/smartphones_processed.json', 'r') as f:
        data_records = json.load(f)
    df = pd.DataFrame(data_records) # Ubah jadi dataframe 
    
    with open('app/data/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('app/data/tfidf_matrix.pkl', 'rb') as f:
        tfidf_matrix = pickle.load(f)

    # Simpan semua ke app.config
    app.config['DATAFRAME'] = df
    app.config['VECTORIZER'] = vectorizer
    app.config['TFIDF_MATRIX'] = tfidf_matrix

    # Import routes dan daftarkan blueprint
    from .routes import main_app
    app.register_blueprint(main_app)

    return app