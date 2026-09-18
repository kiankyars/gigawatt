import {flexibleSchedule} from './operations-model.js';

function rowMeasurements(){
 const rows=[['Rack power','2.09 MW','2.09 MW'],['Water into Row B','30°C','30°C'],['Flow through Row B','100 kg/s','50 kg/s'],['Water leaving Row B','35°C','40°C'],['Hottest chip · limit 80°C','70°C','85°C']];
 return `<div class="oc-comparison"><table class="oc-row-table"><thead><tr><th>Row B</th><th>Before</th><th>After the alarm</th></tr></thead><tbody>${rows.map(([label,before,after],i)=>`<tr class="${i>1?'oc-changed':''}"><th>${label}</th><td>${before}</td><td>${after}</td></tr>`).join('')}</tbody></table></div>`;
}
function heatAccount(){
 const progress=t=>(1-Math.exp(-5*t))/(1-Math.exp(-5));
 const points=Array.from({length:81},(_,i)=>{const t=i/80;return {x:300+650*t,f:progress(t)};});
 const removal=points.map(({x,f},i)=>`${i?'L':'M'}${x.toFixed(1)},${(130-95*f).toFixed(1)}`).join(' ');
 const temperature=points.map(({x,f})=>`L${x.toFixed(1)},${(130-105*f).toFixed(1)}`).join(' ');
 return `<div class="oc-transient">
  <div class="oc-transient-phases"><span>Before</span><span>Flow falls</span><span>Later</span></div>
  <section class="oc-heat-stage" aria-label="Heat generated stays at 2.09 MW. Heat removal initially falls, then recovers to 2.09 MW as temperatures rise.">
   <div class="oc-transient-legend"><span class="oc-generated-key">Heat generated</span><span class="oc-removed-key">Heat removed</span></div>
   <div class="oc-transient-plot oc-heat-plot">
    <svg viewBox="0 0 1000 165" preserveAspectRatio="none" aria-hidden="true"><path d="M300 35L300 130 ${removal.replace(/^M/,'L')}L950 35Z" class="oc-stored-heat"/><path d="M50 35H950" class="oc-generated"/><path d="M50 35H300V130 ${removal.replace(/^M/,'L')}" class="oc-removed"/><path d="M300 0V165" class="oc-flow-event"/></svg>
    <strong class="oc-rate-before">2.09 MW</strong><strong class="oc-rate-after">2.09 MW</strong><span class="oc-accumulation">Heat accumulates</span>
   </div>
  </section>
  <section class="oc-temperature-stage" aria-label="The hottest chip warms from 70 degrees Celsius to a stable 85 degrees Celsius, crossing its 80 degree operating limit.">
   <h2>Hottest chip</h2><div class="oc-transient-plot oc-temperature-plot">
    <svg viewBox="0 0 1000 165" preserveAspectRatio="none" aria-hidden="true"><path d="M50 60H950" class="oc-temperature-limit"/><path d="M300 0V165" class="oc-flow-event"/><path d="M50 130H300 ${temperature}" class="oc-temperature"/></svg>
    <strong class="oc-temp-before">70°C</strong><strong class="oc-temp-after">85°C · stable</strong><span class="oc-limit-label">Limit 80°C</span>
   </div>
  </section>
  <div class="oc-transient-time">Time →</div>
  <p class="oc-transfer-equation">At each chip: heat flow = temperature difference ÷ thermal resistance</p>
 </div>`;
}
function powerPlot(plan,shift){
 const x=h=>68+(h-13)*140,y=p=>125-(p-20)*19;
 const points=[[13,20]];
 for(const segment of plan.segments)points.push([segment.start,20],[segment.start,24],[segment.end,24],[segment.end,20]);
 points.push([20,20]);
 const path=points.map(([h,p],i)=>`${i?'L':'M'}${x(h)},${y(p)}`).join(' ');
 return `<section class="oc-power-plan"><div class="oc-power-heading"><h2>${shift?'Pause during the grid event':'Run without pausing'}</h2><strong>Finish ${plan.finishHour}:00</strong></div><svg viewBox="0 0 1100 170" role="img" aria-label="${shift?'Paused':'Uninterrupted'} workload; ${plan.eventPeakMW} MW during the event; completes at ${plan.finishHour}:00"><rect x="208" y="30" width="280" height="110" fill="var(--warning-surface)"/><text x="348" y="22" text-anchor="middle">Grid event</text>${[20,24].map(p=>`<path d="M68 ${y(p)}H1048" class="oc-gridline"/><text x="56" y="${y(p)+6}" text-anchor="end">${p}</text>`).join('')}<text x="10" y="26">MW</text><path d="${path} L1048 140 L68 140 Z" fill="var(--positive-surface)"/><path d="${path}" class="oc-power-line"/>${[13,14,16,18,20].map(h=>`<text x="${x(h)}" y="164" text-anchor="middle">${h}:00</text>`).join('')}</svg></section>`;
}
function schedule(){
 const normal=flexibleSchedule({shift:false}),paused=flexibleSchedule({shift:true});
 return `<div class="oc-scheduling"><div class="oc-schedule-givens"><span>Illustrative 20 MW base load</span><span>+4 MW flexible job · 3 running hours</span><span>Deadline 20:00</span></div>${powerPlot(normal,false)}${powerPlot(paused,true)}<p class="oc-takeaway">Job energy stays at 12 MWh; grid-event demand falls from 24 to 20 MW.</p></div>`;
}
export function operationsComparison(id){
 switch(id){case 'measurement-boundaries':return rowMeasurements();case 'heat-balance':return heatAccount();case 'deadline-scheduling':return schedule();default:return null;}
}
