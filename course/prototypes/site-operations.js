/** Chapter 5: service, recovery and operating boundaries.
 * Physical illustrations are conceptual; named quantities are sourced in scene notes.
 * This module returns HTML so photographs retain their proportions at every viewport.
 */
import { renderEgress } from "./site-egress.js";
export const operationsAliases = Object.freeze({
  "space-migration": "service-envelope",
  "site-handoff": "service-check",
  "phased-campus": "replacement-route",
  "room-layout": "site-purpose",
  "stored-energy": "hot-swap",
  "access-boundaries": "service-envelope",
  "control-boundaries": "service-check",
});

const esc = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const text = (x, y, words, klass = "op-label", anchor = "start") =>
  `<text x="${x}" y="${y}" class="${klass}" text-anchor="${anchor}">${esc(words)}</text>`;
const svg = (id, body, viewBox = "0 0 1100 410") =>
  `<svg class="op-diagram" viewBox="${viewBox}" role="img" aria-labelledby="${id}-title"><title id="${id}-title">${esc(descriptions[id] || id)}</title>${body}</svg>`;
const rack = (x, y, w = 48, h = 114) =>
  `<g transform="translate(${x} ${y})"><rect x="4" y="5" width="${w}" height="${h}" rx="3" class="op-shadow"/><rect width="${w}" height="${h}" rx="3" class="op-rack"/>${[1, 2, 3, 4, 5, 6].map((n) => `<path d="M8 ${(n * h) / 7}H${w - 8}" class="op-rack-slot"/>`).join("")}<circle cx="${w - 9}" cy="9" r="2.5" class="op-led"/></g>`;
const planRacks = () =>
  [98, 169, 240, 460, 531, 602].map((x) => rack(x, 86, 43, 112)).join("");
const planShell = (plantLabel = true) =>
  `<rect x="42" y="42" width="982" height="310" rx="6" class="op-floor"/><path d="M42 42H1024V352H850M776 352H42V42M717 42V120M717 190V352" class="op-wall"/>${planRacks()}<path d="M770 42V124H1024M770 191V262H1024" class="op-partition"/>${text(100, 235, "Data hall", "op-small")}${text(855, 92, "Receiving", "op-small", "middle")}${plantLabel ? text(852, 304, "Plant rooms", "op-small", "middle") : ""}`;
const image = (path, alt) =>
  `<img class="op-illustration" src="${path}" alt="${esc(alt)}" decoding="async">`;
const descriptions = {
  "service-envelope":
    "A server tray is supported on a material lift at rack height, with the technician standing beside it and space reserved for withdrawal.",
  "replacement-route":
    "A plan follows the handling assembly out of a rack row, around a corridor turn, and toward receiving. A highlighted swept envelope occupies the turning area beside the door.",
  "load-path":
    "Installed supports and moving wheels concentrate loads at their contacts with the floor. Lenovo specifies approximately 1.58 tonnes for the complete GB300 rack solution.",

};

const compactKeys = {
  "replacement-route": [
    [357, 132, "Tray + lift"],
    [684, 264, "Turning envelope"],
    [856, 151, "Receiving dock"],
  ],
  "load-path": [
    [260, 243, "Installed supports"],
    [820, 262, "Moving wheels"],
  ],

};
function compactFigure(id, markup, compact) {
  let keys = compact && compactKeys[id];
  if (!keys) return markup;
  const markers = keys
    .map(
      ([x, y], i) =>
        `<g class="op-mobile-marker"><circle cx="${x}" cy="${y}" r="31"/><text class="op-marker-number" x="${x}" y="${y + 11}" text-anchor="middle">${i + 1}</text></g>`,
    )
    .join("");
  return `<div class="op-compact-figure">${markup.replace("</svg>", markers + "</svg>")}<div class="op-mobile-key">${keys.map(([, , label], i) => `<div><b>${i + 1}</b><span>${esc(label)}</span></div>`).join("")}</div></div>`;
}

export function renderOperations(id, state = {}, compact = false) {
  if (id === "fire-and-egress") return renderEgress(state);
  const description = descriptions[id];
  if (!description) return null;
  let markup = "";
  if (id === "service-envelope") {
    markup = `<div class="op-service op-service-full"><figure>${image("../assets/generated/site-tray-service.png", "Illustration of a generic tray supported on a material lift at working height beside a data center rack.")}</figure></div>`;
  }
  if (id === "replacement-route") {
    markup = svg(
      id,
      `${planShell()}<path d="M357 132V270Q357 292 379 292H663Q690 292 690 267V166Q690 152 714 152H854" class="op-route-halo"/><path d="M357 132V270Q357 292 379 292H663Q690 292 690 267V166Q690 152 714 152H854" class="op-route"/><path d="M824 141L847 152L824 163" class="op-route"/><path d="M612 254Q655 262 688 200L711 208Q709 301 631 332Z" class="op-sweep"/><g transform="translate(649 241) rotate(-44)"><rect x="-20" y="-39" width="40" height="78" rx="4" class="op-cart"/><path d="M-17 -29H17M-17 29H17" class="op-cart-detail"/></g>${text(357, 110, "Tray + lift", "op-small", "middle")}${text(788, 232, "Turning envelope", "op-label")}<path d="M775 235L715 259" class="op-leader"/>${text(875, 171, "Dock", "op-small", "middle")}`,
    );
  }
  if (id === "load-path") {
    const floor = (x) =>
      `<g transform="translate(${x} 0)"><path d="M40 273L105 247H435L400 285Z" class="op-slab-top"/><path d="M40 273L400 285V317L40 306Z" class="op-slab-front"/><path d="M400 285L435 247V278L400 317Z" class="op-slab-side"/></g>`;
    markup = `<div class="op-floor-comparison">${svg(id, `${floor(25)}${floor(570)}<path d="M0 0V360" transform="translate(548 20)" class="op-divider"/>${text(268, 43, "Installed supports", "op-panel-title", "middle")}${text(815, 43, "Moving equipment", "op-panel-title", "middle")}<g transform="translate(196 68)"><rect width="133" height="176" rx="3" class="op-cabinet"/>${Array.from({ length: 8 }, (_, i) => `<path d="M12 ${19 + i * 18}H121" class="op-slot"/>`).join("")}<path d="M18 177V193M112 177V193" class="op-support"/><path d="M6 193H30M100 193H124" class="op-support"/></g><path d="M213 271V293M308 271V293" class="op-force"/><g transform="translate(756 88)"><rect x="0" y="0" width="133" height="130" rx="4" class="op-cabinet"/><path d="M-17 139H150M-17 139V162M150 139V162" class="op-support"/><circle cx="2" cy="173" r="16" class="op-wheel"/><circle cx="132" cy="173" r="16" class="op-wheel"/><circle cx="2" cy="173" r="5" class="op-wheel-hub"/><circle cx="132" cy="173" r="5" class="op-wheel-hub"/></g><path d="M758 282V305M888 284V307" class="op-force"/>`)}</div>`;
  }

  return {
    markup: `<div class="op-view" data-operation="${id}"${compact ? ' data-compact="true"' : ""}>${compactFigure(id, markup, compact)}</div>`,
    description,
    format: "html",
  };
}
