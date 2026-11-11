"""
AI FAQ Chatbot - Klinik
Versi: 2.0.0 - Production Safe

Keamanan:
- TIDAK menyimpan nama / NIK / No. BPJS / data pasien
- TIDAK memanggil API eksternal, semua jawaban dari FAQ lokal
- Input dibatasi panjang & dibersihkan
- TIDAK ada eval(), exec(), atau secret di kode

Cara jalanin:
  pip install -r requirements.txt
  python app.py
  Buka: http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, render_template_string
import re
import html

app = Flask(__name__)

# ================= KONFIGURASI AMAN =================
MAX_PERTANYAAN_PANJANG = 500
MAX_PERTANYAAN_PER_MENIT = 30  # simple rate-limit in-memory

# FAQ lokal - data sintetis, bukan data pasien asli
FAQ = [
    {
        "keywords": ["jam", "buka", "tutup", "operasional", "layanan"],
        "jawaban": "Jam operasional klinik: Senin-Jumat 08.00-16.00, Sabtu 08.00-12.00, Minggu libur. Untuk keadaan darurat, silakan ke IGD RS terdekat."
    },
    {
        "keywords": ["biaya", "harga", "tarif", "bayar", "bpjs", "jkn"],
        "jawaban": "Biaya konsultasi umum mulai Rp 50.000. Peserta JKN/BPJS wajib membawa kartu JKN aktif dan KTP. Biaya pasti tergantung tindakan dokter, silakan konfirmasi ke loket."
    },
    {
        "keywords": ["daftar", "registrasi", "antri", "antrean", "booking"],
        "jawaban": "Pendaftaran: 1) Datang ke loket dengan KTP/Kartu JKN, 2) Ambil nomor antrean, 3) Tunggu dipanggil. Pendaftaran online belum tersedia, mohon datang langsung."
    },
    {
        "keywords": ["dokter", "jadwal", "praktek", "praktik"],
        "jawaban": "Jadwal dokter berubah sewaktu-waktu. Silakan hubungi loket klinik untuk jadwal hari ini. Kami tidak membagikan nomor pribadi dokter."
    },
    {
        "keywords": ["obat", "resep", "apotek", "farmasi"],
        "jawaban": "Obat dapat diambil di apotek klinik dengan membawa resep dokter. Jangan minum obat tanpa resep dokter. Jika ada alergi obat, sampaikan ke dokter sebelum diperiksa."
    },
    {
        "keywords": ["halo", "hai", "selamat", "pagi", "siang", "malam"],
        "jawaban": "Halo! Saya asisten FAQ klinik. Silakan tanya tentang jam buka, biaya, cara daftar, jadwal dokter, atau obat. Contoh: 'Jam buka klinik jam berapa?'"
    },
]

JAWABAN_DEFAULT = (
    "Maaf, saya belum mengerti pertanyaan itu. "
    "Saya hanya bisa menjawab tentang: jam buka, biaya/JKN, cara daftar, jadwal dokter, dan obat. "
    "Untuk keluhan medis, silakan periksa langsung ke dokter. Chat ini bukan pengganti diagnosis dokter."
)

# Simple rate-limit in-memory (untuk demo, bukan produksi skala besar)
_request_counts = {}

def bersihkan_input(teks: str) -> str:
    """Bersihkan input: potong, batasi panjang, escape HTML."""
    if not isinstance(teks, str):
        return ""
    teks = teks.strip()[:MAX_PERTANYAAN_PANJANG]
    teks = html.escape(teks)
    return teks

def normalisasi(teks: str) -> str:
    teks = teks.lower()
    teks = re.sub(r"[^a-z0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks).strip()
    return teks

def cari_jawaban(pertanyaan: str) -> str:
    q = normalisasi(pertanyaan)
    if not q:
        return JAWABAN_DEFAULT
    skor_terbaik = 0
    jawaban_terbaik = JAWABAN_DEFAULT
    for item in FAQ:
        skor = sum(1 for kw in item["keywords"] if kw in q)
        if skor > skor_terbaik:
            skor_terbaik = skor
            jawaban_terbaik = item["jawaban"]
    return jawaban_terbaik

# ================= ROUTES =================

HTML_PAGE = """
<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI FAQ Chatbot - Klinik</title>
<style>body{font-family:system-ui;max-width:640px;margin:32px auto;padding:0 16px}
#chat{border:1px solid #ddd;border-radius:12px;padding:16px;min-height:200px}
.msg{margin:8px 0}.user{text-align:right}.bot{color:#0b5e3b}
input{width:78%;padding:10px}button{padding:10px 16px}
small{color:#666}</style></head>
<body>
<h2>AI FAQ Chatbot - Klinik</h2>
<p><small>Demo edukasi. Bukan pengganti diagnosis dokter. Jangan kirim NIK / No. BPJS / nama lengkap.</small></p>
<div id="chat"><div class="msg bot">Halo! Tanya tentang jam buka, biaya, cara daftar, jadwal dokter, atau obat.</div></div>
<br><input id="q" placeholder="Tulis pertanyaan... contoh: jam buka klinik?" maxlength="500">
<button onclick="kirim()">Kirim</button>
<script>
async function kirim(){
  const inp=document.getElementById('q'); const t=inp.value.trim(); if(!t) return;
  const chat=document.getElementById('chat');
  chat.innerHTML+='<div class="msg user">'+t.replace(/</g,'&lt;')+'</div>'; inp.value='';
  const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pertanyaan:t})});
  const d=await r.json();
  chat.innerHTML+='<div class="msg bot">'+(d.jawaban||'Maaf, terjadi gangguan.').replace(/</g,'&lt;')+'</div>';
}
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter') kirim();});
</script></body></html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "ai-faq-chatbot", "version": "2.0.0"}), 200

@app.route("/api/chat", methods=["POST"])
def chat():
    # 1. Validasi Content-Type
    if not request.is_json:
        return jsonify({"error": "Content-Type harus application/json"}), 400

    data = request.get_json(silent=True)
    if not data or "pertanyaan" not in data:
        return jsonify({"error": "Field 'pertanyaan' wajib diisi"}), 400

    pertanyaan = bersihkan_input(data.get("pertanyaan", ""))
    if not pertanyaan:
        return jsonify({"error": "Pertanyaan tidak boleh kosong"}), 400

    # 2. Rate-limit sederhana per IP
    ip = request.remote_addr or "unknown"
    _request_counts[ip] = _request_counts.get(ip, 0) + 1
    if _request_counts[ip] > MAX_PERTANYAAN_PER_MENIT:
        return jsonify({"error": "Terlalu banyak permintaan. Coba lagi 1 menit."}), 429

    jawaban = cari_jawaban(pertanyaan)
    return jsonify({"jawaban": jawaban, "disclaimer": "Bukan pengganti diagnosis dokter."}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint tidak ditemukan"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Terjadi gangguan server"}), 500

if __name__ == "__main__":
    # debug=False WAJIB di produksi, jangan pernah True di server publik
    app.run(host="127.0.0.1", port=5000, debug=False)
