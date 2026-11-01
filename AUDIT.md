# Audit web: Drh. Erlangga Petshop & Petcare

Diaudit pada 1 November 2026 memakai meta prompt "Reusable Creative Website Master Prompt" sebagai daftar periksa, ditambah aturan prioritas dari skill UI/UX Pro Max. Angka diukur langsung di browser (desktop 1024 px dan ponsel 375 px).

## 1. Konfigurasi proyek (diisi dari meta prompt)

```txt
PROJECT_NAME        = "Drh. Erlangga Petshop & Petcare"
PROJECT_TYPE        = "Landing page klinik hewan lokal (Sidoarjo)"
PRIMARY_GOAL        = "Mengubah pemilik hewan menjadi konsultasi WhatsApp"
TARGET_AUDIENCE     = "Pemilik anjing, kucing, dan kelinci di Sidoarjo"
PRIMARY_CTA         = "Konsultasi lewat WhatsApp (0857-4594-8865)"
VISUAL_STYLE        = "Bersih, dominan putih, hangat, bernuansa tulisan tangan"
MOOD                = "Ramah, tepercaya, personal"
COLOR_DIRECTION     = "Putih; pink anggrek logo #b858a0 untuk dekorasi; #a8478f untuk teks dan tombol"
TYPOGRAPHY_STYLE    = "Kaushan Script (nama merek), Courgette (judul), Montserrat (isi dan label)"
GRAPHIC_LANGUAGE    = "Berlian dari logo, cakar, foto asli klinik, kartu edukasi Instagram"
ANIMATION_STYLE     = "Halus dan bermakna; adegan ponsel bergaya video promo; bergerak hanya dengan transform dan opacity"
TECH_STACK          = "HTML + CSS + JS biasa, tanpa build, tanpa dependensi"
```

## 2. Hasil per bagian meta prompt

