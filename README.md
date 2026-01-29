# 🐉 FScan - Advanced Sensitive File Hunter

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.o-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Author-anmxploit-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---

## 📖 Deskripsi
**FScan** adalah alat pemindai keamanan (Security Scanner) interaktif yang dirancang untuk mendeteksi file sensitif dan tersembunyi di server web. Dengan dukungan **Full HTTP Status Analysis**.



## ✨ Fitur Unggulan
- ⚡ **Turbo Multi-Threading**: Proses scanning cepat dengan kendali jumlah thread.
- 🐲 **Interactive UI**: Banner ASCII Naga yang keren dengan navigasi menu yang mudah.
- 📊 **Full Analysis Mode**: Mendeteksi status code `200`, `401`, `403`, `301`, dan `302`.
- 🛠️ **Customizable**: Wordlist dan ekstensi file bisa diatur sesuai target.
- 📈 **Live Progress**: Status bar real-time yang menampilkan persentase, jumlah temuan, dan path saat ini.
- 💾 **Smart Logging**: Hasil tersimpan otomatis dengan timestamp yang rapi.

---

## 🛠️ Instalasi & Persiapan

1. **Clone Repository**
```bash
git clone https://github.com/choirulanam-cybersec/FScan-v3.2-.git
cd fscan

2.Install Requirements

Bash

pip install -r requirements.txt

🚀 Cara Penggunaan

Cukup jalankan script utama, maka menu interaktif akan memandu Anda:
Bash

python fscan.py

📋 Opsi Filter Status:
Mode	Status Code yang Ditangkap	Kegunaan
Default	200, 401, 403, 301, 302	Analisis mendalam (Bug Hunting)
Custom	Sesuai Input (ex: 200)	Fokus pada hasil spesifik
📁 Struktur Proyek
Plaintext

fscan/
├── fscan.py           # Script Utama
├── requirements.txt   # Modul yang dibutuhkan (requests, colorama)
├── targets.txt        # Daftar domain target (jika mode massal)
└── result.txt         # Hasil scan (otomatis dibuat)

⚠️ Disclaimer

    PERINGATAN: Tool ini dibuat hanya untuk tujuan pendidikan dan pengujian keamanan legal (authorized pentesting). Penulis tidak bertanggung jawab atas tindakan ilegal atau penyalahgunaan alat ini. Gunakan dengan bijak!

👤 Author

Created by anmxploit

    💻 GitHub: choirul-anam-cybersec

    🐉 Motto: "See Everything, Miss Nothing"

 Copyright © 2024 anmxploit - FScan v1.0
