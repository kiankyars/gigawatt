import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const source = readFileSync(
  new URL("../course/web/reader-models.js", import.meta.url),
  "utf8",
);
const { acdcWaveModel } = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);
const close = (actual, expected, tolerance = 1e-9) =>
  assert.ok(Math.abs(actual - expected) < tolerance, `${actual} != ${expected}`);
const cycle = (kind, ...args) =>
  Array.from({ length: 360 }, (_, angle) => acdcWaveModel(kind, angle, ...args));
const mean = (values) => values.reduce((sum, value) => sum + value, 0) / values.length;
const rms = (values) => Math.sqrt(mean(values.map((value) => value ** 2)));

test("800 V DC supplies 100 kW continuously at 125 A", () => {
  for (const state of cycle("dc-basics")) {
    assert.equal(state.phases.length, 1);
    close(state.phases[0].voltageV, 800);
    close(state.phases[0].currentA, 125);
    close(state.phases[0].powerKW, 100);
    close(state.instantKW, 100);
    close(state.averageKW, 100);
    close(state.lineABVoltageV, 800);
    close(state.phases[0].peakA, 125);
  }
});

test("single-phase RMS and cycle-average power preserve the same 100 kW load", () => {
  const states = cycle("ac-basics");
  const phase = states[0].phases[0];
  close(phase.rmsVoltageV, 480);
  close(phase.rmsCurrentA, 208.33333333333334);
  close(rms(states.map((state) => state.phases[0].voltageV)), 480);
  close(rms(states.map((state) => state.phases[0].currentA)), 208.33333333333334);
  close(mean(states.map((state) => state.instantKW)), 100);
  close(states[0].instantKW, 0);
  close(states[90].instantKW, 200);
  close(states[180].instantKW, 0);
  close(states[270].instantKW, 200);
});

test("reversing voltage and current together still delivers positive resistor power", () => {
  for (const kind of ["ac-basics", "three-phase"]) {
    const before = acdcWaveModel(kind, 37);
    const after = acdcWaveModel(kind, 217);
    before.phases.forEach((phase, i) => {
      close(phase.voltageV, -after.phases[i].voltageV);
      close(phase.currentA, -after.phases[i].currentA);
      close(phase.powerKW, after.phases[i].powerKW);
      assert.ok(phase.powerKW >= 0);
      assert.ok(after.phases[i].powerKW >= 0);
    });
  }
});

test("balanced 480 V three-phase power stays at 100 kW while currents cancel", () => {
  const states = cycle("three-phase");
  for (const state of states) {
    assert.deepEqual(state.phases.map((phase) => phase.label), ["A", "B", "C"]);
    close(state.instantKW, 100);
    close(state.currentSumA, 0);
    close(state.phaseVoltageRMSV, 277.1281292110204);
    for (const phase of state.phases) {
      close(phase.rmsCurrentA, 120.28130608117204);
      assert.ok(phase.powerKW >= 0);
    }
  }
  for (const index of [0, 1, 2]) {
    close(mean(states.map((state) => state.phases[index].powerKW)), 100 / 3);
    close(rms(states.map((state) => state.phases[index].voltageV)), 277.1281292110204);
    close(rms(states.map((state) => state.phases[index].currentA)), 120.28130608117204);
  }
});

test("line-to-line voltage is the phase-voltage difference, with 480 V RMS", () => {
  const states = cycle("voltage-basis");
  for (const state of states) {
    close(state.lineABVoltageV, state.phases[0].voltageV - state.phases[1].voltageV);
    // For vA = Vpk sin(theta) and vB = Vpk sin(theta - 120 degrees),
    // vAB leads vA by 30 degrees and has sqrt(3) times its amplitude.
    close(
      state.lineABVoltageV,
      480 * Math.SQRT2 * Math.sin(((state.angleDegrees + 30) * Math.PI) / 180),
    );
    const threePhase = acdcWaveModel("three-phase", state.angleDegrees);
    assert.deepEqual(state.phases, threePhase.phases);
    close(state.instantKW, 100);
  }
  close(rms(states.map((state) => state.lineABVoltageV)), 480);
  close(Math.max(...states.map((state) => state.lineABVoltageV)), 480 * Math.SQRT2);
  close(Math.min(...states.map((state) => state.lineABVoltageV)), -480 * Math.SQRT2);
});

test("power scaling and alternate supply voltages retain the power balance", () => {
  const dc = acdcWaveModel("dc-basics", 42, 200, 1000, 400);
  close(dc.instantKW, 200);
  close(dc.phases[0].currentA, 200);
  const single = cycle("ac-basics", 200, 1000, 400);
  close(single[0].phases[0].rmsCurrentA, 500);
  close(mean(single.map((state) => state.instantKW)), 200);
  for (const state of cycle("three-phase", 200, 1000, 400)) {
    close(state.instantKW, 200);
    close(state.currentSumA, 0);
    close(state.phases[0].rmsCurrentA, 288.6751345948129);
  }
});

test("zero load draws zero current and power while the source voltage remains", () => {
  for (const kind of ["dc-basics", "ac-basics", "three-phase", "voltage-basis"]) {
    const state = acdcWaveModel(kind, 43, 0);
    close(state.instantKW, 0);
    close(state.averageKW, 0);
    assert.ok(state.phases.some((phase) => Math.abs(phase.voltageV) > 0));
    for (const phase of state.phases) {
      close(phase.currentA, 0);
      close(phase.rmsCurrentA, 0);
      close(phase.powerKW, 0);
    }
  }
});

test("phase angle is periodic, accepts negative cycles, and remains finite at large angles", () => {
  for (const angle of [-683, -323, 37, 397, 3600000037]) {
    const state = acdcWaveModel("three-phase", angle);
    const reference = acdcWaveModel("three-phase", 37);
    state.phases.forEach((phase, i) => {
      close(phase.voltageV, reference.phases[i].voltageV, 1e-8);
      close(phase.currentA, reference.phases[i].currentA, 1e-8);
    });
    assert.equal(state.angleDegrees, angle);
  }
  assert.ok(Number.isFinite(acdcWaveModel("three-phase", Number.MAX_VALUE).instantKW));
});

test("unknown modes and invalid numeric inputs fail explicitly", () => {
  for (const args of [
    ["unknown", 0],
    ["ac-basics", NaN],
    ["ac-basics", Infinity],
    ["ac-basics", "0"],
    ["ac-basics", 0, -1],
    ["ac-basics", 0, NaN],
    ["ac-basics", 0, Infinity],
    ["dc-basics", 0, 100, 0],
    ["dc-basics", 0, 100, -800],
    ["dc-basics", 0, 100, Infinity],
    ["dc-basics", 0, 100, "800"],
    ["three-phase", 0, 100, 800, 0],
    ["three-phase", 0, 100, 800, -480],
    ["three-phase", 0, 100, 800, NaN],
    ["three-phase", 0, 100, 800, Infinity],
  ]) {
    assert.throws(() => acdcWaveModel(...args), RangeError);
  }
});
