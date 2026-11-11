# AI FAQ Chatbot - Klinik

[![Tests](https://github.com/riyanda-ex/ai-faq-chatbot/actions/workflows/tests.yml/badge.svg)](https://github.com/riyanda-ex/ai-faq-chatbot/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Chatbot FAQ sederhana untuk klinik. Menjawab pertanyaan umum pasien (jam buka, biaya, cara daftar, jadwal dokter, obat) secara otomatis, tanpa menyimpan data pribadi.

> ⚠️ **Disclaimer Medis:** Ini demo edukasi, BUKAN pengganti diagnosis dokter. Jangan kirim NIK / No. BPJS / nama lengkap.

## Fitur

- Jawaban dari FAQ lokal, tanpa API eksternal (cepat, gratis, aman)
- Validasi input, batas 500 karakter, escape HTML
- Rate-limit sederhana per IP
- Health check `/health`
- 8 test otomatis + CI GitHub Actions

## Cara Jalanin

```bash
pip install -r requirements.txt
python app.py
# Buka: http://127.0.0.1:5000