| # | Bagian meta prompt | Sebelum | Sesudah |
|---|---|---|---|
| 2 | Arah kreatif konsisten | Cukup. Blob blur tanpa makna di panggung animasi bertentangan dengan aturan "no meaningless blobs". | Blob diganti motif berlian dari logo. |
| 4 | Stack: semantik, aksesibel, tanpa dependensi | Baik. Satu `h1`, landmark lengkap, `lang="id"`, nol dependensi. | Tetap. |
| 5 | Aset asli, gambar dioptimalkan | Buruk. PNG hero 978 KB, foto depan 392 KB dimuat dua kali. Total 1.644 KB. | WebP 800–1000 px. Total sekitar **250 KB** (turun lebih dari 80%). Gambar hero dipramuat dengan `fetchpriority="high"`. |
| 6 | Struktur halaman | Tidak ada penutup CTA yang tegas sebelum footer. | Tambah pita **Final CTA** dan footer wordmark. |
| 7 | Sistem desain: token, kontras | Satu pasangan kontras 4,37:1 (chip spesialisasi, tautan kartu). | Token `--accent-deep` (#8f3a7b). Semua teks lolos 4,5:1. |
| 9 | Komponen: tombol, kartu, gambar | Kartu layanan seragam 3×3. | Tata letak **bento** (kartu utama melebar), hover spotlight. |
| 10 | Elemen grafis konsisten | Blob acak. | Motif berlian logo, stiker di footer. |
| 12–14 | Animasi hero, scroll, micro-interaction | Hero: naik per blok. Scroll: fade sederhana. | Hero: judul muncul **per kata**. Scroll: bilah progres. Micro: tombol magnetik, spotlight kartu. |
| 15 | Efek khusus | Adegan ponsel tiga langkah (sudah ada). | Tambah ticker layanan. |
| 16 | Performa: hanya transform dan opacity | Dua animasi memakai `max-height` (memicu layout). Enam animasi tak berujung berjalan terus di luar layar. | `max-height` dihapus. Animasi **dijeda di luar layar** (IntersectionObserver). CLS 0. |
| 17 | Responsif | Tidak ada overflow di 375 px. | Tetap. Bento kembali satu kolom di ponsel. |
| 18 | Reduced motion | Sebagian. | Ticker, kata judul, bilah progres, tombol magnetik, dan footer ikut dimatikan. |
| 19 | Aturan kualitas kreatif | Baik: tidak ada glow, glass, atau gradien acak. | Tetap. |

## 3. Temuan terukur (aksesibilitas, prioritas 1–2 skill)

| Temuan | Sebelum | Sesudah |
|---|---|---|
| Target sentuh di bawah 44 px | 14 elemen (menu 38 px, tombol Salin 28 px, tautan 26 px, tombol header 40 px) | **0** |
| Kontras di bawah 4,5:1 | 1 pasangan (4,37:1) | **0** |
| Berat halaman | 1.644 KB | **sekitar 250 KB** |
| Layout shift (CLS) | 0 | 0 |
| Animasi tak berujung di luar layar | 6 berjalan | dijeda |

## 4. Komponen motion bergaya 21st.dev

Komponen di 21st.dev berbasis React, Tailwind, dan Motion, jadi tidak disalin. Polanya ditulis ulang dengan CSS dan JS biasa agar situs tetap tanpa dependensi dan lisensi tiap komponen tidak terlibat.

| Pola 21st.dev | Penerapan di sini |
|---|---|
| Marquee | Ticker layanan di bawah ringkasan. Dijeda saat hover dan di luar layar, statis saat reduced motion. |
| Grids & Bento + spotlight card | Kartu layanan: tiga kartu melebar, cahaya pink mengikuti kursor. |
| Sticker Footer with Script Wordmark | Footer dengan wordmark script besar dan stiker miring. |
| Text reveal | Judul hero muncul per kata. |
| Magnetic button | Tombol utama hero dan pita CTA bergeser tipis mengikuti kursor. |
| Scroll progress | Bilah pink di atas halaman memakai `animation-timeline: scroll()` tanpa JS. |

## 5. Skill UI/UX Pro Max

Terpasang di `.claude/skills/ui-ux-pro-max` (MIT, dari commit yang tercatat di `VENDORED_FROM.txt`). Repo ditinjau lebih dulu: hanya berisi data CSV dan skrip Python pencarian, tanpa panggilan jaringan dan tanpa skrip instalasi otomatis. Dijalankan di Mac ini dengan Python 3.10, tanpa dependensi.

Rekomendasinya (pola "Trust & Authority + Conversion": hero, bukti, solusi, CTA) dipakai untuk urutan bagian dan daftar periksa. Palet teal-oranye dan gaya claymorphism yang ia sarankan **tidak dipakai**, karena arahan Anda adalah palet putih-pink dari logo. Aturan skill sendiri menyebut hasilnya hanya rekomendasi.

## 6. Pengukuran akhir

Diukur ulang setelah semua perbaikan: kontras di bawah 4,5:1 = 0, target sentuh di bawah 44 px = 0 (kecuali tautan lompat yang hanya muncul saat fokus), CLS = 0, tidak ada error di konsol, tidak ada overflow horizontal di 375 px maupun 1024 px.

## 7. Belum selesai

- **Daftar harga** tidak ditemukan di sumber mana pun.
- **Foto potongan** lembut di layar besar. Sumbernya hanya 360×640 px.
- **Skala spasi dan tipografi** belum dijadikan token (masih nilai langsung di CSS).
- **CSS tak terpakai** dari versi lama (`.services` dan sejenisnya) belum dibersihkan.
- **Tes perangkat nyata**: diuji di emulasi browser, belum di ponsel fisik.

## 8. Perubahan dari feedback (Google Docs, 1 November 2026)

| Feedback | Tindakan |
|---|---|
| Ubah teks hero (judul dan paragraf) | Diganti persis sesuai dokumen. Frasa "kebutuhan peliharaan" diberi warna aksen. |
| Hapus: chip status jam, ticker layanan, catatan harga, bagian "Jangan menunggu terlalu lama", peringatan penipuan, wordmark footer | Semua dihapus, termasuk CSS-nya. |
| Dokter: ikuti referensi (kartu foto + salinan) | Kartu foto di kiri dengan lencana nama, judul, kotak kutipan dari ulasan, tiga poin centang, dan tombol WhatsApp. |
| Ulasan: ikuti referensi (kartu testimoni geser) | Lima kartu ulasan asli Google Maps yang bisa digeser dengan panah dan keyboard, plus tombol ke ulasan di kedua klinik. Grafik topik ulasan dihapus. |
| Edukasi dan kanal resmi: ikuti referensi "Social Feed" | Digabung menjadi satu bagian "Kabar terbaru dari klinik" berisi enam kartu postingan Instagram (tanggal, akun, takarir) dan tautan Instagram dan TikTok. |
| Lokasi: ikuti referensi "pilih toko" | Dua panel: detail klinik terpilih di kiri, daftar klinik di kanan. Berfungsi tanpa JavaScript (tombol radio). Di ponsel daftar tampil lebih dulu. |

Hal yang perlu dipastikan pemilik karena berasal dari teks feedback:

- **Home visit** dan **pet hotel** disebut di hero, tetapi tidak ada di sumber publik yang saya baca. Papan klinik hanya menulis "Cat Hotel", dan "home visit" tidak ditemukan di mana pun.
- Hero hanya menyebut **kucing dan anjing** serta **Sukodono**. Konten edukasi masih memuat kelinci, dan klinik kedua di Candi masih ada di bagian lokasi.
- **Foto dokter**: kartu dokter memakai foto petugas berjaket ungu dari postingan testimoni dengan lencana "Tim Drh. Erlangga", karena identitasnya belum dikonfirmasi. Ganti dengan foto dokter dan nama yang benar.
- Teks hero baru mirip susunan layanan di situs Mommy Pet Care. Pastikan wording akhirnya milik klinik sendiri.

## 9. Putaran revisi kedua (1 November 2026)

| Permintaan | Tindakan |
|---|---|
| Rollback bagian dokter, harus ada 2 foto, atau buat aset animasi profil | Bagian "Dua dokter hewan" dipulihkan. Karena belum ada foto dokter, dibuat dua avatar ilustrasi beranimasi (`assets/dokter-erlangga.svg`, `assets/dokter-radhita.svg`): mata berkedip, kepala bergerak halus, stetoskop berdenyut. Animasi mati saat "kurangi gerakan". Ganti dengan foto asli jika sudah ada. |
| Ulasan: bahasa Indonesia, satu review untuk semua klinik | Lima kutipan diterjemahkan ke bahasa Indonesia dengan catatan "diterjemahkan dari bahasa aslinya". Label per klinik dihapus. Rating gabungan sekitar 4,9 dari 1.655 ulasan (1.182 + 473). |
| Istilah "Vetcare" menjadi "Klinik" | "Klinik Suko" dan "Klinik Sidokare Asri" di semua teks, teks alternatif, data terstruktur, dan dokumen. |
| Rollback kabar sosial, judul "Sosial Media kami" | Bagian edukasi dipulihkan (enam kartu), dengan judul dan sub judul baru serta tautan Instagram dan TikTok. Menu: "Sosial Media". |
| Rollback lokasi, hapus tombol "Salin" | Dua kartu klinik dipulihkan. Tombol Salin dan skripnya dihapus. |

Video promo belum dirender ulang, jadi masih menyebut "Vetcare" di versi lama. Skrip pembuatnya sudah diperbarui.

## 10. Sudut pandang teks (1 November 2026)

Seluruh teks halaman ditulis ulang dari sudut pandang klinik ("kami" dan "Anda"). Frasa yang berbicara sebagai pembuat situs dihapus: "mengikuti papan nama klinik", "tercantum di papan klinik", "profil TikTok mencantumkan", "jam mengikuti bio Instagram", "Google Maps mencantumkan tutup 21.00", "cuplikan ulasan asli", "percakapan hanya contoh", dan catatan tanggal rating di footer. Sumber data tetap tercatat di `README.md`.

Konsekuensinya: perbedaan jam tutup Klinik Suko (bio Instagram 20.30, Google Maps 21.00) tidak lagi disebut di halaman. Pemilik perlu memastikan jam yang benar.

## 11. Foto hero baru (1 November 2026)

Foto potongan di hero diganti ilustrasi dokter bersama anjing, kucing, dan kelinci dari sampul reel Instagram klinik (19 September 2026). Sumber 540×960 px dipotong ke rasio 4:5, diperbesar ke 800 px dan dipertajam sedikit (WebP, 120 KB). Diberi label "Ilustrasi" di pojok kiri bawah. Foto potongan lama (`hero-cutout.*`) tidak lagi dipakai di halaman. Video promo masih memakainya sampai dirender ulang.

## 12. Hero tanpa latar dan bagian dokter baru (1 November 2026)

- **Hero:** ilustrasi dipisahkan dari latar (Vision, di Mac, tanpa unduhan model). Papan tulis, rak buku, tanaman, meja, buku, buku catatan, dan laptop dibuang. Yang tersisa dokter dan enam hewan (WebP transparan 900 px, 90 KB). Label "Ilustrasi", kartu pink, border, dan dua foto klinik dihapus dari hero.
- **Dokter di balik klinik:** layout mengikuti referensi Nicepage "Our Medical Team": judul di tengah di atas pita warna aksen, kartu putih berisi potret (avatar animasi), nama berwarna aksen, dan spesialisasi miring. Statistik pengikut dan tombol TikTok dan Instagram dihapus dari bagian ini karena sudah ada di bagian Sosial Media.
- Skrip `tools/cutout.swift` sekarang juga bisa mengekspor peta objek per elemen.

## 13. Penutup bagian ulasan (1 November 2026)

Catatan "Ulasan diterjemahkan ke bahasa Indonesia" dan dua tombol "Semua ulasan Klinik Suko" dan "Semua ulasan Klinik Sidokare Asri" dihapus dari bagian ulasan atas permintaan pemilik. Tautan ke Google Maps masih tersedia di bagian Pilih klinik (tombol Petunjuk arah).
