// Original teaching comparisons. Uptime's public explanations were reviewed
// through their indexed text on 2026-09-12; direct page requests returned 403.
// These diagrams explain selected outcomes, not a certification checklist.
export const reliabilitySources = Object.freeze({
  tiers: "https://uptimeinstitute.com/tiers",
  availability: "https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/",
  generators: "https://uptimeinstitute.com/myths",
  case: "https://journal.uptimeinstitute.com/modular-and-phased-construction/",
});

export const reliabilityScenes = Object.freeze([
  {
    id: "tier-topology", label: "Tier outcomes", reliability: true,
    title: "Tier III supports maintenance; Tier IV also tolerates a single infrastructure fault.",
    notes: [
      "Uptime Institute's tiers describe site infrastructure outcomes across power and cooling. Tier I establishes basic capacity; Tier II adds redundant capacity components; Tier III adds concurrent maintainability; Tier IV adds fault tolerance and continuous cooling.",
      "Change the event. 'Not required' does not predict an outage: that outcome is not established by that tier alone. N+1, N+2 and 2N component counts do not determine a tier.",
      "These are selected outcomes, not a certification checklist. Tier IV does not promise survival of every combination of maintenance and additional failures.",
    ],
    cue: "Compare planned path maintenance with an unplanned distribution fault.",
  },
  {
    id: "tier-generation", label: "Tier generation", reliability: true,
    title: "Backup generation is already part of Tier I, not an upgrade reserved for Tier IV.",
    notes: [
      "Uptime's Tier I definition includes an engine generator for power outages; higher tiers inherit this baseline. A second utility feed does not replace the tier's generation requirement.",
      "For Tier III and IV, the generator plant must support the critical load without runtime limits in its capacity rating. This is capability, not an instruction to run generators all day.",
      "Fuel, refueling, maintenance, cooling and operating permissions still matter. An unlimited-runtime equipment rating does not create an infinite fuel supply.",
      "Standby generation that bridges utility outages and a continuously operated on-site power plant are different operating strategies. The latter is not required simply by selecting Tier IV.",
    ],
    cue: "Identify what all tiers need, then distinguish generator capability from its normal operating schedule.",
  },
  {
    id: "availability-budget", label: "Availability budget", reliability: true,
    title: "One 45-minute outage nearly spends a four-nines annual downtime budget.",
    notes: [
      "This example counts every minute at one declared service boundary over exactly 365 days. Three nines allows 525.6 minutes, four nines 52.56, and five nines 5.256.",
      "At four nines, a 45-minute outage uses 85.6% of the annual allowance. At five nines, this one outage already exceeds the allowance. The same event changes the engineering consequence when the target changes.",
      "Availability is a measured result or a defined target, not a tier label. Uptime removed expected-downtime assignments in 2009. An actual SLA may use a monthly window, a request-based measure or exclusions; read its definition before applying this calculation.",
    ],
    cue: "Keep the outage fixed and change the target. Ask how much allowance remains.",
  },
  {
    id: "tier-investment", label: "Resilience decision", reliability: true,
    title: "This cloud operator planned to fund Tier IV cooling when a customer needed it.",
    notes: [
      "Uptime's 2015 case describes a U.S. cloud facility with Tier III constructed-facility certification and a planned Tier IV phase. The owner deferred the mechanical UPS, meaning UPS support for cooling equipment, until a client's requirement justified continuous-cooling investment.",
      "Other Tier IV capabilities had already been designed and demonstrated. The case is not a recipe saying that adding cooling storage upgrades any Tier III facility to Tier IV.",
      "This is a commercial cloud example, not a government-only category. Choose resilience around service consequences, maintenance needs and the business case; do not infer a universal customer mix or market share.",
      "The diagram represents the published decision and proposed second phase. It does not claim that the later upgrade was completed.",
    ],
    cue: "Change the customer's requirement and identify which additional capability would justify the spending.",
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

export function reliabilityTitle(scene, state) {
  if (scene.id !== "availability-budget") return scene.title;
  return {
    3: "A 45-minute outage uses 8.6% of a three-nines annual allowance.",
    4: "A 45-minute outage uses 86% of a four-nines annual allowance.",
    5: "A 45-minute outage exceeds a five-nines annual allowance more than eightfold.",
  }[state.nines];
}

const link = (url, label) => `<a href="${url}" target="_blank" rel="noopener">${label} ↗</a>`;
const button = (key, value, label, state) => `<button data-reliability-key="${key}" data-reliability-value="${value}" aria-pressed="${String(state[key]) === String(value)}">${label}</button>`;
export function reliabilityControls(id, state) {
  if (id === "tier-topology") return button("tierEvent", "maintenance", "Maintain a distribution path", state) + button("tierEvent", "fault", "Fail one distribution element", state);
  if (id === "availability-budget") return [3,4,5].map(n => button("nines", n, `${"9".repeat(2)}.${"9".repeat(n-2)}%`, state)).join("");
  if (id === "tier-investment") return button("tierUpgrade", false, "Before Tier IV demand", state) + button("tierUpgrade", true, "Customer requires Tier IV", state);
  return "";
}

function hierarchy(state) {
  const maintenance = state.tierEvent !== "fault";
  const tiers = [
    ["I", "Basic capacity", "Dedicated power and cooling"],
    ["II", "Redundant capacity", "Spare capacity components"],
    ["III", "Concurrent maintenance", "Maintain the infrastructure with IT operating"],
    ["IV", "Fault tolerance", "A single infrastructure failure leaves IT operating"],
  ];
  return `<div class="tier-hierarchy" aria-label="Uptime Institute Tier I through IV comparison">${tiers.map(([tier, name, meaning], i) => {
    const meets = i >= (maintenance ? 2 : 3);
    return `<div class="tier-row" data-meets-event="${meets}"><strong class="tier-number">${tier}</strong><div><strong>${name}</strong><span>${meaning}</span></div><span class="tier-verdict">${meets ? "Required outcome" : "Not established"}</span></div>`;
  }).join("")}</div><p class="reliability-scope">Selected power + cooling outcomes · spare-module counts alone do not establish Tier</p>`;
}

function generation() {
  return `<div class="generation-requirements"><div class="generation-base"><div class="tier-range">I · II · III · IV</div><svg viewBox="0 0 520 200" role="img" aria-label="An on-site engine generator supplies the site's supported power and cooling during a utility outage"><rect x="22" y="28" width="210" height="140" rx="16" fill="var(--diagram-face, #e7eddf)" stroke="var(--green)" stroke-width="2"/><circle cx="81" cy="99" r="29" fill="none" stroke="var(--green)" stroke-width="3"/><text x="81" y="108" text-anchor="middle" fill="var(--ink)" font-size="26">G</text><text x="164" y="91" text-anchor="middle" fill="var(--ink)" font-size="19">On-site</text><text x="164" y="118" text-anchor="middle" fill="var(--ink)" font-size="19">generator</text><path d="M232 99H277M277 55V145M277 55H309M277 145H309" fill="none" stroke="var(--green)" stroke-width="4"/><rect x="309" y="22" width="185" height="65" rx="10" fill="var(--diagram-face, #e7eddf)"/><rect x="309" y="112" width="185" height="65" rx="10" fill="var(--diagram-face, #e7eddf)"/><text x="401" y="62" text-anchor="middle" fill="var(--ink)" font-size="19">IT power path</text><text x="401" y="152" text-anchor="middle" fill="var(--ink)" font-size="19">Cooling support</text></svg><strong>Source for utility outages</strong></div><div class="generation-rating"><div class="tier-range">III · IV</div><strong>Critical-load capability<br>without runtime limits</strong><span>At the equipment's applicable capacity rating</span><div class="capability-not-schedule"><span>CAPABILITY</span><b>≠</b><span>RUNNING 24/7</span></div></div></div><p class="reliability-scope">Functional scope, not a one-line design · fuel and refueling still bound operation</p>`;
}

function availability(state) {
  const m = availabilityBudget(Number(state.nines));
  const remaining = Math.abs(m.remainingMinutes).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
  return `<div class="availability-example" data-within-budget="${m.withinBudget}" data-allowed-minutes="${m.allowedMinutes}" data-remaining-minutes="${m.remainingMinutes}"><div class="availability-account"><div><span>Annual allowance</span><strong>${m.allowedMinutes.toFixed(3).replace(/0+$/, "").replace(/\.$/, "")} <small>min</small></strong></div><div><span>One outage</span><strong>45 <small>min</small></strong></div><div class="availability-result"><span>${m.withinBudget ? "Allowance remaining" : "Over the allowance"}</span><strong>${remaining} <small>min</small></strong></div></div><div class="budget-ruler"><span style="width:${Math.min(100,m.usedPercent)}%"></span></div><div class="budget-percent">${m.usedPercent.toFixed(1)}% of the annual allowance used</div><p class="availability-equation">Downtime allowance = (1 − availability) × 365 × 24 × 60 min</p></div><p class="reliability-scope">All minutes counted at one service boundary · a 365-day example, not an SLA or a Tier prediction</p>`;
}

function investment(state) {
  const upgrade = Boolean(state.tierUpgrade);
  return `<div class="tier-investment" data-upgrade="${upgrade}"><div class="investment-panel"><span>BUILT PHASE</span><strong>Tier III</strong><p>Concurrent maintenance</p><small>Constructed facility certified</small></div><div class="investment-arrow" aria-hidden="true">→</div><div class="investment-panel upgrade-panel"><span>${upgrade ? "CUSTOMER REQUIREMENT" : "UPGRADE HELD"}</span><strong>Continuous cooling</strong><p>UPS-backed cooling equipment</p><small>${upgrade ? "Proposed Tier IV phase justified" : "Wait for a client who needs Tier IV"}</small></div></div><p class="reliability-scope">Uptime's 2015 U.S. cloud case · other Tier IV capabilities already in place · later completion not claimed</p>`;
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
    "availability-budget": link(reliabilitySources.availability, "Why Tiers have no downtime prediction"),
    "tier-investment": link(reliabilitySources.case, "Published cloud-facility case"),
  }[id];
  return `<div class="reliability-main">${content()}</div><div class="reliability-actions">${reliabilityControls(id,state)}</div><div class="reliability-source">${source}</div>`;
}
