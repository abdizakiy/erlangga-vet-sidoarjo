"""Bangun editor.html: salinan index.html dengan editor visual di dalamnya.

Jalankan dari akar proyek:  python3 tools/build-editor.py

Editor.html bekerja tanpa server dan tanpa instalasi. Buka di browser (folder
assets/ harus ada di sebelahnya), edit teks dan susunan bagian, lalu klik
"Ekspor HTML" untuk mendapatkan index.html baru yang bersih.
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")

# 1. Jangan ganti langkah animasi otomatis saat mode edit aktif.
old = "timer = setInterval(function () { go(step % 3 + 1); }, DUR);"
assert old in src, "kode interval animasi berubah, perbarui build-editor.py"
src = src.replace(old, "timer = setInterval(function () { if (document.documentElement.classList.contains('editing')) return; go(step % 3 + 1); }, DUR);")

src = src.replace("<title>", "<title>[Editor] ", 1)
src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)

EDITOR_CSS = r"""
<style id="ed-style">
html.editing .fab, html.editing .progress { display: none !important; }
html.editing .rv:not(.in) { opacity: 1 !important; transform: none !important; }
html.editing .hero h1 .w, html.editing .need, html.editing .shot { animation: none !important; }
html.editing [contenteditable="true"] { cursor: text; }
html.editing [contenteditable="true"]:hover { outline: 1px dashed #a8478f; outline-offset: 2px; }
html.editing [contenteditable="true"]:focus { outline: 2px solid #a8478f; outline-offset: 2px; background: rgba(184, 88, 160, 0.1); }
html.editing .ed-sel { outline: 3px solid #1b7a43 !important; outline-offset: 3px; }
html.editing [data-ed-hidden] { opacity: 0.3; outline: 2px dashed #888; outline-offset: -2px; }
html:not(.editing) [data-ed-hidden] { display: none !important; }
#ed-ui, #ed-ui * { box-sizing: border-box; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; letter-spacing: 0; text-transform: none; }
#ed-bar { position: fixed; z-index: 10000; left: 50%; bottom: 14px; transform: translateX(-50%); display: flex; flex-wrap: wrap; gap: 6px; align-items: center; justify-content: center; max-width: calc(100vw - 20px); padding: 8px; background: #1d1a1f; color: #fff; border-radius: 16px; box-shadow: 0 12px 34px rgba(0, 0, 0, 0.35); font-size: 13px; }
#ed-bar button, .ed-mini button { font: inherit; font-size: 13px; color: #fff; background: #3a3340; border: 0; border-radius: 10px; min-height: 36px; padding: 0 12px; cursor: pointer; }
#ed-bar button:hover, .ed-mini button:hover { background: #55495e; }
#ed-bar button.on { background: #a8478f; }
#ed-bar .msg { opacity: 0.75; padding: 0 6px; max-width: 220px; }
.ed-mini { position: fixed; z-index: 10001; display: none; gap: 3px; padding: 4px; background: #1d1a1f; border-radius: 10px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3); }
.ed-mini button { min-height: 30px; min-width: 30px; padding: 0 8px; }
.ed-mini .lbl { color: #bbb; font-size: 11px; align-self: center; padding: 0 6px 0 4px; }
.ed-panel { position: fixed; z-index: 10000; left: 14px; bottom: 74px; width: min(330px, calc(100vw - 28px)); background: #fff; color: #1d1a1f; border: 1px solid #ddd; border-radius: 14px; box-shadow: 0 12px 34px rgba(0, 0, 0, 0.25); padding: 14px; display: none; font-size: 13px; }
.ed-panel h4 { margin: 0 0 10px; font-size: 14px; }
.ed-panel label { display: block; margin: 8px 0 3px; font-weight: 600; }
.ed-panel input[type=text], .ed-panel select { width: 100%; padding: 8px 10px; border: 1px solid #ccc; border-radius: 8px; font: inherit; }
.ed-panel input[type=color] { width: 44px; height: 32px; padding: 0; border: 1px solid #ccc; border-radius: 6px; }
.ed-panel .row { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 8px; }
.ed-panel .hint { color: #666; margin-top: 8px; line-height: 1.4; }
.ed-panel .close { position: absolute; right: 8px; top: 6px; border: 0; background: none; font-size: 18px; cursor: pointer; }
#ed-export { position: fixed; inset: 0; z-index: 10002; background: rgba(0, 0, 0, 0.55); display: none; place-items: center; }
#ed-export .box { background: #fff; color: #1d1a1f; width: min(720px, calc(100vw - 28px)); max-height: 86vh; border-radius: 16px; padding: 18px; display: grid; gap: 10px; }
#ed-export textarea { width: 100%; height: 40vh; font: 12px/1.4 ui-monospace, monospace; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }
#ed-export button { font: inherit; padding: 8px 14px; border-radius: 10px; border: 1px solid #a8478f; background: #a8478f; color: #fff; cursor: pointer; }
</style>
"""

EDITOR_UI = r"""
<div id="ed-ui">
  <div id="ed-bar" role="toolbar" aria-label="Editor">
    <button type="button" id="ed-toggle" class="on" title="Aktifkan atau matikan mode edit">Mode edit: aktif</button>
    <button type="button" id="ed-style-btn">Gaya</button>
    <button type="button" id="ed-export-btn">Ekspor HTML</button>
    <button type="button" id="ed-copy-btn">Salin HTML</button>
    <button type="button" id="ed-reset-btn">Reset</button>
    <span class="msg" id="ed-msg">Klik teks untuk mengubah. Arahkan kursor ke bagian untuk memindah.</span>
  </div>
  <div class="ed-mini" id="ed-sec"></div>
  <div class="ed-mini" id="ed-item"></div>
  <div class="ed-panel" id="ed-link">
    <button type="button" class="close" aria-label="Tutup">×</button>
    <h4 id="ed-link-title">Tautan</h4>
    <div id="ed-link-fields"></div>
  </div>
  <div class="ed-panel" id="ed-styles">
    <button type="button" class="close" aria-label="Tutup">×</button>
    <h4>Gaya halaman</h4>
    <div class="row"><span>Pink dekorasi</span><input type="color" id="ed-c-pink" value="#b858a0"></div>
    <div class="row"><span>Warna tombol dan teks aksen</span><input type="color" id="ed-c-accent" value="#a8478f"></div>
    <div class="row"><span>Latar bagian pink muda</span><input type="color" id="ed-c-band" value="#fdf4f9"></div>
    <label for="ed-font">Font judul</label>
    <select id="ed-font"><option value="Courgette">Courgette (sekarang)</option><option value="Kaushan Script">Kaushan Script</option><option value="Montserrat">Montserrat</option></select>
    <label for="ed-scale">Ukuran teks: <span id="ed-scale-v">100</span>%</label>
    <input type="range" id="ed-scale" min="90" max="120" value="100" step="2" style="width:100%">
    <p class="hint">Warna teks tombol bisa tidak terbaca jika terlalu terang. Periksa kontrasnya sebelum dipakai.</p>
  </div>
  <div id="ed-export"><div class="box">
    <strong>HTML siap disalin</strong>
    <textarea id="ed-ta" readonly></textarea>
    <div><button type="button" id="ed-ta-copy">Salin semua</button> <button type="button" id="ed-ta-close" style="background:#fff;color:#a8478f">Tutup</button></div>
  </div></div>
</div>
"""

RESTORE = r"""<script id="ed-restore">
(function () {
  try {
    var raw = localStorage.getItem('erlangga-editor-v1');
    if (!raw) return;
    var d = JSON.parse(raw);
    var map = [['header.top', d.header], ['main', d.main], ['footer', d.footer]];
    map.forEach(function (m) { var el = document.querySelector(m[0]); if (el && m[1]) el.outerHTML = m[1]; });
    if (d.style) document.documentElement.setAttribute('style', d.style);
  } catch (e) {}
})();
</script>
"""

EDITOR_JS = r"""<script id="ed-script">
(function () {
  var root = document.documentElement;
  var KEY = 'erlangga-editor-v1';
  var ITEM_PARENTS = '.needs, .team-grid, .rev, .edu, .places';
  var $ = function (id) { return document.getElementById(id); };
  var on = false, secTarget = null, itemTarget = null, selected = null, saveTimer = null;

  function isUI(n) { return n && n.closest && n.closest('#ed-ui'); }
  function msg(t) { $('ed-msg').textContent = t; }

  // ---------- teks yang bisa diedit ----------
  function inlineDisplay(el) {
    var d = getComputedStyle(el).display;
    return d === 'inline' || d === 'inline-block' || d === 'contents';
  }
  function isLeaf(el) {
    if (/^(SCRIPT|STYLE|SVG|IMG|VIDEO|PATH|G|CIRCLE|RECT|ELLIPSE|DIALOG|NOSCRIPT|BR)$/i.test(el.tagName)) return false;
    if (el.closest('svg') || isUI(el)) return false;
    var hasText = [].some.call(el.childNodes, function (n) { return n.nodeType === 3 && n.textContent.trim(); });
    if (!hasText) return false;
    return [].every.call(el.children, function (c) { return c.tagName === 'BR' || inlineDisplay(c); });
  }
  function leaves() { return [].filter.call(document.body.querySelectorAll('*'), isLeaf); }
  function unwrapWords() {
    [].slice.call(document.querySelectorAll('.hero h1 .w')).forEach(function (w) { w.replaceWith.apply(w, w.childNodes); });
    var h = document.querySelector('.hero h1'); if (h) h.normalize();
  }
  function setEdit(v) {
    on = v;
    root.classList.toggle('editing', v);
    $('ed-toggle').classList.toggle('on', v);
    $('ed-toggle').textContent = 'Mode edit: ' + (v ? 'aktif' : 'mati');
    if (v) {
      unwrapWords();
      leaves().forEach(function (el) { el.setAttribute('contenteditable', 'true'); el.setAttribute('spellcheck', 'false'); });
    } else {
      [].forEach.call(document.querySelectorAll('[contenteditable]'), function (el) { el.removeAttribute('contenteditable'); el.removeAttribute('spellcheck'); });
      hideBars(); closePanels();
    }
  }

  // ---------- ekspor bersih ----------
  function clean(keepHidden) {
    var doc = root.cloneNode(true);
    doc.querySelectorAll('#ed-ui, #ed-style, #ed-script, #ed-restore').forEach(function (n) { n.remove(); });
    if (!keepHidden) doc.querySelectorAll('[data-ed-hidden]').forEach(function (n) { n.remove(); });
    doc.querySelectorAll('[contenteditable], [spellcheck]').forEach(function (n) { n.removeAttribute('contenteditable'); n.removeAttribute('spellcheck'); });
    doc.querySelectorAll('.hero h1 .w').forEach(function (w) { w.replaceWith.apply(w, w.childNodes); });
    var h1 = doc.querySelector('.hero h1'); if (h1) h1.normalize();
    ['rv', 'in', 'is-off', 'paused', 'ed-sel'].forEach(function (c) {
      doc.querySelectorAll('.' + c).forEach(function (n) { n.classList.remove(c); if (!n.getAttribute('class')) n.removeAttribute('class'); });
    });
    doc.classList.remove('js', 'editing');
    if (!doc.getAttribute('class')) doc.removeAttribute('class');
    doc.querySelectorAll('[style]').forEach(function (n) {
      ['transform', '--mx', '--my'].forEach(function (p) { n.style.removeProperty(p); });
      if (!(n.getAttribute('style') || '').trim()) n.removeAttribute('style');
    });
    var st = doc.querySelector('#stage'); if (st) st.setAttribute('data-step', '1');
    doc.querySelectorAll('.ls').forEach(function (b, i) { b.setAttribute('aria-current', i === 0 ? 'step' : 'false'); });
    var t = doc.querySelector('title'); if (t) t.textContent = t.textContent.replace('[Editor] ', '');
    var rb = doc.querySelector('meta[name="robots"]'); if (rb) rb.remove();
    return doc;
  }
  function html() { return '<!doctype html>\n' + clean(false).outerHTML; }

  function touch() {
    msg('Menyimpan...');
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      try {
        var d = clean(true);
        var data = {
          header: d.querySelector('header.top').outerHTML,
          main: d.querySelector('main').outerHTML,
          footer: d.querySelector('footer').outerHTML,
          style: d.getAttribute('style') || ''
        };
        localStorage.setItem(KEY, JSON.stringify(data));
        msg('Tersimpan otomatis di browser ini.');
      } catch (e) { msg('Tidak bisa menyimpan otomatis. Gunakan Ekspor HTML.'); }
    }, 700);
  }

  // ---------- penanganan input ----------
  document.addEventListener('input', function (e) {
    if (!on || isUI(e.target)) return;
    var el = e.target.closest && e.target.closest('[contenteditable]');
    if (el && el.closest('.ticker .tk')) {
      var spans = [].slice.call(document.querySelectorAll('.ticker .tk > span'));
      var i = spans.indexOf(el), half = spans.length / 2;
      if (i >= 0 && half) { var twin = spans[(i + half) % spans.length]; twin.textContent = el.textContent; }
    }
    touch();
  });
  document.addEventListener('keydown', function (e) {
    if (!on || isUI(e.target)) return;
    var el = e.target.closest && e.target.closest('[contenteditable]');
    if (!el) return;
    if (e.key === 'Enter') { e.preventDefault(); return; }
    if (e.key === ' ' && el.closest('button')) { e.preventDefault(); document.execCommand('insertText', false, ' '); }
  }, true);
  document.addEventListener('paste', function (e) {
    if (!on || isUI(e.target) || !(e.target.closest && e.target.closest('[contenteditable]'))) return;
    e.preventDefault();
    var t = (e.clipboardData || window.clipboardData).getData('text/plain').replace(/\s+/g, ' ');
    document.execCommand('insertText', false, t);
  }, true);

  // ---------- tautan dan gambar ----------
  function closePanels() { $('ed-link').style.display = 'none'; $('ed-styles').style.display = 'none'; }
  function clearSel() { if (selected) selected.classList.remove('ed-sel'); selected = null; }
  function field(label, value, onInput) {
    var wrap = document.createElement('div');
    var l = document.createElement('label'); l.textContent = label;
    var i = document.createElement('input'); i.type = 'text'; i.value = value || '';
    i.addEventListener('input', function () { onInput(i.value); touch(); });
    wrap.appendChild(l); wrap.appendChild(i); return wrap;
  }
  function openLink(el) {
    clearSel(); selected = el; el.classList.add('ed-sel');
    var box = $('ed-link-fields'); box.innerHTML = '';
    if (el.tagName === 'IMG') {
      $('ed-link-title').textContent = 'Gambar';
      box.appendChild(field('Berkas gambar', el.getAttribute('src'), function (v) { el.setAttribute('src', v); }));
      box.appendChild(field('Teks alternatif (untuk pembaca layar)', el.getAttribute('alt'), function (v) { el.setAttribute('alt', v); }));
    } else {
      $('ed-link-title').textContent = 'Tautan';
      box.appendChild(field('Alamat tujuan (URL)', el.getAttribute('href'), function (v) { el.setAttribute('href', v); }));
    }
    $('ed-styles').style.display = 'none';
    $('ed-link').style.display = 'block';
  }
  document.addEventListener('click', function (e) {
    if (!on || isUI(e.target)) return;
    var a = e.target.closest('a'), img = e.target.closest('img');
    if (a) e.preventDefault();
    var pick = img || a;
    if (pick) openLink(pick); else { clearSel(); $('ed-link').style.display = 'none'; }
  }, true);

  // ---------- gagang pindah bagian dan item ----------
  function mini(box, label, buttons) {
    box.innerHTML = '';
    var l = document.createElement('span'); l.className = 'lbl'; l.textContent = label; box.appendChild(l);
    buttons.forEach(function (b) {
      var x = document.createElement('button'); x.type = 'button'; x.textContent = b[0]; x.title = b[1];
      x.addEventListener('click', function (ev) { ev.stopPropagation(); b[2](x); });
      box.appendChild(x);
    });
  }
  function place(box, el, anchor) {
    var r = el.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) { box.style.display = 'none'; return; }
    box.style.display = 'flex';
    var w = box.offsetWidth;
    box.style.left = Math.max(6, Math.min(innerWidth - w - 6, r.right - w - 8)) + 'px';
    box.style.top = Math.max(6, Math.min(innerHeight - 50, anchor === 'top' ? r.top + 8 : r.top + 8)) + 'px';
  }
  function hideBars() { $('ed-sec').style.display = 'none'; $('ed-item').style.display = 'none'; secTarget = itemTarget = null; }
  function padTarget(sec) {
    var wrap = sec.querySelector(':scope > .wrap');
    return parseFloat(getComputedStyle(sec).paddingTop) > 0 || !wrap ? sec : wrap;
  }
  function showSection(sec) {
    var movable = sec.parentElement && sec.parentElement.tagName === 'MAIN';
    var btns = [];
    if (movable) {
      btns.push(['↑', 'Pindah ke atas', function () { var p = sec.previousElementSibling; if (p) { sec.parentNode.insertBefore(sec, p); touch(); showSection(sec); sec.scrollIntoView({ block: 'center' }); } }]);
      btns.push(['↓', 'Pindah ke bawah', function () { var n = sec.nextElementSibling; if (n) { sec.parentNode.insertBefore(n, sec); touch(); showSection(sec); sec.scrollIntoView({ block: 'center' }); } }]);
      btns.push(['Sembunyikan', 'Sembunyikan atau tampilkan bagian ini', function () { if (sec.hasAttribute('data-ed-hidden')) sec.removeAttribute('data-ed-hidden'); else sec.setAttribute('data-ed-hidden', '1'); touch(); }]);
    }
    var pt = padTarget(sec);
    btns.push(['Spasi −', 'Kurangi jarak atas-bawah', function () { var v = Math.max(0, Math.round(parseFloat(getComputedStyle(pt).paddingTop)) - 16); pt.style.paddingBlock = v + 'px'; touch(); }]);
    btns.push(['Spasi +', 'Tambah jarak atas-bawah', function () { var v = Math.min(240, Math.round(parseFloat(getComputedStyle(pt).paddingTop)) + 16); pt.style.paddingBlock = v + 'px'; touch(); }]);
    if (sec.classList.contains('block')) btns.push(['Latar', 'Ganti latar putih atau pink muda', function () { sec.classList.toggle('band'); touch(); }]);
    mini($('ed-sec'), 'Bagian', btns);
    secTarget = sec; place($('ed-sec'), sec, 'top');
  }
  function showItem(it) {
    var btns = [
      ['◀', 'Geser ke kiri atau atas', function () { var p = it.previousElementSibling; if (p) { it.parentNode.insertBefore(it, p); touch(); showItem(it); } }],
      ['▶', 'Geser ke kanan atau bawah', function () { var n = it.nextElementSibling; if (n) { it.parentNode.insertBefore(n, it); touch(); showItem(it); } }],
      ['Gandakan', 'Gandakan item ini', function () {
        var c = it.cloneNode(true);
        c.querySelectorAll('[id]').forEach(function (n) { n.removeAttribute('id'); });
        c.querySelectorAll('[aria-labelledby]').forEach(function (n) { n.removeAttribute('aria-labelledby'); });
        it.parentNode.insertBefore(c, it.nextSibling); touch(); hideBars();
      }],
      ['Hapus', 'Hapus item ini', function (btn) {
        if (btn.dataset.sure) { it.remove(); touch(); hideBars(); return; }
        btn.dataset.sure = '1'; btn.textContent = 'Yakin?'; setTimeout(function () { btn.dataset.sure = ''; btn.textContent = 'Hapus'; }, 2200);
      }]
    ];
    mini($('ed-item'), 'Item', btns);
    itemTarget = it;
    var r = it.getBoundingClientRect(), box = $('ed-item');
    box.style.display = 'flex';
    box.style.left = Math.max(6, Math.min(innerWidth - box.offsetWidth - 6, r.left + 8)) + 'px';
    box.style.top = Math.max(6, Math.min(innerHeight - 50, r.top + 8)) + 'px';
  }
  var raf = 0;
  document.addEventListener('pointermove', function (e) {
    if (!on) return;
    if (isUI(e.target)) return;
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {
      var t = e.target; if (!t || !t.closest) return;
      var sec = t.closest('main > *, header.top, footer');
      var it = t.closest(ITEM_PARENTS.split(',').map(function (s) { return s.trim() + ' > *'; }).join(', '));
      if (sec && sec !== secTarget) showSection(sec); else if (sec) place($('ed-sec'), sec, 'top');
      if (!sec) { $('ed-sec').style.display = 'none'; secTarget = null; }
      if (it && it !== itemTarget) showItem(it); else if (!it) { $('ed-item').style.display = 'none'; itemTarget = null; }
    });
  }, { passive: true });
  addEventListener('scroll', function () { if (secTarget) place($('ed-sec'), secTarget, 'top'); if (itemTarget) showItem(itemTarget); }, { passive: true });

  // ---------- gaya global ----------
  function setVar(name, v) { root.style.setProperty(name, v); touch(); }
  $('ed-c-pink').addEventListener('input', function (e) { setVar('--pink', e.target.value); });
  $('ed-c-accent').addEventListener('input', function (e) { setVar('--accent', e.target.value); });
  $('ed-c-band').addEventListener('input', function (e) { setVar('--band', e.target.value); });
  $('ed-font').addEventListener('change', function (e) { var f = e.target.value; setVar('--font-headline', '"' + f + '", "Kaushan Script", cursive'); });
  $('ed-scale').addEventListener('input', function (e) { $('ed-scale-v').textContent = e.target.value; root.style.fontSize = e.target.value + '%'; touch(); });

  // ---------- tombol bilah alat ----------
  $('ed-toggle').addEventListener('click', function () { setEdit(!on); });
  $('ed-style-btn').addEventListener('click', function () { var p = $('ed-styles'); var show = p.style.display !== 'block'; closePanels(); p.style.display = show ? 'block' : 'none'; });
  document.querySelectorAll('#ed-ui .ed-panel .close').forEach(function (b) { b.addEventListener('click', function () { b.parentNode.style.display = 'none'; clearSel(); }); });
  $('ed-export-btn').addEventListener('click', function () {
    var blob = new Blob([html()], { type: 'text/html' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'index.html';
    document.body.appendChild(a); a.click(); a.remove();
    msg('Berkas index.html diunduh. Jika tidak muncul, pakai Salin HTML.');
  });
  function showText() { $('ed-ta').value = html(); $('ed-export').style.display = 'grid'; $('ed-ta').select(); }
  $('ed-copy-btn').addEventListener('click', function () {
    var h = html();
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(h).then(function () { msg('HTML disalin ke papan klip.'); }, showText);
    else showText();
  });
  $('ed-ta-copy').addEventListener('click', function () { $('ed-ta').select(); document.execCommand('copy'); });
  $('ed-ta-close').addEventListener('click', function () { $('ed-export').style.display = 'none'; });
  $('ed-reset-btn').addEventListener('click', function (e) {
    var b = e.currentTarget;
    if (b.dataset.sure) { try { localStorage.removeItem(KEY); } catch (x) {} location.reload(); return; }
    b.dataset.sure = '1'; b.textContent = 'Yakin reset?'; setTimeout(function () { b.dataset.sure = ''; b.textContent = 'Reset'; }, 2500);
  });

  // mulai
  var rs = root.style.fontSize; if (rs) { $('ed-scale').value = parseInt(rs, 10); $('ed-scale-v').textContent = parseInt(rs, 10); }
  setEdit(true);
  window.__editor = { html: html, clean: clean };
})();
</script>
"""

marker = "<script>\n(function () {"
i = src.index(marker)
src = src[:i] + RESTORE + src[i:]
src = src.replace("</head>", EDITOR_CSS + "</head>", 1)
src = src.replace("</body>", EDITOR_UI + EDITOR_JS + "</body>", 1)

(root / "editor.html").write_text(src, encoding="utf-8")
print("editor.html", len(src))
