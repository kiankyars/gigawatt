// The reader runs as a module. build_expanded.py inlines reader-models.js
// before this file; the labs import the tested chapter models. Paths resolve
// against course/index.html here and against read.html on the published site.
import { facilityLedger, profileSummary, efficiencyCase } from "./prototypes/orientation-model.js";
import { llamaMemory, sameWorkEnergy, phaseSchedule } from "./prototypes/workload-model.js";
import { stagedLoad, projectOptions } from "./prototypes/grid-queues-model.js";
import { movingLoad } from "./prototypes/site-model.js";
import { phaseLedger, loadFromDc, conversionPath } from "./prototypes/distribution-model.js";
import { migrationDecision } from "./prototypes/rack-energy-model.js";
import { roofline, workloadBound, serviceDomains } from "./prototypes/compute-model.js";
import { fabricBudget, messageTime, communicationTime } from "./prototypes/networking-model.js";
import { checkpointTransfer, checkpointTimeline, eligibleGroups } from "./prototypes/storage-model.js";
import { deviceTemperature, hydraulicPoint } from "./prototypes/cooling-capture-model.js";
import { chillerBalance, operatingPoint, towerLedger } from "./prototypes/heat-rejection-model.js";
import { deliverySchedule, modularSchedule, rackInterfaces, acceptedPaths } from "./prototypes/procurement-model.js";
import { heatBalance, transition, unavailableUnion } from "./prototypes/operations-model.js";
import { rentalRevenue } from "./prototypes/capacity-model.js";
import { coupledOutage, weatherCapacity, densityRetrofit, stalledJob, phaseAcceptance } from "./prototypes/integrated-cases-model.js";

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
// Fixed decimals, so 1 reads "1.00" beside 0.95 on a slider with a 0.01 step.
const fixed = (n, d = 0) =>
  Number(n).toLocaleString("en-US", {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  });
const LESSONS = DATA.lessons,
  byLesson = new Map(LESSONS.map((l, i) => [l.id, i]));
const domainById = new Map(DATA.domains.map((d) => [d.id, d]));
const CHAPTERS = DATA.chapters;
const REFERENCE_GROUPS = DATA.references || [];
const READING_GROUPS = [...CHAPTERS, ...REFERENCE_GROUPS];
const chapterById = new Map(READING_GROUPS.map((chapter) => [chapter.id, chapter]));
const chapterByLesson = new Map(READING_GROUPS.flatMap(chapter => chapter.lesson_ids.map(id => [id, chapter])));
const chapterName = (chapter) => chapter.number ? `${chapter.number}. ${chapter.title}` : chapter.title;
const topicTitle = (id) => chapterById.has(id)
  ? chapterName(chapterById.get(id)) : "the next chapter";
const sourcesById = new Map(DATA.sources.map((s) => [s.id, s]));
const PRIMER_VIEW = "primer-vocabulary";
let current = 0,
  // false while a lesson is open; "glossary" or "primer" for the other views.
  lookupMode = false;
