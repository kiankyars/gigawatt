const PSU =
  "https://www.advancedenergy.com/en-us/products/ac-dc-power-supply-units/power-shelves/ocp-compliant/orv3-psu/";
const BBU =
  "https://www.delta-americas.com/en-US/products/Power-Management/12018";

export const rackProducts = Object.freeze({
  "psu-hardware": {
    source: PSU,
    credit: "Advanced Energy · Artesyn ORv3",
    description:
      "Manufacturer photographs show a removable Advanced Energy 3 kW ORv3 PSU and its six-module power shelf. The PSU takes nominal 200–277 V single-phase AC and supplies 50 V DC; six modules provide 18 kW installed capacity before redundancy reserves.",
    items: [
      {
        file: "ae-orv3-psu.jpg",
        width: 4096,
        height: 4096,
        crop: "130 1090 3860 2110",
        name: "PSU module",
        rating: "3 kW",
        detail: "200–277 V AC → 50 V DC",
      },
      {
        file: "ae-orv3-shelf.jpg",
        width: 530,
        height: 530,
        crop: "12 166 510 204",
        name: "Power shelf",
        rating: "6 PSUs",
        detail: "18 kW installed capacity",
      },
    ],
  },
  "bbu-hardware": {
    source: BBU,
    credit: "Delta · Battery Backup System",
    description:
      "Delta product photographs show a removable 3 kW battery backup module and its six-module battery shelf. Delta rates the system at 15 kW and 48 V DC. The published system rating is 15 kW; the module sum does not increase that rating.",
    items: [
      {
        file: "delta-bbu-module.jpg",
        width: 756,
        height: 504,
        crop: "240 160 370 195",
        name: "BBU module",
        rating: "3 kW",
        detail: "48 V DC output",
      },
      {
        file: "delta-bbu-shelf.jpg",
        width: 756,
        height: 504,
        crop: "115 202 595 155",
        name: "Battery shelf",
        rating: "6 BBUs",
        detail: "15 kW system rating",
      },
    ],
  },
});

export function renderRackProduct(id, compact) {
  const product = rackProducts[id];
  const text = (x, y, value, size = 24, color = "var(--text)") =>
    `<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}">${value}</text>`;
  const cards = product.items
    .map((item, i) => {
      const x = compact ? 15 : 28 + i * 588,
        y = compact ? 12 + i * 303 : 34,
        w = compact ? 360 : 556,
        h = compact ? 196 : 295;
      return `<g data-product-photo="${item.file}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#fff"/><svg x="${x + 14}" y="${y + 12}" width="${w - 28}" height="${h - 24}" viewBox="${item.crop}" preserveAspectRatio="xMidYMid meet" overflow="hidden"><title>${product.credit}: ${item.name}</title><image href="../assets/references/${item.file}" width="${item.width}" height="${item.height}" preserveAspectRatio="xMidYMid meet"/></svg>${text(x + w / 2, y + h + 33, item.name, compact ? 23 : 27)}${text(x + w / 2, y + h + 68, item.rating, compact ? 28 : 37, "var(--power)")}${text(x + w / 2, y + h + 99, item.detail, compact ? 18 : 22)}</g>`;
    })
    .join("");
  return (
    cards +
    `<a href="${product.source}" target="_blank" rel="noopener">${text(compact ? 195 : 600, compact ? 654 : 532, product.credit, compact ? 14 : 18, "var(--muted)")}</a>`
  );
}
