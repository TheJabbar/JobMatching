# Gunakan base image Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin file requirements dan install dependensi
COPY ui/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh isi folder frontend ke image
COPY  ui/ /app

EXPOSE 8501

# Jalankan Streamlit saat container dimulai
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]