const drafts = new Map();
const checkinDrafts = new Map();
const CASE_STUDY_LINKS = {
  "d12-hazards-and-site-evidence": [["land", "Greenfield and brownfield: Abilene and Colossus"], ["colossus", "Colossus 1: a reused factory, new power infrastructure"]],
  "d03-voltage-and-distance": [["procurement", "xAI: equipment lead times and the MV supply path"], ["current", "The current and loss tradeoff"]],
  "d05-storage-power-and-time": [["sparks", "Crusoe and Redwood: solar and batteries in Sparks"], ["availability", "Solar energy share versus availability"]],
  "d09-service-acceptance": [["demand-response", "Google: scheduling flexible work"]],
  "d11-water-and-heat-reuse": [["abilene-cooling", "Abilene: closed-loop cooling and outdoor heat rejection"]],
  "c00-abilene-ai-factory": [["abilene-ledger", "Abilene: separate buildings and capacity milestones"], ["abilene-cooling", "Abilene: closed-loop cooling and outdoor heat rejection"]],
};
// course/assets/README.md limits each generated illustration to an orientation
// role. Only the campus cutaway fits the lessons that request an image: the
// rack, cooling, power and network plates show connections, plumbing or
// internals that those capstone lessons would teach from, so they stay unused.
const ART = {
  campus: {
    file: "campus-cutaway.png",
    label: "CAMPUS ORIENTATION",
    alt: "Generated cutaway of a hypothetical campus: an electrical yard on the left, server rows in the central building and heat-rejection equipment on the right.",
    caption:
      "Generated illustration of a hypothetical campus. Power enters through the electrical yard on the left, the racks do the work in the central building, and the mechanical yard on the right returns heat to the outdoors. Use it to find these three areas, not to trace cables or pipes.",
  },
};
function artFor(l) {
  return ART[l.image] || null;
}
// Terms the Primer uses, in its order. Each entry: term, two-sentence definition,
// the glossary term that goes further (if any) and the lesson that develops it.
const PRIMER_VOCABULARY = [
  ["Source, circuit and load", [
    ["Source and load", "The source supplies electrical energy and the load receives it, for example to run electronics or produce heat. Charge circulates around the loop; the load uses energy, not charge.", null, "d01-boundaries"],
    ["Circuit", "A circuit is a complete conducting loop from the source, through the load and back. Opening a switch breaks the loop, so current stops even though a voltage remains across the open switch.", null, "d03-voltage-and-distance"],
  ]],
  ["Volts and amperes", [
    ["Voltage (V)", "Voltage is the electric potential difference between two points: energy per unit of charge, measured in volts. A voltmeter compares two points, so every voltage names both of them.", "Voltage (volts, V)", "d03-voltage-and-distance"],
    ["Current (A)", "Current is the rate of charge flow through a path, measured in amperes, often called amps. In a single loop the same current flows out and back, so adding the two wire readings would count it twice.", "Current (amperes or amps, A)", "d03-voltage-and-distance"],
  ]],
  ["Resistance and loss", [
    ["Resistance (Ω)", "Resistance, measured in ohms, relates voltage and current in a simple resistor: V = I × R. With 6 Ω fixed, 12 V drives 2 A and 24 V drives 4 A.", "Electrical resistance (ohms, Ω)", "d03-voltage-and-distance"],
    ["Resistive heating (I²R)", "Current through a resistance produces heat at a rate of I²R, so doubling the current at the same resistance produces four times the heat. Wires have resistance too, which is why the same rule sets conductor losses.", null, "d03-voltage-and-distance"],
  ]],
  ["Watts", [
    ["Power (W)", "Power is the rate of energy transfer: one watt is one joule each second. For a steady DC load, power is voltage times current, so 12 V × 2 A = 24 W.", "Power (watts, W)", "d01-power-over-time"],
  ]],
  ["Watt-hours and scale", [
    ["Energy (kWh)", "Energy is power multiplied by time when the power holds steady: a 1 kW load running for 2 hours uses 2 kWh. A kilowatt-hour is an amount of energy, not a rate.", "Watt-hour (Wh)", "d01-power-over-time"],
    ["Kilo, mega and giga", "The prefixes k, M and G mean one thousand, one million and one billion. So 1 MW = 1,000 kW and 1 GW = 1,000 MW, and the same prefixes apply to watt-hours.", null, "d01-power-over-time"],
  ]],
  ["AC, DC and frequency", [
    ["Direct current (DC)", "Direct current flows in one direction because the source keeps the same polarity. The electronics inside a server run on regulated DC from a power supply.", "Direct current (DC)", "d03-voltage-and-distance"],
    ["Alternating current (AC)", "Alternating current reverses direction as the voltage changes polarity in each cycle. At each zero crossing the voltage passes through zero and a resistor carries no current.", "Alternating current (AC)", "d03-voltage-and-distance"],
    ["Frequency (Hz)", "Frequency counts the full AC cycles each second, measured in hertz. A higher frequency means the polarity reverses more often.", null, "d03-voltage-and-distance"],
  ]],
  ["AC waveform shapes", [
    ["Waveform", "A waveform is the shape of a voltage over time. Sine, square, triangle and sawtooth voltages all count as AC when they reverse polarity, and utility voltage is approximately a sine wave.", null, "d03-voltage-and-distance"],
  ]],
  ["Voltage variation", [
    ["Nominal voltage", "Nominal voltage is the named reference level of a supply, such as 12 V. The actual voltage varies with the source, the load and the wiring, and each equipment rating states the range it accepts.", null, "d04-read-the-power-train"],
  ]],
  ["Three-phase AC", [
    ["Three-phase AC", "Three-phase AC uses three voltages staggered by one-third of a cycle, or 120 degrees. It is the predominant form of AC power distribution in data centers.", "Three-phase AC", "d03-voltage-and-distance"],
    ["Power supply unit (PSU)", "A power supply unit (PSU) turns the incoming AC into the regulated DC that electronics use, and it can contain several conversion stages. A rack spreads its single-phase PSU loads across the three phases, and each PSU uses two current-carrying conductors.", "Power supply unit (PSU)", "d06-conversion-ledger"],
  ]],
  ["Three-phase power", [
    ["Instantaneous power", "Instantaneous power is voltage times current at one moment. In a balanced three-phase supply feeding equal resistive loads, three phases that each average 10 kW add to a steady 30 kW at every moment.", null, "d03-voltage-and-distance"],
  ]],
  ["Power factor", [
    ["RMS (root mean square)", "RMS, short for root mean square, is the effective magnitude of an AC voltage or current: the value that heats a resistor as much as the same DC value. Quoted AC voltages, such as 480 V, are normally RMS values.", "RMS", "d03-voltage-and-distance"],
    ["Power factor", "Power factor is real power in kW divided by apparent power in kVA (kilovolt-amperes). At power factor 0.8 a load needs 25 percent more current than at power factor 1 to receive the same power, which takes more wiring and supply capacity.", "Power factor", "d04-current-and-rating"],
    ["Apparent power (kVA)", "Apparent power is RMS voltage times RMS current, measured in volt-amperes. Delivering 8 kW at power factor 0.8 takes 10 kVA of supply capacity.", "Apparent power", "d04-current-and-rating"],
  ]],
  ["Conversion equipment", [
    ["Transformer", "A transformer changes an AC voltage level through magnetic coupling between its windings. Its turns ratio is fixed, so its output voltage follows its input.", "Transformer", "d04-read-the-power-train"],
    ["Rectifier", "A rectifier converts AC to DC. Power supplies and the input stage of an online UPS both contain one.", "Rectifier", "d04-conversion-placement"],
    ["Inverter", "An inverter converts DC to AC. In an online UPS, the inverter rebuilds AC for the load from the DC link.", "Inverter", "d04-read-the-power-train"],
  ]],
  ["Transformer input range", [
    ["Input voltage range", "A transformer rating states the input voltages it accepts on each connection: Schneider Electric's 400 V Phaseo ABL6TS25B controls transformer permits 360 to 440 V. Within that range its output still moves up and down with its input.", "Transformer", "d04-read-the-power-train"],
  ]],
  ["UPS, battery and generator", [
    ["Uninterruptible power supply (UPS)", "An uninterruptible power supply (UPS) keeps its protected load powered when the normal source is interrupted. Its runtime is finite, so it bridges the gap until a generator takes over or the supply returns.", "Uninterruptible power supply (UPS)", "d05-paths-and-transitions"],
    ["Battery", "A battery stores energy for the UPS. Its kWh rating is the energy it holds, and its kW limit is the rate at which it can deliver that energy.", null, "d05-storage-power-and-time"],
    ["DC link", "The DC link is the DC connection between a UPS's rectifier and its inverter. The battery supports the DC link when the input supply fails.", null, "d05-storage-power-and-time"],
    ["Generator", "A generator is a local source that can take over the upstream supply after it starts and qualifies. The UPS carries the load during that start interval.", null, "d05-paths-and-transitions"],
  ]],
  ["Offline and online UPS", [
    ["Offline (standby) UPS", "An offline or standby UPS normally passes utility AC straight to the load and switches to its battery-powered inverter when the supply fails. That switch takes a brief transfer interval, which suits home computers and desktop equipment.", "Uninterruptible power supply (UPS)", "d05-paths-and-transitions"],
    ["Online double-conversion UPS", "An online double-conversion UPS always feeds the load through a rectifier, a DC link and an inverter. When the battery takes over the DC link, the inverter keeps running without a transfer break, so critical data-center loads often use this design.", "Uninterruptible power supply (UPS)", "d05-paths-and-transitions"],
  ]],
  ["Load, rating and redundancy", [
    ["Load and rating", "Load is actual demand; a rating is a component's capability under stated conditions. A 100 kW load therefore needs two qualified 50 kW modules.", null, "d04-current-and-rating"],
    ["N and N+1", "N is the number of modules the load requires, and N+1 adds one spare. With N = 2 plus a spare, two modules remain after one fails, although shared paths, controls and cooling can still stop the service.", "N+1", "d05-paths-and-transitions"],
  ]],
  ["Rack, server, CPU and GPU", [
    ["Rack", "A rack is a frame that holds computing, networking, storage and supporting equipment. Data centers often state power per rack, such as a 100 kW rack.", "Rack", "d07-data-path"],
    ["Server", "A server is a computer that performs work or provides a service to other computers over a network. A compute server for AI contains a CPU, system memory and a GPU with its own memory.", "Server", "d07-data-path"],
    ["CPU (central processing unit)", "The central processing unit (CPU) coordinates the server's work. It uses the server's system memory to hold active data.", "Central processing unit (CPU)", "d07-data-path"],
    ["GPU (graphics processing unit)", "The graphics processing unit (GPU) performs the parallel numerical work used to run many AI models. It has its own memory close to its processing cores.", "Graphics processing unit (GPU)", "d07-data-path"],
    ["IT (information technology)", "IT equipment means computing, networking and storage. Facility accounts separate IT power from the power used by cooling and electrical support.", "IT load", "d01-boundaries"],
  ]],
  ["Memory and storage", [
    ["Storage", "Storage keeps data, such as a saved model file, when the power is off. A storage server holds the model and sends it across the data-center network when a compute server needs it.", null, "d09-storage-paths"],
    ["RAM (random-access memory)", "RAM is working memory that holds data while a computer runs. Model data arrives in the server's system RAM before it is copied into GPU memory.", null, "d07-data-path"],
    ["HBM (high-bandwidth memory)", "Many accelerators use HBM placed beside the GPU as their working memory. The GPU cores compute on data already in this memory, and its capacity sets how much of the model fits.", "HBM", "d07-data-path"],
  ]],
  ["Bandwidth and latency", [
    ["Bandwidth", "Bandwidth is how much data a path can carry each second. At an ideal 10 Gb/s, an 8 MB chunk (64 megabits) takes 6.4 ms to send; at 100 Gb/s it takes 0.64 ms.", null, "d08-topology-budget"],
    ["Latency", "Latency is how long a defined event takes, such as the first bit reaching the receiver. More bandwidth shortens the whole transfer but leaves that first-bit latency unchanged.", "Latency", "d08-topology-budget"],
    ["Bits and bytes", "A lowercase b means bits and an uppercase B means bytes, and one byte is eight bits. Network rates are given in bits per second and data in bytes, so convert before dividing.", null, "d08-topology-budget"],
  ]],
  ["Heat and temperature", [
    ["Heat", "The electrical energy a chip uses becomes heat, measured as a rate in watts. A GPU drawing 500 W in steady operation must shed 500 W of heat.", null, "d10-local-thermal-paths"],
    ["Temperature", "Temperature tells how hot one location is, in degrees Celsius. It does not by itself give the rate of heat transfer, which also depends on the thermal path.", "Thermal resistance", "d10-local-thermal-paths"],
  ]],
  ["Cold plate, coolant and CDU", [
    ["Cold plate", "A cold plate is a heat exchanger attached to a chip, with coolant flowing through it. It moves the chip's heat into the liquid loop.", "Cold plate", "d10-local-thermal-paths"],
    ["Coolant and pumps", "Coolant is the liquid that carries heat away from the cold plates. Pumps circulate it, and they need electricity too.", null, "d10-flow-and-pressure"],
    ["CDU (coolant distribution unit)", "A coolant distribution unit (CDU) passes heat from the equipment coolant loop into a separate facility loop through a heat exchanger. The two fluids stay apart, and the facility loop carries the heat to the outdoor plant.", "CDU", "d10-cdu-interfaces"],
    ["Outdoor plant", "Outdoor equipment rejects the heat to the environment. A dry cooler transfers heat to outdoor air, while a chiller uses refrigeration to cool a fluid.", "Dry cooler", "d11-heat-rejection"],
  ]],
  ["Facility energy and PUE", [
    ["PUE (power usage effectiveness)", "Power usage effectiveness (PUE) divides total facility energy by IT energy over the same interval. A facility using 120 kWh while its IT uses 100 kWh has a PUE of 1.20; PUE measures facility overhead, not useful computation.", "Power usage effectiveness (PUE)", "d01-metrics-and-evidence"],
  ]],
];
function referenceFigures(figures) {
  return (figures || [])
    .map(
      (f) =>
        `<figure class="source-figure"><a href="assets/${esc(f.asset)}" target="_blank" rel="noopener" aria-label="Open full-size: ${esc(f.alt)}"><img src="assets/${esc(f.asset)}" alt="${esc(f.alt)}" loading="lazy" /></a><figcaption>${esc(f.caption)} <a href="${esc(f.source_url)}" target="_blank" rel="noopener">${esc(f.source_title)}</a> · <a href="assets/${esc(f.asset)}" target="_blank" rel="noopener">Open full-size image</a></figcaption></figure>`,
    )
    .join("");
}
function renderContents() {
  const q = $("search").value.trim().toLowerCase(),
    terms = q.split(/\s+/).filter(Boolean);
  const matches = (value) => terms.every((term) => value.toLowerCase().includes(term));
  const visible = READING_GROUPS.map((chapter) => {
    const chapterMatch = matches(`${chapterName(chapter)} ${chapter.presentations.map((p) => `${p.id} ${p.title}`).join(" ")}`);
    const lessons = chapter.lesson_ids.map((id) => LESSONS[byLesson.get(id)])
      .filter((lesson) => lesson && (chapterMatch || matches(lessonSearchText(lesson))));
    return { chapter, lessons, show: chapterMatch || lessons.length > 0 };
  }).filter((item) => item.show);
  // Unnumbered case studies sit between chapters; count numbered chapters as the homepage does.
  const chapterCount = CHAPTERS.filter((chapter) => chapter.number).length;
  $("lesson-count").textContent = `${chapterCount} ${chapterCount === 1 ? "chapter" : "chapters"}`;
  $("search-status").textContent = q ? `${visible.length} matching ${visible.length === 1 ? "chapter" : "chapters"}`
    : "Open a chapter for its reading and slides.";
  $("contents").innerHTML = visible.map(({ chapter, lessons }) => {
    const slideLinks = presentationLinks(chapter);
    const activeChapter = chapter.id === chapterByLesson.get(LESSONS[current]?.id)?.id && !lookupMode;
    const heading = `<span class="chapter-name">${esc(chapterName(chapter))}</span>`;
    const primer = chapter.id === "primer"
      ? `<button class="lesson-link${lookupMode === "primer" ? " active" : ""}" data-view="${PRIMER_VIEW}" ${lookupMode === "primer" ? 'aria-current="page"' : ""}><span class="lesson-number">1.1</span> Primer vocabulary</button>`
      : "";
    const reading = lessons.map((lesson) => {
      const selected = LESSONS[current]?.id === lesson.id && !lookupMode;
      const number = chapter.number ? `${chapter.number}.${chapter.lesson_ids.indexOf(lesson.id) + 1}` : "";
      return `<button class="lesson-link${selected ? " active" : ""}" data-lesson="${esc(lesson.id)}" ${selected ? 'aria-current="page"' : ""}><span class="lesson-number">${number}</span> ${esc(lesson.title)}${lesson.optional === true ? '<small class="lesson-optional">Optional practice</small>' : ""}${lesson.domain_checkin ? '<small class="lesson-checkin-note">Ends with a check-in</small>' : ""}</button>`;
    }).join("");
    return `<details class="chapter-group" data-chapter="${esc(chapter.id)}" ${q || activeChapter || chapter.id === "primer" ? "open" : ""}><summary>${heading}</summary><div class="chapter-content">${slideLinks}${primer}${reading}</div></details>`;
  }).join("") || '<p class="muted">No matching chapters. Try another term.</p>';
  $("contents")
    .querySelectorAll("[data-lesson], [data-view]")
    .forEach((b) => b.addEventListener("click", () => go(b.dataset.lesson || b.dataset.view)));
  renderGlossary();
}
// Search the words a reader can see in each lesson, built once per lesson.
const searchIndex = new Map();
function lessonSearchText(lesson) {
  if (!searchIndex.has(lesson.id)) {
    const w = lesson.worked_example || {},
      p = lesson.practice || {},
      c = lesson.domain_checkin || {};
    searchIndex.set(lesson.id, [
      lesson.title, lesson.summary, lesson.question,
      ...asList(lesson.sections).flatMap((s) => [s.heading, ...asList(s.paragraphs), ...asList(s.figures).map((f) => f.caption)]),
      w.title, ...asList(w.givens), ...asList(w.steps), w.result, w.boundary,
      ...asList(lesson.tradeoff), ...asList(lesson.failure),
      p.question, p.answer, ...asList(p.explanation),
      c.title, ...asList(c.scenario), c.prompt, c.answer, ...asList(c.explanation), ...asList(c.bridge),
      lesson.takeaway,
    ].filter(Boolean).join(" ").toLowerCase());
  }
  return searchIndex.get(lesson.id);
}
function presentationLinks(chapter) {
  return chapter.presentations.map((deck) =>
    `<div class="deck-entry"><a class="slides-link" href="${esc(deck.href)}" aria-label="Open slides for ${esc(chapterName(chapter))}: ${esc(deck.title)}"><span aria-hidden="true">▷</span> ${chapter.presentations.length > 1 ? esc(deck.title) : "Open slides"}</a></div>`,
  ).join("");
}
function renderGlossary() {
  // The Glossary page has its own filter; the sidebar search fills it too.
  const shown = $("glossary-filter").value.trim(),
    query = shown.toLowerCase();
  const items = DATA.glossary.filter((g) =>
    `${g.term} ${g.definition}`.toLowerCase().includes(query),
  );
  $("glossary").innerHTML = items.length
    ? `<div class="glossary-grid">${items.map((g) => `<article class="glossary-card"><h2>${esc(g.term)}</h2><p>${esc(g.definition)}</p><button data-lesson="${esc(g.lesson)}">Read the explanation →</button></article>`).join("")}</div>`
    : `<div class="glossary-empty" role="status"><p>No glossary entry for “${esc(shown)}”.</p><button data-search-lessons>Search the lessons instead →</button></div>`;
  $("glossary")
    .querySelectorAll("[data-lesson]")
    .forEach((b) => b.addEventListener("click", () => go(b.dataset.lesson)));
  $("glossary")
    .querySelector("[data-search-lessons]")
    ?.addEventListener("click", () => {
      $("search").value = shown;
      renderContents();
      openRail();
    });
}
function renderPrimer() {
  const primer = chapterById.get("primer");
  $("primer-slides").innerHTML = primer ? presentationLinks(primer) : "";
  $("primer-next").textContent = `Continue to ${chapterName(chapterByLesson.get(LESSONS[0].id))} →`;
  const glossaryTerms = new Set(DATA.glossary.map((g) => g.term));
  $("primer-list").innerHTML = PRIMER_VOCABULARY.map(([topic, entries], index) =>
    `<section class="vocab-group"><h2><span>${index + 1}</span> ${esc(topic)}</h2><dl>${entries.map(([term, definition, glossary, lesson]) => {
      const links = [
        glossary && glossaryTerms.has(glossary) ? `<button data-glossary="${esc(glossary)}">Glossary: ${esc(glossary)}</button>` : "",
        byLesson.has(lesson) ? `<a href="#${esc(lesson)}" data-lesson="${esc(lesson)}">Read more: ${esc(LESSONS[byLesson.get(lesson)].title)} →</a>` : "",
      ].filter(Boolean).join("");
      return `<div class="vocab-entry"><dt>${esc(term)}</dt><dd><p>${esc(definition)}</p>${links ? `<p class="vocab-links">${links}</p>` : ""}</dd></div>`;
    }).join("")}</dl></section>`,
  ).join("");
  $("primer-list")
    .querySelectorAll("[data-lesson]")
    .forEach((a) => a.addEventListener("click", (event) => {
      event.preventDefault();
      go(a.dataset.lesson);
    }));
  $("primer-list")
    .querySelectorAll("[data-glossary]")
    .forEach((b) => b.addEventListener("click", () => {
      $("glossary-filter").value = b.dataset.glossary;
      modeLookup("glossary");
    }));
}
function showView(view) {
  lookupMode = view === "lesson" ? false : view;
  $("lookup").hidden = view !== "glossary";
  $("primer").hidden = view !== "primer";
  $("lesson").hidden = view !== "lesson";
  $("lookup-toggle").setAttribute("aria-pressed", String(view === "glossary"));
}
function modeLookup(value) {
  showView(value ? "glossary" : "lesson");
  if (!value) renderLesson();
  renderContents();
  if (value) {
    window.scrollTo({ top: 0, behavior: "instant" });
    $("lookup-title").tabIndex = -1;
    $("lookup-title").focus({ preventScroll: true });
  }
}
function openRail() {
  $("sidebar").classList.add("open");
  $("contents-toggle").setAttribute("aria-expanded", "true");
  $("search").focus();
}
function closeRail() {
  $("sidebar").classList.remove("open");
  $("contents-toggle").setAttribute("aria-expanded", "false");
}
function setHash(id, historyMode, focusCheckin = false) {
  const targetUrl = new URL(location.href);
  targetUrl.hash = id;
  if (focusCheckin) targetUrl.searchParams.set("checkin", "1");
  else targetUrl.searchParams.delete("checkin");
  if (historyMode !== "none" && targetUrl.href !== location.href)
    history[historyMode === "replace" ? "replaceState" : "pushState"](
      null,
      "",
      targetUrl,
    );
}
function saveDrafts() {
  const previous = LESSONS[current];
  if (previous && $("response")) drafts.set(previous.id, $("response").value);
  // Keyed by chapter: two chapters can share a domain (Chapters 8 and 9 are both D06).
  if (previous?.domain_checkin && $("checkin-response"))
    checkinDrafts.set(previous.domain_checkin.chapter, $("checkin-response").value);
}
function go(id, historyMode = "push", focusCheckin = false) {
  saveDrafts();
  // The Primer has no lessons; its reading is the vocabulary view.
  if (id === "primer" || id === PRIMER_VIEW) {
    showView("primer");
    setHash(PRIMER_VIEW, historyMode);
    document.title = "Primer vocabulary — From Watts to Tokens";
    renderPrimer();
    renderContents();
    closeRail();
    window.scrollTo({ top: 0, behavior: "instant" });
    $("primer-title").tabIndex = -1;
    $("primer-title").focus({ preventScroll: true });
    return;
  }
  // A chapter address opens that chapter's first lesson.
  const chapter = chapterById.get(id);
  if (!byLesson.has(id) && chapter?.lesson_ids.length) id = chapter.lesson_ids[0];
  if (!byLesson.has(id)) id = LESSONS[0].id;
  current = byLesson.get(id);
  showView("lesson");
  setHash(id, historyMode, focusCheckin);
  renderLesson();
  renderContents();
  closeRail();
  const target = focusCheckin && LESSONS[current].domain_checkin
    ? $("domain-checkin") : $("lesson");
  if (target.id === "domain-checkin") {
    target.tabIndex = -1;
    target.scrollIntoView({ block: "start", behavior: "instant" });
  } else window.scrollTo({ top: 0, behavior: "instant" });
  target.focus({ preventScroll: true });
}
function renderLesson() {
  const l = LESSONS[current],
    d = domainById.get(l.domain),
    art = artFor(l);
  const chapter = chapterByLesson.get(l.id);
  const lessonNumber = chapter.lesson_ids.indexOf(l.id) + 1;
  document.title = `${l.title} — From Watts to Tokens`;
  $("eyebrow").textContent =
    chapter.number ? `${chapter.number}.${lessonNumber} · ${chapter.title}` : chapter.title;
  $("optional-label").hidden = l.optional !== true;
  $("title").textContent = l.title;
  $("summary").textContent = l.summary;
  const caseLinks = CASE_STUDY_LINKS[l.id] || [];
  $("case-links").hidden = !caseLinks.length;
  $("case-links").innerHTML = caseLinks.length
    ? `<p>Case-study slides</p><ul>${caseLinks.map(([id, label]) => `<li><a href="prototypes/case-studies.html#${esc(id)}">${esc(label)} →</a></li>`).join("")}</ul>`
    : "";
  $("question").textContent = l.question;
  $("chapter-slides").hidden = chapter.presentations.length === 0;
  $("chapter-slides").innerHTML = presentationLinks(chapter);
  $("teaching-image").closest("figure").hidden = !art;
  if (art) {
    $("teaching-image").src = `assets/${art.file}`;
    $("teaching-image").alt = art.alt;
    $("image-index").textContent = art.label;
    $("image-caption").textContent = art.caption;
  } else {
    $("teaching-image").removeAttribute("src");
  }
  $("anatomy").replaceChildren();
  $("prose").innerHTML = l.sections
    .map(
      (s, i) =>
        `<section class="reading-section" id="section-${i + 1}"><h2>${esc(s.heading)}</h2>${prose(s.paragraphs)}${referenceFigures(s.figures)}</section>`,
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
    `What you will learn${l.objectives.map((id) => `<p>${esc(DATA.domains.flatMap((topic) => topic.objectives).find((o) => o.id === id)?.capability || "Apply the ideas across the system.")}</p>`).join("")}`;
  const visual = l.visual;
  $("concept").hidden = !visual;
  $("concept").classList.remove("parcel-concept");
  if (visual?.kind === "parcel") {
    $("prose").closest(".reading-layout").before($("concept"));
    renderParcelComparison(visual);
  } else {
    $("lab").before($("concept"));
  }
  if (visual && visual.kind !== "parcel") {
    $("concept").innerHTML =
      `<div class="eyebrow">THE MECHANISM AT A GLANCE</div><h2 id="concept-title">${esc(visual.title)}</h2><div class="concept-grid">${visual.nodes.map((n, i) => `<div class="concept-node"><span>${String(i + 1).padStart(2, "0")}</span><h3>${esc(n.label)}</h3><p>${esc(n.detail)}</p></div>`).join("")}</div>${visual.caption ? `<p class="boundary">${esc(visual.caption)}</p>` : ""}`;
  }
  const w = l.worked_example;
  $("worked").innerHTML =
    `<div class="eyebrow">FOLLOW A COMPLETE EXAMPLE</div><h2 id="worked-title">${esc(w.title)}</h2><div class="givens">${prose(w.givens)}</div><ol>${w.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol><p class="result">${esc(w.result)}</p>${w.boundary ? `<p class="boundary">${esc(w.boundary)}</p>` : ""}`;
  // Tradeoff and failure are optional: show only the ones a lesson carries.
  const consequences = [
    ["The tradeoff", l.tradeoff],
    ["When the situation changes", l.failure],
  ].filter(([, value]) => asList(value).length);
  $("consequences").hidden = !consequences.length;
  $("consequences").classList.toggle("single", consequences.length === 1);
  $("consequences").innerHTML = consequences
    .map(([heading, value]) => `<section><h2>${heading}</h2>${prose(value)}</section>`)
    .join("");
  const p = l.practice;
  $("practice").innerHTML =
    `<div class="eyebrow">PREDICT · CALCULATE · EXPLAIN</div><h2 id="practice-title">Apply the idea</h2>${prose(p.question)}<label for="response">Your reasoning — private to this open page</label><textarea id="response" placeholder="State the boundary, work through the change, and name what remains unknown."></textarea><details><summary>Reveal the worked answer</summary><div><p class="answer">${esc(p.answer)}</p>${prose(p.explanation)}</div></details>`;
  $("response").value = drafts.get(l.id) || "";
  renderSources(l);
  renderDomainCheckin(l.domain_checkin);
  $("position").textContent = `Reading ${lessonNumber} of ${chapter.lesson_ids.length}`;
  $("previous").disabled = current === 0;
  const nextChapter = chapterByLesson.get(LESSONS[current + 1]?.id);
  const crossesChapter = !!nextChapter && nextChapter.id !== chapter.id;
  $("next").textContent =
    current === LESSONS.length - 1
      ? "Back to start ↻"
      : crossesChapter && REFERENCE_GROUPS.includes(nextChapter)
        ? "Further reading →"
      : crossesChapter
        ? `Continue to ${chapterName(nextChapter)} →`
        : "Next lesson →";
  renderLab(l);
}
// Sources render as a bibliography: title, publisher, dates and what each supports.
function renderSources(l) {
  const claims = new Map();
  for (const note of l.source_notes)
    if (sourcesById.has(note.id))
      claims.set(note.id, [...(claims.get(note.id) || []), note.claim]);
  $("evidence").innerHTML =
    `<h2 id="evidence-title">Sources</h2><details><summary>${claims.size} ${claims.size === 1 ? "source" : "sources"}</summary>${[...claims]
      .map(([id, notes]) => {
        const s = sourcesById.get(id);
        const dates = [
          s.publisher,
          s.published_on && `Published ${s.published_on}`,
          s.reviewed_on && `Reviewed ${s.reviewed_on}`,
        ].filter(Boolean);
        return `<div class="source"><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>${dates.map(esc).join(" · ")}</p>${notes.map((claim) => `<p class="source-claim">${esc(claim)}</p>`).join("")}<p><a href="../research/sources/${esc(id)}.md">Local source note ↗</a></p></div>`;
      })
      .join("")}</details>`;
}
function renderDomainCheckin(checkin) {
  const section = $("domain-checkin");
  section.hidden = !checkin;
  section.replaceChildren();
  if (!checkin) return;
  const nextLabel = checkin.next_label || topicTitle(checkin.next_domain);
  section.innerHTML =
    `<div class="eyebrow">PAUSE · PREDICT · CONNECT</div><h2 id="domain-checkin-title">Check your understanding</h2><h3>${esc(checkin.title)}</h3><p class="boundary">Pause and make a prediction, then compare your reasoning.</p>${prose(checkin.scenario)}<p class="checkin-prompt">${esc(checkin.prompt)}</p><label for="checkin-response">Your reasoning — private to this page; clears on reload</label><textarea id="checkin-response" autocomplete="off" placeholder="Make your prediction and explain why."></textarea><details><summary>Compare your reasoning</summary><div><p class="answer">${esc(checkin.answer)}</p>${prose(checkin.explanation)}</div></details><div class="checkin-bridge"><h3>The next problem</h3>${prose(checkin.bridge)}<a href="#${esc(checkin.next_lesson)}" id="checkin-continue">Continue to ${esc(nextLabel)} →</a></div>`;
  $("checkin-response").value = checkinDrafts.get(checkin.chapter) || "";
  $("checkin-continue").addEventListener("click", (event) => {
    event.preventDefault();
    go(checkin.next_lesson);
  });
}
function renderParcelComparison(visual) {
  const brief = visual.brief;
  $("concept").classList.add("parcel-concept");
  $("concept").innerHTML =
    `<div class="eyebrow">ONE BRIEF · TWO PARCELS</div><h2 id="concept-title">${esc(visual.title)}</h2><ul class="parcel-brief"><li>${brief.power_mw} MW at the customer bus</li><li>${brief.campus_acres} usable acres</li><li>${brief.fiber_routes} separate fiber routes</li></ul><div class="parcel-picker" role="group" aria-label="Choose a hypothetical parcel">${visual.parcels.map((p, i) => `<button data-parcel="${esc(p.id)}" aria-pressed="${i === 0}">${esc(p.label)} <span>${p.gross_acres} gross ac</span></button>`).join("")}</div><div id="parcel-view"></div><p class="boundary">${esc(visual.caption)}</p>`;
  const update = (id) => {
    const p = visual.parcels.find((parcel) => parcel.id === id);
    const usable = p.gross_acres - p.drainage_acres - p.easement_acres;
    const ready = Math.max(...Object.values(p.readiness));
    const constraint = Object.entries(p.readiness).find(
      ([, month]) => month === ready,
    )[0];
    const pass =
      usable >= brief.campus_acres &&
      ready <= brief.deadline_month &&
      p.rights_resolved &&
      p.control_month >= ready;
    const scale =
      600 / Math.max(...visual.parcels.map((parcel) => parcel.gross_acres));
    const parcelWidth = p.gross_acres * scale;
    const drainageWidth = p.drainage_acres * scale;
    const easementWidth = p.easement_acres * scale;
    const usableX = 20 + drainageWidth + easementWidth;
    const usableWidth = usable * scale;
    const campusWidth = brief.campus_acres * scale;
    const campusX = usableX + (usableWidth - campusWidth) / 2;
    const campusCenter = campusX + campusWidth / 2;
    $("concept")
      .querySelectorAll("[data-parcel]")
      .forEach((button) =>
        button.setAttribute(
          "aria-pressed",
          String(button.dataset.parcel === id),
        ),
      );
    $("parcel-view").innerHTML =
      `<div class="parcel-map"><svg viewBox="0 0 640 330" role="img" aria-label="${esc(p.label)}: ${p.gross_acres} gross acres, ${p.drainage_acres} drainage and flood exclusion acres, ${p.easement_acres} easement acres, ${usable} usable acres. The supplied 40-acre campus envelope fits. Equipment and route locations are schematic."><rect x="20" y="60" width="${parcelWidth}" height="180" rx="5" class="parcel-land"/><path d="M20 60h${drainageWidth}v180H20Z" class="parcel-drainage"/><path d="M${20 + drainageWidth} 60h${easementWidth}v180h-${easementWidth}Z" class="parcel-easement"/><path d="M${20 + drainageWidth + easementWidth / 2} 70v160" class="parcel-corridor"/><rect x="${campusX}" y="60" width="${campusWidth}" height="180" class="parcel-envelope"/><rect x="${campusX + campusWidth * 0.12}" y="106" width="${campusWidth * 0.43}" height="84" rx="4" class="parcel-building"/><path d="M${campusX + campusWidth * 0.19} 122h${campusWidth * 0.28}M${campusX + campusWidth * 0.19} 147h${campusWidth * 0.28}M${campusX + campusWidth * 0.19} 173h${campusWidth * 0.28}" class="parcel-roof"/><rect x="${campusX + campusWidth * 0.65}" y="112" width="${campusWidth * 0.22}" height="32" rx="3" class="parcel-plant"/><rect x="${campusX + campusWidth * 0.65}" y="158" width="${campusWidth * 0.22}" height="32" rx="3" class="parcel-plant"/><path d="M${campusCenter} 18v42" class="parcel-grid-line"/><circle cx="${campusCenter}" cy="18" r="6" class="parcel-grid-point"/><text x="${campusCenter + 14}" y="25" class="parcel-map-label">Grid · month ${p.readiness.Power}</text><text x="${campusCenter}" y="88" text-anchor="middle" class="parcel-map-label">${brief.campus_acres} ac campus</text><path d="M${campusX + campusWidth * 0.2} 240v30H35M${campusX + campusWidth * 0.8} 240v64H605" class="parcel-fiber-line"/><circle cx="35" cy="270" r="5" class="parcel-fiber-point"/><circle cx="605" cy="304" r="5" class="parcel-fiber-point"/><text x="43" y="294" class="parcel-route-label">Fiber 1</text><text x="600" y="287" text-anchor="end" class="parcel-route-label">Fiber 2</text></svg><div class="parcel-area-ledger"><span><i class="parcel-key drainage"></i>Drainage / flood <b>${p.drainage_acres} ac</b></span><span><i class="parcel-key easement"></i>Easements <b>${p.easement_acres} ac</b></span><span><i class="parcel-key usable"></i>Usable <b>${usable} ac</b></span></div></div><div class="parcel-verdict ${pass ? "passes" : "blocked"}" role="status"><strong>${pass ? `${esc(p.label)} meets the month-${brief.deadline_month} brief` : `${esc(p.label)} misses the month-${brief.deadline_month} brief`}</strong><span>Services ready in month ${ready} · ${esc(constraint === "Two fiber routes" ? "the second fiber route" : constraint.toLowerCase())} sets the date${p.rights_resolved ? "" : "; land control remains unresolved"}.</span></div><dl class="parcel-decisions">${p.decisions.map((decision) => `<div class="${esc(decision.status)}"><dt>${esc(decision.label)}${decision.status === "pass" ? "" : `<span>${decision.status === "late" ? "Late" : "Unresolved"}</span>`}</dt><dd>${esc(decision.detail)}</dd></div>`).join("")}</dl>`;
  };
  $("concept")
    .querySelectorAll("[data-parcel]")
    .forEach((button) =>
      button.addEventListener("click", () => update(button.dataset.parcel)),
    );
  update(visual.parcels[0].id);
}

// ---- Lab definitions
// Each lab type is a thin interface over a tested model function. A lesson
// chooses its lab with "lab" ("none" hides the panel) and sets starting values
// with "lab_params", keyed by control id. Lessons without "lab" fall back to
// their domain's lab.
const DOMAIN_LABS = {
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
};
const COLOR = { amber: "#e5bb6e", grey: "#78999e", green: "#92ceb7", blue: "#8cb3ce", red: "#e59a8c" };
const range = (id, label, min, max, step, value, unit = "") => ({ id, kind: "range", label, min, max, step, value, unit });
const choice = (id, label, options, value) => ({ id, kind: "choice", label, options, value });
const verdict = (pass) => (pass ? "passes" : "fails");
// "a", "a and b", "a, b and c"
const listed = (items) => (items.length < 3 ? items.join(" and ") : `${items.slice(0, -1).join(", ")} and ${items.at(-1)}`);
function labType(l) {
  if (l.visual?.kind === "parcel" || l.lab === "none") return null;
  return l.lab || DOMAIN_LABS[l.domain] || null;
}
// Slider labels show as many decimals as the step, so 0.95 never reads as "1".
function valueLabel(control, value) {
  if (control.kind === "choice")
    return control.options.find(([option]) => option === value)?.[1] ?? String(value);
  const number = fixed(value, stepDecimals(control.step));
  return control.unit ? `${number} ${control.unit}` : number;
}
function flowRow(label, nodes) {
  return `<div><div class="diagram-label">${esc(label)}</div><div class="diagram-row">${nodes.map((n, i) => `${i ? '<span class="arrow" aria-hidden="true">→</span>' : ""}<span>${esc(n)}</span>`).join("")}</div></div>`;
}
function barChart(rows, max, label) {
  const top = Math.max(max, ...rows.map(([, value]) => value)) || 1;
  return `<div class="bars" role="img" aria-label="${esc(label)}">${rows.map(([title, value, color]) => `<div class="bar-item"><div class="bar-label"><span>${esc(title)}</span><b>${fmt(value)}</b></div><div class="bar-track"><div style="width:${Math.max(0, (value / top) * 100)}%;background:${color}"></div></div></div>`).join("")}</div>`;
}
function timelineBar(segments, finish) {
  const colors = { work: COLOR.green, save: COLOR.grey, lost: COLOR.red, recovery: COLOR.amber };
  const names = { work: "useful work", save: "checkpoint", lost: "lost work", recovery: "restore" };
  const summary = segments.map((s) => `${names[s.kind]} ${fmt(s.start)} to ${fmt(s.end)} min`).join("; ");
  return `<div class="lab-timeline" role="img" aria-label="Timeline: ${esc(summary)}">${segments.map((s) => `<span style="width:${(s.duration / finish) * 100}%;background:${colors[s.kind]}"></span>`).join("")}</div><p class="lab-legend">${Object.keys(names).map((kind) => `<span><i style="background:${colors[kind]}"></i>${names[kind]}</span>`).join("")}</p>`;
}
function positionGrid(positions) {
  const accepted = positions.filter((p) => p.accepted).length;
  return `<div class="lab-grid" role="img" aria-label="${accepted} of ${positions.length} positions have all three acceptances">${positions.map((p) => `<span class="${p.accepted ? "complete" : p.electrical || p.cooling || p.network ? "partial" : ""}"></span>`).join("")}</div><p class="lab-legend"><span><i class="complete"></i>all three accepted</span><span><i class="partial"></i>partly accepted</span></p>`;
}
function labDefinition(type) {
  if (type === "energy")
    return {
      title: "The same peak, a different energy bill",
      intro: "Build a day from up to three constant-power segments. Before you move a control, predict what changes: the height of the power trace or the area under it.",
      controls: [
        range("p1", "Segment 1 power", 0, 20, 1, 5, "MW"),
        range("h1", "Segment 1 duration", 0, 24, 1, 8, "h"),
        range("p2", "Segment 2 power", 0, 20, 1, 0, "MW"),
        range("h2", "Segment 2 duration", 0, 24, 1, 0, "h"),
        range("p3", "Segment 3 power", 0, 20, 1, 0, "MW"),
        range("h3", "Segment 3 duration", 0, 24, 1, 0, "h"),
      ],
      run(v) {
        const segments = [1, 2, 3]
          .map((i) => ({ powerMW: v[`p${i}`], hours: v[`h${i}`] }))
          .filter((s) => s.hours > 0);
        if (!segments.length) throw new RangeError("Give at least one segment a duration.");
        const m = profileSummary(segments);
        return {
          output: `${fmt(m.energyMWh)} MWh over ${fmt(m.hours)} h · average ${fmt(m.averageMW, 2)} MW · peak ${fmt(m.peakMW)} MW.`,
          boundary: "Each segment holds a constant load at one meter, so its energy is power × time. A varying trace needs interval-by-interval integration, and its peak alone sets no energy total.",
          graphic: barChart(
            segments.map((s, i) => [`Segment ${i + 1}: ${fmt(s.powerMW)} MW × ${fmt(s.hours)} h (MWh)`, profileSummary([s]).energyMWh, COLOR.amber]),
            0,
            "Energy in each segment is the area under its power trace.",
          ),
        };
      },
    };
  if (type === "facility")
    return {
      title: "Count every load once",
      intro: "Add identical racks, separately metered networking and storage, and facility overhead at matching boundaries. Then hold the total for a few hours to turn power into energy.",
      controls: [
        range("racks", "Identical racks", 1, 40, 1, 10),
        range("rack", "Input per rack", 10, 200, 5, 100, "kW"),
        range("network", "Networking and storage", 0, 400, 10, 100, "kW"),
        range("electrical", "Electrical losses", 0, 200, 5, 40, "kW"),
        range("cooling", "Cooling", 0, 600, 10, 160, "kW"),
        range("other", "Other facility loads", 0, 100, 5, 20, "kW"),
        range("hours", "Duration", 1, 24, 1, 4, "h"),
      ],
      run(v) {
        const m = facilityLedger({ racks: v.racks, rackKW: v.rack, networkKW: v.network, electricalLossKW: v.electrical, coolingKW: v.cooling, otherKW: v.other });
        const energy = profileSummary([{ hours: v.hours, powerMW: m.facilityKW / 1000 }]);
        return {
          output: `IT ${fmt(m.itKW)} kW + overhead ${fmt(m.overheadKW)} kW = ${fmt(m.facilityKW)} kW facility input · ${fmt(energy.energyMWh * 1000)} kWh over ${fmt(v.hours)} h · power ratio ${fixed(m.pue, 2)}.`,
          boundary: "All values are simultaneous steady real power. Rack inputs include their own power supplies and fans; networking and storage sit outside the rack totals and count once. The power ratio equals power usage effectiveness (PUE) only when both energies cover the same interval.",
          graphic: barChart(
            [
              ["Compute racks (kW)", m.rackTotalKW, COLOR.amber],
              ["Networking and storage (kW)", v.network, COLOR.blue],
              ["Facility overhead (kW)", m.overheadKW, COLOR.grey],
              ["Facility input (kW)", m.facilityKW, COLOR.green],
            ],
            0,
            "Facility input is IT power plus overhead.",
          ),
        };
      },
    };
  if (type === "pue")
    return {
      title: "Attach a denominator to the ratio",
      intro: "Enter one day of facility accounts. When IT energy falls while overhead stays fixed, power usage effectiveness (PUE) and energy per accepted job can move in opposite directions.",
      controls: [
        range("it", "IT energy", 10, 400, 1, 192, "MWh/day"),
        range("overhead", "Facility overhead energy", 0, 120, 1, 48, "MWh/day"),
        range("jobs", "Accepted jobs", 10, 200, 1, 96, "thousand/day"),
      ],
      run(v) {
        // Daily totals become average hourly rates over the same 24 hours.
        const m = efficiencyCase({ itKW: (v.it * 1000) / 24, overheadKW: (v.overhead * 1000) / 24, usefulUnitsPerHour: (v.jobs * 1000) / 24 });
        return {
          output: `PUE ${fmt(m.pue, 3)} · ${fmt(m.energyKWhPerUnit, 3)} kWh of facility energy per accepted job.`,
          boundary: "Facility and IT energy cover the same day, and every job is identical accepted work. PUE measures facility overhead; energy per job measures the service.",
          graphic: barChart(
            [
              ["IT energy (MWh/day)", v.it, COLOR.amber],
              ["Overhead energy (MWh/day)", v.overhead, COLOR.grey],
            ],
            0,
            "IT energy and overhead energy for one day.",
          ),
        };
      },
    };
  if (type === "kvcache")
    return {
      title: "How many requests fit in the cache?",
      intro: "Each active request keeps a key-value (KV) cache entry for every token of its context. Change the context length and predict how many complete requests a fixed pool can hold.",
      controls: [
        range("context", "Tokens per request", 1024, 131072, 1024, 8192, "tokens"),
        range("pool", "KV cache pool", 8, 256, 8, 64, "GiB"),
      ],
      run(v) {
        const m = llamaMemory({ contextTokens: v.context, kvPoolGiB: v.pool });
        return {
          output: `${fmt(m.kvBytesPerToken / 1024)} KiB per token × ${fmt(v.context)} tokens = ${fmt(m.requestGiB, 2)} GiB per request · ${m.concurrentRequests} complete ${m.concurrentRequests === 1 ? "request fits" : "requests fit"} in ${fmt(v.pool)} GiB.`,
          boundary: "Llama 3.1 70B geometry with bfloat16 (BF16) entries: 2 (key and value) × 80 layers × 8 KV heads × 128 dimensions × 2 bytes = 320 KiB per token. The pool excludes weights and workspace, and every request holds its full context without prefix sharing, block rounding or cache quantization.",
          graphic: barChart(
            [
              ["Cache per request (GiB)", m.requestGiB, COLOR.amber],
              ["Pool (GiB)", v.pool, COLOR.grey],
            ],
            0,
            "Cache per request compared with the pool.",
          ),
        };
      },
    };
  if (type === "samework")
    return {
      title: "Lower power can still cost more energy",
      intro: "Two runs finish the same accepted work. Change run B's mean power and duration, then compare complete-run energy instead of power.",
      controls: [
        range("apower", "Run A mean power", 20, 200, 5, 100, "kW"),
        range("aminutes", "Run A duration", 1, 60, 1, 10, "min"),
        range("bpower", "Run B mean power", 20, 200, 5, 80, "kW"),
        range("bminutes", "Run B duration", 1, 60, 1, 15, "min"),
      ],
      run(v) {
        const m = sameWorkEnergy({ powerRatio: v.bpower / v.apower, durationRatio: v.bminutes / v.aminutes, basePowerKW: v.apower, baseMinutes: v.aminutes });
        const change = (m.energyRatio - 1) * 100;
        return {
          output: `Run A ${fmt(m.runA.energyKWh)} kWh · run B ${fmt(m.runB.energyKWh)} kWh: ${Math.abs(change) < 1e-9 ? "the same energy" : `${fmt(Math.abs(change))}% ${change > 0 ? "more" : "less"} energy`} for the same output. At ${fmt(v.bpower)} kW, run B breaks even if it finishes within ${fmt(m.breakEvenDurationRatio * v.aminutes, 1)} min.`,
          boundary: "Each power is the mean over the entire run at the same meter, and both runs deliver identical accepted output at the same quality. Energy is mean power × duration.",
          graphic: barChart(
            [
              ["Run A energy (kWh)", m.runA.energyKWh, COLOR.grey],
              ["Run B energy (kWh)", m.runB.energyKWh, COLOR.amber],
            ],
            0,
            "Complete-run energy for the same accepted output.",
          ),
        };
      },
    };
  if (type === "phases")
    return {
      title: "Stagger the jobs, keep the energy",
      intro: "Four identical jobs repeat a 60-second cycle: 30 s at 120 kW, 15 s at 40 kW and 15 s at 60 kW. Offset their starts and compare the peak with the energy per cycle.",
      controls: [range("offset", "Offset between job starts", 0, 15, 5, 15, "s")],
      run(v) {
        const m = phaseSchedule({ offsetsSeconds: [0, 1, 2, 3].map((i) => i * v.offset) });
        const together = phaseSchedule({ offsetsSeconds: [0, 0, 0, 0] });
        return {
          output: `Peak ${fmt(m.peakKW)} kW (all in step: ${fmt(together.peakKW)} kW) · minimum ${fmt(m.minKW)} kW · average ${fmt(m.averageKW)} kW · ${fmt(m.energyKWh, 3)} kWh per cycle · ${m.maxTransitionKW ? `largest step ${fmt(m.maxTransitionKW)} kW` : "no step changes"}.`,
          boundary: "Independent jobs in steady periodic operation. Staggering adds no waiting or resource contention in this model, and ramp shapes and startup are left out.",
          graphic: barChart(
            [
              ["Peak (kW)", m.peakKW, COLOR.amber],
              ["Average (kW)", m.averageKW, COLOR.green],
              ["Minimum (kW)", m.minKW, COLOR.grey],
            ],
            together.peakKW,
            "Peak, average and minimum aggregate power over one cycle.",
          ),
        };
      },
    };
  if (type === "feeder")
    return {
      title: "Raise the voltage, cut the current",
      intro: "Deliver the same real power over the same three conductors at two voltages. Predict the current and the conductor heat before you move the controls.",
      controls: [
        range("power", "Delivered real power", 1, 20, 1, 10, "MW"),
        range("low", "Voltage A, line-to-line", 1, 40, 1, 10, "kV"),
        range("high", "Voltage B, line-to-line", 1, 40, 1, 20, "kV"),
        range("resistance", "Resistance per phase conductor", 0.01, 0.5, 0.01, 0.1, "Ω"),
        range("pf", "Power factor", 0.7, 1, 0.01, 1),
      ],
      run(v) {
        const at = (kV) => acdcConductorModel(v.power * 1000, kV * 1000, kV * 1000, v.pf, v.resistance, 1).ac;
        const a = at(v.low),
          b = at(v.high);
        return {
          output: `${fmt(v.low)} kV: ${fmt(a.amps, 2)} A per phase, ${fmt(a.lossKW)} kW conductor heat · ${fmt(v.high)} kV: ${fmt(b.amps, 2)} A, ${fmt(b.lossKW)} kW · difference ${fmt(Math.abs(a.lossKW - b.lossKW))} kW.`,
          boundary: "Balanced sinusoidal three-phase load with line-to-line RMS (root mean square) voltage: I = P / (√3 × V × power factor), and conductor heat = 3 × I² × R. Transformers, reactance and voltage drop are left out.",
          graphic: barChart(
            [
              [`${fmt(v.low)} kV conductor heat (kW)`, a.lossKW, COLOR.grey],
              [`${fmt(v.high)} kV conductor heat (kW)`, b.lossKW, COLOR.amber],
            ],
            0,
            "Conductor heat at the two voltages for the same delivered power.",
          ),
        };
      },
    };
  if (type === "staged")
    return {
      title: "Stage the supply behind an import limit",
      intro: "A 1,000 MW campus has a 100 MW grid import limit. Commission local generators, each able to supply up to 500 MW, and see how much load can run.",
      controls: [choice("generators", "Local generators available", [[0, "None"], [1, "One"], [2, "Two"]], 2)],
      run(v) {
        const served = stagedLoad(v.generators),
          campus = projectOptions().plannedMW;
        const trip = v.generators ? ` If one generator trips at this load, at least ${fmt(served - stagedLoad(v.generators - 1))} MW must come off at once.` : "";
        return {
          output: `${fmt(served)} MW of the ${fmt(campus)} MW campus can run.${trip}`,
          boundary: "Arithmetic upper bound with losses ignored. Surviving-generator ramp limits and reserve requirements can force a larger reduction.",
          graphic: barChart(
            [
              ["Load that can run (MW)", served, COLOR.amber],
              ["Campus load (MW)", campus, COLOR.grey],
            ],
            0,
            "Load that can run compared with the campus load.",
          ),
        };
      },
    };
  if (type === "wheel")
    return {
      title: "Check the route on the rack's heaviest day",
      intro: "Moving a rack puts its weight, plus the trolley, onto a few wheels. Compare the average force per wheel with the route's limit.",
      controls: [
        range("mass", "Rack or moving-assembly mass", 500, 4000, 50, 2200, "kg"),
        range("wheels", "Wheels sharing the load", 2, 8, 1, 4),
        range("limit", "Route limit per wheel", 1, 10, 0.5, 3, "kN"),
      ],
      run(v) {
        const m = movingLoad({ massKg: v.mass, contacts: v.wheels });
        const within = m.perContactKN <= v.limit;
        return {
          output: `${fixed(m.totalKN, 3)} kN total · ${fixed(m.perContactKN, 2)} kN average per wheel against a ${fixed(v.limit, 1)} kN limit: ${within ? "the average is within the limit; the actual load sharing decides" : "the route fails"}.`,
          boundary: "Average force per wheel with g = 9.81 m/s². The most heavily loaded wheel carries at least this, so a failure holds for any sharing; a pass still needs the actual load sharing, dynamic allowances and the support arrangement.",
          graphic: barChart(
            [
              ["Average force per wheel (kN)", m.perContactKN, within ? COLOR.green : COLOR.red],
              ["Route limit per wheel (kN)", v.limit, COLOR.grey],
            ],
            0,
            "Average force per wheel compared with the route limit.",
          ),
        };
      },
    };
  if (type === "ledger")
    return {
      title: "Check both limits in the power train",
      intro: "Add the proposed IT load, support load and losses, then test the upstream service and the downstream IT branch separately.",
      controls: [
        range("it", "IT load", 2, 8, 0.1, 5.1, "MW"),
        range("auxiliary", "Auxiliary loads", 0, 3, 0.1, 1.1, "MW"),
        range("losses", "Electrical losses", 0, 0.5, 0.01, 0.22, "MW"),
        range("service", "Service limit", 3, 10, 0.1, 6, "MW"),
        range("branch", "IT branch limit", 2, 8, 0.1, 4.8, "MW"),
      ],
      run(v) {
        const m = phaseLedger({ itMW: v.it, auxiliaryMW: v.auxiliary, lossMW: v.losses, serviceMW: v.service, branchMW: v.branch });
        const margin = (x) => (x >= 0 ? `${fixed(x, 2)} MW spare` : `${fixed(-x, 2)} MW over`);
        return {
          output: `Facility input ${fixed(m.inputMW, 2)} MW against the ${fmt(v.service)} MW service: ${margin(m.serviceHeadroomMW)} · IT ${fmt(v.it)} MW against the ${fmt(v.branch)} MW branch: ${margin(m.branchHeadroomMW)}.`,
          boundary: "Both limits are usable real-power limits. IT, auxiliaries and electrical losses are separate categories; losses are given estimates.",
          graphic: barChart(
            [
              ["Facility input (MW)", m.inputMW, m.serviceHeadroomMW >= 0 ? COLOR.green : COLOR.red],
              ["Service limit (MW)", v.service, COLOR.grey],
              ["IT load (MW)", v.it, m.branchHeadroomMW >= 0 ? COLOR.green : COLOR.red],
              ["IT branch limit (MW)", v.branch, COLOR.grey],
            ],
            0,
            "Facility input against the service limit, and IT load against the branch limit.",
          ),
        };
      },
    };
  if (type === "kva")
    return {
      title: "Kilowatts do not fill a kilovolt-ampere rating",
      intro: "Start from the DC output a converter must deliver. Divide by efficiency for input power and by power factor for apparent power, then find the line current at 480 V.",
      controls: [
        range("output", "DC output", 100, 1500, 10, 900, "kW"),
        range("efficiency", "Conversion efficiency", 0.85, 1, 0.01, 0.96),
        range("pf", "Input power factor", 0.7, 1, 0.01, 0.9),
        range("rating", "Usable apparent-power rating", 500, 2000, 50, 1000, "kVA"),
      ],
      run(v) {
        const m = loadFromDc({ outputKW: v.output, efficiency: v.efficiency, powerFactor: v.pf, voltageLL: 480, limitKVA: v.rating });
        return {
          output: `Input ${fmt(m.inputKW)} kW (${fmt(m.lossKW)} kW converter heat) · ${fmt(m.apparentKVA, 2)} kVA · ${fmt(m.currentA, 0)} A per line at 480 V · ${fmt(m.loading * 100, 2)}% of the ${fmt(v.rating)} kVA rating: ${verdict(m.passes)}.`,
          boundary: "Balanced three-phase input at 480 V line-to-line RMS (root mean square). Apparent power in kilovolt-amperes (kVA) = input kW ÷ power factor, and line current = VA ÷ (√3 × 480 V). Harmonics, imbalance and protective-device settings are left out.",
          graphic: barChart(
            [
              ["DC output (kW)", v.output, COLOR.blue],
              ["Input real power (kW)", m.inputKW, COLOR.amber],
              ["Apparent power (kVA)", m.apparentKVA, m.passes ? COLOR.green : COLOR.red],
              ["Rating (kVA)", v.rating, COLOR.grey],
            ],
            0,
            "Output, input real power and apparent power against the rating.",
          ),
        };
      },
    };
  if (type === "conversion")
    return {
      title: "Multiply the stages, then compare inputs",
      intro: "Two conversion paths deliver the same output. Overall efficiency is the product of the stage efficiencies, so work backward from the load to each path's input.",
      controls: [
        range("output", "Delivered output", 100, 5000, 100, 1000, "kW"),
        range("a1", "Path A, first stage", 0.9, 1, 0.005, 0.98),
        range("a2", "Path A, second stage", 0.9, 1, 0.005, 0.96),
        range("b1", "Path B, first stage", 0.9, 1, 0.005, 0.975),
        range("b2", "Path B, second stage", 0.9, 1, 0.005, 0.99),
      ],
      run(v) {
        const a = conversionPath(v.output, [v.a1, v.a2]),
          b = conversionPath(v.output, [v.b1, v.b2]);
        return {
          output: `Path A input ${fmt(a.inputKW)} kW (${fmt(a.lossKW)} kW lost) · path B input ${fmt(b.inputKW)} kW (${fmt(b.lossKW)} kW lost) · difference ${fmt(Math.abs(a.inputKW - b.inputKW))} kW.`,
          boundary: "Efficiencies are fixed values at one operating point, and each stage's output is the next stage's input. The comparison follows from the efficiencies, whatever the placement is called.",
          graphic: barChart(
            [
              ["Path A loss (kW)", a.lossKW, COLOR.grey],
              ["Path B loss (kW)", b.lossKW, COLOR.amber],
            ],
            0,
            "Conversion loss on each path for the same output.",
          ),
        };
      },
    };
  if (type === "migration")
    return {
      title: "Negotiate the rack upgrade",
      intro: "Two new racks share a 96% efficient sidecar with 3 kW of auxiliaries. Choose the rack setting, the row allocation and the deadline, then check power and schedule together.",
      controls: [
        choice("rack", "DC load per rack", [[120, "120 kW (full setting)"], [110, "110 kW (reduced setting)"]], 120),
        choice("allocation", "Row allocation", [[240, "240 kW (existing)"], [260, "260 kW (expanded)"]], 240),
        choice("deadline", "Service deadline", [[3, "3 weeks"], [8, "8 weeks"]], 3),
      ],
      run(v) {
        const m = migrationDecision({ rackKW: v.rack, allocationKW: v.allocation, deadlineWeeks: v.deadline });
        return {
          output: `Input ${fixed(m.inputKW, 3)} kW against ${fmt(v.allocation)} kW: ${m.marginKW >= 0 ? `${fixed(m.marginKW, 3)} kW spare` : `${fixed(-m.marginKW, 3)} kW short`} (${verdict(m.powerPass)}) · ready in ${m.readyWeeks} weeks against a ${m.deadlineWeeks}-week deadline (${verdict(m.schedulePass)}).`,
          boundary: "Row input = 2 × rack DC load ÷ 0.96 + 3 kW, with no simultaneous-load discount. Passing both screens still leaves workload and interface acceptance to prove.",
          graphic: barChart(
            [
              ["Row input (kW)", m.inputKW, m.powerPass ? COLOR.green : COLOR.red],
              ["Row allocation (kW)", v.allocation, COLOR.grey],
            ],
            0,
            "Row input compared with the allocation.",
          ),
        };
      },
    };
  if (type === "dc")
    return {
      title: "Move the conversion boundary",
      intro: "Hold the DC power fixed and change the distribution voltage. Compare the current, and the conductor loss at equal resistance, with a 50 V rack bus.",
      architecture: true,
      controls: [
        range("kw", "DC load", 50, 300, 10, 100, "kW"),
        range("volts", "DC distribution voltage", 50, 800, 1, 800, "V"),
      ],
      run(v) {
        const m = dcModel(v.kw, v.volts, 50);
        return {
          output: `${fmt(m.amps)} A at ${fmt(v.volts)} V against ${fmt(m.referenceAmps)} A at 50 V · conductor loss at equal resistance is ${fmt(m.lossRatio * 100, 2)}% of the 50 V loss.`,
          boundary: "Ideal P = V × I at the chosen DC segment, with the same load and the same conductor resistance, including the return path. Converters, insulation, protection, thermal limits, conductor sizing and cost are left out. The architecture buttons set representative 50 V or 800 V segments.",
          graphic: barChart(
            [
              ["50 V reference current (A)", m.referenceAmps, COLOR.grey],
              [`${fmt(v.volts)} V current (A)`, m.amps, COLOR.amber],
            ],
            0,
            "Current falls as voltage rises at fixed DC power.",
          ),
        };
      },
    };
  if (type === "acdc")
    return {
      title: "480 V three-phase AC versus 800 V DC",
      intro: "Hold delivered real power fixed. Distinguish the current in each conductor from the heat produced by all the conductors together.",
      architecture: true,
      controls: [
        range("kw", "Delivered real power", 50, 300, 10, 100, "kW"),
        range("volts", "DC pair voltage", 400, 1000, 1, 800, "V"),
        range("pf", "AC power factor", 0.7, 1, 0.01, 1),
        range("resistance", "Resistance per conductor", 1, 20, 1, 10, "mΩ"),
      ],
      run(v) {
        const m = acdcConductorModel(v.kw, 480, v.volts, v.pf, v.resistance / 1000, 1);
        return {
          output: `AC: ${fmt(m.ac.amps)} A RMS per line, ${fmt(m.ac.lossKW * 1000)} W conductor heat · DC: ${fmt(m.dc.amps)} A per conductor, ${fmt(m.dc.lossKW * 1000)} W conductor heat · DC heat is ${fmt(m.lossRatio * 100)}% of AC heat.`,
          boundary: "Receiving-end voltages: 480 V AC line-to-line RMS and the DC voltage across the pair. Balanced sinusoidal AC on three current-carrying conductors against two for DC, with equal resistance per conductor; neutral and protective earth are not counted. AC: P = √3 × V × I × power factor and heat = 3I²R. DC: P = VI and heat = 2I²R. Converters and cooling are left out, so the result sizes no cable. The architecture buttons locate conversion and leave these numbers unchanged.",
          graphic: barChart(
            [
              ["480 V AC: total conductor heat (W)", m.ac.lossKW * 1000, COLOR.grey],
              [`${fmt(v.volts)} V DC: total conductor heat (W)`, m.dc.lossKW * 1000, COLOR.amber],
            ],
            0,
            "Total conductor heat at equal delivered real power and resistance per conductor.",
          ),
        };
      },
    };
  if (type === "roofline")
    return {
      title: "Two ceilings on the same work",
      intro: "Arithmetic intensity counts the floating-point operations (FLOP) performed per byte moved across high-bandwidth memory (HBM). Move it and predict which ceiling binds first.",
      controls: [
        range("intensity", "Arithmetic intensity", 1, 400, 0.5, 12.5, "FLOP/byte"),
        range("bandwidth", "HBM bandwidth", 1, 8, 0.5, 8, "TB/s"),
        range("compute", "Compute rate", 100, 2500, 50, 200, "TFLOP/s"),
      ],
      run(v) {
        const m = roofline({ arithmeticIntensity: v.intensity, computeFlopsPerSecond: v.compute * 1e12, hbmBytesPerSecond: v.bandwidth * 1e12 });
        const binds = { memory: "memory bandwidth binds", compute: "the compute rate binds", balanced: "both ceilings meet" }[m.bottleneck];
        return {
          output: `${fmt(m.attainableFlopsPerSecond / 1e12)} TFLOP/s upper bound · ${binds} · ridge at ${fmt(m.kneeFlopsPerByte, 1)} FLOP/byte.`,
          boundary: "Ideal roofline: attainable rate = min(compute rate, bandwidth × intensity) for one numerical format, with traffic counted at the HBM boundary. It is a ceiling, not a benchmark or a token-rate prediction.",
          graphic: barChart(
            [
              ["Compute ceiling (TFLOP/s)", v.compute, COLOR.grey],
              ["Bandwidth × intensity ceiling (TFLOP/s)", m.bandwidthCeilingFlopsPerSecond / 1e12, COLOR.amber],
            ],
            0,
            "The lower of the compute and memory-bandwidth ceilings limits the operation.",
          ),
        };
      },
    };
  if (type === "bound")
    return {
      title: "Two time accounts for one operation",
      intro: "An operation needs arithmetic time (floating-point operations, or FLOP, ÷ compute rate) and memory time (bytes ÷ high-bandwidth memory (HBM) bandwidth). With ideal overlap, the longer account sets the bound.",
      controls: [
        range("work", "Arithmetic work", 0, 20, 0.5, 2, "TFLOP"),
        range("traffic", "HBM traffic", 1, 500, 1, 160, "GB"),
        range("compute", "Compute rate", 50, 2500, 50, 200, "TFLOP/s"),
        range("bandwidth", "HBM bandwidth", 1, 16, 0.5, 8, "TB/s"),
      ],
      run(v) {
        const m = workloadBound({ flops: v.work * 1e12, hbmBytes: v.traffic * 1e9, computeFlopsPerSecond: v.compute * 1e12, hbmBytesPerSecond: v.bandwidth * 1e12 });
        const binds = { memory: "memory traffic sets it", compute: "arithmetic sets it", balanced: "both accounts are equal", idle: "no work" }[m.bottleneck];
        return {
          output: `Arithmetic ${fmt(m.computeSeconds * 1000, 2)} ms · memory ${fmt(m.memorySeconds * 1000, 2)} ms · bound ${fmt(m.overlappedSeconds * 1000, 2)} ms with ideal overlap (${binds}) · ${fmt(m.serialSeconds * 1000, 2)} ms if fully serial.`,
          boundary: "Decimal units: 1 TB/s = 10¹² bytes per second. Rates are effective rates for this operation; network, launch and synchronization work are left out.",
          graphic: barChart(
            [
              ["Arithmetic time (ms)", m.computeSeconds * 1000, COLOR.grey],
              ["Memory time (ms)", m.memorySeconds * 1000, COLOR.amber],
            ],
            0,
            "Arithmetic and memory time for the same operation.",
          ),
        };
      },
    };
  if (type === "domains")
    return {
      title: "Where the failures land",
      intro: "Four independent groups of eight graphics processing units (GPUs) each host whole jobs. Place failures in different groups and count the jobs that can still run.",
      controls: [
        range("g1", "Failed GPUs in group 1", 0, 8, 1, 4),
        range("g2", "Failed GPUs in group 2", 0, 8, 1, 0),
        range("g3", "Failed GPUs in group 3", 0, 8, 1, 0),
        range("g4", "Failed GPUs in group 4", 0, 8, 1, 0),
        range("job", "GPUs per job", 1, 8, 1, 8),
      ],
      run(v) {
        const m = serviceDomains({ devicesPerGroup: 8, failedByGroup: [v.g1, v.g2, v.g3, v.g4], devicesPerJob: v.job });
        return {
          output: `${m.healthyDevices} healthy GPUs · ${m.runnableJobs} of ${m.nominalJobs} ${v.job}-GPU job slots can run · ${m.strandedHealthyDevices} healthy GPUs left over.`,
          boundary: "Each job must fit inside one group, and healthy GPUs in different groups cannot be combined in this scheduling mode.",
          graphic: barChart(
            m.groups.map((g) => [`Group ${g.index + 1}: healthy GPUs (${g.runnableJobs} ${g.runnableJobs === 1 ? "job" : "jobs"})`, g.healthyDevices, g.runnableJobs ? COLOR.green : COLOR.grey]),
            8,
            "Healthy GPUs and runnable jobs in each group.",
          ),
        };
      },
    };
  if (type === "fabric")
    return {
      title: "Count the paths, not the ports",
      intro: "Leaf switches connect endpoints below and spine switches above. Compare the capacity toward the endpoints with the capacity toward the spines, then bound a transfer between two leaves.",
      controls: [
        range("endpoints", "Endpoints per leaf", 1, 16, 1, 4),
        range("leaves", "Leaf switches", 2, 16, 1, 4),
        range("uplinks", "Uplinks per leaf", 1, 16, 1, 2),
        range("link", "Link rate", 100, 800, 100, 400, "Gb/s"),
        range("payload", "Payload between leaves", 1, 200, 1, 32, "GB"),
      ],
      run(v) {
        const m = fabricBudget({ endpointsPerLeaf: v.endpoints, leaves: v.leaves, uplinksPerLeaf: v.uplinks, linkGbps: v.link, payloadGB: v.payload });
        return {
          output: `${m.cables} cables and ${m.switchPorts} switch ports · ${fmt(m.downGbps)} Gb/s toward endpoints and ${fmt(m.upGbps)} Gb/s toward spines per leaf (${fmt(m.oversubscription, 2)}:1) · ${fmt(m.transferSeconds, 2)} s to move ${fmt(v.payload)} GB.`,
          boundary: "One direction, decimal units, eight bits per byte and evenly spread traffic. Protocol overhead and queueing are left out.",
          graphic: barChart(
            [
              ["Toward endpoints per leaf (Gb/s)", m.downGbps, COLOR.grey],
              ["Toward spines per leaf (Gb/s)", m.upGbps, COLOR.amber],
            ],
            0,
            "Leaf capacity toward endpoints and toward spines.",
          ),
        };
      },
    };
  if (type === "overlap")
    return {
      title: "Hide communication behind compute",
      intro: "Each of four workers sends 1.5 GB per ring all-reduce: six rounds of 0.25 GB. Change the ring rate and the overlap, and watch the step time.",
      controls: [
        range("rate", "Payload rate per ring edge", 5, 100, 5, 50, "GB/s"),
        range("compute", "Compute per step", 100, 400, 10, 200, "ms"),
        range("overlap", "Communication overlapped with compute", 0, 100, 5, 20, "ms"),
      ],
      run(v) {
        const exchange = messageTime({ bytes: 1.5e9, gbps: v.rate * 8, startupUs: 0 });
        const m = communicationTime({ communicationMs: exchange.totalUs / 1000, computeMs: v.compute, overlapMs: v.overlap });
        return {
          output: `Communication ${fmt(m.communicationMs)} ms, ${fmt(m.exposedMs)} ms exposed · step ${fmt(m.sequentialStepMs)} ms without overlap, ${fmt(m.overlappedStepMs)} ms with it.`,
          boundary: "Bandwidth-only ring model with every edge running at once. Per-round startup and reduction work are left out.",
          graphic: barChart(
            [
              ["Compute (ms)", v.compute, COLOR.grey],
              ["Exposed communication (ms)", m.exposedMs, COLOR.amber],
              ["Step with overlap (ms)", m.overlappedStepMs, COLOR.green],
            ],
            m.sequentialStepMs,
            "Compute, exposed communication and the overlapped step time.",
          ),
        };
      },
    };
  if (type === "network")
    return {
      title: "A port rate is not a job rate",
      intro: "Hold the payload fixed. Predict how link rate and the achieved useful fraction change an ideal transfer time.",
      controls: [
        range("payload", "Payload (decimal)", 10, 500, 10, 100, "GB"),
        range("rate", "Aggregate link rate", 100, 1600, 100, 400, "Gb/s"),
        range("efficiency", "Achieved useful fraction", 25, 100, 5, 80, "%"),
      ],
      run(v) {
        const m = transferModel(v.payload, v.rate, v.efficiency / 100);
        return {
          output: `${fmt(m.GBps)} GB/s effective payload rate · ${fmt(m.seconds, 2)} s ideal transfer time.`,
          boundary: "Decimal GB and Gb with eight bits per byte, for one serial transfer at the given achieved fraction. Queueing, startup latency, collective structure, storage limits and overlapping work are left out.",
          graphic: flowRow("A PAYLOAD MUST CROSS THE SPECIFIED BOUNDARY", ["Sender", "Shared fabric resources", "Receiver"]),
        };
      },
    };
  if (type === "ckptwrite")
    return {
      title: "The slowest stage sets the checkpoint",
      intro: "A checkpoint crosses source staging, the network and backend storage, after serialized shard setup and before a final commit. Find the stage that limits it.",
      controls: [
        range("payload", "Checkpoint size", 64, 2048, 64, 512, "GB"),
        range("source", "Source staging rate", 4, 64, 1, 16, "GB/s"),
        range("network", "Network rate", 4, 64, 1, 24, "GB/s"),
        range("backend", "Backend write rate", 4, 64, 1, 20, "GB/s"),
        range("shards", "Shards", 256, 16384, 256, 4096),
      ],
      run(v) {
        const m = checkpointTransfer({ payloadGB: v.payload, sourceGBps: v.source, networkGBps: v.network, backendGBps: v.backend, shards: v.shards, metadataOps: 1024, commitSeconds: 2 });
        const limit = [["source staging", v.source], ["the network", v.network], ["backend storage", v.backend]]
          .filter(([, rate]) => rate === m.payloadGBps)
          .map(([name]) => name);
        return {
          output: `${fmt(m.metadataSeconds)} s shard setup + ${fmt(m.payloadSeconds)} s payload at ${fmt(m.payloadGBps)} GB/s (limited by ${listed(limit)}) + ${fmt(m.commitSeconds)} s commit = ${fmt(m.totalSeconds)} s to a durable checkpoint.`,
          boundary: "Payload stages overlap ideally. Shard setup runs first at 1,024 metadata operations per second, and a 2-second commit follows the transfer.",
          graphic: barChart(
            [
              ["Shard setup (s)", m.metadataSeconds, COLOR.grey],
              ["Payload (s)", m.payloadSeconds, COLOR.amber],
              ["Commit (s)", m.commitSeconds, COLOR.blue],
            ],
            0,
            "Time spent in each checkpoint phase.",
          ),
        };
      },
    };
  if (type === "timeline")
    return {
      title: "Count preserved and lost progress",
      intro: "A job needs 60 useful minutes and fails once. Change how often it saves and when the failure strikes, then follow the finish time.",
      controls: [
        range("interval", "Useful minutes between checkpoints", 5, 60, 5, 20, "min"),
        range("save", "Checkpoint pause", 1, 10, 1, 2, "min"),
        range("failure", "Failure at wall-clock minute", 0, 120, 1, 35),
        range("recovery", "Restore time", 0, 15, 1, 5, "min"),
      ],
      run(v) {
        const m = checkpointTimeline({ targetMinutes: 60, intervalMinutes: v.interval, saveMinutes: v.save, failureMinute: v.failure, recoveryMinutes: v.recovery });
        return {
          output: m.failed
            ? `Finishes at minute ${fmt(m.finishMinute)}: ${fmt(m.lostMinutes)} useful minutes lost, ${fmt(m.saveMinutes)} min saving, ${fmt(m.recoveryMinutes)} min restoring.`
            : `Finishes at minute ${fmt(m.finishMinute)}, before the failure time: ${fmt(m.saveMinutes)} min saving.`,
          boundary: "A valid checkpoint exists at zero progress, and no final checkpoint is needed to finish. Work since the last completed checkpoint is lost at the failure.",
          graphic: timelineBar(m.segments, m.finishMinute),
        };
      },
    };
  if (type === "checkpoint")
    return {
      title: "Save too often or repeat too much",
      intro: "Longer intervals reduce checkpoint overhead but increase the progress a failure is expected to erase. Compare the two terms.",
      controls: [
        range("interval", "Useful-work checkpoint interval", 60, 3600, 30, 900, "s"),
        range("pause", "Checkpoint pause", 5, 180, 5, 30, "s"),
        range("mttf", "Mean time to failure", 1, 48, 1, 10, "h"),
      ],
      run(v) {
        const m = checkpointModel(v.pause, v.interval, v.mttf);
        const young = `Young's interval for these inputs is ${fmt(m.optimumSeconds, 0)} s.`;
        if (m.checkpointFraction > 0.1)
          return {
            output: `Checkpoint pauses take ${fmt(m.checkpointFraction * 100)}% of useful time, beyond this first-order model's 10% limit. ${young}`,
            boundary: "Use a detailed timeline when overhead is this large.",
            graphic: "",
          };
        return {
          output: `${fmt(m.checkpointFraction * 100, 2)}% checkpoint overhead + ${fmt(m.recomputeFraction * 100, 2)}% expected recomputation. ${young}`,
          boundary: "First-order model: overhead C ÷ T plus expected lost work T ÷ (2M), for checkpoint pause C, useful-work interval T and mean time to failure (MTTF) M. Failures arrive at random at a steady average rate, overhead is small and restarts cost nothing. The two terms balance at T = √(2CM), the first-order interval Young derived in 1974.",
          graphic: barChart(
            [
              ["Checkpoint overhead (%)", m.checkpointFraction * 100, COLOR.grey],
              ["Expected recomputation (%)", m.recomputeFraction * 100, COLOR.amber],
            ],
            10,
            "Checkpointing more often trades shorter lost work for more checkpoint pauses.",
          ),
        };
      },
    };
  if (type === "placement")
    return {
      title: "Free GPUs are not always usable",
      intro: "A job needs a number of free nodes inside one topology group, eight graphics processing units (GPUs) per node. Change how many nodes are free in each group and check whether it can launch.",
      controls: [
        range("a", "Free nodes in group A", 0, 4, 1, 2),
        range("b", "Free nodes in group B", 0, 4, 1, 2),
        range("nodes", "Nodes the job needs", 1, 4, 1, 4),
      ],
      run(v) {
        const group = (free) => [0, 1, 2, 3].map((i) => i < free);
        const m = eligibleGroups({ groups: [group(v.a), group(v.b)], nodesRequired: v.nodes, gpusPerNode: 8 });
        return {
          output: `${m.freeGPUs} free GPUs · ${m.eligible.length ? `group ${m.eligible.map((i) => "AB"[i]).join(" or ")} can host the ${v.nodes}-node job` : `no group has ${v.nodes} free ${v.nodes === 1 ? "node" : "nodes"}, so the job waits`}.`,
          boundary: "Every free node is healthy and runs the validated software image. Placement across groups is outside the accepted service configuration.",
          graphic: barChart(
            m.freeByGroup.map((free, i) => [`Group ${"AB"[i]}: free nodes`, free, free >= v.nodes ? COLOR.green : COLOR.grey]),
            4,
            "Free nodes in each topology group.",
          ),
        };
      },
    };
  if (type === "heat")
    return {
      title: "Carry the heat, then reject it",
      intro: "Predict how much water flow is needed when the permitted temperature rise changes. The heat duty stays fixed.",
      controls: [
        range("duty", "IT heat captured", 50, 300, 10, 100, "kW"),
        range("delta", "Water temperature rise", 5, 20, 1, 10, "°C"),
        range("auxiliary", "Auxiliary work within boundary", 0, 50, 5, 20, "kW"),
      ],
      run(v) {
        const m = thermalModel(v.duty, v.delta, v.auxiliary);
        return {
          output: `${fmt(m.kgPerSecond, 2)} kg/s ≈ ${fmt(m.litersPerMinute)} L/min of water · ${fmt(m.rejectedKW)} kW rejected within the boundary.`,
          boundary: "Q = mass flow × specific heat × temperature rise, with water cp = 4.18 kJ/(kg·K) and density 1 kg/L. All auxiliary input inside the boundary becomes heat. Pressure drop, approach temperature and equipment ratings are left out.",
          graphic: flowRow("SEPARATE FLUID CIRCUITS; HEAT CROSSES THE WALL", ["Chip loop", "Heat exchanger wall", "Facility loop", "Environment"]),
        };
      },
    };
  if (type === "junction")
    return {
      title: "Same heat, different chip temperature",
      intro: "A device's temperature is its local coolant temperature plus heat × the effective thermal resistance of its path. Change the path and compare the result with the limit.",
      controls: [
        range("heat", "Device heat", 100, 1200, 10, 400, "W"),
        range("fluid", "Local coolant temperature", 15, 50, 1, 35, "°C"),
        range("resistance", "Effective thermal resistance", 0.02, 0.2, 0.005, 0.08, "K/W"),
        range("limit", "Maximum junction temperature", 60, 110, 1, 80, "°C"),
      ],
      run(v) {
        const m = deviceTemperature({ watts: v.heat, fluidC: v.fluid, resistance: v.resistance, limitC: v.limit });
        return {
          output: `${fmt(m.junctionC)} °C at the junction · ${m.passes ? `${fmt(m.marginK)} K below` : `${fmt(-m.marginK)} K above`} the ${fmt(v.limit)} °C limit.`,
          boundary: "Steady state, with one effective resistance from the junction to the local coolant reference.",
          graphic: barChart(
            [
              ["Junction temperature (°C)", m.junctionC, m.passes ? COLOR.green : COLOR.red],
              ["Limit (°C)", v.limit, COLOR.grey],
            ],
            0,
            "Junction temperature compared with the limit.",
          ),
        };
      },
    };
  if (type === "pump")
    return {
      title: "Where the pump and the circuit agree",
      intro: "The pump curve (Δp = 160 − 10q² kPa, with q in L/s) meets the circuit curve (Δp = k × q²) at one flow. Change the circuit and follow the flow, pressure, pump power and coolant temperature rise.",
      controls: [
        range("resistance", "Circuit coefficient k", 5, 90, 5, 30, "kPa per (L/s)²"),
        range("heat", "Heat captured", 20, 200, 2, 84, "kW"),
      ],
      run(v) {
        const m = hydraulicPoint({ resistance: v.resistance, heatKW: v.heat, cp: 4.2 });
        return {
          output: `${fixed(m.flowLs, 2)} L/s (${fmt(m.flowLs * 60)} L/min) at ${fmt(m.pressureKPa)} kPa · ${fmt(m.hydraulicW)} W hydraulic, ${fmt(m.inputW)} W pump input · ${fmt(m.deltaK)} K coolant rise.`,
          boundary: "Water with cp = 4.2 kJ/(kg·K) and density 1 kg/L; overall pump efficiency 60%. Both curves are teaching inventions, and pump heat is left out of the temperature rise.",
          graphic: barChart(
            [
              ["Hydraulic power (W)", m.hydraulicW, COLOR.grey],
              ["Pump electrical input (W)", m.inputW, COLOR.amber],
            ],
            0,
            "Hydraulic power and pump input at the operating point.",
          ),
        };
      },
    };
  if (type === "chiller")
    return {
      title: "Follow the heat past the chiller",
      intro: "A chiller moves heat from its evaporator to its condenser using compressor work. Change the load and the electrical inputs, and compare the chiller and plant coefficients of performance (COP).",
      controls: [
        range("duty", "Evaporator load", 1, 20, 0.5, 10, "MW"),
        range("compressor", "Compressor input", 0.5, 6, 0.1, 2, "MW"),
        range("auxiliary", "Pumps and fans outside the chiller", 0, 2, 0.1, 0.5, "MW"),
      ],
      run(v) {
        const m = chillerBalance({ dutyMW: v.duty, compressorMW: v.compressor, auxiliaryMW: v.auxiliary });
        return {
          output: `Chiller COP ${fmt(m.compressorCOP, 2)} · plant COP ${fmt(m.plantCOP, 2)} · the condenser rejects ${fmt(m.condenserMW)} MW, and ${fmt(m.condenserMW + v.auxiliary)} MW reaches the environment in total.`,
          boundary: "Steady operating point. The chiller COP counts compressor input only; the plant COP adds the pumps and fans, whose heat leaves outside the condenser.",
          graphic: barChart(
            [
              ["Evaporator load (MW)", v.duty, COLOR.blue],
              ["Condenser heat (MW)", m.condenserMW, COLOR.amber],
              ["Plant electrical input (MW)", m.plantInputMW, COLOR.grey],
            ],
            0,
            "Heat extracted, heat rejected at the condenser and plant electrical input.",
          ),
        };
      },
    };
  if (type === "weather")
    return {
      title: "Which limit binds on a hot day?",
      intro: "Cooling electricity grows as the coefficient of performance (COP) falls, and the plant can reject less heat. Choose a weather bin and an IT load, then check the electrical and thermal limits.",
      controls: [
        choice("condition", "Weather bin", [["cool", "Cool: COP 8, 9 MW thermal limit"], ["hot", "Hot: COP 4, 8.5 MW thermal limit"]], "hot"),
        range("it", "Requested IT load", 1, 12, 0.1, 8, "MW"),
        range("site", "Site electrical limit", 5, 15, 0.1, 10, "MW"),
        range("other", "Other facility load", 0, 2, 0.1, 0.4, "MW"),
      ],
      run(v) {
        const m = operatingPoint({ condition: v.condition, requestedITMW: v.it, siteMW: v.site, otherMW: v.other });
        return {
          output: `Demand ${fmt(m.totalMW, 2)} MW against ${fmt(v.site)} MW: ${m.electricalFits ? "fits" : "exceeds the site limit"} · IT ceilings: electrical ${fmt(m.electricalMW, 2)} MW, thermal ${fmt(m.thermalMW, 2)} MW, so at most ${fmt(m.feasibleMW, 2)} MW of IT can run.`,
          boundary: "Constant COP within each bin, and cooling input covers all plant auxiliaries. IT power becomes the cooling duty.",
          graphic: barChart(
            [
              ["Electrical IT ceiling (MW)", m.electricalMW, COLOR.amber],
              ["Thermal IT ceiling (MW)", m.thermalMW, COLOR.blue],
              ["Requested IT (MW)", v.it, m.electricalFits && m.thermalFits ? COLOR.green : COLOR.red],
            ],
            0,
            "Electrical and thermal ceilings on IT load compared with the request.",
          ),
        };
      },
    };
  if (type === "tower")
    return {
      title: "Count water at the boundary",
      intro: "A cooling tower loses water to evaporation and bleeds some off as blowdown to limit dissolved solids. Count intake and consumption against the same day's IT energy.",
      controls: [
        range("evaporation", "Evaporation", 10, 300, 5, 100, "m³/day"),
        range("cycles", "Concentration ratio", 1.5, 10, 0.5, 5),
        range("it", "IT energy", 10, 300, 5, 100, "MWh/day"),
        choice("returned", "Blowdown returned to the same basin", [["yes", "Yes, after treatment"], ["no", "Not accounted for"]], "yes"),
      ],
      run(v) {
        // Water intensity here uses IT energy only, so the facility total equals it.
        const m = towerLedger({ evaporationM3: v.evaporation, cycles: v.cycles, itMWh: v.it, facilityMWh: v.it, returnKnown: v.returned === "yes" });
        return {
          output: `Blowdown ${fmt(m.blowdownM3)} m³ · makeup ${fmt(m.makeupM3)} m³ · intake ${fixed(m.intakeLitresPerKWh, 2)} L/kWh · consumption ${m.consumptionLitresPerKWh === null ? "unknown until the return flow is accounted for" : `${fixed(m.consumptionLitresPerKWh, 2)} L/kWh`}.`,
          boundary: "One day with negligible drift, leaks and storage change; dissolved solids leave only through blowdown, so blowdown = evaporation ÷ (concentration ratio − 1).",
          graphic: barChart(
            [
              ["Evaporation (m³)", m.evaporationM3, COLOR.blue],
              ["Blowdown (m³)", m.blowdownM3, COLOR.grey],
              ["Makeup intake (m³)", m.makeupM3, COLOR.amber],
            ],
            0,
            "Daily evaporation, blowdown and makeup water.",
          ),
        };
      },
    };
  if (type === "schedule")
    return {
      title: "The join waits for every path",
      intro: "Electrical and cooling procurement start after a 2-week requirements phase and are followed by 3 and 4 weeks of installation; the utility path runs from the start. Final integration takes 4 weeks after all three are ready.",
      controls: [
        range("electrical", "Electrical procurement", 2, 40, 1, 18, "weeks"),
        range("cooling", "Cooling procurement", 2, 40, 1, 10, "weeks"),
        range("utility", "Utility path ready at week", 2, 50, 1, 16),
      ],
      run(v) {
        const m = deliverySchedule({ electricalProcurement: v.electrical, coolingProcurement: v.cooling, utilityReady: v.utility });
        return {
          output: `Electrical ready week ${m.electrical} · cooling week ${m.cooling} · utility week ${m.utility} · accepted at week ${m.finish}, set by ${listed([...m.critical])}.`,
          boundary: "Continuous weeks with unconstrained resources and no calendar effects.",
          graphic: barChart(
            [
              ["Electrical ready (week)", m.electrical, m.critical.includes("electrical") ? COLOR.amber : COLOR.grey],
              ["Cooling ready (week)", m.cooling, m.critical.includes("cooling") ? COLOR.amber : COLOR.grey],
              ["Utility ready (week)", m.utility, m.critical.includes("utility") ? COLOR.amber : COLOR.grey],
              ["Accepted (week)", m.finish, COLOR.green],
            ],
            0,
            "Ready weeks for each path and the acceptance week.",
          ),
        };
      },
    };
  if (type === "interfaces")
    return {
      title: "Same megawatts, new interfaces",
      intro: "Denser racks keep a zone's total power but concentrate it on each branch. Check a reused 480 V branch's current, coolant flow and pressure, then see how the approval date moves acceptance.",
      controls: [
        range("rack", "Rack power", 100, 250, 10, 200, "kW"),
        range("approval", "Required approvals arrive at week", 0, 8, 1, 3),
      ],
      run(v) {
        const m = rackInterfaces({ rackKW: v.rack });
        const s = modularSchedule({ approvalWeek: v.approval });
        return {
          output: `${fmt(m.amps)} A against 160 A (${verdict(m.electricalPass)}) · ${fmt(m.flow, 2)} kg/s against 3.0 kg/s (${verdict(m.flowPass)}) · ${fmt(m.pressure)} kPa against 60 kPa available (${verdict(m.pressurePass)}) · accepted at week ${s.finish}.`,
          boundary: "Balanced 480 V three-phase input at power factor 1 on one supply path; all IT heat enters water with a 10 K rise, and branch pressure drop scales with flow squared from 20 kPa at the old flow. Factory work takes 6 weeks and transport 1; site work finishes at week 8, then connections take 2 weeks and acceptance 2.",
          graphic: barChart(
            [
              ["Branch current as % of 160 A", (m.amps / 160) * 100, m.electricalPass ? COLOR.green : COLOR.red],
              ["Flow as % of 3.0 kg/s", (m.flow / 3) * 100, m.flowPass ? COLOR.green : COLOR.red],
              ["Pressure as % of 60 kPa", (m.pressure / 60) * 100, m.pressurePass ? COLOR.green : COLOR.red],
            ],
            100,
            "Each branch quantity as a share of its limit.",
          ),
        };
      },
    };
  if (type === "paths")
    return {
      title: "Commission the intersection",
      intro: "Each discipline accepts a range of the 100 rack positions A01 to A100. Only positions that every discipline has accepted form complete service paths.",
      controls: [
        range("electrical", "Electrical accepted A01 to", 0, 100, 1, 80),
        range("coolingfrom", "Cooling accepted from", 1, 100, 1, 21),
        range("coolingto", "Cooling accepted to", 1, 100, 1, 100),
        range("network", "Network accepted A01 to", 0, 100, 1, 60),
        range("rack", "Power per position", 50, 200, 10, 100, "kW"),
      ],
      run(v) {
        const m = acceptedPaths({ electricalEnd: v.electrical, coolingStart: v.coolingfrom, coolingEnd: v.coolingto, networkEnd: v.network, rackKW: v.rack });
        const name = (id) => `A${String(id).padStart(2, "0")}`;
        return {
          output: m.count
            ? `${m.count} complete rack paths (${name(m.accepted[0].id)} to ${name(m.accepted.at(-1).id)}) · ${fmt(m.envelopeMW)} MW envelope at ${fmt(v.rack)} kW per position.`
            : "No position has all three acceptances.",
          boundary: "All other acceptance criteria are met for the intersecting positions. The envelope is accepted capacity, not operating demand.",
          graphic: positionGrid(m.positions),
        };
      },
    };
  if (type === "heatbalance")
    return {
      title: "Match the readings before you multiply",
      intro: "Heat duty is flow × specific heat × temperature rise. Combine a flow and temperatures observed on the same loop at the same time; a stale reading gives a believable wrong duty.",
      controls: [
        range("flow", "Flow", 10, 200, 5, 100, "kg/s"),
        range("supply", "Supply temperature", 20, 40, 0.5, 30, "°C"),
        range("return", "Return temperature", 20, 55, 0.5, 35, "°C"),
      ],
      run(v) {
        const m = heatBalance({ flow: v.flow, supply: v.supply, returnTemperature: v.return, cp: 4.18 });
        return {
          output: `${fmt(m.heatMW * 1000)} kW = ${fmt(v.flow)} kg/s × 4.18 kJ/(kg·K) × ${fmt(m.deltaT)} K.`,
          boundary: "Steady loop, with water cp = 4.18 kJ/(kg·K). The three readings must describe the same loop over the same interval.",
          graphic: "",
        };
      },
    };
  if (type === "transition")
    return {
      title: "Admit the load when the cooling is ready",
      intro: "A step in heat input can outrun the cooling that is already running. Until standby capacity is ready, the difference draws down a limited thermal buffer.",
      controls: [
        range("load", "Heat input after the step", 1, 12, 0.5, 6, "MW"),
        range("removal", "Active heat removal", 1, 12, 0.5, 5, "MW"),
        range("delay", "Standby readiness delay", 0, 10, 0.5, 2, "min"),
        range("buffer", "Usable thermal buffer", 0.01, 0.2, 0.01, 0.04, "MWh"),
        choice("admit", "Admit the new work", [["now", "Now"], ["ready", "After standby cooling is ready"]], "now"),
      ],
      run(v) {
        const m = transition({ loadMW: v.load, removalMW: v.removal, delayMinutes: v.delay, allowanceMWh: v.buffer, admit: v.admit });
        // With no buffer, name that directly instead of a "0.00 MWh buffer".
        const noBuffer = v.buffer === 0;
        const bufferState = noBuffer ? "so no thermal buffer is needed" : `and the ${fixed(v.buffer, 2)} MWh buffer stays full`;
        const output = m.imbalanceMW === 0
          ? v.admit === "ready"
            ? `The work waits ${fmt(m.waitMinutes)} min for standby cooling, ${bufferState}.`
            : `Active removal covers the heat input, ${bufferState}.`
          : noBuffer
            ? `${fmt(m.imbalanceMW)} MW imbalance for ${fmt(v.delay)} min leaves ${fixed(m.consumedMWh, 4)} MWh of heat with no thermal buffer to absorb it.`
            : `${fmt(m.imbalanceMW)} MW imbalance for ${fmt(v.delay)} min uses ${fixed(m.consumedMWh, 4)} MWh of the ${fixed(v.buffer, 2)} MWh buffer: ${m.withinBudget ? `${fixed(m.remainingMWh, 4)} MWh remains` : `${fixed(-m.remainingMWh, 4)} MWh short`}.`;
        return {
          output,
          boundary: "Energy arithmetic only: imbalance × delay. All other operating conditions are assumed met, and temperatures, rates of change and control behavior need their own checks.",
          graphic: barChart(
            [
              ["Heat accumulated before standby is ready (MWh)", m.consumedMWh, m.withinBudget ? COLOR.green : COLOR.red],
              ["Buffer available (MWh)", v.buffer, COLOR.grey],
            ],
            0,
            "Heat accumulated before standby cooling is ready, compared with the thermal buffer available.",
          ),
        };
      },
    };
  if (type === "availability")
    return {
      title: "Count overlapping outages once",
      intro: "Two incidents affect the same service during a 30-day window of 43,200 minutes. Where their impact overlaps, count the shared minutes once.",
      controls: [
        range("a", "Incident A impact", 0, 120, 1, 12, "min"),
        range("b", "Incident B impact", 0, 120, 1, 18, "min"),
        range("overlap", "Minutes both incidents share", 0, 120, 1, 4, "min"),
      ],
      run(v) {
        const overlap = Math.min(v.overlap, v.a, v.b);
        const m = unavailableUnion([[0, v.a], [v.a - overlap, v.a - overlap + v.b]], { windowStart: 0, windowEnd: 43200 });
        return {
          output: `${fmt(m.downtime)} unavailable minutes (${fmt(v.a)} + ${fmt(v.b)} − ${fmt(overlap)}) · availability ${fixed(m.availability * 100, 4)}%${overlap < v.overlap ? " · the shared minutes cannot exceed the shorter incident" : ""}.`,
          boundary: "A retrospective, time-based measure of one defined service over the stated window. It certifies no topology and guarantees no future availability.",
          graphic: "",
        };
      },
    };
  if (type === "rental")
    return {
      title: "Commitment or pool?",
      intro: "A committed contract pays for every GPU-hour in the year; a pool earns only on the hours it rents. Change the rates and the occupancy, and find where the two revenues meet.",
      controls: [
        range("gpus", "GPUs", 128, 8192, 128, 1024),
        range("committed", "Committed rate", 0.5, 6, 0.05, 2.5, "$/GPU-hour"),
        range("pool", "Pool rate", 0.5, 8, 0.05, 4, "$/GPU-hour"),
        range("occupancy", "Pool occupancy", 0, 100, 1, 50, "%"),
      ],
      run(v) {
        const m = rentalRevenue({ gpus: v.gpus, hours: 8760, committedRate: v.committed, marketRate: v.pool, occupancy: v.occupancy / 100 });
        return {
          output: `${fmt(m.availableHours)} GPU-hours in a year · committed $${fmt(m.committed, 0)} · pool $${fmt(m.market, 0)} at ${fmt(v.occupancy)}% occupancy · equal revenue at ${fmt(m.breakEven * 100)}% occupancy.`,
          boundary: "Rental revenue only, for the same service scope over one year. Costs, financing and risk can change which strategy is better.",
          graphic: barChart(
            [
              ["Committed revenue ($ million)", m.committed / 1e6, COLOR.grey],
              ["Pool revenue ($ million)", m.market / 1e6, COLOR.amber],
            ],
            0,
            "Committed and pool revenue over one year.",
          ),
        };
      },
    };
  if (type === "capacity")
    return {
      title: "Count complete service paths",
      intro: "All limits use the same 100 kW rack load. A larger electrical budget adds racks only when cooling and accepted paths keep up.",
      controls: [
        range("overhead", "Site auxiliary draw", 10, 35, 1, 20, "MW"),
        range("cooling", "Cooling limit at IT boundary", 40, 90, 5, 60, "MW"),
        range("accepted", "Accepted rack paths", 100, 1000, 50, 900, "racks"),
      ],
      run(v) {
        const m = capacityModel(100, v.overhead, v.cooling, 100, v.accepted);
        return {
          output: `${m.racks} complete 100 kW rack equivalents · binding: ${listed([...m.binding])}.`,
          boundary: "A 100 MW site limit, instantaneous auxiliary draw, 100 kW per rack, cooling stated at the IT boundary and accepted end-to-end rack paths, in whole racks. Workload performance, reserve margins and local distribution limits are left out.",
          graphic: barChart(
            [
              ["Electrical IT budget (MW)", m.powerMW, COLOR.amber],
              ["IT cooling limit (MW)", v.cooling, COLOR.green],
              ["Accepted rack-path equivalent (MW)", m.acceptedMW, COLOR.blue],
            ],
            100,
            "The minimum of electrical, cooling and accepted-path capacities bounds the number of usable racks.",
          ),
        };
      },
    };
  if (type === "continuity")
    return {
      title: "Power survives. Does the service?",
      intro: "Stored energy, inverter power and cooling support answer three different questions. Change one at a time.",
      controls: [
        range("energy", "Usable stored DC energy", 50, 1500, 10, 250, "kWh"),
        range("efficiency", "Discharge efficiency", 0.8, 1, 0.01, 0.9),
        range("load", "Protected load", 500, 8000, 100, 1000, "kW"),
        range("inverter", "Inverter output limit", 500, 10000, 100, 1200, "kW"),
        choice("support", "Cooling and control supply", [["unsupported", "Unsupported auxiliary path"], ["supported", "Electrical support supplied"]], "unsupported"),
      ],
      run(v) {
        const m = continuityModel(v.energy, v.efficiency, v.load, v.inverter, v.support === "supported");
        return {
          output: m.powerSufficient
            ? `${fmt(m.electricalMinutes, 2)} minutes (${fmt(m.electricalMinutes * 60, 2)} s) of ideal ${fmt(v.load)} kW electrical support. ${m.auxiliarySupported ? "Cooling and control have electrical support; thermal performance still needs evidence." : "Cooling and control support is missing, so continued service is unproven."}`
            : `The ${fmt(v.inverter)} kW inverter cannot carry the ${fmt(v.load)} kW load, whatever the stored energy.`,
          boundary: "Ideal constant-load duration after the power check passes. Battery ageing, discharge curves, transfer behavior and thermal dynamics are left out, so the result is neither thermal ride-through nor an uninterruptible power supply (UPS) rating.",
          graphic: flowRow("CHECK BOTH DEPENDENCIES", [
            m.powerSufficient ? "IT electrical path supported" : "IT power limit exceeded",
            m.auxiliarySupported ? "Auxiliary electrical path supplied" : "Auxiliary electrical path missing",
            "Useful service requires both",
          ]),
        };
      },
    };
  if (type === "outage")
    return {
      title: "Electrical ride-through is not service",
      intro: "Check the inverter's power, then the stored energy, then ask what happens to the cooling pumps. Change one thing at a time.",
      controls: [
        choice("plan", "Plan", [["existing", "As built"], ["energy", "Add 200 kWh of storage"], ["auxiliaries", "Put 0.2 MW of pumps on the battery system"]], "existing"),
        range("it", "IT load", 0.5, 4, 0.1, 2, "MW"),
        range("energy", "Usable DC energy", 100, 1500, 50, 600, "kWh"),
        range("inverter", "Inverter rating", 0.5, 4, 0.1, 2.5, "MW"),
        range("minutes", "Restoration sequence", 1, 30, 1, 12, "min"),
      ],
      run(v) {
        const m = coupledOutage({ plan: v.plan, itMW: v.it, auxiliaryMW: 0.2, dcKWh: v.energy, eta: 0.9, inverterMW: v.inverter, minutes: v.minutes });
        return {
          output: `The inverter ${m.powerPass ? "carries" : "cannot carry"} ${fmt(m.supportedMW)} MW · ${fmt(m.acKWh)} kWh AC gives ${fmt(m.idealMinutes)} ideal minutes · the ${fmt(v.minutes)}-minute restoration needs ${fmt(m.requiredKWh)} kWh (${m.energyPass ? `${fmt(m.reserveKWh)} kWh to spare` : `${fmt(-m.reserveKWh)} kWh short`}) · the pumps ${m.pumpSupplySurvives ? "stay powered" : "lose power"}, and thermal support is still unproven.`,
          boundary: "Constant load with 90% discharge efficiency and no load shedding. Thermal storage and temperature limits are not given, so no plan here proves useful service.",
          graphic: barChart(
            [
              ["Usable AC energy (kWh)", m.acKWh, COLOR.amber],
              ["Energy for the restoration (kWh)", m.requiredKWh, m.energyPass ? COLOR.green : COLOR.red],
            ],
            0,
            "Usable AC energy compared with the energy the restoration needs.",
          ),
        };
      },
    };
  if (type === "weathercap")
    return {
      title: "A hot day moves two limits",
      intro: "Usable capacity is the smallest of the electrical budget, the cooling limit and the accepted rack paths. Switch the weather and try each remedy.",
      controls: [
        choice("weather", "Weather", [["mild", "Mild: 15 MW auxiliaries, 70 MW cooling"], ["hot", "Hot: 25 MW auxiliaries, 55 MW cooling"]], "hot"),
        choice("remedy", "Remedy", [["none", "None"], ["auxiliaries", "Cut auxiliaries by 10 MW"], ["cooling", "Add 10 MW of cooling"]], "none"),
        range("racks", "Accepted rack paths", 100, 1000, 50, 900),
      ],
      run(v) {
        const m = weatherCapacity({ weather: v.weather, remedy: v.remedy, acceptedRacks: v.racks });
        const names = { electrical: "electrical budget", cooling: "cooling", paths: "accepted paths" };
        return {
          output: `${m.racks} rack equivalents (${fmt(m.capacityMW)} MW) · electrical ${fmt(m.electricalMW)} MW, cooling ${fmt(m.coolingMW)} MW, paths ${fmt(m.pathMW)} MW · binding: ${listed(m.binding.map((key) => names[key]))}.`,
          boundary: "A 100 MW site limit and 100 kW rack equivalents, with auxiliary demand fixed at each weather point.",
          graphic: barChart(
            [
              ["Electrical budget (MW)", m.electricalMW, COLOR.amber],
              ["Cooling limit (MW)", m.coolingMW, COLOR.green],
              ["Accepted paths (MW)", m.pathMW, COLOR.blue],
            ],
            100,
            "Electrical, cooling and accepted-path limits.",
          ),
        };
      },
    };
  if (type === "retrofit")
    return {
      title: "Does the denser rack fit the building?",
      intro: "Compare one 96% conversion stage (A) with a 97% sidecar feeding an 800 V segment and a 98% near-load stage (B). Check the feeder, the room's cooling and the service bay.",
      controls: [
        range("load", "Final DC load", 60, 160, 1, 120, "kW"),
        choice("architecture", "Candidate", [["a", "A: one conversion stage"], ["b", "B: sidecar and 800 V segment"]], "b"),
        choice("route", "Last service bay", [["blocked", "Taken by the sidecar"], ["clear", "Kept clear"]], "blocked"),
      ],
      run(v) {
        const m = densityRetrofit({ loadKW: v.load, architecture: v.architecture, route: v.route });
        return {
          output: `A needs ${fixed(m.aInputKW, 3)} kW AC; B needs ${fixed(m.bInputKW, 3)} kW (${fixed(m.extraKW, 3)} kW more) and carries ${fmt(m.amps, 2)} A on its 800 V segment · ${v.architecture.toUpperCase()} against the 160 kW feeder ${verdict(m.electricalPass)}, against 140 kW of room cooling ${verdict(m.thermalPass)}, and on service access ${verdict(m.accessPass)}.`,
          boundary: "Steady state with no other room load; the room cooling boundary contains both the rack and the sidecar, so room heat equals AC input.",
          graphic: barChart(
            [
              ["A input (kW)", m.aInputKW, COLOR.grey],
              ["B input (kW)", m.bInputKW, COLOR.amber],
              ["Room cooling limit (kW)", 140, COLOR.blue],
              ["Feeder limit (kW)", 160, COLOR.green],
            ],
            0,
            "AC input for each candidate against the cooling and feeder limits.",
          ),
        };
      },
    };
  if (type === "stalled")
    return {
      title: "Upgrade the link that is actually slow",
      intro: "Each cycle computes, sends a payload through the sender, fabric and receiver, then does fixed other work. Double one rate and see what happens to the whole cycle.",
      controls: [
        choice("upgrade", "Upgrade", [["none", "None"], ["endpoint", "E: double the sender rate"], ["fabric", "F: double the fabric bottleneck"]], "none"),
        range("payload", "Payload per cycle", 100, 2000, 50, 800, "GB"),
        range("compute", "Useful compute per cycle", 10, 200, 5, 60, "s"),
        range("fabric", "Fabric bottleneck rate", 10, 160, 5, 40, "GB/s"),
      ],
      run(v) {
        const m = stalledJob({ upgrade: v.upgrade, payloadGB: v.payload, computeSeconds: v.compute, fabricGBps: v.fabric });
        return {
          output: `${fmt(m.achievedGBps)} GB/s path rate (limited by the ${listed([...m.binding])}) · ${fmt(m.communicationSeconds)} s communication · ${fmt(m.cycleSeconds)} s cycle · ${fixed(m.throughputRatio, 3)}× baseline throughput · useful compute ${fmt(m.computeShare * 100)}% of the cycle.`,
          boundary: "Serial cycle with no overlap and fixed work per cycle; sender and receiver run at 80 GB/s and other work takes 10 s. Verify the changed end-to-end rate and correct output before claiming the gain.",
          graphic: barChart(
            [
              ["Compute (s)", v.compute, COLOR.green],
              ["Communication (s)", m.communicationSeconds, COLOR.amber],
              ["Other work (s)", 10, COLOR.grey],
            ],
            0,
            "Time in each phase of one cycle.",
          ),
        };
      },
    };
  if (type === "phase")
    return {
      title: "Open only what the evidence supports",
      intro: "Group A (300 racks) has passed acceptance. Group B (250) needs 4 days of network work and 2 of testing; group C (250) needs 3 days of delivery, 1 of installation and 3 of cooling tests. Move the day forward and choose what to open.",
      controls: [
        range("day", "Day", 0, 14, 1, 0),
        choice("ctest", "Group C cooling test", [["pass", "Passes"], ["fail", "Fails, then passes a retest"]], "pass"),
        choice("open", "Open", [["a", "Group A"], ["ab", "Groups A and B"], ["all", "All three groups"]], "a"),
      ],
      run(v) {
        const m = phaseAcceptance({ day: v.day, cTest: v.ctest, open: v.open });
        return {
          output: `Day ${fmt(v.day)}: ${m.acceptedRacks} accepted racks (${fmt(m.acceptedMW)} MW) of ${m.installedRacks} installed (${fmt(m.installedMW)} MW) · B ready on day ${m.bReadyDay}, C on day ${m.cReadyDay} · opening ${m.requestedRacks} racks is ${m.canOpen ? "supported" : "not yet supported"} by the evidence.`,
          boundary: "Each rack represents 100 kW. Groups proceed independently with the resources they need, and every projected date depends on its tests passing.",
          graphic: barChart(
            m.groups.map((g) => [`Group ${g.id} (racks)`, g.racks, g.accepted ? COLOR.green : COLOR.grey]),
            300,
            "Racks in each group, marked by acceptance.",
          ),
        };
      },
    };
  return null;
}
// ---- End of lab definitions

function controlMarkup(control) {
  const id = `lab-${control.id}`;
  if (control.kind === "choice")
    return `<div class="lab-control"><label for="${id}">${esc(control.label)}</label><select id="${id}">${control.options.map(([value, label]) => `<option value="${esc(value)}"${value === control.value ? " selected" : ""}>${esc(label)}</option>`).join("")}</select></div>`;
  return `<div class="lab-control"><label for="${id}">${esc(control.label)} <output id="${id}-value" for="${id}">${esc(valueLabel(control, control.value))}</output></label><input id="${id}" type="range" min="${control.min}" max="${control.max}" step="${control.step}" value="${control.value}"></div>`;
}
const ARCHITECTURES = {
  ac: ["Facility AC", "Rack AC/DC", "Low-voltage DC", "Point-of-load conversion"],
  hybrid: ["Existing facility AC", "Sidecar AC/DC", "800 V DC segment", "Near-load DC/DC"],
  facility: ["Upstream AC service", "Facility conversion", "800 V DC distribution", "Near-load DC/DC"],
};
const ARCHITECTURE_NOTES = {
  ac: "Power conversion sits at the rack. The diagram omits switching, protection and storage details.",
  hybrid: "Retained AC equipment still constrains the upstream path. The sidecar adds interfaces and service-space requirements.",
  facility: "This is a conceptual broader DC option. Its switching, fault clearing, grounding and storage interfaces need their own specified design.",
};
function renderLab(l) {
  const type = labType(l),
    lab = type && labDefinition(type);
  $("lab").hidden = !lab;
  if (!lab) {
    $("lab").replaceChildren();
    return;
  }
  const controls = labSettings(lab.controls, l.lab_params || {});
  const architecture = lab.architecture
    ? '<div class="segmented" aria-label="Illustrative power architecture"><button data-arch="ac" aria-pressed="false">AC to the rack</button><button data-arch="hybrid" aria-pressed="false">AC + DC sidecar</button><button data-arch="facility" aria-pressed="false">Broader facility DC</button></div><div id="architecture"></div>'
    : "";
  $("lab").innerHTML =
    `<div class="eyebrow">TEST A BOUNDED MODEL</div><h2 id="lab-title">${esc(lab.title)}</h2><p class="lab-intro">${esc(lab.intro)}</p>${architecture}<div class="lab-controls">${controls.map(controlMarkup).join("")}</div><div id="lab-graphic"></div><div id="lab-output" class="lab-output" role="status"></div><p id="lab-boundary" class="boundary"></p>`;
  const values = () =>
    Object.fromEntries(
      controls.map((control) => {
        const field = $(`lab-${control.id}`);
        return [
          control.id,
          control.kind === "choice"
            ? control.options.find(([value]) => String(value) === field.value)[0]
            : Number(field.value),
        ];
      }),
    );
  function update() {
    const v = values();
    for (const control of controls)
      if (control.kind === "range")
        $(`lab-${control.id}-value`).textContent = valueLabel(control, v[control.id]);
    try {
      const result = lab.run(v);
      $("lab-output").textContent = result.output;
      $("lab-boundary").textContent = result.boundary;
      $("lab-graphic").innerHTML = result.graphic;
    } catch (error) {
      $("lab-output").textContent = `These inputs fall outside the model: ${error.message}`;
      $("lab-graphic").replaceChildren();
    }
  }
  if (lab.architecture) {
    const show = (id, preset) => {
      $("architecture").innerHTML =
        flowRow("ILLUSTRATIVE CONVERSION PLACEMENT", ARCHITECTURES[id]) +
        `<p class="diagram-note">${ARCHITECTURE_NOTES[id]}</p>`;
      $("lab")
        .querySelectorAll("[data-arch]")
        .forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.arch === id)));
      // In the DC lab each placement also sets a representative bus voltage.
      if (preset && type === "dc") {
        $("lab-volts").value = id === "ac" ? 50 : 800;
        update();
      }
    };
    // lab_params.arch opens a lesson on one placement. Otherwise the DC lab
    // starts from its voltage, and the AC/DC lab from AC to the rack.
    const arch = (l.lab_params || {}).arch;
    show(Object.hasOwn(ARCHITECTURES, arch ?? "") ? arch
      : type === "dc" && Number($("lab-volts").value) < 400 ? "ac" : type === "dc" ? "facility" : "ac");
    $("lab")
      .querySelectorAll("[data-arch]")
      .forEach((b) => b.addEventListener("click", () => show(b.dataset.arch, true)));
  }
  $("lab")
    .querySelectorAll("input, select")
    .forEach((field) => field.addEventListener("input", update));
  update();
}

