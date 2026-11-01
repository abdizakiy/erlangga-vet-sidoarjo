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

const FPS = 30;
const preview = process.argv.includes('--preview');
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
  await page.setViewport({ ...size, deviceScaleFactor: 1 });
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
  const frames = path.join(here, 'frames-live-' + fmt);
  await rm(frames, { recursive: true, force: true });
  await mkdir(frames, { recursive: true });
  const n = Math.round(total * FPS);
  for (let i = 0; i < n; i++) {
    await shot(page, i / FPS, path.join(frames, String(i).padStart(4, '0') + '.jpg'), { type: 'jpeg', quality: 93 });
    if (i % 90 === 0) console.log(`[${fmt}] frame ${i}/${n}`);
  }
  await page.close();
  const out = path.join(here, `erlangga-live-${fmt === '169' ? '16x9' : '9x16'}.mp4`);
  await new Promise((resolve, reject) => {
    const ff = spawn(ffmpegPath, ['-y', '-framerate', String(FPS), '-i', path.join(frames, '%04d.jpg'),
      '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', '-shortest',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS),
      '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', out], { stdio: 'inherit' });
    ff.on('exit', (c) => (c === 0 ? resolve() : reject(new Error('ffmpeg kode ' + c))));
  });
  await rm(frames, { recursive: true, force: true });
  console.log('Selesai:', out);
}
await browser.close(); server.close();
