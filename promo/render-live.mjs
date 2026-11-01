// Render video "live preview" (ponsel berisi situs asli yang digulir).
//
//   cd promo && npm install
//   node render-live.mjs --preview          (frame contoh ke folder preview-live/)
//   node render-live.mjs                    (kedua format: 9x16 dan 16x9)
//   node render-live.mjs 916                (hanya 9:16)  |  node render-live.mjs 169
//
// Butuh Google Chrome. Atur CHROME_PATH jika letaknya berbeda.
import puppeteer from 'puppeteer-core';
import ffmpegPath from 'ffmpeg-static';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { mkdir, rm, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..');
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(chrome)) throw new Error('Chrome tidak ditemukan di ' + chrome + '. Atur CHROME_PATH.');

const FPS = Number((process.argv.find((a) => a.startsWith('--fps=')) || '--fps=60').split('=')[1]);
const preview = process.argv.includes('--preview');
// supersampling: halaman dirender SS kali lebih besar lalu diperkecil ke ukuran akhir (gerak lebih halus, teks lebih tajam)
const SS = Number((process.argv.find((a) => a.startsWith('--ss=')) || '--ss=2').split('=')[1]);
const pick = process.argv.slice(2).filter((a) => a === '916' || a === '169');
const formats = pick.length ? pick : ['916', '169'];
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.json': 'application/json' };

// server statis untuk akar repo agar iframe satu asal (same-origin)
const server = http.createServer(async (req, res) => {
  try {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const file = path.join(repo, p === '/' ? 'index.html' : p);
    if (!file.startsWith(repo)) { res.writeHead(403); return res.end(); }
    const buf = await readFile(file);
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
    res.end(buf);
  } catch { res.writeHead(404); res.end('tidak ada'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--font-render-hinting=none'] });

async function openPage(fmt) {
  const page = await browser.newPage();
  const size = fmt === '169' ? { width: 1920, height: 1080 } : { width: 1080, height: 1920 };
  await page.setViewport({ ...size, deviceScaleFactor: SS });
  await page.goto(`http://127.0.0.1:${port}/promo/live.html?fmt=${fmt}`, { waitUntil: 'networkidle0' });
  await page.evaluate(() => window.liveReady);
  return page;
}
const shot = async (page, t, file, opts) => { await page.evaluate((x) => window.seek(x), t); await page.screenshot({ path: file, ...opts }); };

if (preview) {
  for (const fmt of formats) {
    const page = await openPage(fmt);
    const dir = path.join(here, 'preview-live');
    await mkdir(dir, { recursive: true });
    for (const t of [1.5, 3.2, 6.5, 9.0, 12.0, 16.5, 21.5, 26.5]) {
      await shot(page, t, path.join(dir, `${fmt}-t${String(t).replace('.', '_')}.png`), { type: 'png' });
    }
    await page.close();
  }
  await browser.close(); server.close();
  console.log('Pratinjau di', path.join(here, 'preview-live'));
  process.exit(0);
}

for (const fmt of formats) {
  const page = await openPage(fmt);
  const total = await page.evaluate(() => window.TOTAL);
  const out = path.join(here, `erlangga-live-${fmt === '169' ? '16x9' : '9x16'}.mp4`);
  // frame PNG (tanpa kompresi lossy) dialirkan langsung ke ffmpeg, tanpa menulis ke disk
  const ff = spawn(ffmpegPath, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000', '-shortest',
    '-vf', `scale=${fmt === '169' ? 1920 : 1080}:${fmt === '169' ? 1080 : 1920}:in_range=full:out_range=tv:out_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p`,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-level', '4.2', '-g', String(FPS * 2), '-bf', '2',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((resolve, reject) => ff.on('exit', (c) => (c === 0 ? resolve() : reject(new Error('ffmpeg kode ' + c)))));
  const n = Math.round(total * FPS);
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await page.evaluate((x) => window.seek(x), i / FPS);
    const buf = await page.screenshot({ type: 'png', optimizeForSpeed: true });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 120 === 0) console.log(`[${fmt}] frame ${i}/${n} @ ${FPS} fps, ${SS}x, ${Math.round((Date.now() - t0) / 1000)} dtk`);
  }
  ff.stdin.end();
  await done;
  await page.close();
  console.log('Selesai:', out);
}
await browser.close(); server.close();
