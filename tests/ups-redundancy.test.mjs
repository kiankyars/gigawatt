import test from "node:test";
import assert from "node:assert/strict";
import {
  redundancyModel as model,
  renderRedundancy,
} from "../course/prototypes/ups-redundancy.js";

test("N+1 survives one isolated module failure but not failure during module maintenance", () => {
  const failed = model({ kind: "n1", fault: true });
  assert.equal(failed.availableCapacityKW, 100);
  assert.equal(failed.canSupportLoad, true);
  const both = model({ kind: "n1", maintenance: true, fault: true });
  assert.equal(both.availableCapacityKW, 50);
  assert.equal(both.shortfallKW, 50);
  assert.equal(both.canSupportLoad, false);
  assert.doesNotMatch(renderRedundancy(both), /50 kW delivered/);
});

test("N+2 retains N through module maintenance and another module failure", () => {
  const result = model({ kind: "n2", maintenance: true, fault: true });
  assert.equal(result.availableCapacityKW, 100);
  assert.equal(result.canSupportLoad, true);
});

test("extra UPS modules do not bypass a failed shared output bus", () => {
  for (const kind of ["n", "n1", "n2"]) {
    const result = model({ kind, busFault: true });
    assert.ok(result.routes[0].healthyCapacityKW >= 100);
    assert.equal(result.availableCapacityKW, 0);
    assert.equal(result.canSupportLoad, false);
  }
});

test("2N retains a full path during A maintenance but cannot lose a B module at this load", () => {
  const maintenance = model({ kind: "two_n", maintenance: true });
  assert.deepEqual(
    maintenance.routes.map((route) => route.capacityKW),
    [0, 100],
  );
  assert.equal(maintenance.independentFullRoutes, 1);
  const both = model({ kind: "two_n", maintenance: true, fault: true });
  assert.deepEqual(
    both.routes.map((route) => route.capacityKW),
    [0, 50],
  );
  assert.equal(both.canSupportLoad, false);
});

test("2(N+1) retains N during A maintenance and one isolated B-module failure", () => {
  const result = model({ kind: "two_n1", maintenance: true, fault: true });
  assert.deepEqual(
    result.routes.map((route) => route.capacityKW),
    [0, 100],
  );
  assert.equal(result.independentFullRoutes, 1);
  assert.equal(result.canSupportLoad, true);
});

test("A output-bus failure leaves B available and combinations remain consistent", () => {
  const result = model({ kind: "two_n", busFault: true });
  assert.deepEqual(
    result.routes.map((route) => route.capacityKW),
    [0, 100],
  );
  assert.equal(result.canSupportLoad, true);
  const both = model({
    kind: "two_n1",
    maintenance: true,
    fault: true,
    busFault: true,
  });
  assert.deepEqual(
    both.routes.map((route) => route.capacityKW),
    [0, 100],
  );
});

test("load growth changes installed redundancy classification", () => {
  assert.equal(model({ kind: "n2", loadKW: 150 }).label, "N+1");
  assert.equal(model({ kind: "two_n1", loadKW: 150 }).label, "2N");
  assert.equal(model({ kind: "n1", loadKW: 150 }).label, "N");
});

test("aggregate capacity is distinct from a complete surviving path", () => {
  const result = model({ kind: "two_n", loadKW: 150 });
  assert.equal(result.availableCapacityKW, 200);
  assert.equal(result.canSupportLoad, true);
  assert.equal(result.independentFullRoutes, 0);
  assert.equal(result.sharingRequired, true);
  assert.equal(result.label, "Neither path meets N");
  const svg = renderRedundancy(result);
  assert.match(svg, /Both paths needed/);
  assert.match(svg, /0\/2 paths can carry the whole load/);
});

test("capacity remains bounded across every supported combination", () => {
  for (const kind of ["n", "n1", "n2", "two_n", "two_n1"]) {
    for (const loadKW of [50, 100, 100.01, 150, 200, 300]) {
      for (const maintenance of [false, true])
        for (const fault of [false, true])
          for (const busFault of [false, true]) {
            const result = model({
              kind,
              loadKW,
              maintenance,
              fault,
              busFault,
            });
            assert.ok(
              result.availableCapacityKW >= 0 &&
                result.availableCapacityKW <= result.installedCapacityKW,
            );
            assert.equal(
              result.canSupportLoad,
              result.availableCapacityKW >= loadKW,
            );
            assert.equal(
              result.independentFullRoutes,
              result.routes.filter((route) => route.capacityKW >= loadKW)
                .length,
            );
          }
    }
  }
});

test("invalid inputs do not silently become plausible capacity claims", () => {
  for (const loadKW of [0, -1, NaN, Infinity, "100", null]) {
    assert.throws(() => model({ kind: "n", loadKW }), RangeError);
  }
  assert.throws(() => model({ kind: "bogus" }), RangeError);
  assert.throws(() => model({ kind: "n", maintenance: "false" }), TypeError);
});

test("both render geometries have accessible descriptions and retain separate PSU labels", () => {
  for (const compact of [false, true]) {
    const svg = renderRedundancy(model({ kind: "two_n1", maintenance: true }), {
      compact,
    });
    assert.match(svg, /role="img" aria-labelledby=/);
    assert.match(svg, /PSU A/);
    assert.match(svg, /PSU B/);
    assert.match(svg, /AC outputs stay separate/);
    assert.match(svg, /data-state="maintenance"/);
  }
});
