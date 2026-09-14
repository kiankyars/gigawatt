import test from "node:test";
import assert from "node:assert/strict";
import {
  movingLoad,
  survivingFiber,
  controlResponse,
  egressRouteModel,
} from "../course/prototypes/site-model.js";
import {
  scenes,
  initialState,
  learningContract,
} from "../course/prototypes/site-scenes.js";
import { operationsAliases } from "../course/prototypes/site-operations.js";
import { renderSite } from "../course/prototypes/site-visuals.js";
import { existsSync } from "node:fs";
test("Moving assembly uses total mass and specified contacts without claiming structural adequacy", () => {
  const a = movingLoad();
  assert.ok(Math.abs(a.totalKN - 21.582) < 1e-10);
  assert.ok(Math.abs(a.perContactKN - 5.3955) < 1e-10);
  assert.equal(movingLoad({ contacts: 8 }).totalKN, a.totalKN);
  for (const x of [0, -1, Infinity, NaN])
    assert.throws(() => movingLoad({ massKg: x }), RangeError);
  assert.throws(() => movingLoad({ contacts: 2.5 }), RangeError);
});
test("Physical route diversity removes only the modeled shared crossing", () => {
  assert.deepEqual(survivingFiber({ crossingFailed: false }), ["A", "B"]);
  assert.deepEqual(survivingFiber(), []);
  assert.deepEqual(survivingFiber({ arrangement: "separate" }), ["B"]);
  assert.throws(
    () => survivingFiber({ arrangement: "carrier-brand" }),
    RangeError,
  );
});
test("Shared controller affects both trains despite separate equipment", () => {
  assert.deepEqual(controlResponse("normal"), {
    trainA: true,
    trainB: true,
    commonDependency: "Shared controller",
  });
  assert.deepEqual(controlResponse("stop"), {
    trainA: false,
    trainB: false,
    commonDependency: "Shared controller",
  });
});
test("Chapter has a motivated opening, every state renders in both layouts, with a live-campus expansion check-in", () => {
  assert.equal(scenes.length, 19);
  assert.equal(new Set(scenes.map((s) => s.id)).size, scenes.length);
  assert.equal(scenes[0].id, "site-purpose");
  assert.equal(scenes.at(-1).id, "service-check");
  assert.equal(Object.keys(learningContract).length, 6);
  for (const scene of scenes) {
    assert.ok(scene.reference.startsWith("d12-"));
    assert.ok(scene.explanation.length >= 2);
    assert.equal(scene.reveal, undefined);
    for (const compact of [false, true]) {
      const states = [{ ...initialState }];
      for (const g of scene.controls || [])
        for (const [value] of g.options)
          states.push({ ...initialState, [g.key]: value });
      for (const state of states) {
        const v = renderSite(scene.id, state, compact);
        assert.ok(v.markup.length > 50);
        assert.ok(v.description.length > 60);
        assert.doesNotMatch(v.markup, /NaN|undefined|Infinity/);
      }
    }
  }
});

test("Retired scene links resolve to a taught replacement", () => {
  for (const [retired, target] of Object.entries(operationsAliases)) {
    assert.ok(!scenes.some((s) => s.id === retired));
    assert.ok(scenes.some((s) => s.id === target));
  }
});

test("Each new case context leads directly into the retained engineering lesson", () => {
  for (const [context, lesson] of [["docklands-context", "ground-and-foundations"], ["harvey-context", "outside-flood"]]) {
    const index = scenes.findIndex(scene => scene.id === context);
    assert.ok(index > 0);
    assert.equal(scenes[index + 1].id, lesson);
    assert.equal(scenes[index].reference, scenes[index + 1].reference);
    const visual = renderSite(context, initialState);
    const image = visual.markup.match(/<img src="([^"]+)"/);
    assert.ok(image, context);
    assert.ok(existsSync(new URL(image[1], new URL("../course/prototypes/site-format.html", import.meta.url))));
  }
  const flood = renderSite("harvey-context", initialState);
  assert.match(flood.markup, /Houston-area flooding/);
  assert.match(flood.markup, /TxDOT \/ NWS/);
  assert.doesNotMatch(flood.markup, /HO1/);
  assert.match(renderSite("docklands-context", initialState).markup, /Proposed campus/);
});

test("A shared approach can lose both exits to one incident while a separate approach survives", () => {
  for (const layout of ["shared", "separate"]) {
    assert.deepEqual(egressRouteModel({layout}).reachable, ["west", "east"]);
    assert.deepEqual(egressRouteModel({layout, incident: "east"}).reachable, ["west"]);
  }
  assert.deepEqual(egressRouteModel({layout:"shared", incident:"west"}).reachable, []);
  assert.deepEqual(egressRouteModel({layout:"separate", incident:"west"}).reachable, ["east"]);
  assert.throws(() => egressRouteModel({layout:"two-doors"}), RangeError);
  assert.throws(() => egressRouteModel({incident:"smoke-simulation"}), RangeError);
});
