from pydantic import BaseModel, Field
from typing import Optional
# Tambahkan import urlquote di bagian atas file
from urllib.parse import quote as urlquote
from pydantic import BaseModel, Field
from typing import Optional

class CustomerChat(BaseModel):
    chat_text: str = Field(..., description="Teks percakapan utuh atau pesanan acak dari pelanggan florist")

class OrderSummary(BaseModel):
    nama_pemesan: str = Field(..., description="Nama pelanggan atau penerima bunga")
    alamat_pengiriman: str = Field(..., description="Alamat lengkap tujuan pengiriman bunga")
    jenis_rangkaian: str = Field(..., description="Detail jenis bunga atau rangkaian yang dipesan")
    isi_ucapan: Optional[str] = Field(None, description="Isi kartu ucapan, berikan string kosong jika tidak ada")
    total_harga: str = Field(..., description="Estimasi atau total harga yang disebutkan dalam chat")


class OrderHandoverResponse(BaseModel):
    summary: OrderSummary
    whatsapp_link: str = Field(..., description="Link WhatsApp otomatis untuk meneruskan pesanan ke pemilik toko")
    printable_text: str = Field(..., description="Format teks rapi siap copy-paste untuk tim produksi/florist")