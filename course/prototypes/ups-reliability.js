// Original teaching comparisons. Uptime's public explanations were reviewed
// through their indexed text on 2026-09-12; direct page requests returned 403.
// These diagrams explain selected outcomes, not a certification checklist.
export const reliabilitySources = Object.freeze({
  tiers: "https://uptimeinstitute.com/tiers",
  availability: "https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/",
  generators: "https://uptimeinstitute.com/myths",
  case: "https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/",
});

export const reliabilityScenes = Object.freeze([
  {
    id: "tier-topology", label: "Tier outcomes", reliability: true,
    title: "Tier III permits maintenance; Tier IV also withstands a single fault.",
    notes: [
      "Uptime Institute's tiers describe site infrastructure outcomes across power and cooling. Tier I establishes basic capacity; Tier II adds redundant capacity components; Tier III adds concurrent maintainability; Tier IV adds fault tolerance and continuous cooling.",
      "The two illustrations show required operating outcomes. Tier III and IV allow planned maintenance with IT online; Tier IV additionally contains an individual equipment or distribution-path failure. Lower tiers may survive particular events, but the higher tier requires the wider capability across the infrastructure.",
      "These are selected outcomes, not a certification checklist. Tier IV does not promise survival of every combination of maintenance and additional failures.",
    ],
    cue: "Point to what each tier adds, then compare planned maintenance with a sudden failure.",
  },
  {
    id: "tier-generation", label: "Tier generation", reliability: true,
    title: "All four Uptime Tiers include a generator for utility outages.",
    notes: [
      "Uptime's Tier I definition includes an engine generator for power outages; higher tiers inherit this baseline. A second utility feed does not replace the tier's generation requirement.",
      "For Tier III and IV, the generator plant must support the critical load without runtime limits in its capacity rating. This is capability, not an instruction to run generators all day.",
      "Fuel, refueling, maintenance, cooling and operating permissions still matter. An unlimited-runtime equipment rating does not create an infinite fuel supply.",
      "Standby generation that bridges utility outages and a continuously operated on-site power plant are different operating strategies. The latter is not required simply by selecting Tier IV.",
    ],
    cue: "Identify what all tiers need, then distinguish generator capability from its normal operating schedule.",
  },
  {
    id: "availability-budget", label: "Nines in practice", reliability: true,
    title: "Compare three, four and five nines using real data centers.",
    notes: [
      "Sparks: Crusoe reports 99.9% Cloud availability using grid backup. Its separate 99.2% microgrid result covers seven months; the Cloud claim does not supply a separate measurement window.",
      "Fairwater Atlanta: Microsoft describes four-nines design capability. Vienna 1: NTT DATA advertises a five-nines power uptime SLA. Neither is an observed annual application-availability result.",
      "The lower row converts each percentage to downtime in a hypothetical all-minutes-counted 365-day year. These durations do not specify the actual terms or observed downtime of the facilities above.",
      "Uptime's Tiers describe infrastructure capabilities, not fixed availability percentages. Match the measurement boundary and period before comparing published nines.",
    ],
    cue: "Name the facility, identify what its number measures, then compare the annual mathematical equivalents.",
  },
  {
    id: "tier-investment", label: "Fairwater Atlanta", reliability: true,
    title: "Fairwater Atlanta relies on utility resilience to simplify GPU power delivery.",
    notes: [
      "Microsoft's November 2025 Fairwater article names Atlanta and describes selecting its site for resilient utility power. Microsoft claims capability for four-nines availability at three-nines cost; it does not publish a measured availability series or establish an Uptime Tier certification in this article.",
      "The company says this utility resilience permits omitting on-site generation, UPS systems and dual-corded distribution for the GPU fleet. The scope matters: it does not establish the backup arrangement for every other load on the campus.",
      "The design trades the cost and construction time of local backup hardware against reliance on the selected utility supply. That makes the site's utility reliability part of the design decision, rather than assuming every AI campus must maximize its Tier.",
      "The article also describes on-site energy storage for smoothing power oscillations. Power smoothing and generator-outage backup are different functions; omitting traditional GPU UPSs does not mean the campus contains no storage.",
    ],
    cue: "Identify which hardware Microsoft can omit because of the chosen site's utility resilience.",
  },
]);

