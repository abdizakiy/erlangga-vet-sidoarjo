"""Bangun promo.html (kanvas 1080x1920) dari komponen animasi di ../index.html.

Jalankan: python3 build-promo.py
CSS dan adegan ponsel diambil langsung dari index.html supaya video selalu
sama dengan animasi di halaman. Hanya tata letak kanvas dan teks promo yang
ditulis di sini.
"""
import re
from pathlib import Path

root = Path(__file__).resolve().parent
src = (root.parent / "index.html").read_text(encoding="utf-8")

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
font = re.search(r'<link rel="stylesheet" href="https://fonts[^>]*>', src).group(0)
stage = src[src.index('<div class="stage"'):src.index('<ol class="live"')].rstrip()
stage = stage.replace('role="img" aria-label="Animasi contoh percakapan WhatsApp dengan klinik, memilih hari praktik, lalu datang ke klinik"', 'aria-hidden="true"')
stage = stage.replace('src="assets/', 'src="../assets/')
if stage.endswith("</div>\n        </div>") or True:
    pass

promo_css = """
html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #fff; }
*, *::before, *::after { transition: none !important; }
html { scroll-behavior: auto; }
#canvas { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #fff; }
.glow { position: absolute; border-radius: 50%; filter: blur(90px); pointer-events: none; }
.glow.g1 { width: 760px; height: 760px; background: var(--soft); top: -240px; right: -260px; }
.glow.g2 { width: 700px; height: 700px; background: #fbe6d9; opacity: 0.7; bottom: -300px; left: -260px; }
.brandbar { position: absolute; left: 60px; top: 70px; display: flex; align-items: center; gap: 24px; z-index: 5; animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) 0.1s both; }
.brandbar img { width: 100px; height: 100px; border-radius: 50%; border: 2px solid var(--line); background: #fff; }
.brandbar .nm { display: grid; gap: 6px; }
.brandbar .nm b { font-family: var(--font-script); font-weight: 400; font-size: 62px; line-height: 1; }
.brandbar .nm i { font-style: normal; font-size: 20px; font-weight: 600; letter-spacing: 0.26em; text-transform: uppercase; color: var(--accent); }
.phase { position: absolute; inset: 0; display: none; }
body[data-phase="intro"] #intro, body[data-phase="s1"] #steps, body[data-phase="s2"] #steps, body[data-phase="s3"] #steps, body[data-phase="outro"] #outro { display: block; }

/* intro */
#intro h1 { position: absolute; left: 60px; top: 250px; width: 960px; margin: 0; font-size: 90px; line-height: 1.26; }
#intro .photos { position: absolute; left: 60px; top: 830px; width: 960px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
#intro figure { margin: 0; position: relative; border-radius: 36px; overflow: hidden; border: 2px solid var(--line); background: var(--band); }
#intro figure img { display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; }
#intro figcaption { position: absolute; left: 18px; bottom: 18px; background: #fff; border: 2px solid var(--line); border-radius: 999px; padding: 10px 24px; font-size: 26px; font-weight: 600; }
#intro .pills { position: absolute; left: 60px; top: 1480px; width: 960px; display: flex; flex-wrap: wrap; gap: 16px; }
.pill { background: #fff; border: 2px solid var(--line); border-radius: 999px; padding: 12px 28px; font-size: 30px; font-weight: 600; box-shadow: 0 8px 18px rgba(75, 29, 94, 0.08); }
.pill b { color: var(--accent); }
body[data-phase="intro"] #intro .r { animation: rise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) var(--d, 0s) both; }

/* langkah */
.sinfo { position: absolute; left: 60px; top: 230px; width: 960px; display: none; gap: 30px; align-items: flex-start; }
.sinfo .n { width: 100px; height: 100px; border-radius: 50%; background: var(--accent); color: var(--accent-ink); font-weight: 700; font-size: 54px; display: grid; place-items: center; flex: none; }
.sinfo h2 { margin: 0; font-size: 70px; line-height: 1.2; }
.sinfo p { margin: 12px 0 0; font-size: 34px; line-height: 1.4; color: var(--muted); }
body[data-phase="s1"] .sinfo.i1, body[data-phase="s2"] .sinfo.i2, body[data-phase="s3"] .sinfo.i3 { display: flex; animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) 0.05s both; }
#stagewrap { position: absolute; left: 60px; top: 500px; width: 480px; height: 540px; transform: scale(2); transform-origin: 0 0; }
#stagewrap .stage { width: 480px; height: 540px; min-height: 0; }
.foot { position: absolute; left: 60px; top: 1600px; font-size: 26px; color: var(--muted); }
.pdots { position: absolute; right: 60px; top: 1604px; display: flex; gap: 12px; }
.pdots span { width: 18px; height: 18px; border-radius: 50%; background: var(--line); }
body[data-phase="s1"] .pdots span:nth-child(1), body[data-phase="s2"] .pdots span:nth-child(2), body[data-phase="s3"] .pdots span:nth-child(3) { background: var(--accent); width: 54px; border-radius: 9px; }

/* penutup */
#outro .mid { position: absolute; left: 60px; top: 300px; width: 960px; display: grid; justify-items: center; text-align: center; gap: 0; }
#outro .big { width: 230px; height: 230px; border-radius: 50%; border: 4px solid var(--pink); background: #fff; overflow: hidden; box-shadow: 0 20px 44px rgba(75, 29, 94, 0.16); }
#outro .big img { display: block; width: 100%; height: 100%; }
#outro .wm { font-family: var(--font-script); font-size: 130px; line-height: 1.1; margin-top: 34px; }
#outro .ws { font-size: 30px; font-weight: 600; letter-spacing: 0.3em; text-transform: uppercase; color: var(--accent); margin-top: 6px; }
#outro .cta { margin-top: 70px; background: var(--accent); color: var(--accent-ink); border-radius: 999px; padding: 30px 64px; font-size: 48px; font-weight: 700; display: flex; align-items: center; gap: 22px; box-shadow: 0 18px 36px rgba(168, 71, 143, 0.35); }
#outro .cta svg { width: 62px; height: 62px; fill: currentColor; }
#outro .num { margin-top: 34px; font-size: 76px; font-weight: 700; letter-spacing: 0.02em; font-variant-numeric: tabular-nums; }
#outro .sub2 { margin-top: 8px; font-size: 32px; color: var(--muted); }
#outro .locs { margin-top: 60px; display: grid; gap: 14px; font-size: 34px; }
#outro .locs b { color: var(--accent); }
#outro .hn { margin-top: 56px; font-size: 30px; color: var(--muted); display: grid; gap: 6px; }
body[data-phase="outro"] #outro .r { animation: rise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) var(--d, 0s) both; }
body[data-phase="outro"] #outro .cta { animation: rise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.6s both, nudge 1.6s ease-in-out 1.6s infinite; }
@keyframes nudge { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.04); } }
"""

