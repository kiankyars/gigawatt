import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {computeDestination, computeDestinations} from '../course/prototypes/compute-migration.js';
import {scenes as workload} from '../course/prototypes/workload-scenes.js';
import {scenes as rack} from '../course/prototypes/rack-energy-scenes.js';
import {scenes as network} from '../course/prototypes/networking-scenes.js';
import {scenes as storage} from '../course/prototypes/storage-scenes.js';

test('all retired compute fragments resolve to a real slide or preserved reader lesson', async () => {
  const legacy = 'compute-purpose consumer-hardware-meme rack tray superchip data-path hbm-package memory-locality capacity-bandwidth weight-read operand-reuse peak-flops operation-bounds roofline switched-rack model-placement rack-interfaces tray-repair fault-placement recover-work diagnose-upgrade network-handoff'.split(' ');
  assert.deepEqual(Object.keys(computeDestinations).sort(), legacy.sort());
  const decks = new Map([
    ['workload-format.html', workload], ['rack-energy-format.html', rack],
    ['networking-format.html', network], ['storage-format.html', storage],
  ]);
  const course = JSON.parse(await readFile(new URL('../course/expanded-course.json', import.meta.url)));
  for (const id of legacy) {
    const [path, target] = computeDestination(`#${id}`).split('#');
    const candidates = path === '../index.html' ? course.lessons : decks.get(path);
    assert.ok(candidates?.some(scene => scene.id === target), `${id} -> ${path}#${target}`);
  }
  for (const hash of ['', '#unknown', '#%E0%A4%A', '#__proto__']) {
    assert.equal(computeDestination(hash), 'networking-format.html#networking-purpose');
  }
  assert.equal(computeDestination('#operand%2Dreuse'), 'workload-format.html#operand-reuse');
});

test('the retired URL loads the redirect instead of the old slide player', async () => {
  const html = await readFile(new URL('../course/prototypes/compute-format.html', import.meta.url), 'utf8');
  assert.match(html, /compute-migration\.js/);
  assert.match(html, /destination\.search = location\.search/);
  assert.match(html, /location\.replace/);
  assert.doesNotMatch(html, /compute-controller\.js/);
});
