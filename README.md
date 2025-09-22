# SmartRec: Sistem Rekomendasi Smartphone

SmartRec adalah aplikasi web yang membantu pengguna menemukan smartphone yang paling sesuai dengan preferensi spesifikasi mereka. Pengguna dapat memasukkan kriteria yang diinginkan, seperti merek, RAM, kapasitas baterai, dan lainnya, lalu sistem akan memberikan daftar 10 smartphone teratas yang paling mirip.

## ✨ Tampilan Aplikasi

<table>
  <tr>
    <td><b>Halaman Utama</b></td>
    <td><b>Halaman Cara Kerja</b></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/k6x3gD2.jpeg" width="400"></td>
    <td><img src="https://i.imgur.com/gK6kU1C.png" width="400"></td>
  </tr>
  <tr>
    <td><b>Formulir Rekomendasi</b></td>
    <td><b>Hasil Rekomendasi</b></td>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/Csc6s6f.png" width="400"></td>
    <td><img src="https://i.imgur.com/39Q8QzP.png" width="400"></td>
  </tr>
</table>

---

## 🧠 Cara Kerja Sistem

Sistem ini menggunakan metode **Content-Based Filtering** dengan **TF-IDF (Term Frequency-Inverse Document Frequency)** dan **Cosine Similarity** untuk menemukan kecocokan antara preferensi pengguna dan database smartphone.

1.  **Preprocessing Data (`preprocessing.py`, `build.py`)**
    * Data mentah dari `smartphones.csv` dibersihkan dan diproses.
    * Fitur-fitur baru diekstraksi seperti merek, merek prosesor, dan dukungan fitur (5G, NFC, Dual SIM).
    * Spesifikasi numerik (baterai, layar, harga, kamera) dikelompokkan ke dalam rentang kategori (misal, kapasitas baterai menjadi '3000-5000 mAh').
    * Semua fitur relevan untuk setiap smartphone digabungkan menjadi satu string teks (dokumen).

2.  **Vectorization & Model Building (`build.py`)**
    * Menggunakan **TF-IDF Vectorizer** dari Scikit-learn, setiap string fitur smartphone diubah menjadi vektor numerik. Proses ini menghasilkan matriks TF-IDF yang merepresentasikan bobot setiap fitur untuk setiap smartphone.
    * Objek `TfidfVectorizer` dan matriks TF-IDF yang telah dilatih kemudian disimpan sebagai file `vectorizer.pkl` dan `tfidf_matrix.pkl`.

3.  **Perhitungan Kemiripan (`recommend.py`)**
    * Ketika pengguna mengirimkan preferensi mereka melalui form, input tersebut digabungkan menjadi sebuah string.
    * String input pengguna diubah menjadi vektor TF-IDF menggunakan `vectorizer` yang telah disimpan sebelumnya.
    * **Cosine Similarity** dihitung antara vektor input pengguna dan semua vektor smartphone dalam matriks TF-IDF. Skor kemiripan (antara 0 dan 1) menunjukkan seberapa "mirip" setiap smartphone dengan preferensi pengguna.

4.  **Penyajian Hasil (`routes.py`)**
    * Aplikasi Flask mengambil 10 smartphone dengan skor Cosine Similarity tertinggi dan menampilkannya secara berurutan di halaman hasil rekomendasi.

---

## 🛠️ Teknologi yang Digunakan

* **Backend:** Python, Flask
* **Data Processing:** Pandas
* **Machine Learning:** Scikit-learn
* **Frontend:** HTML, CSS

---

## 📂 Struktur Proyek

```
.
├── app/
│   ├── data/
│   │   ├── smartphones_processed.json
│   │   ├── tfidf_matrix.pkl
│   │   └── vectorizer.pkl
│   ├── templates/
│   │   ├── form.html
│   │   ├── index.html
│   │   └── recommendations.html
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── recommend.py
│   └── routes.py
├── build.py
├── main.py
├── Procfile
├── README.md
├── requirements.txt
└── smartphones.csv
```

---

## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

1.  **Clone Repositori**
    ```bash
    git clone <URL_REPOSITORI_ANDA>
    cd <NAMA_DIREKTORI_PROYEK>
    ```

2.  **Buat dan Aktifkan Virtual Environment (Direkomendasikan)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Build Model dan Data**
    Jalankan skrip `build.py` untuk memproses dataset dan membuat file model yang diperlukan.
    ```bash
    python build.py
    ```
    Pastikan file `vectorizer.pkl`, `tfidf_matrix.pkl`, dan `smartphones_processed.json` berhasil dibuat di dalam direktori `app/data/`.

5.  **Jalankan Aplikasi Flask**
    ```bash
    python main.py
    ```

6.  **Buka di Browser**
    Buka browser Anda dan kunjungi `http://127.0.0.1:4000/`
