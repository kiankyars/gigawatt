// Reader labs: each lab type is a thin interface over a tested model function.
// These tests run the lab definitions from course/web/reader.js with the models
// they import, and check that each lesson's lab reproduces its worked example.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const read = (path) => readFileSync(new URL(path, import.meta.url), "utf8");
const source = read("../course/web/reader.js");
const between = (start, end) => {
  const from = source.indexOf(start),
    to = source.indexOf(end, from);
  assert.ok(from >= 0 && to > from, `reader.js must contain ${start} … ${end}`);
  return source.slice(from, to);
};

// The models the reader imports, loaded from the same files.
const context = {};
for (const [, names, file] of source.matchAll(/^import \{([^}]+)\} from "\.\/prototypes\/([a-z-]+\.js)";$/gm)) {
  const module = await import(new URL(`../course/prototypes/${file}`, import.meta.url));
  for (const name of names.split(",").map((n) => n.trim())) {
    assert.equal(typeof module[name], "function", `${file} exports ${name}`);
    context[name] = module[name];
  }
}
// build_expanded.py inlines reader-models.js ahead of reader.js.
const models = await import(
  `data:text/javascript;base64,${Buffer.from(read("../course/web/reader-models.js")).toString("base64")}`
);
Object.assign(context, models);
const labs = vm.runInNewContext(
  `${between("const esc =", "const LESSONS =")}\n${between("// ---- Lab definitions", "// ---- End of lab definitions")}\n({ labDefinition, labType, valueLabel, DOMAIN_LABS });`,
  context,
);
const course = JSON.parse(read("../course/expanded-course.json"));
const lessons = new Map(course.lessons.map((lesson) => [lesson.id, lesson]));
const labTypes = [...new Set([...source.matchAll(/\btype === "([a-z][a-z0-9-]*)"/g)].map((m) => m[1]))];

function run(type, params = {}) {
  const lab = labs.labDefinition(type);
  assert.ok(lab, `lab type ${type} is defined`);
  const controls = models.labSettings(lab.controls, params);
  return lab.run(Object.fromEntries(controls.map((control) => [control.id, control.value])));
}

