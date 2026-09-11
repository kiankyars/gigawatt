const MODULE_KW = 50;
const CONFIGURATIONS = {
  n: [2],
  n1: [3],
  n2: [4],
  two_n: [2, 2],
  two_n1: [3, 3],
};

/** Capacity screen, not a dispatch, overload, protection or load-shedding model. */
export function redundancyModel({
  kind,
  loadKW = 100,
  maintenance = false,
  fault = false,
  busFault = false,
} = {}) {
  if (!Object.hasOwn(CONFIGURATIONS, kind)) {
    throw new RangeError(`Unknown redundancy architecture: ${kind}`);
  }
  if (!Number.isFinite(loadKW) || loadKW <= 0) {
    throw new RangeError("Load must be a finite positive number of kW.");
  }
  for (const [name, value] of Object.entries({
    maintenance,
    fault,
    busFault,
  })) {
    if (typeof value !== "boolean")
      throw new TypeError(`${name} must be boolean.`);
  }
  const counts = CONFIGURATIONS[kind];
  const dual = counts.length === 2;
  const requiredModules = Math.ceil(loadKW / MODULE_KW);
  const extraModulesPerRoute = counts[0] - requiredModules;
  const label =
    extraModulesPerRoute < 0
      ? dual
        ? "Neither path meets N"
        : "Below N"
      : dual
        ? extraModulesPerRoute === 0
          ? "2N"
          : `2(N+${extraModulesPerRoute})`
        : extraModulesPerRoute === 0
          ? "N"
          : `N+${extraModulesPerRoute}`;
  const routes = counts.map((count, routeIndex) => {
    const id = dual ? (routeIndex === 0 ? "A" : "B") : "UPS";
    const maintained = dual && maintenance && routeIndex === 0;
    const failedBus = busFault && routeIndex === 0;
    const modules = Array.from({ length: count }, (_, index) => {
      const moduleMaintenance =
        maintained || (!dual && maintenance && index === 0);
      const moduleFault =
        fault && (dual ? routeIndex === 1 && index === 0 : index === 1);
      return {
        id: `${dual ? id : "M"}${index + 1}`,
        capacityKW: MODULE_KW,
        state: moduleMaintenance
          ? "maintenance"
          : moduleFault
            ? "fault"
            : "available",
      };
    });
    const healthyCapacityKW =
      modules.filter((module) => module.state === "available").length *
      MODULE_KW;
    const capacityKW = maintained || failedBus ? 0 : healthyCapacityKW;
    return {
      id,
      modules,
      installedCapacityKW: count * MODULE_KW,
      healthyCapacityKW,
      capacityKW,
      maintained,
      failedBus,
      available: !maintained && !failedBus && capacityKW > 0,
      supportsWholeLoad: capacityKW >= loadKW,
    };
  });
  const availableCapacityKW = routes.reduce(
    (total, route) => total + route.capacityKW,
    0,
  );
  const independentFullRoutes = routes.filter(
    (route) => route.supportsWholeLoad,
  ).length;
  const canSupportLoad = availableCapacityKW >= loadKW;
  return {
    kind,
    label,
    loadKW,
    moduleKW: MODULE_KW,
    requiredModules,
    extraModulesPerRoute,
    dual,
    maintenance,
    fault,
    busFault,
    routes,
    installedCapacityKW: counts.reduce(
      (total, count) => total + count * MODULE_KW,
      0,
    ),
    availableCapacityKW,
    shortfallKW: Math.max(0, loadKW - availableCapacityKW),
    canSupportLoad,
    independentFullRoutes,
    sharingRequired: canSupportLoad && dual && independentFullRoutes === 0,
    // A capacity upper bound; never interpreted as actual delivered power.
    supportableCapacityKW: Math.min(loadKW, availableCapacityKW),
  };
}

const n = (value) =>
  Number.isInteger(value) ? String(value) : value.toFixed(1);
const esc = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (char) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        char
      ],
  );
const colors = {
  available: "var(--available, #087d69)",
  maintenance: "var(--maintenance, #a76516)",
  fault: "var(--fault, #82918c)",
  inactive: "var(--inactive-route, #b4bdb7)",
};
const text = (x, y, value, cls = "", extra = "") =>
  `<text x="${x}" y="${y}" class="${cls}" ${extra}>${esc(value)}</text>`;

