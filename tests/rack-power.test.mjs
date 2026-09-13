import test from 'node:test';
import assert from 'node:assert/strict';
import { localPower, supplyHandoff, bbuShelf, burstRecharge, phaseWaveforms } from '../course/prototypes/rack-power-model.js';

test('high current and resistive drop share the same declared core boundary', () => {
  const a = localPower(), b = localPower({ loopMicroOhms: 10 });
  assert.equal(a.rackAmps, 20); assert.equal(a.coreAmps, 1000);
  assert.ok(Math.abs(a.lossWatts - 100) < 1e-8); assert.ok(Math.abs(a.dropVolts - 0.1) < 1e-8);
  assert.ok(Math.abs(b.lossWatts - 10) < 1e-8); assert.ok(Math.abs(b.dropVolts - 0.01) < 1e-8);
});
test('linear source ramp requires the triangle of missing power, not a rectangle', () => {
  assert.equal(supplyHandoff().energyKJ, 4);
  assert.equal(supplyHandoff({ responseSeconds: 0.4 }).energyKJ, 8);
  assert.equal(supplyHandoff({ responseSeconds: 0.4 }).peakBufferKW, 40);
});
test('one BBU module failure preserves 15 kW, two lose capacity', () => {
  assert.equal(bbuShelf({ failedModules: 1 }).availableKW, 15);
  assert.equal(bbuShelf({ failedModules: 1 }).capacityPass, true);
  assert.equal(bbuShelf({ failedModules: 2 }).capacityPass, false);
  assert.equal(bbuShelf({ failedModules: 2 }).deficitKW, 3);
});
test('repeated bursts include the recharge budget and average source constraint', () => {
  const a = burstRecharge(), b = burstRecharge({ restSeconds: 0.2 });
  assert.equal(a.energyKJ, 8); assert.equal(a.requiredRestSeconds, 0.8); assert.equal(a.missingKJ, 0);
  assert.equal(b.rechargeKJ, 2); assert.equal(b.missingKJ, 6); assert.equal(b.averageLoadKW, 135);
});
test('interleaving changes ripple while preserving average current and finite ripple', () => {
  const a = phaseWaveforms(1), b = phaseWaveforms(4);
  const mean = v => v.slice(0, -1).reduce((a,b) => a+b, 0) / (v.length - 1);
  assert.ok(Math.abs(mean(a.sum) - 1000) < 1e-8); assert.ok(Math.abs(mean(b.sum) - 1000) < 1e-8);
  assert.ok(b.peakToPeakAmps < a.peakToPeakAmps); assert.ok(b.peakToPeakAmps > 0);
});
