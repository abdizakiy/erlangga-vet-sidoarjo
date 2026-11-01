// Render promo.html menjadi MP4 9:16 (1080x1920, 30 fps) dan gambar sampul.
//
//   npm install
//   python3 build-promo.py        (jika index.html berubah)
//   node render.mjs               (video penuh)
//   node render.mjs --preview     (hanya beberapa frame contoh ke folder preview/)
//
// Butuh Google Chrome terpasang. Atur CHROME_PATH jika letaknya berbeda.
import puppeteer from 'puppeteer-core';
import ffmpegPath from 'ffmpeg-static';
import { spawn } from 'node:child_process';
import { mkdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(chrome)) throw new Error('Chrome tidak ditemukan di ' + chrome + '. Atur CHROME_PATH.');

const FPS = 30;
const preview = process.argv.includes('--preview');

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox', '--hide-scrollbars', '--font-render-hinting=none'] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(here, 'promo.html')).href, { waitUntil: 'networkidle0' });
await page.evaluate(() => window.ready);
const total = await page.evaluate(() => window.TOTAL);

async function shot(t, file, opts) {
  await page.evaluate((x) => window.seek(x), t);
  await page.screenshot({ path: file, ...opts });
}

if (preview) {
  const dir = path.join(here, 'preview');
  await rm(dir, { recursive: true, force: true });
  await mkdir(dir, { recursive: true });
  for (const t of [0.4, 2.2, 3.9, 6.5, 9.0, 12.5, 16.2, 19.0, 20.5, 21.5]) {
    await shot(t, path.join(dir, `t${String(t).replace('.', '_')}.png`), { type: 'png' });
  }
  await browser.close();
  console.log('Pratinjau tersimpan di', dir);
  process.exit(0);
}

const frames = path.join(here, 'frames');
await rm(frames, { recursive: true, force: true });
await mkdir(frames, { recursive: true });
const n = Math.round(total * FPS);
for (let i = 0; i < n; i++) {
  await shot(i / FPS, path.join(frames, String(i).padStart(4, '0') + '.jpg'), { type: 'jpeg', quality: 94 });
  if (i % 60 === 0) console.log(`frame ${i}/${n}`);
}
await shot(2.4, path.join(here, 'erlangga-promo-sampul.png'), { type: 'png' });
await browser.close();

const out = path.join(here, 'erlangga-promo-9x16.mp4');
await new Promise((resolve, reject) => {
  const ff = spawn(ffmpegPath, [
    '-y', '-framerate', String(FPS), '-i', path.join(frames, '%04d.jpg'),
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-r', String(FPS), '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', out,
  ], { stdio: 'inherit' });
  ff.on('exit', (c) => (c === 0 ? resolve() : reject(new Error('ffmpeg keluar dengan kode ' + c))));
});
await rm(frames, { recursive: true, force: true });
console.log('Selesai:', out);
