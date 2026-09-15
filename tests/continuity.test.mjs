import test from "node:test";
import assert from "node:assert/strict";
import {
  storageModel,
  isolationModel,
  serviceModel,
} from "../course/prototypes/continuity-model.js";
import {
  continuityScenes,
  resolveContinuityScene,
} from "../course/prototypes/continuity-scenes.js";
import { renderContinuityVisual } from "../course/prototypes/continuity-visuals.js";
import { renderOnlineUPS } from "../course/prototypes/continuity-online.js";
import {
  capacitorModel,
  recoveryModel,
} from "../course/prototypes/ups-capacitors.js";

test("usable energy window is applied once; inadequate power has no full-load runtime", () => {
  const a = storageModel(8, 6),
    b = storageModel(4, 6);
  assert.ok(Math.abs(a.deliveredMWh - 0.76) < 1e-12);
  assert.ok(Math.abs(a.runtimeMinutes - 7.6) < 1e-12);
  assert.equal(b.canSupport, false);
  assert.equal(b.runtimeMinutes, null);
  assert.throws(() => storageModel(-1, 6));
});
test("selective branch clearing preserves unrelated groups; bus loss does not", () => {
  assert.deepEqual(isolationModel("branch").healthy, [true, false, true]);
  assert.deepEqual(isolationModel("branch").branchContactsClosed, [
    true,
    false,
    true,
  ]);
  for (const zone of ["upstream", "bus"]) {
    assert.deepEqual(isolationModel(zone).healthy, [false, false, false]);
    assert.deepEqual(isolationModel(zone).branchContactsClosed, [
      true,
      true,
      true,
    ]);
  }
});
test("electrical transfer does not repair utility-only controls or prove thermal margin", () => {
  for (const stage of ["bridge", "generator", "recovery"]) {
    const m = serviceModel({ stage });
    assert.equal(m.itPower, true);
    assert.equal(m.controls, false);
    assert.equal(m.service, "controlled stop");
    const repaired = serviceModel({ stage, protectedControls: true });
    assert.equal(repaired.controls, true);
    assert.equal(repaired.service, "thermal margin required");
  }
  assert.equal(serviceModel({ stage: "bridge" }).pumps, false);
  assert.equal(serviceModel({ stage: "generator" }).pumps, true);
});
test("legacy UPS scene hashes stay reachable in the separate Chapter7 deck", () => {
  const old = [
    "campus",
    "electrical-room",
    "equipment",
    "normal",
    "outage",
    "capacitors",
    "generator",
    "dc-link-recovery",
    "static-bypass",
    "maintenance-bypass",
    "capacity-n",
    "capacity-n1",
    "capacity-n2",
    "shared-bus",
    "two-n",
    "two-n-plus-one",
    "load-growth",
    "tier-topology",
    "tier-generation",
    "availability-budget",
    "tier-investment",
    "return",
  ];
  for (const id of old)
    assert.equal(
      continuityScenes[resolveContinuityScene(id)].id,
      { "electrical-room": "equipment", return: "service-check" }[id] || id,
    );
  assert.equal(
    continuityScenes[resolveContinuityScene("electrical-room")].id,
    "equipment",
  );
  assert.equal(
    continuityScenes[resolveContinuityScene("return")].id,
    "service-check",
  );
  assert.equal(
    new Set(continuityScenes.map((s) => s.id)).size,
    continuityScenes.length,
  );
  assert.ok(continuityScenes.every((s) => s.domain === "D05"));
  assert.deepEqual(
    [...new Set(continuityScenes.flatMap((s) => s.objectives))].sort(),
    ["D05.1", "D05.2", "D05.3", "D05.4"],
  );
  assert.equal(continuityScenes.filter((s) => s.check).length, 2);
});
test("new visuals retain accessible labels in both geometries", () => {
  for (const compact of [false, true])
    for (const scene of continuityScenes.filter(
      (s) => !s.ups && !s.reliability,
    )) {
      const html = renderContinuityVisual(
        scene,
        { serviceReveal: true, protectedControls: true },
        compact,
      );
      assert.ok(html.length > 100, scene.id);
      assert.ok(!html.includes("undefined"), scene.id);
      assert.ok(!html.includes("NaN"), scene.id);
    }
});
test("online UPS extraction preserves powered output while its AC source is absent", () => {
  for (const compact of [false, true]) {
    const r = renderOnlineUPS(true, compact);
    assert.match(r.svg, /class="wire active" data-path="ac-output"/);
    assert.match(r.svg, /class="wire " data-path="utility"/);
  }
});
test("capacitor cutoff retains energy and recovery requires a surplus", () => {
  const cutoff = capacitorModel("alone", 15);
  assert.equal(cutoff.voltageV, 700);
  assert.equal(0.5 * 0.2 * cutoff.voltageV ** 2, 49000);
  const flat = recoveryModel(100, 0);
  assert.equal(flat.recoveredJ, 0);
  assert.equal(flat.settled, false);
  const restored = recoveryModel(50, 100000);
  assert.ok(Math.abs(restored.voltageV - 800) < 1e-9);
  assert.equal(restored.recoveredJ, 5000);
});

test("bus failure precedes upstream clearing and cannot be repaired by that trip", () => {
  const fault = isolationModel("bus");
  const cleared = isolationModel("bus-cleared");
  assert.equal(fault.upstream, true);
  assert.equal(cleared.upstream, false);
  assert.deepEqual(fault.healthy, [false, false, false]);
  assert.deepEqual(cleared.healthy, fault.healthy);
});
