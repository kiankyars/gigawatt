import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const prototypes = new URL('course/prototypes/', root);
const references = new URL('course/assets/references/', root);
const sources = readdirSync(prototypes).filter(name => /\.(?:js|html)$/.test(name))
  .map(name => ({ name, text: readFileSync(new URL(name, prototypes), 'utf8') }));

// Width and height from the file header, for the formats the decks load.
function imageSize(bytes) {
  if (bytes.readUInt32BE(0) === 0x89504e47) return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
  if (bytes.toString('ascii', 0, 4) === 'RIFF' && bytes.toString('ascii', 8, 12) === 'WEBP') {
    const chunk = bytes.toString('ascii', 12, 16);
    if (chunk === 'VP8X') return [1 + bytes.readUIntLE(24, 3), 1 + bytes.readUIntLE(27, 3)];
    if (chunk === 'VP8L') {
      const bits = bytes.readUInt32LE(21);
      return [1 + (bits & 0x3fff), 1 + ((bits >> 14) & 0x3fff)];
    }
    if (chunk === 'VP8 ') return [bytes.readUInt16LE(26) & 0x3fff, bytes.readUInt16LE(28) & 0x3fff];
  }
  if (bytes[0] === 0xff && bytes[1] === 0xd8) {
    for (let i = 2; i < bytes.length;) {
      const marker = bytes[i + 1], length = bytes.readUInt16BE(i + 2);
      if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker))
        return [bytes.readUInt16BE(i + 7), bytes.readUInt16BE(i + 5)];
      i += 2 + length;
    }
  }
  return null;
}

test('slides load third-party figures from local copies, not from the publisher', () => {
  const imageUrl = /https?:\/\/[^\s"'`<>)]+?\.(?:png|jpe?g|gif|webp|avif|svg)(?=[\s"'`<>)=?#&]|$)/gi;
  const hotlinks = [];
  for (const { name, text } of sources) {
    for (const match of text.matchAll(imageUrl)) {
      const before = text.slice(Math.max(0, match.index - 400), match.index);
      const creditLink = /<a\b[^>]*$/.test(before);
      if (!creditLink) hotlinks.push(`${name}: ${match[0]}`);
    }
  }
  assert.deepEqual(hotlinks, []);
});

test('every local reference figure a slide names exists', () => {
  const missing = [];
  for (const { name, text } of sources)
    for (const [, file] of text.matchAll(/\.\.\/assets\/references\/([A-Za-z0-9._-]+\.[a-z]+)/g))
      if (!existsSync(new URL(file, references))) missing.push(`${name}: ${file}`);
  assert.deepEqual(missing, []);
});

test('localized figures match the bytes and size recorded in their provenance', () => {
  const localized = [
    'overview-google-new-albany-aisles.webp', 'overview-nvidia-nvl72-rack-front.png',
    'overview-google-tpu-v4-racks.png', 'site-lenovo-gb300-compute-tray-rear.png',
    'siting-ge-vernova-gas-turbine-cutaway.jpg', 'siting-siemens-energy-combined-cycle.jpg',
    'siting-siemens-energy-peaker-dispatch.png', 'siting-ge-vernova-dania-beach.webp',
    'workload-choukse-2025-fig1.svg',
  ];
  for (const file of localized) {
    const record = JSON.parse(readFileSync(new URL(file.replace(/\.[a-z]+$/, '.provenance.json'), references), 'utf8'));
    const bytes = readFileSync(new URL(file, references));
    assert.equal(record.asset, `course/assets/references/${file}`);
    assert.equal(record.retrieved_on, '2026-09-26', file);
    assert.match(record.original_url, /^https:\/\//, file);
    assert.ok(record.credit && record.rights, file);
    assert.equal(bytes.length, record.bytes, file);
    assert.equal(createHash('sha256').update(bytes).digest('hex'), record.sha256, file);
    if (record.dimensions) assert.deepEqual(imageSize(bytes), record.dimensions, file);
    else assert.match(bytes.toString('utf8', 0, 200), /^<svg[^>]*viewBox="0 0 1080 360"/, file);
    assert.ok(record.used_by.every(path => existsSync(new URL(path, root)) &&
      readFileSync(new URL(path, root), 'utf8').includes(`../assets/references/${file}`)), file);
  }
});
