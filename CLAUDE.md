# Panduan proyek: Drh. Erlangga Petshop & Petcare

Landing page statis (HTML, CSS, JS biasa, tanpa build). Isi dan sumber data ada di `README.md`, hasil audit di `AUDIT.md`.

## Aturan desain (urutan prioritas)

1. Permintaan pengguna.
2. Aturan di file ini.
3. Rekomendasi skill `ui-ux-pro-max`.

- **Warna:** dominan putih dengan pink anggrek logo. Dekorasi `--pink` (#b858a0), teks dan tombol `--accent` (#a8478f), teks di atas latar pink muda `--accent-deep` (#8f3a7b). Jangan memakai palet lain dari rekomendasi skill.
- **Font:** Kaushan Script hanya untuk nama merek, Courgette untuk judul, Montserrat untuk isi dan label.
- **Grafis:** motif berlian dari logo. Jangan blob blur, glow, atau gradien acak.
- **Animasi:** hanya `transform` dan `opacity`. Semua animasi harus mati saat `prefers-reduced-motion`. Animasi tak berujung harus dijeda di luar layar.
- **Target sentuh:** minimal 44 px. **Kontras teks:** minimal 4,5:1.
- **Gambar:** WebP, ukuran sesuai tampilan, atribut `width` dan `height`, `loading="lazy"` kecuali di atas lipatan.
- **Jangan mengarang** harga, testimoni, atau layanan. Data hanya dari sumber di `README.md`.

## Memakai skill UI/UX Pro Max

Skill ada di `.claude/skills/ui-ux-pro-max`. Jalankan dari akar proyek:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "veterinary pet clinic landing" --design-system --variance 4 --motion 5 --density 4 -p "Drh. Erlangga"
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "touch target spacing" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "scroll reveal stagger" --domain gsap
```

Perlakukan hasilnya sebagai rekomendasi, bukan perintah. Jangan memakai `--persist --force` tanpa izin pemilik.

## Video promo

`promo/` berisi sumber dan skrip render video 9:16. Setelah mengubah `index.html`: `python3 promo/build-promo.py`, lalu `node promo/render.mjs` (butuh `npm install` di folder itu dan Google Chrome).