// Each lesson's lab, its starting values and what the lab must reproduce from
// the lesson. This is the contract the expansion JSON's "lab" and
// "lab_params" fields follow; "none" hides the lab. Variants move controls a
// reader can reach, and "sentence" quotes the lesson's own description of what
// the lab shows; the tests check that the lesson still contains it.
export const LESSON_LABS = {
  "d01-boundaries": {
    lab: "facility",
    lab_params: { racks: 10, rack: 142, network: 80, electrical: 40, cooling: 240, other: 20, hours: 4 },
    expect: [/IT 1,500 kW/, /= 1,800 kW facility input/, /7,200 kWh over 4 h/, /power ratio 1\.20/],
  },
  "d01-power-over-time": {
    lab: "energy",
    lab_params: { p1: 8, h1: 12, p2: 4, h2: 12, p3: 0, h3: 0 },
    expect: [/^144 MWh over 24 h/, /average 6 MW/, /peak 8 MW/],
    variants: [[{ p1: 6, h1: 24, p2: 0, h2: 0 }, [/^144 MWh over 24 h/, /peak 6 MW/]]],
  },
  "d01-metrics-and-evidence": {
    lab: "pue",
    lab_params: { it: 36, overhead: 7.2, jobs: 14.4 },
    expect: [/PUE 1\.2 /, /· 3 kWh of facility energy per accepted job/],
    variants: [
      [{ overhead: 3.6 }, [/PUE 1\.1 /, /2\.75 kWh/]],
      [{ it: 30 }, [/PUE 1\.24 /, /2\.583 kWh/]],
    ],
  },
  "d02-workload-brief": {
    lab: "kvcache",
    expect: [/320 KiB per token/, /= 2\.5 GiB per request/, /25 complete requests fit in 64 GiB/],
    variants: [[{ context: 32768 }, [/= 10 GiB per request/, /6 complete requests/]]],
  },
  "d02-productive-utilization": { lab: "samework", expect: [/Run A 16\.7 kWh/, /run B 20 kWh: 20% more energy/, /within 12\.5 min/] },
  "d02-phases-and-envelopes": {
    lab: "phases",
    expect: [/Peak 340 kW \(all in step: 480 kW\)/, /average 340 kW/, /5\.667 kWh per cycle/],
    variants: [[{ offset: 0 }, [/Peak 480 kW/, /minimum 160 kW/, /5\.667 kWh/]]],
  },
  "d03-power-and-procurement": {
    lab: "energy",
    lab_params: { p1: 20, h1: 12, p2: 0, h2: 12 },
    expect: [/^240 MWh over 24 h/, /average 10 MW/, /peak 20 MW/],
    sentence:
      "In the lab below, 20 MW for 12 hours followed by 0 MW for 12 hours gives the same 240 MWh and 10 MW average as the constant load, at twice its peak.",
  },
  "d03-voltage-and-distance": {
    lab: "feeder",
    lab_params: { power: 200, low: 34.5, high: 161, resistance: 0.01, pf: 1 },
    expect: [/34\.5 kV: 3,346\.96 A per phase, 336\.1 kW/, /161 kV: 717\.21 A, 15\.4 kW/, /difference 320\.6 kW/],
    variants: [[{ power: 10, low: 10, high: 20, resistance: 0.1 }, [/10 kV: 577\.35 A per phase, 100 kW/, /20 kV: 288\.68 A, 25 kW/, /difference 75 kW/]]],
  },
  "d03-service-and-siting": { lab: "none" },
  "d03-interconnection-queues": {
    lab: "staged",
    lab_params: { generators: 2 },
    expect: [/^1,000 MW of the 1,000 MW campus/, /at least 400 MW must come off/],
    variants: [[{ generators: 1 }, [/^600 MW/]], [{ generators: 0 }, [/^100 MW/]]],
  },
  "d12-room-and-replacement-route": {
    lab: "wheel",
    lab_params: { mass: 1580 },
    expect: [/^15\.500 kN total/, /3\.87 kN average per wheel against a 3\.0 kN limit: the route fails/],
    variants: [
      [{ mass: 2200 }, [/^21\.582 kN total/, /5\.40 kN average per wheel/]],
      [{ mass: 1000 }, [/2\.45 kN average per wheel against a 3\.0 kN limit: the average is within the limit; the actual load sharing decides/]],
    ],
  },
  "d12-hazards-and-site-evidence": { lab: "none" },
  "d12-safety-and-control-boundaries": { lab: "none" },
  "d04-read-the-power-train": {
    lab: "ledger",
    expect: [/Facility input 6\.42 MW against the 6 MW service: 0\.42 MW over/, /4\.8 MW branch: 0\.30 MW over/],
    variants: [[{ it: 4.6, auxiliary: 1, losses: 0.2 }, [/Facility input 5\.80 MW/]]],
  },
  "d04-current-and-rating": {
    lab: "kva",
    lab_params: { output: 900, efficiency: 1, pf: 0.8, rating: 1000 },
    expect: [/Input 900 kW \(0 kW converter heat\)/, /1,125 kVA/, /1,353 A per line at 480 V/, /112\.5% of the 1,000 kVA rating: fails/],
    variants: [
      [{ pf: 1 }, [/ 900 kVA/, /1,083 A per line/, /90% of the 1,000 kVA rating: passes/]],
      [{ efficiency: 0.96, pf: 0.9 }, [/Input 937\.5 kW \(37\.5 kW converter heat\)/, /1,041\.67 kVA/, /1,253 A per line at 480 V/, /104\.17% of the 1,000 kVA rating: fails/]],
    ],
  },
  "d04-conversion-placement": { lab: "conversion", expect: [/Path A input 1,062\.9 kW/, /path B input 1,036 kW/, /difference 26\.9 kW/] },
  "d05-storage-power-and-time": {
    lab: "continuity",
    lab_params: { energy: 800, efficiency: 0.95, load: 6000, inverter: 8000 },
    expect: [/^7\.6 minutes \(456 s\) of ideal 6,000 kW/],
    variants: [[{ inverter: 4000 }, [/4,000 kW inverter cannot carry the 6,000 kW load/]]],
  },
  "d05-paths-and-transitions": {
    lab: "continuity",
    lab_params: { energy: 120, efficiency: 1, load: 5500, inverter: 5500 },
    expect: [/\(78\.55 s\) of ideal 5,500 kW/],
  },
  "d05-protection-and-fault-domains": { lab: "none" },
  "d06-conversion-ledger": { lab: "dc", expect: [/^125 A at 800 V against 2,000 A at 50 V/, /0\.39% of the 50 V loss/] },
  "d06-rack-migration": {
    lab: "migration",
    expect: [/Input 253\.000 kW against 240 kW: 13\.000 kW short \(fails\)/],
    variants: [
      [{ rack: 110 }, [/Input 232\.167 kW/, /7\.833 kW spare \(passes\)/]],
      [{ allocation: 260 }, [/7\.000 kW spare/, /ready in 6 weeks against a 3-week deadline \(fails\)/]],
    ],
  },
  "d06-eight-hundred-volt-architectures": {
    lab: "acdc",
    lab_params: { kw: 100, volts: 800, pf: 1, resistance: 10 },
    expect: [/AC: 120\.3 A RMS per line, 434 W/, /DC: 125 A per conductor, 312\.5 W/, /DC heat is 72% of AC heat/],
    variants: [[{ pf: 0.9 }, [/AC: 133\.6 A RMS per line, 535\.8 W/, /DC heat is 58\.3% of AC heat/]]],
    sentence:
      "The lab below compares the two feeders at 100 kW with 10 mΩ per conductor: 480 V three-phase AC carries 120.3 A in each of three conductors and produces 434 W of conductor heat, while 800 V DC carries 125 A in each of two conductors and produces 312.5 W, 28% less.",
  },
  "d08-topology-budget": {
    lab: "fabric",
    expect: [/^24 cables and 32 switch ports/, /\(2:1\)/, /0\.32 s to move 32 GB/],
    variants: [[{ uplinks: 4 }, [/0\.16 s/]]],
  },
  "d08-collective-progress": {
    lab: "overlap",
    expect: [/Communication 30 ms, 10 ms exposed/, /step 230 ms without overlap, 210 ms with it/],
    variants: [[{ rate: 25 }, [/Communication 60 ms/, /240 ms with it/]]],
  },
  "d08-copper-light-service": { lab: "none" },
  "d10-local-thermal-paths": {
    lab: "junction",
    expect: [/^67 °C at the junction · 13 K below the 80 °C limit/],
    variants: [[{ resistance: 0.12 }, [/^83 °C/, /3 K above/]]],
  },
  "d10-flow-and-pressure": {
    lab: "pump",
    expect: [/^2\.00 L\/s \(120 L\/min\) at 120 kPa/, /240 W hydraulic, 400 W pump input/, /10 K coolant rise/],
    variants: [[{ resistance: 70 }, [/^1\.41 L\/s/, /at 140 kPa/, /14\.1 K coolant rise/]]],
  },
  "d10-cdu-interfaces": { lab: "none" },
  "d11-heat-rejection": { lab: "chiller", expect: [/Chiller COP 5 · plant COP 4 /, /rejects 12 MW/, /12\.5 MW reaches the environment/] },
  "d11-weather-and-operating-envelope": {
    lab: "weather",
    expect: [/Demand 10\.4 MW against 10 MW: exceeds/, /electrical 7\.68 MW, thermal 8\.5 MW, so at most 7\.68 MW/],
  },
  "d11-water-and-heat-reuse": { lab: "tower", expect: [/Blowdown 25 m³ · makeup 125 m³ · intake 1\.25 L\/kWh · consumption 1\.00 L\/kWh/] },
  "d13-delivery-dependencies": { lab: "schedule", expect: [/Electrical ready week 23 · cooling week 16 · utility week 16 · accepted at week 27, set by electrical/] },
  "d13-interface-contracts": {
    lab: "interfaces",
    expect: [/^240\.6 A against 160 A \(fails\)/, /4\.78 kg\/s/, /80 kPa against 60 kPa available \(fails\)/, /accepted at week 14/],
    variants: [[{ approval: 0 }, [/accepted at week 12/]], [{ rack: 100 }, [/^120\.3 A/, /2\.39 kg\/s/, /20 kPa/]]],
  },
  "d13-commissioning-complete-paths": {
    lab: "paths",
    lab_params: { rack: 200 },
    expect: [/^40 complete rack paths \(A21 to A60\) · 8 MW envelope at 200 kW per position/],
    variants: [
      [{ coolingfrom: 1 }, [/^60 complete rack paths \(A01 to A60\) · 12 MW envelope/]],
      [{ network: 100 }, [/^60 complete rack paths \(A21 to A80\) · 12 MW envelope/]],
    ],
  },
  "d14-telemetry-and-observability": {
    lab: "heatbalance",
    expect: [/^2,090 kW/],
    variants: [[{ return: 40 }, [/^4,180 kW/]], [{ flow: 50, return: 40 }, [/^2,090 kW/]]],
  },
  "d14-coordinating-control-and-work": {
    lab: "transition",
    lab_params: { delay: 3, buffer: 0 },
    expect: [/^1 MW imbalance for 3 min leaves 0\.0500 MWh of heat with no thermal buffer to absorb it/],
    variants: [
      [{ admit: "ready" }, [/^The work waits 3 min for standby cooling, so no thermal buffer is needed/]],
      [{ buffer: 0.04, delay: 2 }, [/uses 0\.0333 MWh of the 0\.04 MWh buffer: 0\.0067 MWh remains/]],
      [{ buffer: 0.04 }, [/0\.0500 MWh of the 0\.04 MWh buffer: 0\.0100 MWh short/]],
      [{ load: 5.5 }, [/0\.0250 MWh/]],
    ],
  },
  "d14-maintenance-and-service-reliability": { lab: "availability", expect: [/^26 unavailable minutes/, /availability 99\.9398%/] },
  "d15-capacity-ledger": { lab: "none" },
  "d15-cost-per-service": {
    lab: "rental",
    expect: [/^8,970,240 GPU-hours/, /committed \$22,425,600/, /pool \$17,940,480 at 50% occupancy/, /equal revenue at 62\.5% occupancy/],
  },
  "d15-upgrade-and-evidence": { lab: "none" },
  "c00-abilene-ai-factory": { lab: "none" },
  "c01-coupled-outage": {
    lab: "outage",
    lab_params: { plan: "existing", it: 2, energy: 600, inverter: 2.5, minutes: 12 },
    expect: [/carries 2 MW/, /540 kWh AC gives 16\.2 ideal minutes/, /needs 400 kWh \(140 kWh to spare\)/, /pumps lose power/],
    variants: [[{ plan: "auxiliaries" }, [/carries 2\.2 MW/, /pumps stay powered/]]],
  },
  "c02-weather-capacity": {
    lab: "weathercap",
    lab_params: { weather: "hot", remedy: "none", racks: 900 },
    expect: [/^550 rack equivalents \(55 MW\)/, /binding: cooling/],
    variants: [
      [{ weather: "mild" }, [/^700 rack equivalents/]],
      [{ remedy: "cooling" }, [/^650 rack equivalents/]],
      [{ remedy: "auxiliaries" }, [/^550 rack equivalents/]],
    ],
  },
  "c03-density-retrofit": {
    lab: "retrofit",
    lab_params: { load: 120, architecture: "b", route: "blocked" },
    expect: [/A needs 125\.000 kW AC; B needs 126\.236 kW \(1\.236 kW more\)/, /153\.06 A/, /service access fails/],
  },
  "c04-stalled-job": {
    lab: "stalled",
    lab_params: { upgrade: "none", payload: 800, compute: 60, fabric: 40 },
    expect: [/^40 GB\/s path rate \(limited by the fabric\)/, /20 s communication · 90 s cycle · 1\.000×/, /66\.7% of the cycle/],
    variants: [[{ upgrade: "fabric" }, [/80 s cycle · 1\.125×/]], [{ upgrade: "endpoint" }, [/90 s cycle · 1\.000×/]]],
  },
  "c05-open-a-phase": {
    lab: "phase",
    lab_params: { day: 0, ctest: "pass", open: "a" },
    expect: [/^Day 0: 300 accepted racks \(30 MW\) of 800 installed \(80 MW\)/, /B ready on day 6, C on day 7/],
    variants: [
      [{ day: 7, open: "all" }, [/800 accepted racks/, /opening 800 racks is supported/]],
      [{ ctest: "fail" }, [/C on day 12/]],
    ],
  },
  "d07-data-path": { lab: "bound", lab_params: { work: 0, traffic: 144 }, expect: [/memory 18 ms · bound 18 ms/] },
  "d07-bottleneck-model": {
    lab: "roofline",
    lab_params: { compute: 200, bandwidth: 8, intensity: 12.5 },
    expect: [/^100 TFLOP\/s upper bound · memory bandwidth binds · ridge at 25 FLOP\/byte/],
    variants: [[{ intensity: 10 }, [/^80 TFLOP\/s/]]],
    sentence:
      "In the lab below, the worked example’s operation, 2 × 10¹² FLOP over 160 GB, is 12.5 FLOP/byte, so its bandwidth ceiling is 8 × 10¹² × 12.5 = 100 TFLOP/s, which completes 2 × 10¹² FLOP in the same 20 ms as the HBM account.",
  },
  "d07-rack-as-system": {
    lab: "domains",
    expect: [/^28 healthy GPUs · 3 of 4 8-GPU job slots/],
    variants: [
      [{ g1: 1, g2: 1, g3: 1, g4: 1 }, [/0 of 4 8-GPU job slots/]],
      [{ g1: 1, g2: 1, g3: 1, g4: 1, job: 4 }, [/4 of 8 4-GPU job slots can run · 12 healthy GPUs left over/]],
    ],
  },
  "d09-storage-paths": { lab: "ckptwrite", expect: [/^4 s shard setup \+ 32 s payload at 16 GB\/s \(limited by source staging\) \+ 2 s commit = 38 s/] },
  "d09-checkpoint-timeline": {
    lab: "timeline",
    expect: [/^Finishes at minute 82: 13 useful minutes lost/],
    variants: [[{ interval: 40 }, [/^Finishes at minute 102: 35 useful minutes lost/]]],
  },
  "d09-service-acceptance": { lab: "placement", expect: [/^32 free GPUs · no group has 4 free nodes, so the job waits/] },
};

