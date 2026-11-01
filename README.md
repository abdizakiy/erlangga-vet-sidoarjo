# Drh. Erlangga Petshop & Petcare, Sidoarjo

Landing page statis untuk klinik hewan Drh. Erlangga di Sidoarjo. Satu file HTML dengan CSS dan JS inline, tanpa backend dan tanpa proses build.

## Isi

- `index.html`: seluruh halaman (hero, layanan, ulasan, edukasi, lokasi, kontak, data terstruktur JSON-LD).
- `assets/`: logo dan gambar edukasi dari akun Instagram klinik (`logo.jpg`, `testimoni.jpg`, `edukasi-*.jpg`), serta tiga foto klinik yang diunggah akun klinik sendiri di Google Maps (`klinik-suko-depan.jpg`, `klinik-vet2-resepsi.jpg`, `klinik-vet2-kandang.jpg`).

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
- **Interaksi:** tombol konsultasi dan kartu layanan membuka WhatsApp dengan pesan yang sudah terisi. Tombol salin nomor ada di kartu lokasi.

## Sumber data (per 1 November 2026)

| Data | Sumber |
|---|---|
| Alamat, rating, jumlah ulasan, topik ulasan | Google Maps, kedua klinik |
| Jam praktik | Bio Instagram `@drh.erlangga_petshop_petcare`; papan klinik menyebut praktik sesuai perjanjian |
| Spesialisasi dokter (surgery, interna, dermatology) | Bio TikTok `@doktererlanggavetcare` |
| Nama dua dokter, nomor WhatsApp dan telepon, daftar layanan, "buka sesuai perjanjian" | Papan nama klinik pada foto tampak depan Suko (Google Maps) |
| Gambar edukasi dan testimoni, peringatan penipuan | Postingan Instagram klinik |

## Hal yang perlu diperiksa pemilik

- **Daftar harga:** tidak ditemukan di Google Maps, Instagram (tanpa login hanya 12 postingan terbaru yang terlihat), TikTok, maupun papan klinik. Tidak ada angka harga di halaman. Tambahkan bagian harga setelah daftar tersedia, misalnya tabel di bawah bagian Layanan.
- **Daftar layanan:** diambil dari spanduk kiri pada papan klinik, yang sebagian tertutup tanaman. Bagian yang terbaca: pengobatan semua hewan, cat hotel, bedah, sterilisasi, grooming terapi, vaksinasi, nebulizer, USG, dan inap. Satu baris tidak terbaca. Pastikan daftar ini benar dan lengkap.
- **Jam praktik:** papan klinik menulis "buka sesuai perjanjian", sedangkan bio Instagram menulis 12.00–20.30 (Suko) dan 11.00–20.30 (Sidokare Asri). Google Maps menulis Suko tutup 21.00. Samakan.
- **Nomor telepon:** papan klinik mencantumkan dua nomor, 0857-4594-8865 (ada ikon WhatsApp) dan 0812-8740-2949, di bawah kedua alamat klinik. Halaman memakai 0857 sebagai WhatsApp utama. Ubah di `index.html` dan data JSON-LD jika berbeda.
- **Dokter:** papan klinik menyebut Drh. Yudha Bayu Erlangga dan Drh. Radhita Andriani. Spesialisasi (surgery, interna, dermatology) berasal dari bio TikTok akun "Drh. Erlangga". Dianggap sama dengan Drh. Yudha Bayu Erlangga. Pastikan, dan tambahkan keterangan untuk Drh. Radhita Andriani.
- **Tanda darurat:** daftar umum, bukan dari sumber klinik. Sesuaikan dengan pedoman dokter.
- **Rating dan jumlah ulasan** ditulis manual dan akan basi. Perbarui secara berkala.
- **Video:** halaman video TikTok tidak bisa dimuat saat pengumpulan data, jadi belum ada video di halaman.
- **Foto lain:** foto interior lain di Google Maps diunggah pelanggan, jadi tidak dipakai. Ganti atau tambah dengan foto asli klinik beresolusi tinggi jika ada. Gambar Instagram hanya 512x640 px dan logo 150x150 px.

## Publikasi

Situs ini dipublikasikan lewat GitHub Pages dari branch `main`, folder root.