export function availabilityBudget(nines, outageMinutes = 45, days = 365) {
  if (![3, 4, 5].includes(nines)) throw new RangeError("Choose three, four or five nines");
  if (!Number.isFinite(outageMinutes) || outageMinutes < 0 || !Number.isFinite(days) || days <= 0)
    throw new RangeError("Time inputs must be finite and nonnegative; days must be positive");
  const windowMinutes = days * 24 * 60;
  const allowedMinutes = windowMinutes * 10 ** -nines;
  return Object.freeze({
    nines, days, outageMinutes, windowMinutes, allowedMinutes,
    remainingMinutes: allowedMinutes - outageMinutes,
    usedPercent: outageMinutes / allowedMinutes * 100,
    withinBudget: outageMinutes <= allowedMinutes,
  });
}

export function reliabilityTitle(scene) {
  return scene.title;
}

const link = (url, label) => `<a href="${url}" target="_blank" rel="noopener">${label} ↗</a>`;
export function reliabilityControls() {
  return "";
}

export const availabilityExamples = Object.freeze([
  { nines: 3, name: "Crusoe Spark", place: "Sparks, Nevada", boundary: "Cloud service", kind: "Operator report", source: "https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density" },
  { nines: 4, name: "Microsoft Fairwater", place: "Atlanta, Georgia", boundary: "Site availability", kind: "Design claim", source: reliabilitySources.case },
  { nines: 5, name: "NTT DATA Vienna 1", place: "Vienna, Austria", boundary: "Power uptime", kind: "Advertised SLA", source: "https://services.global.ntt/-/media/ntt/global/insights-and-resources/data-sheets/vienna-1-data-sheet.pdf?rev=9057842951194cb1b9d1cf884282f421#page=2" },
].map(Object.freeze));

function pathOutcome(kind) {
  const fault = kind === "fault";
  return `<div class="tier-outcome" data-tier-outcome="${kind}"><div class="tier-outcome-heading"><strong>${fault ? "One sudden failure" : "Planned maintenance"}</strong><span>${fault ? "Tier IV" : "Tier III + IV"}</span></div><svg viewBox="0 0 460 170" role="img" aria-label="${fault ? "A single fault is isolated" : "One path is isolated for planned maintenance"}; the remaining path keeps IT operating. This illustrates an outcome, not a complete Tier topology."><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M30 65H149M204 65H331" stroke="var(--muted)" stroke-width="3" stroke-dasharray="6 7"/><path d="M30 125H278V95H330" stroke="var(--green)" stroke-width="5"/>${fault ? '<path d="M180 40L165 66H183L170 90" stroke="var(--gold)" stroke-width="4"/>' : '<path d="M150 65L196 40" stroke="var(--gold)" stroke-width="4"/>'}<path d="M319 86L332 95L319 104" stroke="var(--green)" stroke-width="4"/></g><g fill="var(--muted)" font-size="15"><text x="30" y="43">Path A</text><text x="30" y="151">Path B</text></g><rect x="337" y="47" width="104" height="81" rx="10" fill="var(--note-surface, #e8f0e5)" stroke="var(--green)" stroke-width="2"/><g fill="var(--green)" text-anchor="middle"><text x="389" y="80" font-size="22" font-weight="600">IT</text><text x="389" y="106" font-size="17">online</text></g></svg></div>`;
}

function hierarchy() {
  const tiers = [
    ["I", "Power + cooling"],
    ["II", "+ Spare equipment"],
    ["III", "+ Maintenance with IT online"],
    ["IV", "+ Single-fault tolerance"],
  ];
  return `<div class="tier-hierarchy" aria-label="Each Uptime Tier includes the preceding tiers; Tier IV is the highest infrastructure-resilience level.">${tiers.map(([tier, capability]) => `<div class="tier-step" data-tier="${tier}"><strong class="tier-number">${tier}</strong><span>${capability}</span></div>`).join("")}</div><div class="tier-outcomes">${pathOutcome("maintenance")}${pathOutcome("fault")}</div>`;
}