function cabinet(module, x, y, width, height, compact) {
  const color = colors[module.state];
  const status =
    module.state === "maintenance"
      ? "Isolated"
      : module.state === "fault"
        ? "Failed"
        : `${MODULE_KW} kW`;
  const fontSize = compact ? 19 : 24;
  return `<g class="ur-module ur-${module.state}" data-module="${module.id}" data-state="${module.state}">
    <rect x="${x + 5}" y="${y + 5}" width="${width}" height="${height}" rx="9" fill="var(--ink, #203b32)" opacity=".06"/>
    <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="9" fill="var(--diagram-face, #fafbf7)" stroke="${color}" stroke-width="2"/>
    <rect x="${x}" y="${y}" width="${width}" height="7" rx="3" fill="${color}"/>
    ${text(x + 13, y + 28, module.id, "ur-module-id")}
    <circle cx="${x + width - 15}" cy="${y + 23}" r="4" fill="${color}"/>
    ${text(x + width / 2, y + height * 0.64, status, "ur-module-value", `text-anchor="middle" style="font-size:${fontSize}px;fill:${color}"`)}
    <path d="M${x + 14} ${y + height - 13}h${width - 28} m-${width - 28} -5h${width - 28}" stroke="${color}" opacity=".22" stroke-width="2"/>
  </g>`;
}

function wire(d, active, marker, extra = "") {
  return `<path d="${d}" fill="none" stroke="${active ? colors.available : colors.inactive}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" ${active ? "" : 'stroke-dasharray="7 7"'} ${marker ? `marker-end="url(#${marker})"` : ""} ${extra}/>`;
}

function busFaultMark(x, y, compact) {
  return `<g class="ur-bus-fault"><circle cx="${x}" cy="${y}" r="13" fill="var(--paper, #f4f3ee)" stroke="${colors.fault}" stroke-width="2"/><path d="M${x - 5} ${y - 5}l10 10 m-10 0l10 -10" stroke="${colors.fault}" stroke-width="2.5"/>${text(x, y + (compact ? 34 : 32), "Bus fault", "ur-small", 'text-anchor="middle"')}</g>`;
}

function rack(x, y, width, height, model, compact) {
  const dual = model.dual;
  let content = `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="10" fill="var(--rack-surface, #e8ede5)" stroke="var(--diagram-border, #556c62)" stroke-width="2"/>
    ${text(x + width / 2, y + 28, "IT demand", "ur-rack-title", 'text-anchor="middle"')}
    ${text(x + width / 2, y + 57, `${n(model.loadKW)} kW`, "ur-rack-value", 'text-anchor="middle"')}`;
  if (dual && compact) {
    model.routes.forEach((route, i) => {
      const px = x + 12 + i * (width / 2);
      content += wire(
        `M${i === 0 ? x : x + width} ${y + 98}H${i === 0 ? px : px + width / 2 - 24}`,
        route.available,
      );
      content += `<rect x="${px}" y="${y + 78}" width="${width / 2 - 24}" height="40" rx="4" fill="var(--diagram-face, #fafbf7)" stroke="${route.available ? colors.available : colors.inactive}" stroke-width="2"/>${text(px + (width / 2 - 24) / 2, y + 104, `PSU ${route.id}`, "ur-small", 'text-anchor="middle"')}`;
    });
  } else if (dual) {
    model.routes.forEach((route, i) => {
      const py = y + 80 + i * 66;
      content += wire(`M${x} ${py + 20}H${x + 20}`, route.available);
      content += `<rect x="${x + 20}" y="${py}" width="${width - 40}" height="40" rx="4" fill="var(--diagram-face, #fafbf7)" stroke="${route.available ? colors.available : colors.inactive}" stroke-width="2"/>${text(x + width / 2, py + 27, `PSU ${route.id}`, "ur-small", 'text-anchor="middle"')}`;
    });
  } else {
    content += `<path d="M${x + 16} ${y + height - 48}h${width - 32} m-${width - 32} 12h${width - 32} m-${width - 32} 12h${width - 32}" stroke="var(--cabinet-detail, #82958a)" stroke-width="5"/>`;
  }
  return `<g class="ur-rack">${content}</g>`;
}

