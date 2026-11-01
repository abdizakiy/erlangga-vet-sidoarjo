# Panduan editor

`editor.html` adalah halaman yang sama dengan `index.html`, ditambah alat edit di dalam browser. Tanpa instalasi dan tanpa akun.

## Membuka

- **Online:** https://abdizakiy.github.io/erlangga-vet-sidoarjo/editor.html
- **Di komputer:** ekstrak zip, lalu klik dua kali `editor.html`. Folder `assets/` harus tetap di sebelahnya agar gambar tampil. Font memerlukan internet.

## Mengubah kata-kata

Klik teks apa saja lalu ketik. Teks yang bisa diubah diberi garis putus-putus saat kursor lewat. Tombol Enter dinonaktifkan agar susunan tidak rusak. Teks yang ditempel akan menjadi teks polos.

Ticker layanan (pita pink di atas) memuat tiap kata dua kali. Editor otomatis menyamakan pasangannya.

## Mengubah tata letak

Arahkan kursor ke sebuah bagian. Bilah kecil muncul di pojok kanan atasnya:

| Tombol | Fungsi |
|---|---|
| ↑ ↓ | Pindah bagian ke atas atau bawah |
| Sembunyikan | Sembunyikan bagian (tidak ikut diekspor). Klik lagi untuk menampilkan. |
| Spasi − / + | Kurangi atau tambah jarak atas-bawah |
| Latar | Ganti latar putih atau pink muda |

Arahkan kursor ke satu kartu atau item (kartu layanan, foto edukasi, lokasi, dan sebagainya), bilah **Item** muncul di pojok kirinya: ◀ ▶ menggeser, **Gandakan** membuat salinan, **Hapus** menghapus (klik dua kali).

Klik sebuah **tautan** atau **gambar** untuk mengubah alamat URL, berkas gambar, dan teks alternatifnya. Untuk gambar baru, taruh berkasnya di folder `assets/` lalu tulis `assets/nama-berkas.jpg`.

Tombol **Gaya** mengubah warna pink dan aksen, font judul, dan ukuran teks.

## Menyimpan

- Pekerjaan **tersimpan otomatis** di browser yang sama, jadi bisa ditutup lalu dilanjutkan.
- **Ekspor HTML** mengunduh `index.html` baru yang bersih. Tidak ada kode editor di dalamnya, dan bagian yang disembunyikan dibuang. Salin berkas itu menggantikan `index.html` lama di folder yang sama dengan `assets/`.
- **Salin HTML** menyalin isinya ke papan klip jika unduhan diblokir.
- **Reset** menghapus simpanan dan kembali ke versi awal.
- Matikan **Mode edit** untuk melihat hasilnya tanpa garis bantu.

## Menerbitkan perubahan

Kirim `index.html` hasil ekspor ke Claude, atau unggah ke repo GitHub menggantikan berkas lama. GitHub Pages memperbaruinya sendiri dalam sekitar satu menit.

## Batasan

- Simpanan otomatis hanya ada di browser dan perangkat yang dipakai. Ekspor untuk membawa hasilnya.
- Teks di dalam ilustrasi ponsel (percakapan contoh) ikut bisa diedit, tetapi hanya tampak saat langkah itu aktif. Klik daftar langkah di sebelahnya untuk berpindah.
- Mengubah `index.html` secara manual tidak otomatis masuk ke `editor.html`. Jalankan `python3 tools/build-editor.py` untuk membuat ulang.
