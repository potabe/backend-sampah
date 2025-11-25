import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from PIL import Image

app = Flask(__name__)

# --- KONFIGURASI ---
WEIGHTS_FILENAME = 'hanya_bobot.weights.h5'  # Pastikan nama file sesuai
model = None

# --- FUNGSI MEMBANGUN MODEL ---
# Kita copy-paste arsitektur persis seperti di Colab
def build_model():
    print("Membangun arsitektur MobileNetV2...")
    
    # 1. Base Model (MobileNetV2)
    base_model = MobileNetV2(input_shape=(160, 160, 3),
                             include_top=False,
                             weights=None) # Kita set None karena akan load dari file lokal
    
    # 2. Susun Layer (Harus SAMA PERSIS dengan Colab)
    new_model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        # Pastikan jumlah unit output SAMA dengan jumlah kelas (biasanya 6)
        layers.Dense(6, activation='softmax') 
    ])
    
    return new_model

# --- LOAD MODEL SAAT STARTUP ---
print("="*50)
if os.path.exists(WEIGHTS_FILENAME):
    try:
        # 1. Bangun kerangkanya dulu
        model = build_model()
        
        # 2. Isi dengan bobot dari Colab
        print(f"Memuat bobot dari {WEIGHTS_FILENAME}...")
        model.load_weights(WEIGHTS_FILENAME)
        
        print("✅ SUKSES: Model siap digunakan!")
    except Exception as e:
        print(f"❌ ERROR: Gagal memuat bobot. Pesan error: {e}")
        model = None
else:
    print(f"❌ ERROR FATAL: File '{WEIGHTS_FILENAME}' tidak ditemukan!")
print("="*50)

# Daftar Label
class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def prepare_image(img):
    img = img.resize((160, 160))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model belum siap'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file'}), 400
    
    file = request.files['file']
    
    try:
        img = Image.open(file.stream)
        processed_img = prepare_image(img)
        
        prediction = model.predict(processed_img)
        index_max = np.argmax(prediction)
        
        label_result = class_names[index_max]
        confidence = float(prediction[0][index_max]) * 100
        
        return jsonify({
            'label': label_result,
            'confidence': f"{confidence:.2f}%",
            'message': 'Klasifikasi berhasil'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cloud akan memberi PORT lewat environment variable
    # Jika tidak ada (di laptop), default ke 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)