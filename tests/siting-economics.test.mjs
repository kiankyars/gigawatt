import test from 'node:test';
import assert from 'node:assert/strict';
import { speedPremium, renderEconomics } from '../course/prototypes/siting-economics.js';

const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-8 * Math.max(1, Math.abs(expected)), `${actual} != ${expected}`);

test('fuel spending is derived from equal electricity and conserves conversion energy', () => {
  const a = speedPremium();
  assert.equal(a.outputMWh, 876000);
  close(a.fastFuelMWh * a.fastEfficiency, a.outputMWh);
  close(a.efficientFuelMWh * a.efficientEfficiency, a.outputMWh);
  close(a.fastFuelCost, 43.8e6);
  close(a.efficientFuelCost, 29.2e6);
  close(a.annualFuelPenalty, 14.6e6);
  close(a.requiredMonthlyContribution, 14.6e6);
  assert.equal(a.advantage, null, 'Unknown contribution cannot become an invented profit');
  assert.ok(Object.isFrozen(a));
});

test('earlier contribution must repay both the stated fuel penalty and added build costs', () => {
  const a = speedPremium({ earlierMonths: 2, fasterBuildPremium: 5.4e6, contributionPerMonth: 10e6 });
  close(a.requiredEarlierContribution, 20e6);
  close(a.requiredMonthlyContribution, 10e6);
  close(a.earlierContribution, 20e6);
  close(a.advantage, 0);
  assert.ok(speedPremium({ contributionPerMonth: 14e6 }).advantage < 0);
  assert.ok(speedPremium({ contributionPerMonth: 15e6 }).advantage > 0);
});

test('fuel penalty scales with duty and disappears at equal efficiency without erasing build costs', () => {
  close(speedPremium({ annualHours: 4380 }).annualFuelPenalty, 7.3e6);
  close(speedPremium({ outputMW: 50 }).annualFuelPenalty, 7.3e6);
  close(speedPremium({ fuelPricePerMWh: 40 }).annualFuelPenalty, 29.2e6);
  const a = speedPremium({ fastEfficiency: 0.6, efficientEfficiency: 0.6, fasterBuildPremium: 2e6 });
  assert.equal(a.annualFuelPenalty, 0);
  assert.equal(a.requiredEarlierContribution, 2e6);
  assert.equal(speedPremium({ annualHours: 0 }).annualFuelPenalty, 0);
});

test('invalid energy and time assumptions are rejected before producing economics', () => {
  for (const input of [
    { outputMW: -1 }, { annualHours: 8761 }, { annualHours: Infinity },
    { fuelPricePerMWh: '20' }, { fasterBuildPremium: -1 },
    { fastEfficiency: 0 }, { efficientEfficiency: 1.1 },
    { fastEfficiency: 0.7, efficientEfficiency: 0.6 },
    { earlierMonths: 0 }, { earlierMonths: NaN }, { contributionPerMonth: Infinity },
  ]) assert.throws(() => speedPremium(input), RangeError);
});

test('both visual accounts retain contract timing and leave hypothetical site revenue unknown', () => {
  for (const compact of [false, true]) {
    const contract = renderEconomics('contract-economics', {}, compact);
    assert.match(contract.markup, /October 2026/);
    assert.match(contract.markup, /before costs/);
    assert.match(contract.markup, /forecast/);
    assert.match(contract.description, /not profit/);
    const sensitivity = renderEconomics('speed-premium', {}, compact);
    assert.match(sensitivity.markup, /data-revenue-assumed="false"/);
    assert.match(sensitivity.description, /before the incremental fuel penalty/);
    for (const a of [contract, sensitivity]) assert.doesNotMatch(a.markup, /NaN|Infinity|undefined/);
  }
  assert.equal(renderEconomics('unrelated', {}), null);
});
