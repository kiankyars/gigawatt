import {heatBalance,flexibleSchedule} from './operations-model.js';

function rowMeasurements(){
 const rows=[['Time','10:00','10:10'],['Rack power','2.09 MW','2.09 MW'],['Water into Row B','30°C','30°C'],['Flow through Row B','100 kg/s','50 kg/s'],['Water leaving Row B','35°C','40°C']];
 return `<div class="oc-comparison"><table class="oc-row-table"><thead><tr><th>Row B</th><th>Before</th><th>After the alarm</th></tr></thead><tbody>${rows.map(([label,before,after],i)=>`<tr class="${i>2?'oc-changed':''}"><th>${label}</th><td>${before}</td><td>${after}</td></tr>`).join('')}</tbody></table><p class="oc-takeaway">The inlet temperature did not change. The flow did.</p></div>`;
}
function heatAccount(){
 return `<div class="oc-comparison"><div class="oc-pair">${[[100,35],[50,40]].map(([flow,t],i)=>`<section class="oc-panel"><h2>${i?'After: reduced flow':'Before: normal flow'}</h2><div class="oc-water-route"><span>30°C<small>in</small></span><b>→ Row B →</b><span>${t}°C<small>out</small></span></div><div class="oc-balance"><span>${flow} kg/s × 4.18 × ${t-30}°C</span><strong>= ${heatBalance({flow,supply:30,returnTemperature:t}).heatMW.toFixed(2)} MW</strong></div></section>`).join('')}</div><div class="oc-formula">Q̇ = ṁ cₚ (T<sub>out</sub> − T<sub>in</sub>)<small>Water cₚ = 4.18 kJ/(kg·°C) · two stabilized operating points</small></div></div>`;
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
 return `<div class="oc-scheduling"><div class="oc-schedule-givens"><span>20 MW base load</span><span>+4 MW flexible job · 3 running hours</span><span>Deadline 20:00</span></div>${powerPlot(normal,false)}${powerPlot(paused,true)}<p class="oc-takeaway">Job energy stays at 12 MWh; grid-event demand falls from 24 to 20 MW.</p></div>`;
}
export function operationsComparison(id){
 switch(id){case 'measurement-boundaries':return rowMeasurements();case 'heat-balance':return heatAccount();case 'deadline-scheduling':return schedule();default:return null;}
}