test("the lesson lab map names every lesson once and only known labs", () => {
  for (const [id, entry] of Object.entries(LESSON_LABS)) {
    assert.ok(lessons.has(id), `${id} is a course lesson`);
    assert.ok(entry.lab === "none" || labTypes.includes(entry.lab), `${id}: ${entry.lab} is a lab type`);
    if (entry.lab === "none") assert.equal(entry.lab_params, undefined, id);
    // The expansion JSON carries the same lab and starting values as this map.
    const lesson = lessons.get(id);
    assert.equal(lesson?.lab, entry.lab, `${id}: the lesson's lab`);
    if (entry.lab_params) assert.deepEqual(lesson.lab_params, entry.lab_params, `${id}: the lesson's lab_params`);
  }
  const unmapped = [...lessons.keys()].filter((id) => !(id in LESSON_LABS));
  assert.deepEqual(unmapped, [], "every lesson has a lab or none");
});

test("each lesson's lab reproduces its worked example", () => {
  for (const [id, entry] of Object.entries(LESSON_LABS)) {
    if (entry.lab === "none") continue;
    // Run the lesson's own starting values, as the reader does.
    const params = lessons.get(id)?.lab_params || {};
    const result = run(entry.lab, params);
    for (const pattern of entry.expect) assert.match(result.output, pattern, `${id}: ${result.output}`);
    if (entry.sentence)
      assert.ok(
        lessons.get(id).sections.some((s) => s.paragraphs.some((p) => p.includes(entry.sentence))),
        `${id}: lab sentence is in the lesson`,
      );
    // The reader widens a slider only for the lesson's own lab_params, so every
    // variant value must already be reachable on the controls it renders.
    const controls = new Map(
      models.labSettings(labs.labDefinition(entry.lab).controls, params).map((c) => [c.id, c]),
    );
    for (const [change, patterns] of entry.variants || []) {
      for (const [key, value] of Object.entries(change)) {
        const c = controls.get(key);
        assert.ok(c, `${id}: variant control ${key} exists`);
        if (c.kind === "choice") {
          assert.ok(c.options.some(([option]) => option === value), `${id} ${key}=${value} is an option`);
          continue;
        }
        const steps = (value - c.min) / c.step;
        assert.ok(
          c.min <= value && value <= c.max && Math.abs(steps - Math.round(steps)) < 1e-9,
          `${id} ${key}=${value} (slider [${c.min}, ${c.max}] step ${c.step})`,
        );
      }
      const varied = run(entry.lab, { ...params, ...change });
      for (const pattern of patterns) assert.match(varied.output, pattern, `${id} ${JSON.stringify(change)}: ${varied.output}`);
    }
  }
});

