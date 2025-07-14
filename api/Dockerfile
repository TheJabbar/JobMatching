# Base image Python
FROM python:3.10-slim

# Set working directory di container
WORKDIR /app

# Copy requirements file dan install dependencies
COPY api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh isi folder backend ke dalam /app
COPY api/ /app

# Set environment variable jika perlu
ENV PYTHONPATH=/app

# Expose port sesuai aplikasi
EXPOSE 8000

# Perintah menjalankan aplikasi (contoh menggunakan uvicorn)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "3600", "--log-level", "info"]


