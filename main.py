from fastapi import FastAPI, HTTPException
from skema import CustomerChat, OrderHandoverResponse
from ai_service import extract_order_from_chat
from urllib.parse import quote as urlquote
from fastapi.middleware.cors import CORSMiddleware

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="TieTheText MVP - Smart Order Handover",
    description="Backend AI untuk otomatisasi ekstraksi pesanan UMKM Florist - IDCamp 2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua domain (termasuk Streamlit Cloud)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nomor WhatsApp Pemilik Toko (Ganti dengan nomor tujuan UMKM, gunakan kode negara tanpa '+')
OWNER_PHONE = "6287738726533" 

@app.get("/")
def read_root():
    return {"status": "success", "message": "Backend tiethetext MVP Aktif!"}

@app.post("/api/v1/extract-order", response_model=OrderHandoverResponse)
def extract_order(payload: CustomerChat):
    try:
        # 1. Ekstrak data menggunakan Gemini AI
        summary_result = extract_order_from_chat(payload.chat_text)
        
        # 2. Buat format teks cetak yang rapi untuk Florist
        printable_text = (
            f"📌 *PESANAN BARU FLORA BOT*\n"
            f"───────────────────\n"
            f"👤 Nama Pemesan: {summary_result.nama_pemesan}\n"
            f"📍 Alamat Kirim: {summary_result.alamat_pengiriman}\n"
            f"💐 Rangkaian: {summary_result.jenis_rangkaian}\n"
            f"💌 Isi Ucapan: \"{summary_result.isi_ucapan or '-'}\"\n"
            f"💰 Total Harga: {summary_result.total_harga}\n"
            f"───────────────────\n"
            f"⚙️ *Status: Siap Dirangkai*"
        )
        
        # 3. Generate WhatsApp Click-to-Chat Link
        encoded_text = urlquote(printable_text)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={OWNER_PHONE}&text={encoded_text}"
        
        # 4. Kembalikan respon lengkap sesuai standar MVP
        return OrderHandoverResponse(
            summary=summary_result,
            whatsapp_link=whatsapp_url,
            printable_text=printable_text
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses pesanan: {str(e)}")