import re

nilaiKonversi = 189
brands = ['Samsung', 'Xiaomi', 'Oppo', 'Vivo', 'Realme', 'Apple', 'Asus', 'Sony', 'Huawei', 'Nokia', 'Google Pixel']
brands_p = ['Snapdragon', 'Exynos', 'Dimensity', 'Bionic', 'Unisoc', 'Kirin', 'Helio']

def konversiRupiah(hargaIndia):
    if isinstance(hargaIndia, str):
        hapusSimbol = hargaIndia.replace('₹', '').replace(',', '')
        try:
            rupee = int(hapusSimbol)
            return rupee * nilaiKonversi
        except:
            return None
    return None

def ubahString(rupiah):
    if rupiah is None:
        return None
    try:
        return f"Rp {int(rupiah):,}"
    except:
        return None

def extract_merek(model_name):
    for merek in brands:
        if merek.lower() in str(model_name).lower():
            return merek
    return None

def extract_merek_processor(merek_name):
    for merek in brands_p:
        if merek.lower() in str(merek_name).lower():
            return merek
    return None

def getDukunganDualSim(x):
    if 'Dual Sim' in x.get('sim', ''):
        return 'Support Dual SIM'
    else:
        return 'Tidak Support'

def getDukungan5G(x):
    if '5G' in x.get('sim', ''):
        return 'Support 5G'
    else:
        return 'Tidak Support'

def getDukunganNFC(x):
    if 'NFC' in x.get('sim', ''):
        return 'Support NFC'
    else:
        return 'Tidak Support'

def getRentangBaterai(baterai):
    match = re.search(r'(\d+\.?\d*)', str(baterai))
    if match:
        kapasitasBaterai = float(match.group(1))
        if kapasitasBaterai < 3000:
            return 'Kurang 3000 mAh'
        elif 3001 <= kapasitasBaterai <= 5000:
            return '3000-5000 mAh'
        elif kapasitasBaterai > 5000:
            return 'Lebih dari 5000 mAh'
    return None

def getRentangLayar(layar):
    match = re.search(r'(\d+\.?\d*)', str(layar))
    if match:
        ukuranLayar = float(match.group(1))
        if ukuranLayar < 5:
            return 'Kurang dari 5 Inch'
        elif 5 <= ukuranLayar <= 6:
            return '5-6 Inch'
        elif ukuranLayar > 6:
            return 'Lebih dari 6 Inch'
    return None

def getRentangKamera(camera):
    match = re.search(r'(\d+)', str(camera))
    if match:
        resolusiKamera = int(match.group(1))
        if resolusiKamera < 30:
            return 'Kurang dari 30 MP'
        elif 31 <= resolusiKamera <= 60:
            return '30-60 MP'
        elif 61 <= resolusiKamera <= 90:
            return '60-90 MP'
        elif resolusiKamera > 90:
            return 'Lebih dari 90 MP'
    return None

def getDukunganMemoryCard(mCard):
    if isinstance(mCard, str):
        if 'Memory Card Not Supported' in mCard:
            return 'Tidak Support'
        elif 'Memory Card Supported' in mCard or 'Memory Card' in mCard:
            return 'Support Memory Card'
    return None

def getRentangHarga(harga):
    if harga < 2000000:
        return 'Kurang dari 2.000.000 Rupiah'
    elif 2000000 <= harga < 5000000:
        return '2.000.000-5.000.000 Rupiah'
    elif 5000000 <= harga < 8000000:
        return '5.000.000-8.000.000 Rupiah'
    elif harga >= 8000000:
        return 'Lebih dari 8.000.000'
    return None


def preprocess_data(df):
    # Konversi harga
    df['harga'] = df['price'].apply(konversiRupiah)
    df['harga(string)'] = df['harga'].apply(ubahString)

    # Merek
    df['merek'] = df['model'].apply(extract_merek)

    # Processor
    df['merekProcessor'] = df['processor'].str.split().str[:1].str.join(' ')
    df['merekProcessor'] = df['merekProcessor'].apply(extract_merek_processor)

    # RAM dan ROM
    df['RAM'] = df['ram'].str.split(',').str[0].str.replace(' RAM', '').str.replace(' inbuilt', '').str.strip()
    df['ROM'] = df['ram'].str.split(',').str[1].str.replace(' inbuilt', '').str.strip()

    # Baterai, layar, kamera
    df['baterai'] = df['battery'].str.split().str[:2].str.join(' ')
    df['layar'] = df['display'].str.split(',').str[:1].str.join(' ')
    df['kamera'] = df['camera'].str.split().str[:2].str.join(' ')

    # Dukungan SIM, 5G, NFC
    df['dukunganDualSim'] = df.apply(getDukunganDualSim, axis=1)
    df['dukungan5G'] = df.apply(getDukungan5G, axis=1)
    df['dukunganNFC'] = df.apply(getDukunganNFC, axis=1)

    # Rentang baterai, layar, kamera
    df['rentangBaterai'] = df['baterai'].apply(getRentangBaterai)
    df['rentangLayar'] = df['display'].apply(getRentangLayar)
    df['rentangKamera'] = df['kamera'].apply(getRentangKamera)

    # Memory Card
    df['dukunganMemoryCard'] = df['card'].apply(getDukunganMemoryCard)

    # Rentang Harga
    df['rentangHarga'] = df['harga'].apply(getRentangHarga)

    # Drop data yang masih ada None
    df = df.dropna()

    # Gabungkan fitur untuk rekomendasi
    featuresUsed = ['merek', 'dukunganDualSim', 'dukungan5G', 'dukunganNFC',
                    'merekProcessor', 'RAM', 'ROM', 'rentangBaterai', 'rentangLayar',
                    'rentangKamera', 'dukunganMemoryCard', 'rentangHarga']

    df['features'] = df[featuresUsed].astype(str).agg(' '.join, axis=1)

    return df
