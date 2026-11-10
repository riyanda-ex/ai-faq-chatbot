# Chatbot FAQ Klinik Sederhana

faq = {
    "jam buka": "Klinik buka Senin - Sabtu, jam 08.00 - 20.00 WIB.",
    "daftar": "Untuk daftar, silakan datang langsung bawa KTP atau hubungi nomor klinik.",
    "biaya": "Biaya konsultasi mulai dari Rp 50.000, belum termasuk obat.",
    "dokter": "Hari ini ada dr. Umum dan dr. Gigi. Silakan cek jadwal di resepsionis.",
    "lokasi": "Klinik kami di Kediri, Jawa Timur."
}

print("Halo! Saya chatbot klinik. Ketik 'keluar' untuk berhenti.")

while True:
    tanya = input("Kamu: ").lower()
    if tanya == "keluar":
        print("Bot: Terima kasih, semoga sehat selalu!")
        break

    jawaban = "Maaf, saya belum paham. Coba tanya tentang jam buka, daftar, biaya, dokter, atau lokasi."
    for kunci, nilai in faq.items():
        if kunci in tanya:
            jawaban = nilai
            break
    
    print(f"Bot: {jawaban}")
