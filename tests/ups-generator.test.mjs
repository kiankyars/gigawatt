import test from "node:test";
import assert from "node:assert/strict";
import { generatorModel, renderGeneratorDiagram } from "../course/prototypes/ups-generator.js";

test("only one AC source closes, while battery carries the transfer interval", () => {
  for (const stage of ["utility", "waiting", "generator", "recharge"]) {
    const m = generatorModel(stage);
    assert.equal(m.utilityConnected && m.generatorConnected, false);
    assert.equal(m.rectifierPowered, m.utilityConnected || m.generatorConnected);
    assert.equal(m.batterySupplying, !m.rectifierPowered);
    assert.equal(m.loadKW, 100);
  }
  assert.throws(() => generatorModel("both"));
});
test("generator recharge reverses the battery branch without changing the inverter load", () => {
  const before = generatorModel("generator");
  const charging = generatorModel("recharge");
  assert.equal(charging.batteryCharging, true);
  assert.equal(charging.batterySupplying, false);
  assert.equal(before.batteryCharging, false);
  assert.equal(charging.loadKW, before.loadKW);
  for (const compact of [false, true]) {
    const { svg } = renderGeneratorDiagram({ stage: "recharge", compact });
    assert.match(svg, /class="wire active" data-path="dc-link-to-battery"/);
    assert.match(svg, /data-contact="generator" data-closed="true"/);
    assert.match(svg, /data-contact="utility" data-closed="false"/);
    assert.match(svg, /Charging/);
    assert.doesNotMatch(svg, /class="wire active" data-path="battery-to-dc-link"/);
  }
});
