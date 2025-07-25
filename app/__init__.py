from flask import Flask
import pandas as pd
from .preprocessing import preprocess_data

def create_app():
    app = Flask(__name__)

    # Load data sekali saat app start
    folder_path = 'smartphones.csv'
    df = pd.read_csv(folder_path)

    # Preprocessing
    df = df.dropna()
    df = preprocess_data(df)

    # Tempatkan DataFrame di app config agar bisa diakses di routes via current_app
    app.config['DATAFRAME'] = df

    # Import routes dan daftarkan blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app