function generation() {
  return `<div class="generation-requirements"><div class="generation-base"><div class="tier-range">Tier I · II · III · IV</div><svg viewBox="0 0 700 230" role="img" aria-label="All four tiers include on-site generation for utility outages. A generator supports the IT power path and cooling; the diagram omits switching and distribution equipment."><rect x="35" y="44" width="260" height="142" rx="16" fill="var(--diagram-face, #e7eddf)" stroke="var(--green)" stroke-width="2"/><circle cx="100" cy="115" r="33" fill="none" stroke="var(--green)" stroke-width="3"/><text x="100" y="125" text-anchor="middle" fill="var(--ink)" font-size="29">G</text><text x="205" y="107" text-anchor="middle" fill="var(--ink)" font-size="22">On-site</text><text x="205" y="137" text-anchor="middle" fill="var(--ink)" font-size="22">generator</text><path d="M295 115H361M361 66V164M361 66H430M361 164H430" fill="none" stroke="var(--green)" stroke-width="4"/><path d="M418 57L431 66L418 75M418 155L431 164L418 173" fill="none" stroke="var(--green)" stroke-width="4"/><rect x="441" y="31" width="220" height="70" rx="10" fill="var(--diagram-face, #e7eddf)"/><rect x="441" y="129" width="220" height="70" rx="10" fill="var(--diagram-face, #e7eddf)"/><text x="551" y="74" text-anchor="middle" fill="var(--ink)" font-size="22">IT power path</text><text x="551" y="172" text-anchor="middle" fill="var(--ink)" font-size="22">Cooling</text></svg></div><div class="generation-progression"><span>Higher Tiers add protection</span><strong>Spare equipment <span>→</span> Maintenance <span>→</span> Fault tolerance</strong></div></div>`;
}

function availability() {
  const yearTimes = ["8 h 46 min", "52.6 min", "5.26 min"];
  return `<div class="availability-cases">${availabilityExamples.map(example => `<article class="availability-case" data-nines="${example.nines}"><strong class="availability-nines">99.${"9".repeat(example.nines - 2)}<small>%</small></strong><h2>${example.name}</h2><p>${example.place}</p><div class="availability-claim"><strong>${example.boundary}</strong><span>${example.kind}</span></div></article>`).join("")}</div><div class="availability-year"><p>Downtime equivalent in a full 365-day year</p><div>${availabilityExamples.map((example, i) => `<strong data-allowed-minutes="${availabilityBudget(example.nines, 0).allowedMinutes}">${yearTimes[i]}</strong>`).join("")}</div><small>Mathematical reference; actual reporting and contract terms differ.</small></div>`;
}

function investment() {
  return `<div class="tier-investment" data-evidence="design-claim"><figure class="investment-photo"><img src="../assets/references/microsoft-fairwater-atlanta.jpg" alt="Microsoft's aerial photograph of its Fairwater AI data center near Atlanta, Georgia." decoding="async"/><figcaption>Fairwater, Atlanta · Microsoft</figcaption></figure><div class="investment-panel"><span>MICROSOFT'S DESIGN CLAIM</span><strong>99.99% availability</strong><p class="investment-cost">at “three-nines” cost</p><div class="investment-omissions"><span>GPU fleet omits</span><strong>On-site generators<br>UPS systems<br>Dual-corded distribution</strong></div></div></div><p class="reliability-scope">Availability claim ≠ Tier certification</p>`;
}

export function renderReliability(id, state) {
  const content = {
    "tier-topology": () => hierarchy(state),
    "tier-generation": generation,
    "availability-budget": () => availability(state),
    "tier-investment": () => investment(state),
  }[id];
  if (!content) throw new RangeError("Unknown reliability scene");
  const source = {
    "tier-topology": link(reliabilitySources.tiers, "Uptime: Tier outcomes") + " · " + link(reliabilitySources.generators, "Counts and Tiers"),
    "tier-generation": link(reliabilitySources.tiers, "Tier I requirement") + " · " + link(reliabilitySources.generators, "Generator capability"),
    "availability-budget": availabilityExamples.map(example => link(example.source, example.name)).join(" · "),
    "tier-investment": link(reliabilitySources.case, "Microsoft: Fairwater Atlanta · November 2025"),
  }[id];
  return `<div class="reliability-main">${content()}</div><div class="reliability-actions">${reliabilityControls(id,state)}</div><div class="reliability-source">${source}</div>`;
}