function singleDiagram(model, compact, marker) {
  const route = model.routes[0];
  let output = "";
  if (compact) {
    const start = 104;
    const step = 105;
    const centerY = start + ((route.modules.length - 1) * step) / 2 + 40;
    const rackY = centerY - 75;
    const ys = route.modules.map((_, i) => start + i * step + 40);
    route.modules.forEach((module, i) => {
      output += wire(
        `M178 ${ys[i]}H228`,
        route.available && module.state === "available",
      );
      output += cabinet(module, 34, start + i * step, 144, 80, true);
    });
    output += wire(
      `M228 ${ys[0]}V${ys.at(-1)}`,
      route.available,
      null,
      'class="ur-output-bus"',
    );
    output += wire(
      `M228 ${centerY}H274`,
      route.available,
      route.available ? marker : null,
    );
    output += rack(274, rackY, 108, 150, model, true);
    output += text(34, 83, "50 kW modules", "ur-small");
    output += text(
      228,
      ys.at(-1) + 40,
      "Shared bus",
      "ur-small",
      'text-anchor="middle"',
    );
    if (route.failedBus) output += busFaultMark(228, centerY, true);
  } else {
    const firstX = 95;
    const spacing = 192;
    const busY = 326;
    route.modules.forEach((module, i) => {
      const x = firstX + i * spacing;
      output += wire(
        `M${x + 62} 266V${busY}`,
        route.available && module.state === "available",
      );
      output += cabinet(module, x, 124, 124, 142, false);
    });
    output += wire(
      `M157 ${busY}H900V242H985`,
      route.available,
      route.available ? marker : null,
      'class="ur-output-bus"',
    );
    output += text(95, 96, "50 kW modules", "ur-small");
    output += text(
      450,
      365,
      "Shared output bus",
      "ur-small",
      'text-anchor="middle"',
    );
    output += rack(985, 172, 152, 175, model, false);
    if (route.failedBus) output += busFaultMark(834, busY, false);
  }
  return output;
}

function dualDiagram(model, compact, marker) {
  let output = "";
  if (compact) {
    const rackX = 94;
    const rackY = 468;
    const rackWidth = 212;
    model.routes.forEach((route, r) => {
      const y = 119 + r * 178;
      const busY = y + 99;
      const count = route.modules.length;
      const spacing = count === 3 ? 120 : 152;
      const firstX = count === 3 ? 36 : 80;
      const centers = route.modules.map((_, i) => firstX + i * spacing + 44);
      const outerX = r === 0 ? 16 : 384;
      const psuX = r === 0 ? rackX + 12 : rackX + rackWidth - 12;
      output += text(34, y - 16, `Path ${route.id}`, "ur-path-title");
      output += text(
        366,
        y - 16,
        `${n(route.capacityKW)} kW available`,
        "ur-path-capacity",
        'text-anchor="end"',
      );
      route.modules.forEach((module, i) => {
        const x = firstX + i * spacing;
        output += wire(
          `M${x + 44} ${y + 78}V${busY}`,
          route.available && module.state === "available",
        );
        output += cabinet(module, x, y, 88, 78, true);
      });
      output += wire(
        `M${centers[0]} ${busY}H${centers.at(-1)}`,
        route.available,
        null,
        'class="ur-output-bus"',
      );
      output += wire(
        `M${centers[r === 0 ? 0 : count - 1]} ${busY}H${outerX}V${rackY + 98}H${psuX}`,
        route.available,
        route.available ? marker : null,
      );
      if (route.failedBus) output += busFaultMark(outerX + 38, busY, true);
      if (route.maintained)
        output += text(
          200,
          busY + 32,
          "Path isolated",
          "ur-maintenance",
          'text-anchor="middle"',
        );
    });
    output += rack(rackX, rackY, rackWidth, 134, model, true);
  } else {
    const rackX = 978;
    const rackY = 143;
    model.routes.forEach((route, r) => {
      const y = 83 + r * 179;
      const busY = y + 139;
      const count = route.modules.length;
      const firstX = count === 3 ? 172 : 235;
      const spacing = 185;
      const centers = route.modules.map((_, i) => firstX + i * spacing + 57);
      const outerX = r === 0 ? 834 : 888;
      const psuY = rackY + 100 + r * 66;
      output += text(36, y + 40, `Path ${route.id}`, "ur-path-title");
      output += text(36, y + 69, `${n(route.capacityKW)} kW`, "ur-small");
      output += text(36, y + 94, "available", "ur-small");
      route.modules.forEach((module, i) => {
        const x = firstX + i * spacing;
        output += wire(
          `M${x + 57} ${y + 111}V${busY}`,
          route.available && module.state === "available",
        );
        output += cabinet(module, x, y, 114, 111, false);
      });
      output += wire(
        `M${centers[0]} ${busY}H${outerX}V${psuY}H${rackX + 20}`,
        route.available,
        route.available ? marker : null,
        'class="ur-output-bus"',
      );
      if (route.failedBus) output += busFaultMark(758, busY, false);
      if (route.maintained)
        output += text(666, y + 64, "Isolated", "ur-maintenance");
    });
    output += rack(rackX, rackY, 180, 208, model, false);
  }
  return output;
}

