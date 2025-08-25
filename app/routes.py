from flask import Blueprint, render_template, request, current_app
import re
from .recommend import recommend
import json

main_app = Blueprint('main', __name__)

@main_app.route("/")
def index():
    return render_template('index.html')

@main_app.route('/form', methods=['GET'])
def form():
    df = current_app.config['DATAFRAME']

    # Buat pemetaan Merek -> Chipset
    merek_chipset_map = df.groupby('merek')['merekProcessor'].unique().apply(list).to_dict()

    # 2. Buat daftar SEMUA prosesor unik untuk ditampilkan saat tidak ada merek yang dipilih
    all_chipsets = sorted(df['merekProcessor'].unique())

    brand_options = sorted(df['merek'].unique())
    brand_options.insert(0, '') # Menambahkan string kosong
    dualsim_options = sorted(df['dukunganDualSim'].unique())
    dualsim_options.insert(0, '') # Menambahkan string kosong
    jaringan_options = sorted(df['dukungan5G'].unique())
    jaringan_options.insert(0, '') # Menambahkan string kosong
    nfc_options = sorted(df['dukunganNFC'].unique())
    nfc_options.insert(0, '') # Menambahkan string kosong
    display_options_list = sorted(df['rentangLayar'].unique(), key=lambda x: [float(i) for i in re.findall(r'\d+', x)])
    display_options_list.insert(0, '') # Menambahkan string kosong
    chipset_options = sorted(df['merekProcessor'].unique())
    chipset_options.insert(0, '') # Menambahkan string kosong
    ram_options = sorted(df['RAM'].unique(), key=lambda x: int(''.join(filter(str.isdigit, x))))
    ram_options.insert(0, '') # Menambahkan string kosong
    rom_options = sorted(df['ROM'].unique(), key=lambda x: int(''.join(filter(str.isdigit, x))))
    rom_options.insert(0, '') # Menambahkan string kosong
    battery_options = sorted(df['rentangBaterai'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    battery_options.insert(0, '') # Menambahkan string kosong
    camera_options = sorted(df['rentangKamera'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    camera_options.insert(0, '') # Menambahkan string kosong
    card_options = sorted(df['dukunganMemoryCard'].unique())
    card_options.insert(0, '') # Menambahkan string kosong
    harga_options = sorted(df['rentangHarga'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    harga_options.insert(0, '') # Menambahkan string kosong

    return render_template('form.html',
        mereks=brand_options,
        dualsims=dualsim_options,
        jaringans=jaringan_options,
        nfcs=nfc_options,
        displays=display_options_list,
        chipsets=chipset_options,
        rams=ram_options,
        roms=rom_options,
        batteries=battery_options,
        cameras=camera_options,
        cards=card_options,
        hargas=harga_options,
        merek_chipset_map_json=json.dumps(merek_chipset_map), # Kirim sebagai JSON string
        all_chipsets_json=json.dumps(all_chipsets)
    )

@main_app.route('/recommend', methods=['POST'])
def do_recommend():
    df = current_app.config['DATAFRAME']
    vectorizer = current_app.config['VECTORIZER']
    tfidf_matrix = current_app.config['TFIDF_MATRIX']

    selected_brand = request.form['merek']
    selected_dualsim = request.form['dukunganDualSim']
    selected_jaringan = request.form['dukungan5G']
    selected_nfc = request.form['dukunganNFC']
    selected_display = request.form['rentangLayar']
    selected_chipset = request.form['merekProcessor']
    selected_ram = request.form['RAM']
    selected_rom = request.form['ROM']
    selected_battery = request.form['rentangBaterai']
    selected_camera = request.form['rentangKamera']
    selected_card = request.form['dukunganMemoryCard']
    selected_harga = request.form['rentangHarga']
    
    user_keywords_raw = [
        selected_brand,
        selected_dualsim,
        selected_jaringan,
        selected_nfc,
        selected_display,
        selected_chipset,
        selected_ram,
        selected_rom,
        selected_battery,
        selected_camera,
        selected_card,
        selected_harga
    ]

    # Filter untuk membuang nilai kosong yang berarti pengguna mengabaikan kriteria itu
    user_keywords = [keyword for keyword in user_keywords_raw if keyword]

    # Panggil fungsi recommend dengan argumen baru
    recommendations = recommend(df, vectorizer, tfidf_matrix, user_keywords)

    return render_template('recommendations.html', user_keywords=user_keywords_raw, recommendations=recommendations)