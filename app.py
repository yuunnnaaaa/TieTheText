import streamlit as st
import requests

# Konfigurasi halaman web
st.set_page_config(page_title="FloraBot Dashboard", page_icon="💐", layout="centered")

# --- KUSTOMISASI CSS UNTUK TEMA CERIA ---
st.markdown("""
<style>
    /* Mengubah warna latar belakang aplikasi menjadi pastel cerah */
    .stApp {
        background-color: #FFF5F7; /* Pink sangat muda */
    }
    
    /* Memastikan teks utama berwarna gelap agar terbaca di latar terang */
    [data-testid="stMarkdownContainer"], 
    [data-testid="stCaptionContainer"], 
    .stTextArea label,
    [data-testid="stText"] {
        color: #4A4A4A !important;
    }
    
    /* Memastikan teks di dalam text area dan placeholder terbaca */
    textarea {
        color: #4A4A4A !important;
    }
    
    textarea::placeholder {
        color: #B0B0B0 !important;
    }

    /* Styling untuk tombol utama (Warna Rose/Pink Ceria) */
    div.stButton > button:first-child {
        background-color: #FF6B81;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(255, 107, 129, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #FF4757;
        box-shadow: 0 6px 8px rgba(255, 71, 87, 0.4);
        transform: translateY(-2px);
        color: white;
    }

    /* Styling area teks agar lebih manis */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #FFD1DC;
        background-color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .stTextArea textarea:focus {
        border-color: #FF6B81;
        box-shadow: 0 0 5px rgba(255, 107, 129, 0.5);
    }
    
    /* Styling kotak hasil/sukses */
    div[data-testid="stAlert"] {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.components.v1.html(
    """
    <meta name="dicoding:email" content="yunitaekasalsabila2863@gmail.com">
    """,
    height=0,
)

# --- CUSTOM HEADER DENGAN HTML ---
st.markdown("""
    <div style="text-align: center; padding: 25px 20px; background: linear-gradient(135deg, #FFE6EA 0%, #FFF0F5 100%); border-radius: 20px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #FFE4E1;">
        <h1 style="color: #D81B60; margin-bottom: 5px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">💐 FloraBot</h1>
        <h3 style="color: #F06292; margin-top: 0px; font-weight: 500;">Smart Order Handover</h3>
        <p style="color: #A9A9A9; font-size: 13px; font-style: italic; margin-top: -10px; margin-bottom: 15px;">An AI Bouquet Assistant</p>
        <p style="color: #696969; font-size: 15px; margin-bottom: 0;">Asisten AI untuk otomatisasi ringkasan pesanan dan manajemen UMKM Florist.</p>
    </div>
""", unsafe_allow_html=True)


# Input Teks Chat Pelanggan
st.markdown("### 📥 Masukkan Chat Pelanggan")
chat_input = st.text_area(
    "Tempel (paste) chat acak atau diskusi pesanan dari pelanggan di sini:",
    placeholder="Contoh: Pagi min, mau pesen hand bouquet mawar putih buat besok siang namanya Rian kirim ke Gedung Balai Kartini...",
    height=150,
    label_visibility="collapsed" # Menyembunyikan label bawaan agar lebih rapi
)
st.caption("Tempel (paste) chat acak atau diskusi pesanan dari pelanggan di atas.")

st.markdown("<br>", unsafe_allow_html=True) # Spasi

# Tombol Proses AI
if st.button("✨ Proses Pesanan dengan AI", type="primary"):
    if chat_input.strip() == "":
        st.warning("🌻 Mohon masukkan teks chat pelanggan terlebih dahulu ya!")
    else:
        with st.spinner("🌸 FloraBot sedang merangkai data pesananmu..."):
            try:
                # Backend URL
                backend_url = "http://127.0.0.1:8000/api/v1/extract-order"
                
                response = requests.post(backend_url, json={"chat_text": chat_input})
                
                if response.status_code == 200:
                    data = response.json()
                    summary = data["summary"]
                    
                    st.success("🎉 Yay! Pesanan Berhasil Diekstrak!")
                    
                    # Tampilan Data Terstruktur dalam Kolom (Diberi gaya Card)
                    st.markdown("""
                    <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #FF6B81; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
                        <h4 style="color: #D81B60; margin-top: 0;">📝 Ringkasan Pesanan</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**👤 Nama Pemesan:**\n\n{summary['nama_pemesan']}")
                        st.info(f"**💐 Jenis Rangkaian:**\n\n{summary['jenis_rangkaian']}")
                    with col2:
                        st.info(f"**📍 Alamat Pengiriman:**\n\n{summary['alamat_pengiriman']}")
                        st.info(f"**💰 Total Harga:**\n\n{summary['total_harga']}")
                    
                    st.warning(f"**💌 Isi Kartu Ucapan:**\n\n_{summary['isi_ucapan'] or '-'}_")
                    
                    st.markdown("---")
                    
                    # Bagian Handover / Penerusan Pesanan
                    st.markdown("### 🚀 Serah Terima Pesanan (Handover)")
                    
                    # Menampilkan teks siap cetak
                    st.text_area("📋 Teks Siap Cetak / Copy-Paste:", value=data["printable_text"], height=180)
                    
                    # Tombol Kirim WhatsApp Otomatis (Dibuat mirip tombol HTML)
                    wa_html = f"""
                    <a href="{data['whatsapp_link']}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #25D366; color: white; padding: 12px 20px; text-align: center; border-radius: 15px; font-weight: bold; box-shadow: 0 4px 6px rgba(37, 211, 102, 0.3);">
                            💬 Kirim Notifikasi ke WhatsApp Pemilik Toko
                        </div>
                    </a>
                    """
                    st.markdown(wa_html, unsafe_allow_html=True)
                    
                else:
                    st.error("🥀 Gagal terhubung ke sistem backend. Pastikan server FastAPI menyala.")
            except Exception as e:
                st.error(f"🥀 Terjadi kesalahan teknis: {str(e)}")