test("every lab type renders its defaults and names safe controls", () => {
  assert.ok(labTypes.length >= 40, `found ${labTypes.length} lab types`);
  for (const type of labTypes) {
    const lab = labs.labDefinition(type);
    assert.ok(lab && lab.title && lab.intro, type);
    const ids = lab.controls.map((control) => control.id);
    assert.equal(new Set(ids).size, ids.length, `${type}: unique control ids`);
    for (const control of lab.controls) {
      assert.match(control.id, /^[a-z][a-z0-9-]*$/, `${type}.${control.id}`);
      if (control.kind === "choice") assert.ok(control.options.some(([value]) => value === control.value), `${type}.${control.id}`);
      else assert.ok(control.min <= control.value && control.value <= control.max, `${type}.${control.id} default in range`);
    }
    const result = run(type);
    for (const text of [result.output, result.boundary, result.graphic])
      assert.doesNotMatch(String(text), /NaN|undefined|Infinity/, `${type}: ${text}`);
    assert.doesNotMatch(`${lab.title} ${lab.intro} ${result.boundary}`, /—/, `${type}: no em-dashes in lab prose`);
  }
  for (const [domain, type] of Object.entries(labs.DOMAIN_LABS)) assert.ok(labTypes.includes(type), `${domain} fallback ${type}`);
});

