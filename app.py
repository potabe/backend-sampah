import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)

# Nama file model baru
MODEL_FILE = 'model_mobilenet_auto.h5'
model = None

# Load Model saat Start
if os.path.exists(MODEL_FILE):
    try:
        print("Memuat model...")
        model = load_model(MODEL_FILE, compile=False)
        print("✅ Model Berhasil Dimuat!")
    except Exception as e:
        print(f"❌ Error Load Model: {e}")
else:
    print("❌ File model tidak ditemukan!")

# Label (Sesuaikan urutan abjad folder dataset Anda)
class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def prepare_image(img):
    # 1. Pastikan RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # 2. Resize harus SAMA PERSIS dengan Training (224x224)
    img = img.resize((224, 224))
    
    # 3. Ubah ke Array
    x = image.img_to_array(img)
    
    # 4. Normalisasi harus SAMA PERSIS dengan Training (1/255)
    x = x / 255.0
    
    # 5. Tambah dimensi batch
    x = np.expand_dims(x, axis=0)
    return x

@app.route('/', methods=['GET'])
def index():
    return "Server Reset OK"

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model rusak/hilang'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    try:
        file = request.files['file']
        img = Image.open(file.stream)
        
        # Proses
        processed_img = prepare_image(img)
        prediction = model.predict(processed_img)
        
        # Ambil hasil
        idx = np.argmax(prediction)
        label = class_names[idx]
        confidence = float(prediction[0][idx]) * 100
        
        # Debugging di Log
        print(f"Prediksi: {label} - {confidence}%")
        print(f"Raw: {prediction}")

        return jsonify({'label': label, 'confidence': f"{confidence:.2f}%"})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)