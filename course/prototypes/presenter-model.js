// Pure helpers for the shared presenter window and its one-slide preview.
export const PRESENTER_PROTOCOL = 'gigawatt-presenter-v1';
export const PREVIEW_PARAMETER = 'presenter-preview';

export function previewURL(href, index) {
  if (!Number.isSafeInteger(index) || index < 0) throw new RangeError('Invalid preview slide');
  const url = new URL(href);
  if (!['http:', 'https:'].includes(url.protocol)) throw new TypeError('Presenter needs an HTTP page');
  url.searchParams.set(PREVIEW_PARAMETER, String(index));
  return url.href;
}

export function isPresenterMessage(event, peer, origin, session) {
  return !!peer && event.source === peer && event.origin === origin
    && event.data?.protocol === PRESENTER_PROTOCOL && event.data.session === session;
}

export function slideSelection(doc) {
  const select = doc.querySelector('footer.course-slide-navigation select');
  if (!select || !select.options.length) return null;
  return {
    index: select.selectedIndex,
    slides: Array.from(select.options, option => option.textContent.trim()),
  };
}

export function requestedPreview(href, inFrame) {
  if (!inFrame) return null;
  const value = new URL(href).searchParams.get(PREVIEW_PARAMETER);
  return value !== null && /^(0|[1-9]\d*)$/.test(value) && Number.isSafeInteger(Number(value)) ? Number(value) : null;
}
