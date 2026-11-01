# Panduan proyek: Drh. Erlangga Petshop & Petcare

Landing page statis (HTML, CSS, JS biasa, tanpa build). Isi dan sumber data ada di `README.md`, hasil audit di `AUDIT.md`.

## Aturan desain (urutan prioritas)

1. Permintaan pengguna.
2. Aturan di file ini.
3. Rekomendasi skill `ui-ux-pro-max`.

- **Warna:** dominan putih dengan pink anggrek logo. Dekorasi `--pink` (#b858a0), teks dan tombol `--accent` (#a8478f), teks di atas latar pink muda `--accent-deep` (#8f3a7b). Jangan memakai palet lain dari rekomendasi skill.
- **Font:** Kaushan Script hanya untuk nama merek, Montserrat untuk semua judul (700), isi, dan label, agar mudah dibaca. Font script lain tidak dipakai.
- **Grafis:** motif berlian dari logo. Jangan blob blur, glow, atau gradien acak.
- **Animasi:** hanya `transform` dan `opacity`. Semua animasi harus mati saat `prefers-reduced-motion`. Animasi tak berujung harus dijeda di luar layar.
- **Target sentuh:** minimal 44 px. **Kontras teks:** minimal 4,5:1.
- **Gambar:** WebP, ukuran sesuai tampilan, atribut `width` dan `height`, `loading="lazy"` kecuali di atas lipatan.
- **Sudut pandang teks:** tulis dari sudut pandang klinik ("kami", "Anda"), bukan sebagai pembuat situs. Jangan menyebut sumber data di halaman ("papan klinik", "profil TikTok", "bio Instagram", "hanya contoh"). Sumber dicatat di `README.md`, bukan di halaman.
- **Hierarki kata untuk hewan:** "anabul" untuk judul, banner, dan ajakan (emosional, ringkas). "peliharaan Anda" untuk teks isi agar tidak monoton. "hewan peliharaan" untuk fondasi SEO (meta, data terstruktur, teks alternatif). Teks yang ditulis pemilik tidak diubah.
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

`promo/live.html` memuat `index.html` apa adanya di dalam ponsel, jadi video selalu mengikuti isi situs. Setelah mengubah `index.html`, render ulang: `node promo/render-live.mjs` (butuh `npm install` di folder itu dan Google Chrome). Pakai `--preview` untuk cek frame contoh. Jaga 60 fps dan `--ss=2` agar gerak tidak patah. Teks di `live.html` ditulis tangan, sesuaikan jika wording situs berubah. `build-promo.py` dan `render.mjs` adalah pipeline video lama.
