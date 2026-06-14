import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from skema import OrderSummary

# Load environment variables dari file .env
load_dotenv()

# Inisialisasi client Gemini menggunakan SDK terbaru 2026
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_order_from_chat(chat_text: str) -> OrderSummary:
    """
    Fungsi untuk mengekstrak teks chat acak dari pelanggan florist
    menjadi data pesanan terstruktur menggunakan Gemini AI.
    """
    
    prompt = f"""
    Kamu adalah asisten kasir pintar untuk toko bunga (florist).
    Tugasmu adalah menganalisis chat pesanan dari pelanggan berikut dan mengekstrak informasi penting ke dalam struktur data yang diminta.
    
    Chat Pelanggan:
    "{chat_text}"
    """
    
    # Memanggil model Gemini terbaru (gemini-2.5-flash cocok untuk kecepatan & task ekstraksi)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            # Bagian ini memaksa Gemini mengembalikan format JSON sesuai dengan skema Pydantic kita
            response_mime_type="application/json",
            response_schema=OrderSummary,
            temperature=0.1 # Suhu rendah agar AI konsisten dan tidak "berfantasi"
        ),
    )
    
    # Mengembalikan data yang sudah divalidasi langsung oleh Pydantic schema
    return OrderSummary.model_validate_json(response.text)