test("lessons choose a lab per lesson and fall back to the domain lab", () => {
  assert.equal(labs.labType({ domain: "D15", lab: "rental" }), "rental");
  assert.equal(labs.labType({ domain: "D15", lab: "none" }), null);
  assert.equal(labs.labType({ domain: "D15" }), "capacity");
  assert.equal(labs.labType({ domain: "D12", visual: { kind: "parcel" } }), null);
  assert.equal(labs.labType({ domain: "unknown" }), null);
});

test("lab and lab_params in the course data match the reader's labs", () => {
  for (const lesson of course.lessons) {
    if (!("lab" in lesson)) continue;
    assert.ok(lesson.lab === "none" || labTypes.includes(lesson.lab), `${lesson.id}: ${lesson.lab}`);
    if (!lesson.lab_params) continue;
    const lab = labs.labDefinition(lesson.lab);
    const controls = new Map(lab.controls.map((control) => [control.id, control]));
    for (const [key, value] of Object.entries(lesson.lab_params)) {
      // Power-architecture labs also accept a starting placement.
      if (key === "arch" && lab.architecture) {
        assert.ok(["ac", "hybrid", "facility"].includes(value), `${lesson.id}: arch=${value}`);
        continue;
      }
      const control = controls.get(key);
      assert.ok(control, `${lesson.id}: lab_params.${key} names a ${lesson.lab} control`);
      if (control.kind === "choice") assert.ok(control.options.some(([option]) => option === value), `${lesson.id}: ${key}=${value}`);
      else assert.ok(Number.isFinite(value), `${lesson.id}: ${key} is a number`);
    }
  }
});

test("slider labels keep the step's decimals", () => {
  const pf = { kind: "range", step: 0.01, unit: "" },
    volts = { kind: "range", step: 1, unit: "V" },
    rate = { kind: "range", step: 0.05, unit: "$/GPU-hour" };
  assert.equal(labs.valueLabel(pf, 0.95), "0.95");
  assert.equal(labs.valueLabel(pf, 1), "1.00");
  assert.equal(labs.valueLabel(volts, 800), "800 V");
  assert.equal(labs.valueLabel(rate, 2.5), "2.50 $/GPU-hour");
  assert.equal(labs.valueLabel({ kind: "choice", options: [["hot", "Hot"]] }, "hot"), "Hot");
});
