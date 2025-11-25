import requests

# URL server kita (localhost)
url = 'http://127.0.0.1:5000/predict'

# Ganti dengan nama salah satu file gambar sampah yang Anda punya di laptop
path_gambar = 'glass1.jpg' 

# Pastikan Anda punya file gambar dummy untuk dites
if not os.path.exists(path_gambar):
    print(f"Error: File {path_gambar} tidak ditemukan. Tolong taruh 1 gambar sampah di folder ini untuk tes.")
else:
    files = {'file': open(path_gambar, 'rb')}
    print(f"Mengirim gambar {path_gambar} ke server...")
    
    try:
        response = requests.post(url, files=files)
        print("Respon Server:")
        print(response.json())
    except Exception as e:
        print(f"Gagal connect ke server: {e}")