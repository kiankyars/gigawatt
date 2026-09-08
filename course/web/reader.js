const DATA = JSON.parse(document.getElementById("expanded-data").textContent);
const $ = (id) => document.getElementById(id);
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const asList = (value) => (Array.isArray(value) ? value : value ? [value] : []);
const prose = (value) =>
  asList(value)
    .map((p) => `<p>${esc(p)}</p>`)
    .join("");
const fmt = (n, d = 1) =>
  Number(n).toLocaleString("en-US", { maximumFractionDigits: d });
const LESSONS = DATA.lessons,
  byLesson = new Map(LESSONS.map((l, i) => [l.id, i]));
const domainById = new Map(DATA.domains.map((d) => [d.id, d]));
const sourcesById = new Map(DATA.sources.map((s) => [s.id, s]));
let current = 0,
  lookupMode = false;
const drafts = new Map();
const ART = {
  campus: {
    file: "campus-cutaway.png",
    title: "THE CAMPUS IN CONTEXT",
    alt: "Conceptual cutaway showing an electrical yard on the left, server rows in the building, and heat-rejection equipment on the right.",
    parts: [
      [
        "Power enters",
        "Locate the yard and electrical room on the left. A supply agreement alone cannot establish this physical path.",
      ],
      [
        "Work happens",
        "The central racks host computing and support equipment. Their useful output also depends on data and software.",
      ],
      [
        "Heat leaves",
        "The mechanical yard returns heat to the environment. Installed capacity depends on ambient and operating conditions.",
      ],
    ],
  },
  rack: {
    file: "rack-anatomy.png",
    title: "RACK → TRAY → DEVICES",
    alt: "Illustrative open AI rack with power shelves, switching hardware, a coolant manifold and a pulled-out compute tray with copper cold plates.",
    parts: [
      [
        "Power hardware",
        "The upper shelves illustrate power-conversion equipment. Use the exact line diagram for voltages and protection boundaries.",
      ],
      [
        "Communication",
        "Switching hardware coordinates devices. A physical cable bundle does not specify logical connectivity or usable bandwidth.",
      ],
      [
        "Compute and cooling",
        "The exposed tray shows where cold plates meet devices. The geometry and piping are illustrative, not an OEM assembly drawing.",
      ],
    ],
  },
  cooling: {
    file: "cooling-cutaway.png",
    title: "THE PHYSICAL HEAT PATH",
    alt: "A compute tray, an open coolant distribution cabinet with a plate heat exchanger, and an outdoor dry cooler, shown as three separate equipment groups.",
    parts: [
      [
        "Capture",
        "Cold plates collect device heat into a liquid circuit. Other equipment may still need an air path.",
      ],
      [
        "Transfer",
        "The plate heat exchanger transfers heat between separate circuits. Its fluids do not mix.",
      ],
      [
        "Reject",
        "The cooler transfers heat to outdoor air. A heat balance alone does not establish its performance envelope.",
      ],
    ],
  },
  power: {
    file: "power-equipment.png",
    title: "DISTINCT ELECTRICAL FUNCTIONS",
    alt: "Conceptual electrical-room equipment: a transformer, switchgear, UPS and battery cabinets, and enclosed busway near a server rack.",
    parts: [
      [
        "Transform and isolate",
        "The transformer changes voltage; switchgear provides controlled interruption and isolation. They solve different problems.",
      ],
      [
        "Bridge a disturbance",
        "Power electronics and energy storage have separate output-power and usable-energy constraints.",
      ],
      [
        "Distribute",
        "Busway carries power toward loads. This equipment plate does not specify a circuit or an installation procedure.",
      ],
    ],
  },
  network: {
    file: "network-equipment.png",
    title: "COMPUTE IS PART OF A CLUSTER",
    alt: "Generic compute rack, two fabric switch cabinets, a storage rack and a smaller management cabinet, linked by illustrative cable bundles.",
    parts: [
      [
        "Compute",
        "Devices need timely communication and data to make useful progress. A powered device can still be waiting.",
      ],
      [
        "Fabric",
        "Switches connect communication endpoints. The logical topology and traffic pattern determine shared constraints.",
      ],
      [
        "Storage and control",
        "Persistent data, checkpoints and management have distinct roles; their dependencies must be tested too.",
      ],
    ],
  },
};
function artFor(l) {
  if (l.image && ART[l.image]) return ART[l.image];
  const d = l.domain;
  return ART[
    ["D04", "D05", "D06"].includes(d)
      ? "power"
      : ["D07"].includes(d)
        ? "rack"
        : ["D08", "D09", "D02"].includes(d)
          ? "network"
          : ["D10", "D11"].includes(d)
            ? "cooling"
            : "campus"
  ];
}
function renderContents() {
  const q = $("search").value.trim().toLowerCase(),
    terms = q.split(/\s+/).filter(Boolean);
  const filtered = LESSONS.filter((l) =>
    terms.every((t) => JSON.stringify(l).toLowerCase().includes(t)),
  );
  $("lesson-count").textContent = `${LESSONS.length} lessons`;
  $("search-status").textContent = q
    ? `${filtered.length} matching lessons`
    : "A connected system, one question at a time.";
  $("contents").innerHTML =
    DATA.domains
      .concat([{ id: "capstone", title: "Put the system together" }])
      .map((d) => {
        const ls = filtered.filter((l) => l.domain === d.id);
        if (!ls.length) return "";
        return `<section class="domain-group"><h3><span>${esc(d.id === "capstone" ? "CASE" : d.id)}</span>${esc(d.title)}</h3>${ls.map((l) => `<button class="lesson-link${LESSONS[current]?.id === l.id && !lookupMode ? " active" : ""}" data-lesson="${esc(l.id)}" ${LESSONS[current]?.id === l.id && !lookupMode ? 'aria-current="page"' : ""}>${esc(l.title)}</button>`).join("")}</section>`;
      })
      .join("") ||
    '<p class="muted">No matching lessons. Try a shorter term.</p>';
  $("contents")
    .querySelectorAll("[data-lesson]")
    .forEach((b) => b.addEventListener("click", () => go(b.dataset.lesson)));
  renderGlossary(q);
}
function renderGlossary(query = "") {
  const items = DATA.glossary.filter((g) =>
    `${g.term} ${g.definition}`.toLowerCase().includes(query),
  );
  $("glossary").innerHTML =
    `<div class="glossary-grid">${items.map((g) => `<article class="glossary-card"><h2>${esc(g.term)}</h2><p>${esc(g.definition)}</p><button data-lesson="${esc(g.lesson)}">Read the explanation →</button></article>`).join("")}</div>`;
  $("glossary")
    .querySelectorAll("[data-lesson]")
    .forEach((b) => b.addEventListener("click", () => go(b.dataset.lesson)));
}
function modeLookup(value) {
  lookupMode = value;
  $("lookup").hidden = !value;
  $("lesson").hidden = value;
  $("lookup-toggle").setAttribute("aria-pressed", String(value));
  renderContents();
  if (value) {
    window.scrollTo({ top: 0, behavior: "instant" });
    $("lookup-title").tabIndex = -1;
    $("lookup-title").focus({ preventScroll: true });
  }
}
function closeRail() {
  $("sidebar").classList.remove("open");
  $("contents-toggle").setAttribute("aria-expanded", "false");
}
function go(id, historyMode = "push") {
  if (!byLesson.has(id)) id = LESSONS[0].id;
  const previous = LESSONS[current];
  if (previous && $("response")) drafts.set(previous.id, $("response").value);
  current = byLesson.get(id);
  lookupMode = false;
  $("lookup").hidden = true;
  $("lesson").hidden = false;
  $("lookup-toggle").setAttribute("aria-pressed", "false");
  if (historyMode !== "none" && location.hash !== `#${id}`)
    history[historyMode === "replace" ? "replaceState" : "pushState"](
      null,
      "",
      `#${id}`,
    );
  renderLesson();
  renderContents();
  closeRail();
  window.scrollTo({ top: 0, behavior: "instant" });
  $("lesson").focus({ preventScroll: true });
}
function renderLesson() {
  const l = LESSONS[current],
    d = domainById.get(l.domain),
    art = artFor(l);
  document.title = `${l.title} — GIGAWATT`;
  $("eyebrow").textContent =
    `${String(current + 1).padStart(2, "0")} / ${d?.title || "Integrated case"}`;
  $("title").textContent = l.title;
  $("summary").textContent = l.summary;
  $("question").textContent = l.question;
  $("lesson-meta").innerHTML =
    `<span>${esc(l.domain === "capstone" ? "Integrated practice" : l.domain)}</span><span>Authored draft</span><span>Worked example + transfer practice</span>`;
  $("teaching-image").src = `assets/${art.file}`;
  $("teaching-image").alt = art.alt;
  $("image-index").textContent = art.title;
  $("image-caption").textContent =
    "GPT ImageGen illustration of a hypothetical system. Equipment geometry is illustrative; exact relationships and quantities are explained below.";
  $("anatomy").innerHTML = art.parts
    .map(
      ([title, body], i) =>
        `<button aria-pressed="false" data-part="${i}"><b>${i + 1}. ${esc(title)}</b><span>${esc(body)}</span></button>`,
    )
    .join("");
  $("anatomy")
    .querySelectorAll("button")
    .forEach((b) =>
      b.addEventListener("click", () => {
        const active = b.getAttribute("aria-pressed") === "true";
        $("anatomy")
          .querySelectorAll("button")
          .forEach((x) => x.setAttribute("aria-pressed", "false"));
        b.setAttribute("aria-pressed", String(!active));
        $("image-index").textContent = active
          ? art.title
          : art.parts[Number(b.dataset.part)][0].toUpperCase();
      }),
    );
  $("prose").innerHTML = l.sections
    .map(
      (s, i) =>
        `<section class="reading-section" id="section-${i + 1}"><h2>${esc(s.heading)}</h2>${prose(s.paragraphs)}</section>`,
    )
    .join("");
  const lane = d?.lane || "delivery";
  $("locator").innerHTML = [
    ["foundations", "Brief"],
    ["power", "Power"],
    ["work", "Work"],
    ["heat", "Heat"],
    ["delivery", "Operate"],
  ]
    .map(
      ([id, title]) =>
        `<span class="${id === lane ? "active" : ""}">${title}</span>`,
    )
    .join("");
  $("takeaway").textContent = l.takeaway;
  $("objective-tags").innerHTML =
    `Objectives<br>${l.objectives.map((o) => `<span>${esc(o)}</span>`).join("")}`;
  const visual = l.visual;
  $("concept").hidden = !visual;
  if (visual) {
    $("concept").innerHTML =
      `<div class="eyebrow">THE MECHANISM AT A GLANCE</div><h2 id="concept-title">${esc(visual.title)}</h2><div class="concept-grid">${visual.nodes.map((n, i) => `<div class="concept-node"><span>${String(i + 1).padStart(2, "0")}</span><h3>${esc(n.label)}</h3><p>${esc(n.detail)}</p></div>`).join("")}</div><p class="boundary">Read these roles with the explanation above. The cards summarize relationships; their order and spacing do not specify a physical circuit or a quantitative flow scale.</p>`;
  }
  const w = l.worked_example;
  $("worked").innerHTML =
    `<div class="eyebrow">FOLLOW A COMPLETE EXAMPLE</div><h2 id="worked-title">${esc(w.title)}</h2><div class="givens">${prose(w.givens)}</div><ol>${w.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol><p class="result">${esc(w.result)}</p><p class="boundary">${esc(w.boundary)}</p>`;
  $("consequences").innerHTML =
    `<section><h2>The tradeoff</h2>${prose(l.tradeoff)}</section><section><h2>When the situation changes</h2>${prose(l.failure)}</section>`;
  const p = l.practice;
  $("practice").innerHTML =
    `<div class="eyebrow">PREDICT · CALCULATE · EXPLAIN</div><h2 id="practice-title">Apply the idea</h2>${prose(p.question)}<label for="response">Your reasoning — private to this open page</label><textarea id="response" placeholder="State the boundary, work through the change, and name what remains unknown."></textarea><details><summary>Reveal the worked answer</summary><div><p class="answer">${esc(p.answer)}</p>${prose(p.explanation)}</div></details>`;
  $("response").value = drafts.get(l.id) || "";
  $("evidence").innerHTML =
    `<h2 id="evidence-title">Where the explanation comes from</h2><p class="boundary">Examples marked hypothetical are original teaching scenarios. Source review is limited to the scope recorded below; listing a document does not verify every linked claim or establish an installed deployment.</p><details><summary>${l.source_ids.length} source connections and reading limits</summary>${l.source_notes
      .map((note) => {
        const s = sourcesById.get(note.id);
        return s
          ? `<div class="source"><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>${esc(s.publisher)} · ${esc(s.reviewed_on || "Review date not recorded")} · ${esc(s.review_status?.replaceAll("_", " ") || "reading scope in notes")}</p><p>${esc(note.claim)}</p><p>${esc(note.limits)}</p><p><a href="../research/sources/${esc(note.id)}.md">Local source note ↗</a></p></div>`
          : "";
      })
      .join("")}</details>`;
  $("position").textContent = `${current + 1} / ${LESSONS.length}`;
  $("previous").disabled = current === 0;
  $("next").textContent =
    current === LESSONS.length - 1 ? "Back to start ↻" : "Next lesson →";
  renderLab(l);
}
function control(id, label, min, max, step, value, unit) {
  return `<div class="lab-control"><label for="${id}">${esc(label)} <output id="${id}-value">${value} ${unit}</output></label><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}" data-unit="${unit}"></div>`;
}
function flowRow(label, nodes) {
  return `<div><div class="diagram-label">${esc(label)}</div><div class="diagram-row">${nodes.map((n, i) => `${i ? '<span class="arrow" aria-hidden="true">→</span>' : ""}<span>${esc(n)}</span>`).join("")}</div></div>`;
}
function barChart(rows, max, label) {
  return `<div class="bars" role="img" aria-label="${esc(label)}">${rows.map(([title, value, color]) => `<div class="bar-item"><div class="bar-label"><span>${esc(title)}</span><b>${fmt(value)}</b></div><div class="bar-track"><div style="width:${Math.max(0, (value / max) * 100)}%;background:${color}"></div></div></div>`).join("")}</div>`;
}
function renderLab(l) {
  let type =
    l.lab ||
    {
      D01: "energy",
      D02: "roofline",
      D03: "energy",
      D04: "dc",
      D05: "continuity",
      D06: "dc",
      D07: "roofline",
      D08: "network",
      D09: "checkpoint",
      D10: "heat",
      D11: "heat",
      D12: "capacity",
      D13: "capacity",
      D14: "continuity",
      D15: "capacity",
      capstone: "capacity",
    }[l.domain];
  const spec = {
    energy: [
      "The same peak, a different energy bill",
      "Before moving a control, predict what changes: the height of the power trace or its area?",
    ],
    acdc: [
      "480 V three-phase AC versus 800 V DC",
      "Hold delivered real power fixed. Distinguish current in each conductor from the heat produced by all conductors.",
    ],
    dc: [
      "Move the conversion boundary",
      "Compare topology separately from current arithmetic. A change in distribution voltage cannot by itself prove an efficiency or cost claim.",
    ],
    heat: [
      "Carry the heat, then reject it",
      "Predict how much water flow is needed when the permitted temperature rise changes. The heat duty stays fixed.",
    ],
    network: [
      "A port rate is not a job rate",
      "Hold the payload fixed. Predict how link rate and achieved useful fraction change an ideal transfer time.",
    ],
    roofline: [
      "Two ceilings on the same work",
      "Arithmetic intensity measures operations per byte transferred from the specified memory. Which ceiling binds first?",
    ],
    continuity: [
      "Power survives. Does the service?",
      "Stored energy, inverter power and cooling support answer three different questions. Change one at a time.",
    ],
    checkpoint: [
      "Save too often or repeat too much",
      "Longer intervals reduce checkpoint overhead but increase expected lost progress. Compare the two terms.",
    ],
    capacity: [
      "Count complete service paths",
      "All limits use the same hypothetical rack load. A larger electrical budget does not automatically create commissioned racks.",
    ],
  }[type];
  if (!spec) {
    $("lab").hidden = true;
    return;
  }
  $("lab").hidden = false;
  let controls = "",
    extra = "";
  if (type === "energy")
    controls =
      control("lab-power", "Constant load", 1, 20, 1, 5, "MW") +
      control("lab-hours", "Duration", 1, 24, 1, 8, "h");
  if (type === "dc") {
    controls =
      control("lab-kw", "DC load", 50, 300, 10, 100, "kW") +
      control("lab-volts", "DC distribution voltage", 48, 800, 1, 48, "V");
    extra =
      '<div class="segmented" aria-label="Illustrative power architecture"><button data-arch="ac" aria-pressed="true">AC to the rack</button><button data-arch="hybrid" aria-pressed="false">AC + DC sidecar</button><button data-arch="facility" aria-pressed="false">Broader facility DC</button></div><div id="architecture"></div>';
  }
  if (type === "acdc") {
    controls =
      control("lab-kw", "Delivered real power", 50, 300, 10, 100, "kW") +
      control("lab-volts", "DC pair voltage", 400, 1000, 1, 800, "V") +
      control("lab-pf", "AC power factor", 0.7, 1, 0.01, 1, "") +
      control("lab-resistance", "Resistance per conductor", 1, 20, 1, 10, "mΩ");
    extra =
      '<div class="segmented" aria-label="Illustrative power architecture"><button data-arch="ac" aria-pressed="true">AC to the rack</button><button data-arch="hybrid" aria-pressed="false">AC + DC sidecar</button><button data-arch="facility" aria-pressed="false">Broader facility DC</button></div><div id="architecture"></div>';
  }
  if (type === "heat")
    controls =
      control("lab-duty", "IT heat captured", 50, 300, 10, 100, "kW") +
      control("lab-delta", "Water temperature rise", 5, 20, 1, 10, "°C") +
      control("lab-aux", "Auxiliary work within boundary", 0, 50, 5, 20, "kW");
  if (type === "network")
    controls =
      control("lab-payload", "Payload (decimal)", 10, 500, 10, 100, "GB") +
      control("lab-rate", "Aggregate link rate", 100, 800, 100, 400, "Gb/s") +
      control("lab-eff", "Achieved useful fraction", 25, 100, 5, 80, "%");
  if (type === "roofline")
    controls =
      control(
        "lab-intensity",
        "Arithmetic intensity",
        10,
        400,
        10,
        50,
        "FLOP/byte",
      ) + control("lab-bandwidth", "Memory bandwidth", 1, 5, 0.5, 2, "TB/s");
  if (type === "continuity")
    controls =
      control(
        "lab-energy",
        "Usable stored DC energy",
        50,
        500,
        25,
        250,
        "kWh",
      ) +
      control(
        "lab-inverter",
        "Inverter output limit",
        500,
        2000,
        100,
        1200,
        "kW",
      ) +
      '<div class="lab-control"><label for="lab-cooling">Cooling and control supply</label><select id="lab-cooling"><option value="0">Unsupported auxiliary path</option><option value="1">Electrical support supplied</option></select></div>';
  if (type === "checkpoint")
    controls =
      control(
        "lab-interval",
        "Useful-work checkpoint interval",
        60,
        3600,
        30,
        900,
        "s",
      ) + control("lab-checkpoint", "Checkpoint pause", 5, 60, 5, 30, "s");
  if (type === "capacity")
    controls =
      control("lab-overhead", "Site auxiliary draw", 10, 35, 1, 20, "MW") +
      control(
        "lab-cooling-mw",
        "Cooling limit at IT boundary",
        40,
        90,
        5,
        60,
        "MW",
      ) +
      control(
        "lab-accepted",
        "Accepted rack paths",
        400,
        1000,
        50,
        900,
        "racks",
      );
  $("lab").innerHTML =
    `<div class="eyebrow">TEST A BOUNDED MODEL</div><h2 id="lab-title">${spec[0]}</h2><p class="lab-intro">${spec[1]}</p>${extra}<div class="lab-controls">${controls}</div><div id="lab-graphic"></div><div id="lab-output" class="lab-output" role="status"></div><p id="lab-boundary" class="boundary"></p>`;
  if (type === "dc" || type === "acdc") {
    const architectures = {
      ac: [
        "Facility AC",
        "Rack AC/DC",
        "Low-voltage DC",
        "Point-of-load conversion",
      ],
      hybrid: [
        "Existing facility AC",
        "Sidecar AC/DC",
        "800 V DC segment",
        "Near-load DC/DC",
      ],
      facility: [
        "Upstream AC service",
        "Facility conversion",
        "800 V DC distribution",
        "Near-load DC/DC",
      ],
    };
    const notes = {
      ac: "Power conversion sits at the rack. The diagram omits switching, protection and storage details.",
      hybrid:
        "Retained AC equipment still constrains the upstream path. The sidecar adds interfaces and service-space requirements.",
      facility:
        "This is a conceptual broader DC option. Its switching, fault clearing, grounding and storage interfaces require their own specified design.",
    };
    function architecture(id, refresh = false) {
      $("architecture").innerHTML =
        flowRow("ILLUSTRATIVE CONVERSION PLACEMENT", architectures[id]) +
        `<p class="diagram-note">${notes[id]}</p>`;
      $("lab")
        .querySelectorAll("[data-arch]")
        .forEach((b) =>
          b.setAttribute("aria-pressed", String(b.dataset.arch === id)),
        );
      if (refresh && type === "dc") {
        $("lab-volts").value = id === "ac" ? 48 : 800;
        update();
      }
    }
    architecture("ac");
    $("lab")
      .querySelectorAll("[data-arch]")
      .forEach((b) =>
        b.addEventListener("click", () => architecture(b.dataset.arch, true)),
      );
  }
  const val = (id) => Number($(id).value);
  function update() {
    $("lab")
      .querySelectorAll("input")
      .forEach(
        (x) =>
          ($(x.id + "-value").textContent =
            `${fmt(x.value)} ${x.dataset.unit}`),
      );
    let output = "",
      boundary = "",
      graphic = "";
    if (type === "energy") {
      const p = val("lab-power"),
        h = val("lab-hours");
      output = `${p} MW × ${h} h = ${p * h} MWh.`;
      boundary =
        "Hypothetical constant load at one meter. A variable trace requires interval-by-interval integration. Peak MW does not determine annual MWh.";
      graphic = barChart(
        [["Energy over the chosen interval (MWh)", p * h, "#e5bb6e"]],
        480,
        "Energy is power multiplied by time.",
      );
    }
    if (type === "dc") {
      const m = dcModel(val("lab-kw"), val("lab-volts"));
      output = `${fmt(m.amps)} A at ${val("lab-volts")} V · ${fmt(m.lossRatio * 100, 2)}% of the 48 V conductor loss at equal resistance.`;
      boundary =
        "Ideal P = V × I at the stated DC segment. Same load and conductor resistance; two-conductor/bipolar definitions are not interchangeable. This comparison excludes converters, insulation, protection, thermal limits, conductor sizing and cost. Architecture buttons choose representative 48 V or 800 V segment values. Moving the slider is a hypothetical comparison, not validation of equipment compatibility.";
      graphic = barChart(
        [
          ["48 V reference current (A)", m.referenceAmps, "#78999e"],
          ["Selected voltage current (A)", m.amps, "#e5bb6e"],
        ],
        Math.max(m.referenceAmps, m.amps),
        "Current decreases as voltage increases at fixed DC power.",
      );
    }
    if (type === "acdc") {
      const m = acdcConductorModel(
        val("lab-kw"),
        480,
        val("lab-volts"),
        val("lab-pf"),
        val("lab-resistance") / 1000,
        1,
      );
      output = `AC: ${fmt(m.ac.amps)} A RMS per line, ${fmt(m.ac.lossKW * 1000)} W conductor heat. DC: ${fmt(m.dc.amps)} A per conductor, ${fmt(m.dc.lossKW * 1000)} W conductor heat. DC loss is ${fmt(m.lossRatio * 100, 1)}% of AC loss.`;
      boundary =
        "Receiving-end voltages: 480 V AC line-to-line RMS; DC voltage across the pair. Balanced sinusoidal three-phase AC, three current-carrying conductors versus two for DC. Equal effective resistance per conductor, with neutral and protective earth excluded from this count. AC: P = √3 × V × I × PF and heat = 3I²R. DC: P = VI and heat = 2I²R. Sources supply delivered power plus heat. Converters and cooling are excluded; this does not size a cable or establish equipment compatibility. Architecture buttons locate conversion independently of these arithmetic controls.";
      graphic = barChart(
        [
          ["480 V AC: total conductor heat (W)", m.ac.lossKW * 1000, "#78999e"],
          [
            `${val("lab-volts")} V DC: total conductor heat (W)`,
            m.dc.lossKW * 1000,
            "#e5bb6e",
          ],
        ],
        Math.max(m.ac.lossKW, m.dc.lossKW) * 1000,
        "Total conductor heat at equal delivered real power and resistance per conductor.",
      );
    }
    if (type === "heat") {
      const m = thermalModel(val("lab-duty"), val("lab-delta"), val("lab-aux"));
      output = `${fmt(m.kgPerSecond, 2)} kg/s ≈ ${fmt(m.litersPerMinute)} L/min of water · ${fmt(m.rejectedKW)} kW rejected within the stated boundary.`;
      boundary =
        "Q = mass flow × specific heat × temperature rise. Water cₚ = 4.18 kJ/(kg·K), density approximated as 1 kg/L. All specified auxiliary input becomes heat inside this boundary. No pressure-drop, approach-temperature or equipment-rating model is implied.";
      graphic = flowRow("SEPARATE FLUID CIRCUITS; HEAT CROSSES THE WALL", [
        "Chip loop",
        "Heat exchanger wall",
        "Facility loop",
        "Environment",
      ]);
    }
    if (type === "network") {
      const m = transferModel(
        val("lab-payload"),
        val("lab-rate"),
        val("lab-eff") / 100,
      );
      output = `${fmt(m.GBps)} GB/s effective payload rate · ${fmt(m.seconds, 2)} s ideal transfer time.`;
      boundary =
        "Decimal GB and Gb; eight bits per byte. One serial payload transfer with a supplied achieved fraction. This excludes queueing, startup latency, collective structure, storage limits and overlapping work; it does not predict job completion.";
      graphic = flowRow("A PAYLOAD MUST CROSS THE SPECIFIED BOUNDARY", [
        "Sender",
        "Shared fabric resources",
        "Receiver",
      ]);
    }
    if (type === "roofline") {
      const m = rooflineModel(val("lab-intensity"), val("lab-bandwidth"), 500);
      output = `${fmt(m.ceiling)} TFLOP/s upper bound · constrained by ${m.binding}.`;
      boundary =
        "Synthetic 500 TFLOP/s compute ceiling at one fixed precision and 1–5 TB/s memory bandwidth. Arithmetic intensity uses traffic at that same memory boundary. This ideal roofline is a ceiling, not a benchmark or a token-rate prediction.";
      graphic = barChart(
        [
          ["Compute ceiling (TFLOP/s)", 500, "#78999e"],
          ["Bandwidth × intensity ceiling", m.memoryCeiling, "#e5bb6e"],
        ],
        Math.max(500, m.memoryCeiling),
        "The lower of compute and memory-bandwidth ceilings limits the model.",
      );
    }
    if (type === "continuity") {
      const m = continuityModel(
        val("lab-energy"),
        0.9,
        1000,
        val("lab-inverter"),
        val("lab-cooling"),
      );
      output = m.powerSufficient
        ? `${fmt(m.electricalMinutes)} minutes of ideal 1 MW IT electrical support. ${m.auxiliarySupported ? "Cooling/control electrical support specified; thermal performance still needs evidence." : "Cooling/control support missing; continued useful service is unestablished."}`
        : "The inverter cannot support the 1 MW IT load, regardless of stored energy.";
      boundary =
        "Synthetic battery case, 90% discharge conversion efficiency. Cooling/control have a separately specified support path. Battery ageing, discharge curves, transfer behavior and thermal dynamics are omitted. The result is not thermal ride-through or a UPS product rating.";
      graphic = flowRow("CHECK BOTH DEPENDENCIES", [
        m.powerSufficient
          ? "IT electrical path supported"
          : "IT power limit exceeded",
        m.auxiliarySupported
          ? "Auxiliary electrical path specified"
          : "Auxiliary electrical path missing",
        "Useful service requires both",
      ]);
    }
    if (type === "checkpoint") {
      const m = checkpointModel(val("lab-checkpoint"), val("lab-interval"), 10);
      output = `${fmt(m.checkpointFraction * 100, 2)}% checkpoint overhead + ${fmt(m.recomputeFraction * 100, 2)}% expected recomputation per useful-work time.`;
      boundary = `First-order model: checkpoint pause C divided by useful-work interval T, plus T/(2M), with synthetic system MTTF M = 10 h. Uniform failure phase, small overhead and no restart cost are assumed. Terms are approximate time ratios, not an exact availability. Model minimum T ≈ ${fmt(m.optimumSeconds)} s.`;
      graphic = barChart(
        [
          ["Checkpoint overhead (%)", m.checkpointFraction * 100, "#78999e"],
          ["Expected recomputation (%)", m.recomputeFraction * 100, "#e5bb6e"],
        ],
        Math.max(10, m.checkpointFraction * 100, m.recomputeFraction * 100),
        "Checkpointing more often trades shorter lost work for more checkpoint pauses.",
      );
      if (m.checkpointFraction > 0.1) {
        output =
          "Checkpoint pauses exceed this teaching model’s 10% overhead cutoff. Use a detailed timeline instead of the first-order estimate.";
        graphic = "";
      }
    }
    if (type === "capacity") {
      const m = capacityModel(
        100,
        val("lab-overhead"),
        val("lab-cooling-mw"),
        100,
        val("lab-accepted"),
      );
      output = `${m.racks} complete 100 kW rack equivalents · binding: ${m.binding.join(" + ")}.`;
      boundary =
        "Hypothetical 100 MW site limit, supplied instantaneous auxiliary draw, 100 kW per rack, cooling stated at the IT boundary and accepted end-to-end rack paths. Whole racks only. This model excludes workload performance, reserve margins and local distribution constraints unless represented in the supplied path count.";
      graphic = barChart(
        [
          ["Electrical IT budget (MW)", m.powerMW, "#e5bb6e"],
          ["IT cooling limit (MW)", val("lab-cooling-mw"), "#92ceb7"],
          ["Accepted rack-path equivalent (MW)", m.acceptedMW, "#8cb3ce"],
        ],
        100,
        "The minimum of electrical, cooling and accepted-path capacities bounds the number of usable racks.",
      );
    }
    $("lab-output").textContent = output;
    $("lab-boundary").textContent = boundary;
    $("lab-graphic").innerHTML = graphic;
  }
  $("lab")
    .querySelectorAll("input,select")
    .forEach((x) => x.addEventListener("input", update));
  update();
}
$("search").addEventListener("input", renderContents);
$("contents-toggle").addEventListener("click", () => {
  const open = $("sidebar").classList.toggle("open");
  $("contents-toggle").setAttribute("aria-expanded", String(open));
  if (open) $("search").focus();
});
$("lookup-toggle").addEventListener("click", () => modeLookup(!lookupMode));
$("previous").addEventListener("click", () =>
  go(LESSONS[Math.max(0, current - 1)].id),
);
$("next").addEventListener("click", () =>
  go(LESSONS[(current + 1) % LESSONS.length].id),
);
window.addEventListener("popstate", () => {
  let id;
  try {
    id = decodeURIComponent(location.hash.slice(1));
  } catch {
    id = "";
  }
  go(id, "none");
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeRail();
});
let start;
try {
  start = decodeURIComponent(location.hash.slice(1));
} catch {
  start = "";
}
go(start, "replace");
