# Changelog

## [2.0.0] - 2026-11-11
### Added
- Validasi input (batas 500 karakter, escape HTML)
- Rate-limit sederhana per IP
- Health check `GET /health`
- 8 test otomatis + CI GitHub Actions
- `SECURITY.md`, `CONTRIBUTING.md`, `.gitignore`
- README profesional + badge Tests passing

### Changed
- `app.py` dirombak total jadi versi aman, tanpa API eksternal
- `requirements.txt` dikunci versinya (Flask 3.0.3)

### Security
- `debug=False` wajib di produksi
- Tidak menyimpan data pribadi / data pasien
- Tidak ada `eval()` / `exec()` / secret di kode

## [1.0.0] - 2026-11-10
- Versi awal: chatbot FAQ sederhana untuk klinik