/** Returns a complete, self-contained accessible SVG. `compact` selects a portrait geometry. */
export function renderRedundancy(model, { compact = false } = {}) {
  const width = compact ? 400 : 1200;
  const height = compact ? 650 : 450;
  const suffix = `${model.kind}-${compact ? "portrait" : "landscape"}`;
  const titleId = `ur-title-${suffix}`;
  const descId = `ur-desc-${suffix}`;
  const marker = `ur-arrow-${suffix}`;
  const status = model.canSupportLoad
    ? model.sharingRequired
      ? "Both paths needed"
      : "Capacity sufficient"
    : "Insufficient UPS capacity";
  const capacityDescription = `${n(model.availableCapacityKW)} kW available for ${n(model.loadKW)} kW demand. ${model.dual ? `${model.independentFullRoutes} of 2 paths can independently support the whole load. ` : ""}${model.canSupportLoad ? (model.sharingRequired ? "Meeting demand requires power sharing across both PSU groups." : "Available capacity can support demand.") : "Demand cannot be supported with the available UPS capacity; resulting overload behavior is not modeled."}`;
  const statusX = compact ? 200 : 1162;
  const footer = model.dual
    ? `${model.independentFullRoutes}/2 paths can carry the whole load`
    : `${n(model.availableCapacityKW)} kW available · ${n(model.loadKW)} kW required`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="${titleId} ${descId}" class="ur-svg" data-architecture="${model.kind}" data-supported="${model.canSupportLoad}">
    <title id="${titleId}">${esc(model.label)} UPS capacity and power paths</title>
    <desc id="${descId}">${esc(capacityDescription)} Module failures are assumed isolated. Each PSU group is rated to carry the full load. Aggregate capacity assumes the PSU groups can share demand within each path capacity; this does not simulate their load-sharing controls. A and B AC outputs stay separate.</desc>
    <defs><marker id="${marker}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="${colors.available}" stroke-width="2"/></marker></defs>
    <style>
      .ur-svg{width:100%;height:100%;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink, #193139)}
      .ur-svg text{fill:var(--ink, #193139);font-size:${compact ? 17 : 21}px}
      .ur-svg .ur-small{font-size:${compact ? 16 : 18}px;fill:var(--muted, #61746a)}
      .ur-svg .ur-module-id{font-size:16px;fill:var(--muted, #61746a);letter-spacing:.5px}
      .ur-svg .ur-module-value,.ur-svg .ur-path-title{font-weight:700}
      .ur-svg .ur-path-capacity{font-weight:650}
      .ur-svg .ur-rack-title{font-size:17px;font-weight:650}
      .ur-svg .ur-rack-value{font-size:${compact ? 23 : 29}px;font-weight:750}
      .ur-svg .ur-maintenance{font-size:${compact ? 16 : 18}px;fill:${colors.maintenance}}
      .ur-svg .ur-status{font-size:${compact ? 20 : 23}px;font-weight:700;fill:${model.canSupportLoad ? colors.available : colors.maintenance}}
      .ur-svg .ur-footer{font-size:${compact ? 17 : 20}px;fill:var(--muted, #61746a)}
    </style>
    ${text(statusX, compact ? 39 : 34, status, "ur-status", `text-anchor="${compact ? "middle" : "end"}"`)}
    ${model.dual ? dualDiagram(model, compact, marker) : singleDiagram(model, compact, marker)}
    ${text(compact ? 200 : 600, compact ? 633 : 441, footer, "ur-footer", 'text-anchor="middle"')}
  </svg>`;
}
