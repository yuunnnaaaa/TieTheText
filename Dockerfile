FROM python:3.10-slim

# Tentukan folder kerja di dalam server sandbox cloud
WORKDIR /app

# Copy daftar library dan install di server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code proyekmu ke dalam server
COPY . .

# Buka jalur akses port 8000 untuk FastAPI
EXPOSE 8000

# Perintah untuk menghidupkan server FastAPI di Render secara otomatis
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]