wa_icon = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 1.8a8.2 8.2 0 1 1-4.2 15.2l-.3-.2-2.9.8.8-2.8-.2-.3A8.2 8.2 0 0 1 12 3.8zM8.6 7.4c-.2 0-.5.1-.7.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.2 5 4.4 2.5 1 3 .8 3.5.7.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.7-.4l-1.9-.9c-.3-.1-.5-.1-.7.1l-.9 1.1c-.2.2-.3.2-.7.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.6c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.1c-.2-.5-.5-.4-.7-.4z"/></svg>'

html = f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>Promo Drh. Erlangga 9:16</title>
{font}
<style>{style}
{promo_css}</style></head>
<body data-phase="intro">
<div id="canvas">
  <span class="glow g1"></span><span class="glow g2"></span>

  <div class="brandbar"><img src="../assets/logo.jpg" alt=""><div class="nm"><b>Drh.Erlangga</b><i>Petshop &amp; Petcare</i></div></div>

  <section class="phase" id="intro">
    <h1 class="r" style="--d:.15s">Dokter hewan di Sidoarjo yang <span class="hl">menjelaskan</span> sampai Anda paham.</h1>
    <div class="photos">
      <figure class="r" style="--d:.7s"><img src="../assets/klinik-suko-depan.jpg" alt=""><figcaption>Vetcare 1, Suko</figcaption></figure>
      <figure class="r" style="--d:1s"><img src="../assets/klinik-vet2-resepsi.jpg" alt="" style="object-position:50% 28%"><figcaption>Vetcare 2, Sidokare Asri</figcaption></figure>
    </div>
    <div class="pills">
      <span class="pill r" style="--d:1.5s"><b>4,9</b> di Google Maps</span>
      <span class="pill r" style="--d:1.7s"><b>1.182</b> ulasan</span>
      <span class="pill r" style="--d:1.9s">Selasa–Minggu</span>
    </div>
  </section>

  <section class="phase" id="steps">
    <div class="sinfo i1"><span class="n">1</span><div><h2>Ceritakan kondisinya</h2><p>Kirim keluhan lewat WhatsApp, lengkap dengan foto.</p></div></div>
    <div class="sinfo i2"><span class="n">2</span><div><h2>Buat janji</h2><p>Praktik Selasa sampai Minggu. Senin libur.</p></div></div>
    <div class="sinfo i3"><span class="n">3</span><div><h2>Datang ke klinik</h2><p>Dokter memeriksa dan menjelaskan hasilnya.</p></div></div>
    <div id="stagewrap">
{stage}
    </div>
    <div class="foot">Contoh percakapan, hanya ilustrasi.</div>
    <div class="pdots"><span></span><span></span><span></span></div>
  </section>

  <section class="phase" id="outro">
    <div class="mid">
      <span class="big r" style="--d:.1s"><img src="../assets/logo.jpg" alt=""></span>
      <div class="wm r" style="--d:.25s">Drh.Erlangga</div>
      <div class="ws r" style="--d:.35s">Petshop &amp; Petcare</div>
      <div class="cta">{wa_icon}<span>Konsultasi lewat WhatsApp</span></div>
      <div class="num r" style="--d:.9s">0857-4594-8865</div>
      <div class="sub2 r" style="--d:1s">Praktik sesuai perjanjian · Selasa–Minggu</div>
      <div class="locs">
        <div class="r" style="--d:1.2s"><b>Vetcare 1</b> · Suko, Sukodono</div>
        <div class="r" style="--d:1.4s"><b>Vetcare 2</b> · Sidokare Asri, Candi</div>
      </div>
      <div class="hn r" style="--d:1.7s"><span>Instagram @drh.erlangga_petshop_petcare</span><span>TikTok @doktererlanggavetcare</span></div>
    </div>
  </section>
