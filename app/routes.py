from flask import Blueprint, render_template, request, current_app
import re
from .recommend import recommend

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template('index.html')


@main_bp.route('/form', methods=['GET'])
def form():
    df = current_app.config['DATAFRAME']

    brand_options = sorted(df['merek'].unique())
    dualsim_options = sorted(df['dukunganDualSim'].unique())
    jaringan_options = sorted(df['dukungan5G'].unique())
    nfc_options = sorted(df['dukunganNFC'].unique())
    display_options_list = sorted(df['rentangLayar'].unique(), key=lambda x: [float(i) for i in re.findall(r'\d+', x)])
    chipset_options = sorted(df['merekProcessor'].unique())
    ram_options = sorted(df['RAM'].unique(), key=lambda x: int(''.join(filter(str.isdigit, x))))
    rom_options = sorted(df['ROM'].unique(), key=lambda x: int(''.join(filter(str.isdigit, x))))
    battery_options = sorted(df['rentangBaterai'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    camera_options = sorted(df['rentangKamera'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    card_options = sorted(df['dukunganMemoryCard'].unique())
    harga_options = sorted(df['rentangHarga'].unique(), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])

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
        hargas=harga_options
    )


@main_bp.route('/recommend', methods=['POST'])
def do_recommend():
    df = current_app.config['DATAFRAME']

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

    user_keywords = [
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

    recommendations = recommend(df, user_keywords)

    return render_template('recommendations.html', user_keywords=user_keywords, recommendations=recommendations)
