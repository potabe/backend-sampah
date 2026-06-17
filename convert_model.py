#!/usr/bin/env python3
"""
EcoSort - Model Conversion Script
===================================
Script ini mengkonversi model Keras (.h5) ke format TensorFlow.js
agar bisa dijalankan langsung di browser tanpa backend.

CARA PENGGUNAAN:
1. Install dependencies:
   pip install tensorflowjs tensorflow

2. Jalankan script ini dari folder backend_sampah:
   python convert_model.py

3. Setelah selesai, copy folder 'tfjs_model/' ke:
   ecosort-web/public/model/

CATATAN:
- File model harus bernama 'model_mobilenet_auto.h5'
- Output akan ada di folder 'tfjs_model/'
- File yang dihasilkan: model.json + group1-shard*.bin
"""

import os
import subprocess
import sys

MODEL_H5 = "model_mobilenet_auto.h5"
OUTPUT_DIR = "tfjs_model"

def check_dependencies():
    """Cek apakah tensorflowjs sudah terinstall"""
    try:
        import tensorflowjs
        print(f"✅ tensorflowjs versi {tensorflowjs.__version__} ditemukan")
        return True
    except ImportError:
        print("❌ tensorflowjs belum terinstall")
        print("   Jalankan: pip install tensorflowjs tensorflow")
        return False

def convert_model():
    """Konversi model .h5 ke format TensorFlow.js"""
    
    # 1. Cek file model ada
    if not os.path.exists(MODEL_H5):
        print(f"❌ File model '{MODEL_H5}' tidak ditemukan!")
        print(f"   Pastikan script ini dijalankan dari folder yang sama dengan {MODEL_H5}")
        sys.exit(1)
    
    print(f"✅ File model ditemukan: {MODEL_H5} ({os.path.getsize(MODEL_H5) / 1024 / 1024:.1f} MB)")
    
    # 2. Buat output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 3. Jalankan converter
    print(f"\n🔄 Mengkonversi model ke TensorFlow.js format...")
    print(f"   Input:  {MODEL_H5}")
    print(f"   Output: {OUTPUT_DIR}/\n")
    
    cmd = [
        "tensorflowjs_converter",
        "--input_format=keras",
        "--output_format=tfjs_layers_model",
        "--quantization_bytes=2",   # Kompres bobot model (float32 -> int16, ukuran ~50% lebih kecil)
        MODEL_H5,
        OUTPUT_DIR
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # 4. Hitung ukuran output
        total_size = 0
        files = []
        for f in os.listdir(OUTPUT_DIR):
            path = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(path)
            total_size += size
            files.append((f, size))
        
        print(f"\n✅ Konversi berhasil!")
        print(f"\n📁 File yang dihasilkan di '{OUTPUT_DIR}/':")
        for name, size in sorted(files):
            print(f"   {name:<40} ({size / 1024:.1f} KB)")
        print(f"\n   Total ukuran: {total_size / 1024 / 1024:.2f} MB")
        
        print(f"\n📋 LANGKAH SELANJUTNYA:")
        print(f"   1. Copy seluruh folder '{OUTPUT_DIR}/' ke 'ecosort-web/public/model/'")
        print(f"   2. Struktur akhir: ecosort-web/public/model/model.json")
        print(f"   3. Jalankan 'npm run dev' di folder ecosort-web")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Konversi gagal!")
        print(f"   Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Command 'tensorflowjs_converter' tidak ditemukan!")
        print("   Pastikan tensorflowjs sudah terinstall: pip install tensorflowjs")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 55)
    print("  EcoSort — Model Converter (Keras → TensorFlow.js)")
    print("=" * 55)
    print()
    
    if not check_dependencies():
        sys.exit(1)
    
    convert_model()
