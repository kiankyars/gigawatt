import {checkpointTimeline, recoveryEnergy} from './storage-model.js';

export function renderRepairRecovery() {
 return `<div class="storage-review-repair">
  <figure class="storage-review-tray">
   <img src="../assets/references/nvidia-gb300-tray.png" alt="A removed NVIDIA DGX GB300 compute tray containing four GPUs.">
   <figcaption><strong>4 GPUs unavailable</strong><span>while this compute tray is removed</span><a href="https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html" target="_blank" rel="noopener">NVIDIA · Compute tray</a></figcaption>
  </figure>
  <div class="storage-review-restart">
   <ol aria-label="Recovery sequence">
    <li><span>1</span><b>Detect the failure</b></li>
    <li><span>2</span><b>Allocate replacement workers</b></li>
    <li><span>3</span><b>Restore a complete checkpoint</b></li>
    <li><span>4</span><b>Validate new output</b></li>
   </ol>
   <p>Replacement workers need a compatible runtime and access to the saved state and data.</p>
  </div>
 </div>`;
}

const phases = {work:'Useful work', lost:'Lost work', save:'Save', recovery:'Restore'};
const axisMinutes = 110;
const decimal = value => Number(value.toFixed(3)).toString();

function timeline(timeline, failure) {
 return `<div class="storage-review-track" role="img" aria-label="${timeline.segments.map(s => `${phases[s.kind]} from minute ${s.start} to ${s.end}`).join('; ')}.">
  ${timeline.segments.map(s => `<span class="storage-review-phase phase-${s.kind}" style="left:${s.start / axisMinutes * 100}%;width:${s.duration / axisMinutes * 100}%" title="${phases[s.kind]}: ${s.duration} min">${s.duration >= 10 ? s.duration : ''}</span>`).join('')}
  ${failure === null ? '' : `<i class="storage-review-fault" style="left:${failure / axisMinutes * 100}%" title="Failure at minute ${failure}"></i>`}
 </div>`;
}

function metric(value, unit, label) {
 return `<div class="storage-review-metric"><span class="storage-review-mobile-label">${label}</span><strong>${value}<small>${unit}</small></strong></div>`;
}

export function renderCheckpointPolicy(state, compact = false) {
 const failure = state.failure === undefined ? 35 : state.failure;
 const policies = [20, 40].map(interval => {
  const result = checkpointTimeline({intervalMinutes:interval, failureMinute:failure});
  return {interval, result, energy:recoveryEnergy(result)};
 });
 const verdict = failure === 35
  ? 'Saving every 20 minutes preserves more progress when the failure occurs at minute 35.'
  : failure === 55
   ? 'Both finish at minute 80; saving every 20 minutes loses less work.'
   : 'With no failure, saving every 40 minutes finishes two minutes sooner.';
 return `<div class="storage-review-policy${compact ? ' is-compact' : ''}">
  <div class="storage-review-inputs"><span><b>60 min</b> useful work</span><span><b>2 min</b> per save</span><span><b>5 min</b> to restore</span><span><b>1 MW</b> computing</span></div>
  <div class="storage-review-comparison">
   <div class="storage-review-head" aria-hidden="true"><span>Elapsed time</span><span>Finish</span><span>Lost work</span><span>Energy to<br>repeat lost work</span></div>
   ${policies.map(({interval, result, energy}) => `<section class="storage-review-policy-row" aria-label="Save every ${interval} useful minutes">
    <div class="storage-review-lane"><h2>Save every ${interval} useful minutes</h2>${timeline(result, failure)}</div>
    ${metric(result.finishMinute, 'min', 'Finish')}
    ${metric(result.lostMinutes, 'min', 'Lost work')}
    ${metric(decimal(energy.lostMWh), 'MWh', 'Energy to repeat')}
   </section>`).join('')}
   <div class="storage-review-axis-row" aria-hidden="true"><div class="storage-review-axis">${[0,20,40,60,80,100].map(minute => `<span style="left:${minute / axisMinutes * 100}%">${minute}</span>`).join('')}<small>minutes</small></div></div>
  </div>
  <div class="storage-review-legend">${Object.entries(phases).map(([kind, label]) => `<span><i class="phase-${kind}"></i>${label}</span>`).join('')}${failure === null ? '' : '<span><i class="legend-fault"></i>Failure</span>'}</div>
  <p class="storage-review-verdict">${verdict}</p>
 </div>`;
}