</div>

<script>
// Kendali waktu deterministik: seek(t) menampilkan tepat satu frame pada detik ke-t.
var INTRO = 3.6, STEP = 4.8, STEPS = 3, OUTRO_AT = INTRO + STEP * STEPS, TOTAL = OUTRO_AT + 4.2;
window.TOTAL = TOTAL;
window.seek = function (t) {{
  var phase, lt, step = 0;
  if (t < INTRO) {{ phase = 'intro'; lt = t; }}
  else if (t < OUTRO_AT) {{ var u = t - INTRO; step = Math.floor(u / STEP) + 1; phase = 's' + step; lt = u - (step - 1) * STEP; }}
  else {{ phase = 'outro'; lt = t - OUTRO_AT; }}
  document.body.setAttribute('data-phase', phase);
  if (step) document.getElementById('stage').setAttribute('data-step', String(step));
  var fadeIn = function (x) {{ return Math.max(0, Math.min(1, x / 0.3)); }};
  document.getElementById('steps').style.opacity = phase[0] === 's' ? (step === 1 ? fadeIn(lt) : 1) : 1;
  document.getElementById('outro').style.opacity = phase === 'outro' ? fadeIn(lt) : 1;
  void document.body.offsetHeight;
  document.getAnimations().forEach(function (a) {{
    var el = a.effect && a.effect.target;
    var global = el && el.closest && el.closest('.brandbar');
    a.pause();
    a.currentTime = (global ? t : lt) * 1000;
  }});
}};
window.ready = Promise.all([document.fonts.ready, Promise.all([].map.call(document.images, function (i) {{ return i.decode ? i.decode().catch(function () {{}}) : null; }}))]);
</script>
</body></html>
"""
(root / "promo.html").write_text(html, encoding="utf-8")
print("promo.html", len(html))
