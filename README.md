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

## Desain

- **Warna:** dominan putih dengan pink anggrek dari logo (`--pink: #b858a0` untuk dekorasi, `--accent: #a8478f` untuk teks dan tombol agar kontrasnya cukup). Semua warna ada di blok `:root` pada `index.html`.
- **Font:** Kaushan Script untuk judul, meniru tulisan tangan "Drh.Erlangga" pada logo. Montserrat untuk isi, dengan label huruf kapital renggang seperti "PETSHOP & PETCARE". Keduanya dimuat dari Google Fonts.
- **Pola layout** (terinspirasi dari situs klinik lain, tanpa menyalin teks atau foto): tombol WhatsApp melayang, pilihan layanan berdasarkan kebutuhan, bagian tanda darurat, langkah layanan, dan profil dokter.
- **Interaksi:** semua tombol konsultasi membuka dialog pilihan klinik dengan pesan WhatsApp yang sudah terisi. Status "buka sekarang" dihitung dari jam WIB.

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
- **Status "buka sekarang":** dihitung dengan anggapan klinik buka setiap hari pada jam yang tertulis. Jika ada hari libur, tambahkan aturan harinya di fungsi `updateStatus` pada `index.html`.
- **Tanda darurat:** daftar umum, bukan dari sumber klinik. Sesuaikan dengan pedoman dokter.
- **Layanan:** daftar disusun dari topik ulasan dan bio dokter. Hapus atau tambah sesuai layanan yang sebenarnya.
- **Rating dan jumlah ulasan** ditulis manual dan akan basi. Perbarui secara berkala.
- **Video:** halaman video TikTok tidak bisa dimuat saat pengumpulan data, jadi belum ada video di halaman.
- **Resolusi gambar:** gambar Instagram berukuran 512x640 px dan logo 150x150 px. Ganti dengan berkas asli beresolusi tinggi jika tersedia.

## Publikasi

Situs ini bisa dipublikasikan lewat GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
