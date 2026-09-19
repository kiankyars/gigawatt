// The Markdown remains the single source for narration and the readable notes page.
export const SPEAKER_NOTES_URL = new URL('../SPEAKER_NOTES.md', import.meta.url);
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

export function parseSpeakerNotes(markdown) {
  const notes = new Map();
  let keys = [], lines = [];
  const flush = () => {
    const text = lines.join('\n').trim();
    if (text) for (const key of keys) {
      if (notes.has(key)) throw new Error(`Duplicate speaker note: ${key}`);
      notes.set(key, text);
    }
    keys = []; lines = [];
  };
  for (const line of markdown.split(/\r?\n/)) {
    const marker = line.match(/^\s*<!--\s*speaker:\s*(.*?)\s*-->\s*$/);
    if (marker) {
      flush();
      keys = marker[1].split(/\s+/).filter(Boolean);
      if (keys.some(key => !/^[a-z0-9-]+#[a-z0-9-]+$/.test(key))) throw new Error('Invalid speaker-note slide ID');
    } else if (/^## /.test(line)) flush();
    else if (keys.length) lines.push(line);
  }
  flush();
  return notes;
}

export function speakerNoteKey(snapshot) {
  if (!snapshot?.href) return '';
  const url = new URL(snapshot.href);
  const file = url.pathname.split('/').pop().replace(/(?:-format)?\.html$/, '');
  const deck = ({terminology:'primer', orientation:'overview', workload:'workloads', site:'site-design'})[file] || file;
  let scene = snapshot.sceneId;
  if (!scene) { try { scene = decodeURIComponent(url.hash.slice(1)); } catch { return ''; } }
  return /^[a-z0-9-]+$/.test(scene || '') ? `${deck}#${scene}` : '';
}

function inline(text) {
  // Keep link labels for reading aloud, with no URLs or links to distract the presenter.
  return escapeHTML(text.replace(/!?\[([^\]]+)\]\([^\s)]+\)/g, '$1'))
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}

export function renderSpeakerNotes(markdown) {
  return markdown.split(/\n\s*\n/).flatMap(block => {
    const text = block.trim();
    if (!text || /^(?:Sources?(?: and provenance)?|For the investment structure):/i.test(text) || /^<!--/.test(text)) return [];
    if (/^### /.test(text)) return [`<h3>${inline(text.replace(/^### /, ''))}</h3>`];
    if (/^(?:[-*] |\d+\. )/.test(text)) {
      const tag = /^\d+\./.test(text) ? 'ol' : 'ul';
      return [`<${tag}>${text.split(/\n(?=[-*] |\d+\. )/).map(item => `<li>${inline(item.replace(/^(?:[-*] |\d+\. )/, '').replace(/\n/g, ' '))}</li>`).join('')}</${tag}>`];
    }
    return [`<p>${inline(text.replace(/^> ?/gm, '').replace(/\n/g, ' '))}</p>`];
  }).join('');
}
