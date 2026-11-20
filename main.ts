// news-image-20261119 — entry program (Node 22, no network).
// Copies the pre-rendered front page (entry.png, 1024x1024, 33 stories
// from Thursday 19 November 2026) to /output/entry.png, after checking
// the file is a real PNG inside the competition limits.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const out = join(outDir, "entry.png");

const buf = readFileSync(src);
const isPng = buf.subarray(0, 8).equals(
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
);
if (!isPng) throw new Error("entry.png is not a PNG file");
if (buf.length > 1048576) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}
// IHDR: width at bytes 16-19, height at 20-23 (big-endian uint32).
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
console.log(`entry.png: ${width}x${height}, ${buf.length} bytes`);

mkdirSync(outDir, { recursive: true });
copyFileSync(src, out);
// Determinism: the written file must be byte-identical to the source.
const written = readFileSync(out);
if (!written.equals(buf)) {
  throw new Error("output differs from entry.png");
}
console.log(`wrote ${out} (${statSync(out).size} bytes, byte-identical)`);
