// Stable destinations for every scene in the retired Compute chapter.
// Keep these source paths: stage_site rewrites them for /slides/ publication.
export const computeDestinations = Object.freeze({
  'compute-purpose': 'networking-format.html#networking-purpose',
  'consumer-hardware-meme': 'networking-format.html#consumer-hardware-meme',
  rack: 'rack-energy-format.html#rack-hardware-anatomy',
  tray: 'rack-energy-format.html#rack-hardware-anatomy',
  superchip: 'rack-energy-format.html#rack-hardware-anatomy',
  'data-path': 'networking-format.html#packet-path',
  'hbm-package': '../index.html#d07-data-path',
  'memory-locality': '../index.html#d07-data-path',
  'capacity-bandwidth': '../index.html#d07-bottleneck-model',
  'weight-read': '../index.html#d07-bottleneck-model',
  'operand-reuse': 'workload-format.html#operand-reuse',
  'peak-flops': '../index.html#d07-bottleneck-model',
  'operation-bounds': '../index.html#d07-bottleneck-model',
  roofline: '../index.html#d07-bottleneck-model',
  'switched-rack': 'networking-format.html#three-scales',
  'model-placement': 'networking-format.html#shared-model',
  'rack-interfaces': 'rack-energy-format.html#rack-hardware-anatomy',
  'tray-repair': 'storage-format.html#tray-repair',
  'fault-placement': 'storage-format.html#recovery-placement',
  'recover-work': 'storage-format.html#recovery-path',
  'diagnose-upgrade': '../index.html#d07-bottleneck-model',
  'network-handoff': 'networking-format.html#networking-purpose',
});

export function computeDestination(hash = '') {
  let id;
  try { id = decodeURIComponent(hash.replace(/^#/, '')); } catch { id = ''; }
  return Object.hasOwn(computeDestinations, id)
    ? computeDestinations[id] : computeDestinations['compute-purpose'];
}
