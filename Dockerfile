FROM python:3.10-slim

# Tentukan folder kerja di dalam server sandbox cloud
WORKDIR /app

# Copy daftar library dan install di server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code proyekmu ke dalam server
COPY . .

# PENTING: Ganti ke port 7860 untuk Hugging Face Spaces
EXPOSE 7860

# Jalankan Uvicorn dengan port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]