// Online mechanism extracted without changing its paths from ups-format.html.
const esc = (value) =>
  String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;");
function label(x, y, text, klass = "diagram-label", anchor = "middle") {
  return `<text x="${x}" y="${y}" class="${klass}" text-anchor="${anchor}">${esc(text)}</text>`;
}
function acSymbol(x, y, size = 1) {
  return `<path d="M-19 0 C-12 -21 -6 -21 0 0 S12 21 19 0" class="symbol" transform="translate(${x} ${y}) scale(${size})"/>`;
}
function dcSymbol(x, y, size = 1) {
  return `<g class="symbol" transform="translate(${x} ${y}) scale(${size})"><path d="M-16 -4H16"/><path d="M-16 5H-9 M-3 5H3 M9 5H16"/></g>`;
}
function converter(x, y, kind, active = true) {
  const rectifier = kind === "rectifier";
  return `<g class="${active ? "" : "inactive"}" data-component="${kind}">
          <rect x="${x}" y="${y}" width="112" height="112" rx="5" class="equipment-face ${active ? "" : "inactive"}"/>
          <path d="M${x + 10} ${y + 102}L${x + 102} ${y + 10}" class="symbol" opacity=".45"/>
          ${rectifier ? acSymbol(x + 33, y + 35, 0.75) + dcSymbol(x + 80, y + 80, 0.8) : dcSymbol(x + 33, y + 35, 0.8) + acSymbol(x + 80, y + 80, 0.75)}
        </g>`;
}
function rack(x, y, compact = false) {
  const w = compact ? 60 : 78;
  const h = compact ? 76 : 112;
  return `<g aria-hidden="true"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="var(--rack-frame, #243e36)"/>
          ${[0, 1, 2].map((i) => `<rect x="${x + 8}" y="${y + 9 + (i * (h - 15)) / 3}" width="${w - 16}" height="${(h - 24) / 3}" rx="2" fill="var(--rack-slot, #edf2e9)"/><circle cx="${x + w - 17}" cy="${y + 9 + (i * (h - 15)) / 3 + (h - 24) / 6}" r="2.5" fill="var(--green, #097867)"/>`).join("")}
        </g>`;
}
function battery(x, y, width = 78, height = 96) {
  return `<g aria-hidden="true"><rect x="${x + width * 0.35}" y="${y - 7}" width="${width * 0.3}" height="8" rx="2" fill="var(--diagram-border, #416958)"/>
          <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="5" fill="var(--diagram-face, #f6f8f1)" stroke="var(--diagram-border, #416958)" stroke-width="2"/>
          <path d="M${x + width * 0.3} ${y + height * 0.2}h${width * 0.4} M${x + width * 0.5} ${y + height * 0.1}v${height * 0.2} M${x + width * 0.3} ${y + height * 0.78}h${width * 0.4}" class="symbol"/>
          <rect x="${x + 9}" y="${y + height * 0.4}" width="${width - 18}" height="${height * 0.17}" rx="2" fill="var(--battery-charge, #c7d9c8)"/>
        </g>`;
}
function wire(d, active, id = "") {
  return `<path d="${d}" class="wire ${active ? "active" : ""}" ${id ? `data-path="${id}"` : ""}/>`;
}
function arrow(x, y, rotate = 0) {
  return `<path d="M-5 -6L5 0L-5 6Z" class="direction" transform="translate(${x} ${y}) rotate(${rotate})"/>`;
}
export function renderOnlineUPS(out = false, compact = false) {
  const title = out
    ? "Utility unavailable. Battery supplies the DC link through its interface. The inverter continues supplying the same 100 kW AC load."
    : "Utility AC supplies the rectifier, DC link, inverter and 100 kW AC load. Battery is ready; charging is omitted.";
  let drawing;
  if (!compact) {
    drawing = `
            <rect x="240" y="36" width="654" height="400" rx="18" class="ups-enclosure"/>
            ${label(270, 67, "UPS · DOUBLE CONVERSION", "diagram-kicker", "start")}
            ${wire("M131 188H314", !out, "utility")}
            ${wire("M426 188H568", !out, "rectifier-output")}
            ${wire("M568 188H710", true, "dc-link")}
            ${wire("M822 188H1026", true, "ac-output")}
            ${wire("M139 354H383", out, "battery")}
            ${wire("M553 354H568V188", out, "battery-interface")}
            ${!out ? arrow(231, 188) + arrow(483, 188) : ""}
            ${arrow(645, 188)}${arrow(957, 188)}
            ${out ? arrow(270, 354) + arrow(568, 263, -90) : ""}
            <circle cx="91" cy="188" r="40" class="equipment-face ${out ? "inactive" : ""}"/>
            <g class="${out ? "inactive" : ""}">${acSymbol(91, 188, 1.2)}</g>
            ${label(91, 120, "Utility AC")}
            ${out ? label(91, 252, "Unavailable", "unavailable-label") : ""}
            ${converter(314, 132, "rectifier", !out)}
            ${label(370, 111, "Rectifier")}${label(370, 272, "AC → DC", "diagram-detail")}
            <circle cx="568" cy="188" r="7" class="connection"/>
            ${label(568, 130, "DC link")}

            ${converter(710, 132, "inverter")}
            ${label(766, 111, "Inverter")}${label(766, 272, "DC → AC", "diagram-detail")}
            ${rack(1026, 132)}
            ${label(1065, 111, "Protected load")}
            ${label(1065, 288, "100 kW", "diagram-value")}
            ${battery(61, 306)}
            ${label(101, 433, "UPS battery")}
            ${label(221, 333, out ? "Discharging" : "Ready", "ready-label", "start")}
            <rect x="383" y="327" width="170" height="54" rx="7" class="equipment-face"/>
            ${label(468, 360, "Battery interface", "diagram-detail")}
          `;
  } else {
    drawing = `
            <rect x="17" y="103" width="326" height="412" rx="16" class="ups-enclosure"/>
            ${label(32, 130, "UPS", "diagram-kicker", "start")}

            ${wire("M108 77V163", !out, "utility")}
            ${wire("M108 275V337", !out, "rectifier-output")}
            ${wire("M108 337V370", true, "dc-link")}
            ${wire("M108 482V588", true, "ac-output")}
            ${wire("M268 98V299", out, "battery")}
            ${wire("M248 337H108", out, "battery-interface")}
            ${!out ? arrow(108, 149, 90) + arrow(108, 301, 90) : ""}
            ${arrow(108, 541, 90)}
            ${out ? arrow(268, 271, 90) + arrow(192, 337, 180) : ""}
            <circle cx="108" cy="44" r="33" class="equipment-face ${out ? "inactive" : ""}"/>
            <g class="${out ? "inactive" : ""}">${acSymbol(108, 44)}</g>
            ${label(79, 95, "Utility AC", "diagram-detail", "end")}
            ${converter(52, 163, "rectifier", !out)}
            ${label(182, 211, "Rectifier", "diagram-detail", "start")}
            ${label(182, 235, "AC → DC", "diagram-detail", "start")}
            <circle cx="108" cy="337" r="7" class="connection"/>
            ${label(59, 346, "DC link", "diagram-kicker")}
            ${converter(52, 370, "inverter")}
            ${label(182, 418, "Inverter", "diagram-detail", "start")}
            ${label(182, 442, "DC → AC", "diagram-detail", "start")}
            ${battery(242, 25, 52, 73)}
            ${label(268, 15, "UPS battery", "diagram-detail")}
            <rect x="212" y="299" width="112" height="65" rx="6" class="equipment-face"/>
            ${label(268, 326, "Battery", "diagram-detail")}
            ${label(268, 347, "interface", "diagram-detail")}
            ${label(294, 169, out ? "Active" : "Ready", "ready-label", "start")}
            ${rack(78, 588, true)}
            ${label(166, 605, "Protected load", "diagram-detail", "start")}
            ${label(164, 644, "100 kW", "diagram-value", "start")}
          `;
  }
  return {
    svg: `<title>${esc(title)}</title>${drawing}`,
    viewBox: compact ? "0 0 360 680" : "0 0 1200 490",
  };
}
