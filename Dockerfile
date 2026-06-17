# Gunakan Python 3.9
FROM python:3.9

# Folder kerja
WORKDIR /code

# Copy requirements dan install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy semua file lain (app.py, model, dll)
COPY . .

# Buat folder cache (untuk menghindari error permission matplotlib/font)
RUN mkdir -p /code/cache
RUN chmod 777 /code/cache
ENV MPLCONFIGDIR=/code/cache

# --- BAGIAN PENTING ---
# Gunicorn harus bind ke 0.0.0.0:7860 (Bukan 5000!)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]