$("search").addEventListener("input", () => {
  // The sidebar search also filters the Glossary page.
  $("glossary-filter").value = $("search").value;
  renderContents();
});
$("glossary-filter").addEventListener("input", renderGlossary);
$("contents-toggle").addEventListener("click", () => {
  if ($("sidebar").classList.contains("open")) closeRail();
  else openRail();
});
$("lookup-toggle").addEventListener("click", () => {
  if (lookupMode === "glossary") {
    // Leave the glossary for the reading that was open before it.
    go(PRIMER_VIEW === location.hash.slice(1) ? PRIMER_VIEW : LESSONS[current].id);
    return;
  }
  modeLookup(true);
});
$("previous").addEventListener("click", () => go(LESSONS[Math.max(0, current - 1)].id));
$("next").addEventListener("click", () => go(LESSONS[(current + 1) % LESSONS.length].id));
$("primer-next").addEventListener("click", () => go(LESSONS[0].id));
function hashTarget() {
  try {
    return decodeURIComponent(location.hash.slice(1));
  } catch {
    return "";
  }
}
window.addEventListener("popstate", () =>
  go(hashTarget(), "none", new URLSearchParams(location.search).get("checkin") === "1"),
);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeRail();
});
go(hashTarget(), "replace", new URLSearchParams(location.search).get("checkin") === "1");
