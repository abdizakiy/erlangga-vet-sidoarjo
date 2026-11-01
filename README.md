# Drh. Erlangga Petshop & Petcare, Sidoarjo

Landing page statis untuk klinik hewan Drh. Erlangga di Sidoarjo. Satu file HTML dengan CSS dan JS inline, tanpa backend dan tanpa proses build.

## Isi

- `index.html`: seluruh halaman (hero, layanan, ulasan, edukasi, lokasi, kontak, data terstruktur JSON-LD).
- `assets/`: logo dan gambar yang diambil dari akun Instagram klinik (`logo.jpg`, `testimoni.jpg`, `edukasi-*.jpg`).

## Menjalankan

Buka `index.html` di browser, atau jalankan server lokal:

```bash
python3 -m http.server 8000
```

Lalu buka http://localhost:8000.

## Sumber data (per 1 November 2026)

| Data | Sumber |
|---|---|
| Alamat, rating, jumlah ulasan, topik ulasan | Google Maps, kedua klinik |
| Jam buka | Bio Instagram `@drh.erlangga_petshop_petcare` |
| Spesialisasi dokter (surgery, interna, dermatology) | Bio TikTok `@doktererlanggavetcare` |
| Telepon Vetcare 2 | Google Maps |
| Telepon Vetcare 1 (Suko) | Bio TikTok, karena Google Maps tidak mencantumkannya |
| Gambar edukasi dan testimoni, peringatan penipuan | Postingan Instagram klinik |

## Hal yang perlu diperiksa pemilik

- **Daftar harga:** tidak ditemukan di Google Maps, Instagram, maupun TikTok, jadi tidak ada angka harga di halaman. Tambahkan bagian harga setelah daftar tersedia, misalnya sebagai tabel di bawah bagian Layanan.
- **Nomor telepon Suko:** pastikan nomor `0812-8740-2949` memang untuk klinik Suko dan aktif di WhatsApp. Ubah di dua tempat: tombol WhatsApp di `index.html` dan data JSON-LD.
- **Jam buka Suko:** bio Instagram menulis 12.00–20.30, Google Maps menulis tutup 21.00. Samakan.
- **Layanan:** daftar disusun dari topik ulasan dan bio dokter. Hapus atau tambah sesuai layanan yang sebenarnya.
- **Rating dan jumlah ulasan** ditulis manual dan akan basi. Perbarui secara berkala.
- **Video:** halaman video TikTok tidak bisa dimuat saat pengumpulan data, jadi belum ada video di halaman.
- **Resolusi gambar:** gambar Instagram berukuran 512x640 px dan logo 150x150 px. Ganti dengan berkas asli beresolusi tinggi jika tersedia.

## Publikasi

Situs ini bisa dipublikasikan lewat GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
