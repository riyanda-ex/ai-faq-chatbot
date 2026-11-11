# Security Policy

## Jangan Laporkan Data Pasien di Sini
Repo ini adalah DEMO edukasi. Dilarang mengirim:
- Nama lengkap pasien
- NIK / No. BPJS / No. RM
- Rekam medis asli

## Cara Melaporkan Celah Keamanan
Jangan buat Issue publik untuk celah keamanan.
Hubungi pemilik repo lewat GitHub DM / email yang tertera di profil.

## Yang Sudah Diamankan
- Tidak ada secret / API key di kode
- `debug=False` di produksi
- Input dibatasi 500 karakter & di-escape
- Rate-limit sederhana per IP
- Tidak ada `eval()` / `exec()`
- Tidak menyimpan data pribadi

## Disclaimer Medis
Chatbot ini BUKAN pengganti diagnosis dokter.
Untuk keluhan medis, periksa langsung ke dokter.
