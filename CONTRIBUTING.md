# Contributing

Terima kasih mau berkontribusi!

## Aturan Utama
1. Jangan kirim data pasien asli (nama, NIK, No. BPJS, rekam medis)
2. Jangan kirim secret / API key
3. Semua perubahan wajib lolos test: `python -m pytest test_app.py -v`

## Cara Kontribusi
1. Fork repo ini
2. Buat branch: `git checkout -b fix/nama-perbaikan`
3. Jalankan test sebelum commit
4. Buat Pull Request dengan deskripsi jelas: apa yang diubah + kenapa

## Standar Kode
- Python 3.12, ikuti gaya kode yang sudah ada
- Input baru wajib divalidasi (batas panjang + escape)
- Jangan pakai `eval()` / `exec()` / `debug=True` di produksi
