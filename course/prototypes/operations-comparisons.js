import {sampleQuality,heatBalance,flexibleSchedule} from './operations-model.js';

const arrow='<span class="oc-arrow" aria-hidden="true">→</span>';
const metric=(value,label,tone='')=>`<div class="oc-metric ${tone}"><strong>${value}</strong><span>${label}</span></div>`;

function measurementTime(){
 const samples=[{title:'Old sample',observedAt:0,time:'10:00:00'},{title:'Fresh sample',observedAt:595,time:'10:09:55'}];
 return `<div class="oc-comparison oc-clocks">
  <div class="oc-context"><strong>Now: 10:10:00</strong><span>Required age: 60 seconds or less</span></div>
  <div class="oc-pair">${samples.map(sample=>{
   const quality=sampleQuality({observedAt:sample.observedAt,receivedAt:599,now:600,maxAge:60});
   return `<section class="oc-panel ${quality.fresh?'oc-good':'oc-warning'}"><h2>${sample.title}</h2>
    <div class="oc-sample-value">30 °C</div>
    <dl class="oc-time-details"><div><dt>Measured at</dt><dd>${sample.time}</dd></div><div><dt>Message received</dt><dd>10:09:59</dd></div></dl>
    ${metric(quality.age===600?'10 minutes old':`${quality.age} seconds old`,quality.fresh?'Current measurement':'Stale measurement',quality.fresh?'oc-good':'oc-warning')}
   </section>`;
  }).join('')}</div>
  <p class="oc-takeaway">Measurement age starts at the sensor, not when the message arrives.</p>
 </div>`;
}

function heatAccount(){
 const cases=[{title:'Old flow reading',flow:100,caption:'Measured 10 minutes ago',current:false},{title:'Current flow check',flow:50,caption:'Measured at the row now',current:true}];
 return `<div class="oc-comparison oc-heat">
  <div class="oc-context oc-heat-context"><div><strong>Row B: 2.09 MW electrical input</strong><span>Temperatures have stabilized · all heat enters this water branch</span></div><div><strong>30 → 40 °C</strong><span>Current water temperatures · 10 °C rise</span></div></div>
  <div class="oc-pair">${cases.map(item=>{
   const account=heatBalance({flow:item.flow,supply:30,returnTemperature:40});
   return `<section class="oc-panel ${item.current?'oc-good':'oc-warning'}"><h2>${item.title}</h2>
    ${metric(`${item.flow} kg/s`,item.caption)}
    <div class="oc-heat-calculation"><span>${item.flow} × 4.18 × 10 ÷ 1000</span>${arrow}<strong>${account.heatMW.toFixed(2)} MW</strong></div>
    <p class="oc-account-verdict">${item.current?'Matches the row’s 2.09 MW heat input':'Twice the row’s 2.09 MW heat input'}</p>
   </section>`;
  }).join('')}</div>
  <div class="oc-formula"><span>Heat = flow × water heat capacity × temperature rise</span><small>Water: 4.18 kJ/(kg·°C). Divide kW by 1000 for MW.</small></div>
 </div>`;
}

function configurationMapping(){
 return `<div class="oc-comparison oc-mapping">
  <div class="oc-physical"><span>Physical cooling connection</span><div><strong>Branch C2</strong>${arrow}<strong>Row B</strong></div></div>
  <p class="oc-trigger">C2 cooling alarm → request a workload reduction</p>
  <div class="oc-pair">
   <section class="oc-panel oc-warning"><h2>Old control mapping</h2><div class="oc-command"><span>C2 alarm</span>${arrow}<strong>Row A</strong></div><p class="oc-account-verdict">The wrong row gets the command.</p><p>Row B’s workload stays unchanged.</p></section>
   <section class="oc-panel oc-good"><h2>Corrected control mapping</h2><div class="oc-command"><span>C2 alarm</span>${arrow}<strong>Row B</strong></div><p class="oc-account-verdict">The affected row gets the command.</p><p>Confirm Row B actually responds.</p></section>
  </div>
 </div>`;
}

const timePosition=hour=>(hour-13)/8*100;
function schedulePlan(plan,{title,tone,deadline,shift}){
 const segments=plan.segments.map(segment=>`<span class="oc-run" style="left:${timePosition(segment.start)}%;width:${(segment.end-segment.start)/8*100}%"><span>Run</span></span>`).join('');
 return `<section class="oc-plan ${tone}">
  <div class="oc-plan-heading"><h2>${title}</h2><span><b>${plan.eventPeakMW} MW</b> during grid event</span></div>
  <div class="oc-track" role="img" aria-label="${title}: ${plan.segments.map(segment=>`run ${segment.start}:00 to ${segment.end}:00`).join(', ')}. ${plan.eventPeakMW} megawatts during the grid event. Finish ${plan.finishHour}:00.">
   <span class="oc-event-band" aria-hidden="true"></span>${segments}${shift?'<span class="oc-pause" aria-hidden="true">Pause</span>':''}
   <span class="oc-deadline" style="left:${timePosition(deadline)}%" aria-hidden="true"></span>
  </div>
  <div class="oc-plan-result"><span>Finishes <b>${plan.finishHour}:00</b></span><strong class="${plan.meetsDeadline?'oc-good':'oc-warning'}">${plan.meetsDeadline?`Meets ${deadline}:00 deadline`:`Misses ${deadline}:00 deadline by 1 hour`}</strong></div>
 </section>`;
}

function deadlineScheduling(state){
 const deadline=Number(state.deadline??20),common={deadlineHour:deadline,baseMW:20,jobMW:4,workHours:3,eventStart:14,eventEnd:16,startHour:13};
 const continued=flexibleSchedule({...common,shift:false}),paused=flexibleSchedule({...common,shift:true});
 return `<div class="oc-comparison oc-scheduling">
  <div class="oc-schedule-inputs"><span><b>20 MW</b> base + <b>4 MW</b> job</span><span><b>3 hours</b> running = <b>${continued.jobMWh} MWh</b> in either plan</span></div>
  <div class="oc-event-caption">Grid event: 14:00–16:00 <span>│ Dashed line: ${deadline}:00 deadline</span></div>
  <div class="oc-time-axis" aria-hidden="true">${[13,14,16,18,20,21].map(hour=>`<span style="left:${timePosition(hour)}%">${hour}:00</span>`).join('')}</div>
  ${schedulePlan(continued,{title:'Continue through the event',tone:'oc-continue',deadline,shift:false})}
  ${schedulePlan(paused,{title:'Pause for the event',tone:'oc-shift',deadline,shift:true})}
  <div class="oc-schedule-legend"><span><i class="oc-legend-run"></i>Running: 24 MW total</span><span><i class="oc-legend-idle"></i>Paused or finished: 20 MW total</span></div>
  <p class="oc-schedule-condition">Pausing retains progress and requires 24 MW to be available from 16:00–18:00.</p>
 </div>`;
}

export function operationsComparison(id,state={}){
 switch(id){
  case 'measurement-time':return measurementTime();
  case 'heat-balance':return heatAccount();
  case 'configuration-mapping':return configurationMapping();
  case 'deadline-scheduling':return deadlineScheduling(state);
  default:return null;
 }
}
