const FRONT =
  "../assets/references/cooling-chx2000-front.png";
const INTERNAL =
  "../assets/references/cooling-chx2000-inside.jpeg";
const text = (x, y, value, cls = "svg-label", extra = "") =>
  `<text x="${x}" y="${y}" class="${cls}" ${extra}>${value}</text>`;

export function renderCDU(compact, interior = false) {
  const picture = interior ? INTERNAL : FRONT;
  const photo = compact
    ? `<rect x="97" y="7" width="178" height="230" rx="8" fill="white"/><svg x="101" y="11" width="170" height="220" viewBox="${interior ? "105 0 340 482" : "140 0 305 563"}" overflow="hidden"><image data-product-photo="coolit" href="${picture}" width="${interior ? 548 : 585}" height="${interior ? 482 : 563}"/></svg>`
    : `<rect x="33" y="15" width="325" height="360" rx="10" fill="white"/><svg x="41" y="20" width="309" height="350" viewBox="${interior ? "105 0 340 482" : "140 0 305 563"}" overflow="hidden"><image data-product-photo="coolit" href="${picture}" width="${interior ? 548 : 585}" height="${interior ? 482 : 563}"/></svg>`;
  const rows = [
    [
      "Heat exchanger",
      "2 MW thermal at 5°C approach",
    ],
    [
      "Pumps",
      "2,125 L/min at 35 psi",
    ],
    [
      "Controls and filtration",
      "Temperature · flow · pressure",
    ],
  ];
  let out = photo;
  if (compact) {
    out += text(
      186,
      257,
      "CoolIT CHx2000 · manufacturer photograph",
      "svg-small",
      'text-anchor="middle"',
    );
    rows.forEach(([name, spec], i) => {
      const y = 291 + i * 83;
      out +=
        text(22, y, name, "svg-small facility-text") +
        text(22, y + 24, spec);
    });
  } else {
    out += text(
      195,
      402,
      "Manufacturer photograph",
      "svg-small",
      'text-anchor="middle"',
    );
    rows.forEach(([name, spec], i) => {
      const y = 44 + i * 113;
      out +=
        text(427, y, name, "svg-label facility-text") +
        text(427, y + 39, spec, "svg-equation");
    });
  }
  return out;
}
