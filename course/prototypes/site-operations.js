/** Chapter 5: service, recovery and operating boundaries.
 * Physical illustrations are conceptual; named quantities are sourced in scene notes.
 * This module returns HTML so photographs retain their proportions at every viewport.
 */
const roomReference = "d12-room-and-replacement-route";
const safetyReference = "d12-safety-and-control-boundaries";
export const operationsAliases = Object.freeze({
  "space-migration": "service-envelope",
  "site-handoff": "control-boundaries",
});
export const operationsScenes = [
  {
    id: "service-envelope",
    label: "Withdraw and support the tray",
    title: "Reserve space for the tray, lift and technician.",
    pedagogical_role: "mechanism",
    reference: roomReference,
    explanation: [
      "The previous slide identified the Lenovo GB300 rack and its 29 kg compute tray. Now follow the service movement: support the tray at working height and leave room for the handling equipment and technician. Lenovo’s product guide identifies a Genie GL-8 or appropriate alternative for single-person service. The space reserved for this work is larger than the installed rack footprint.",
      "The generated illustration depicts that physical relationship, not the exact anatomy or approved removal procedure of a Lenovo tray or Genie lift. Actual service instructions determine the supported handling method, required disconnections and clearances. A service envelope belongs in the layout before adjacent equipment is fixed in place.",
    ],
  },
  {
    id: "replacement-route",
    label: "Fit the equipment around the turn",
    title: "The replacement route must fit the equipment through every turn.",
    pedagogical_role: "mechanism",
    reference: roomReference,
    explanation: [
      "Continue the same equipment movement from its working position toward receiving. A door can be wide enough for straight passage while the approach leaves insufficient room to turn the supported assembly. The complete handling envelope includes the equipment and its conveyance; the route therefore needs a swept-path check, not just the width of each opening.",
      "The plan is an original geometric teaching illustration, not the layout of either named campus. The amber region marks the turn that needs dimensional verification. Equipment size, permitted orientation, door openings, floor transitions and loading conditions determine the actual route. There is no arbitrary corridor-width rule or invented pass/fail dimension.",
    ],
  },
  {
    id: "load-path",
    label: "Trace the load into the floor",
    title:
      "A floor must support concentrated loads wherever equipment travels.",
    pedagogical_role: "comparison",
    reference: roomReference,
    explanation: [
      "Lenovo lists approximately 1,580 kg for its complete GB300 rack solution, depending on configuration. That mass is not a floor-pressure specification. Installed feet or rails and the contacts of a moving handling assembly transfer forces into a slab, panel or other floor structure in different ways.",
      "The visual compares those contact patterns without assuming that rack transport is permitted on a particular trolley or that four wheels share load equally. A structural check follows the actual equipment and handling instructions across the complete route, including local contact loads, transitions, loading dock and any raised-floor panels. A distributed floor-load rating alone cannot establish the capacity of each local contact along that route.",
    ],
  },
  {
    id: "fire-and-egress",
    label: "Separate hazards from escape routes",
    title:
      "A plant-room incident should not block the data hall’s escape route.",
    pedagogical_role: "architecture",
    reference: safetyReference,
    explanation: [
      "Place the service and escape routes in the plan alongside electrical equipment, batteries and the compute hall. The drawing gives the data hall a route to an exterior exit that does not pass through the depicted battery room. It locates the design question physically: a room arrangement can couple a hazardous event to the route people need to leave.",
      "This is a design objective, not a compliant evacuation plan. Occupancy, travel distances, number of exits, fire ratings, detection, suppression, battery chemistry and the applicable requirements determine the real design. Those details belong to the site’s fire-protection review. The conceptual plan does not establish a universal rule that every battery installation occupies a separate room.",
    ],
  },
  {
    id: "stored-energy",
    label: "Locate every source of energy",
    title: "Opening an AC feeder can leave the DC link energized.",
    pedagogical_role: "mechanism",
    reference: safetyReference,
    explanation: [
      "The power path learned in the UPS chapter now creates a service boundary. An opened AC feeder removes that contribution, but a connected battery can still supply the DC link and the capacitor can retain charge. Alternate feeds would add further boundaries in an actual installation.",
      "The circuit is conceptual and does not prescribe an isolation sequence. The useful site-design consequence is that service access, isolation points and equipment boundaries must account for every relevant energy source. A stopped load or an open upstream switch alone does not establish an energy-free condition.",
    ],
  },
  {
    id: "access-boundaries",
    label: "Separate service and control access",
    title: "Access to a rack need not grant control of the cooling plant.",
    pedagogical_role: "architecture",
    reference: safetyReference,
    explanation: [
      "A service engineer may need a physical route from receiving to an assigned rack. That job does not inherently require access to plant controls. The visual overlays an example rack-service route and a separate cooling-control boundary on the same facility, rather than treating a campus badge as one all-or-nothing permission.",
      "NIST’s operational-technology guidance considers physical and logical access alongside availability and safety. The example is a scope-of-access design, not a prescribed staffing model. Electrical, mechanical and IT work can legitimately require different access; the authorization should match the specific task.",
    ],
  },
  {
    id: "control-boundaries",
    label: "Trace a common control dependency",
    title: "One shared controller can stop two separate cooling trains.",
    pedagogical_role: "counterexample",
    reference: safetyReference,
    explanation: [
      "Operational technology monitors and controls physical equipment. In this conceptual arrangement, two separately drawn cooling trains take commands from one controller. Sending its shared stop command stops both trains in the model. Duplicated mechanical equipment has therefore not removed this control dependency.",
      "This is neither a reported outage nor a claim about a specific product. Separate permissions, local operating behavior and tested failure responses are design questions, and network segmentation alone does not prove independence. The cooling chapter handles the thermal response; this slide isolates the site’s common control authority, without inventing a shutdown time.",
    ],
    controls: [
      {
        key: "control",
        label: "Controller command",
        options: [
          ["normal", "Run both trains"],
          ["stop", "Stop both trains"],
        ],
      },
    ],
  },
];

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
  "fire-and-egress":
    "A dedicated path leads from the data hall to an exterior exit without going through the conceptual battery room.",
  "stored-energy":
    "The AC feeder is open, while a battery remains connected to the DC link and a capacitor remains across that link.",
  "access-boundaries":
    "The rack-service route is physically separate from access to the plant room and its cooling controls.",
  "control-boundaries":
    "A single controller issues commands to both cooling trains.",
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
  "fire-and-egress": [
    [337, 207, "Data hall"],
    [817, 94, "Battery room"],
    [595, 360, "Exit outside the plant rooms"],
  ],
  "stored-energy": [
    [186, 149, "AC feeder open"],
    [613, 282, "Battery connected"],
    [818, 276, "Capacitor across the DC link"],
  ],
  "access-boundaries": [
    [486, 288, "Rack-service route"],
    [880, 253, "Plant controls: separate authorization"],
  ],
  "control-boundaries": [
    [144, 174, "Shared controller"],
    [525, 141, "Train A"],
    [750, 141, "Train B"],
  ],
};
function compactFigure(id, markup, compact, running) {
  let keys = compact && compactKeys[id];
  if (keys && id === "control-boundaries")
    keys = keys.map(([x, y, label], i) => [
      x,
      y,
      i ? `${label}: ${running ? "running" : "stopped"}` : label,
    ]);
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
  if (id === "fire-and-egress") {
    markup = svg(
      id,
      `<rect x="90" y="50" width="900" height="285" rx="6" class="op-floor"/><rect x="650" y="50" width="340" height="128" class="op-hazard-zone"/><rect x="650" y="190" width="340" height="145" class="op-panel-fill"/>${[137, 205, 273, 395, 463, 531].map((x) => rack(x, 85, 43, 104)).join("")}<path d="M90 50H810M886 50H990V335H633M557 335H90V50M640 50V223M640 293V335M640 181H990" class="op-wall"/>${text(247, 280, "Data hall", "op-panel-title", "middle")}${text(815, 100, "Battery room", "op-label", "middle")}${text(815, 245, "Electrical room", "op-label", "middle")}<path d="M343 173V272Q343 288 369 288H573Q594 288 594 313V375" class="op-route-halo"/><path d="M343 173V272Q343 288 369 288H573Q594 288 594 313V375" class="op-route"/><path d="M582 358L594 380L606 358" class="op-route"/>${text(635, 386, "Exterior exit", "op-label")}<path d="M654 74V155" class="op-fire-boundary"/><path d="M676 127H953" class="op-battery-shelf"/>${[703, 765, 827, 889].map((x) => `<rect x="${x}" y="119" width="31" height="37" rx="3" class="op-battery"/><path d="M${x + 10} 115H${x + 21}" class="op-battery-terminal"/>`).join("")}`,
    );
  }
  if (id === "stored-energy") {
    markup = svg(
      id,
      `${text(108, 91, "AC feeder", "op-label", "middle")}${text(381, 91, "Rectifier", "op-label", "middle")}${text(826, 91, "DC link", "op-panel-title", "middle")}<path d="M44 190H159M220 190H310M452 190H548M452 220H495V370H548" class="op-wire"/><circle cx="167" cy="190" r="7" class="op-switch-contact"/><circle cx="213" cy="190" r="7" class="op-switch-contact"/><path d="M167 182L204 145" class="op-open-switch"/><rect x="310" y="136" width="142" height="105" rx="7" class="op-inactive-device"/>${text(381, 199, "AC → DC", "op-small", "middle")}${text(186, 259, "Open", "op-small", "middle")}<path d="M548 190H978M548 370H978M613 190V247M613 318V370M818 190V262M818 291V370" class="op-live-wire"/><rect x="551" y="247" width="125" height="71" rx="7" class="op-storage"/><path d="M596 263V299M604 270V292M623 263V299M631 270V292" class="op-battery-symbol"/>${text(613, 404, "Battery", "op-label", "middle")}<path d="M793 262H843M793 291H843" class="op-capacitor-symbol"/>${text(863, 286, "Capacitor", "op-label")}<circle cx="966" cy="190" r="5" class="op-live-dot"/><circle cx="966" cy="370" r="5" class="op-live-dot"/>${text(1012, 198, "+", "op-label", "middle")}${text(1012, 378, "−", "op-label", "middle")}${text(797, 146, "Still energized", "op-live-label", "middle")}`,
    );
  }

  if (id === "access-boundaries") {
    markup = svg(
      id,
      `${planShell(false)}<path d="M879 150H736Q683 150 683 201V270Q683 290 655 290H350V148" class="op-route-halo"/><path d="M879 150H736Q683 150 683 201V270Q683 290 655 290H350V148" class="op-route"/>${text(482, 336, "Rack-service route", "op-label", "middle")}<path d="M745 220V332H1005V220Z" class="op-control-zone"/><rect x="834" y="236" width="100" height="52" rx="4" class="op-controller"/><path d="M858 248H910M858 259H891M858 271H919" class="op-controller-detail"/>${text(880, 321, "Plant controls", "op-small", "middle")}<circle cx="758" cy="248" r="14" class="op-access-dot"/><path d="M752 248H764M758 242V254" class="op-lock-mark"/>${text(929, 207, "Separate authorization", "op-small", "middle")}`,
    );
  }
  if (id === "control-boundaries") {
    const running = state.control !== "stop";
    const color = running ? "op-water-flow" : "op-water-idle";
    const pump = (x, y, name) =>
      `<g transform="translate(${x} ${y})"><rect x="0" y="28" width="150" height="166" rx="5" class="op-plant-cabinet"/><path d="M17 50H133M17 60H133M17 70H133" class="op-slot"/><circle cx="75" cy="126" r="32" class="op-pump"/><path d="M75 94L90 130L57 142Z" class="${running ? "op-pump-active" : "op-pump-idle"}"/>${text(75, 230, name, "op-label", "middle")}${text(75, 256, running ? "Running" : "Stopped", running ? "op-run-label" : "op-stop-label", "middle")}</g>`;
    markup = svg(
      id,
      `<rect x="49" y="124" width="191" height="105" rx="9" class="op-controller"/>${text(144, 163, "Shared controller", "op-small", "middle")}${text(144, 201, running ? "RUN" : "STOP", "op-command", "middle")}<path d="M240 174H298V90H421M298 174V323H421" class="op-command-line"/><circle cx="298" cy="174" r="5" class="op-command-dot"/>${pump(450, 3, "Train A")}${pump(675, 3, "Train B")}<path d="M421 90H450M421 323H643V90H675" class="op-command-line"/><path d="M600 128H648V14H991V152M825 128H867V77H966V152" class="${color}"/>${rack(932, 152, 74, 170)}${text(969, 365, "Compute rack", "op-label", "middle")}`,
    );
    return {
      markup: `<div class="op-view" data-operation="${id}" data-state="${running ? "running" : "stopped"}">${compactFigure(id, markup, compact, running)}</div>`,
      description: `${description} Both trains are ${running ? "running" : "stopped"}; ${running ? "the illustrated cooling paths are active" : "neither illustrated train is providing cooling"}.`,
      format: "html",
    };
  }

  return {
    markup: `<div class="op-view" data-operation="${id}"${compact ? ' data-compact="true"' : ""}>${compactFigure(id, markup, compact)}</div>`,
    description,
    format: "html",
  };
}
