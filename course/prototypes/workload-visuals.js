import { memoryBudget, utilizationCase, inferenceSchedule, phaseSchedule, evaluateInferenceAcceptance, transitionRate } from './workload-model.js';
const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',panel:'var(--panel)',paper:'var(--paper)',face:'var(--surface)',compute:'var(--power)',communication:'var(--data)',checkpoint:'var(--heat)',wait:'var(--heat)',idle:'var(--muted)'};
const esc=v=>String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const n=(v,d=0)=>v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const t=(x,y,s,size=22,color=C.ink,anchor='start',extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" ${extra}>${esc(s)}</text>`;
const lines=(x,y,a,size=22,color=C.ink,anchor='start',step=size*1.4)=>a.map((s,i)=>t(x,y+i*step,s,size,color,anchor)).join('');
const r=(x,y,w,h,fill=C.panel,stroke=C.line,rx=9)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}"/>`;
const line=(x,y,xx,yy,color=C.line,width=2,dash='')=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
const arrow=(x,y,xx,yy,color=C.compute)=>`${line(x,y,xx,yy,color,3)}<path d="M${xx-9} ${yy-6}L${xx} ${yy}L${xx-9} ${yy+6}" transform="rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI} ${xx} ${yy})" fill="none" stroke="${color}" stroke-width="3"/>`;
const note=(a,m,y=m?614:516)=>lines(m?195:600,y,Array.isArray(a)?a:[a],m?17:23,C.muted,'middle');
const stamp=(s,m)=>t(m?20:60,34,s,m?Math.min(13,350/(s.length*.57)):16,C.muted);
const result=(value,label,m,y=400,color=C.compute)=>t(m?195:600,y,value,m?Math.min(43,340/(value.length*.56)):66,color,'middle')+t(m?195:600,y+(m?35:42),label,m?Math.min(18,345/(label.length*.52)):24,C.ink,'middle');
const box=(x,y,w,h,label,detail,m,color=C.compute)=>r(x,y,w,h)+t(x+w/2,y+36,label,m?21:26,color,'middle')+lines(x+w/2,y+67,Array.isArray(detail)?detail:[detail],m?16:20,C.ink,'middle');
function brief(s,m){
 const training=s.service==='training';let o=stamp('D01 RACKS → D02 ACCEPTED WORK',m);
 const x=m?95:70,y=m?66:116,w=m?200:270,h=m?110:230;
 o+=r(x,y,w,h,C.face)+t(x+w/2,y+(m?45:65),'64',m?49:76,C.compute,'middle')+t(x+w/2,y+(m?78:109),'accelerators',m?19:27,C.ink,'middle');
 if(!m){for(let i=0;i<8;i++)o+=r(x+23+i*28,y+155,19,42,C.panel);o+=arrow(373,230,460,230);}
 else o+=arrow(195,190,195,224);
 const xx=m?25:505,yy=m?245:82,ww=m?340:620;
 o+=t(xx,yy,training?'FINISH AN EXPERIMENT':'SERVE ARRIVING REQUESTS',m?17:22,C.compute);
 const rows=training?[['Accepted work','Validated training progress'],['Time requirement','Complete by the job deadline'],['Include','Inputs, saves and recovery']]:[['Accepted work','Correct, qualified responses'],['Time requirement','Latency under the arrival trace'],['Include','Queueing and burst traffic']];
 rows.forEach(([a,b],i)=>{const ry=yy+42+i*(m?86:105);o+=line(xx,ry+65,xx+ww,ry+65)+t(xx,ry,a,m?15:19,C.muted)+t(xx,ry+42,b,m?20:28);});
 o+=note(m?['Name model, inputs and quality','before counting machines.']:['Name the model, implementation, inputs and quality before counting machines.'],m,m?595:484);
 return {markup:o,description:`The same request for 64 accelerators becomes ${training?'a validated training progress target with a job deadline, including input staging, checkpointing and recovery':'an inference service with correct qualified responses, latency requirements and arrival traffic'}. Hardware count alone does not specify success.`};
}
function modelWork(s,m){
 const train=s.service==='training',xx=m?35:70,w=m?320:275;let o=stamp('PARAMETERS = NUMERICAL VALUES THAT SHAPE OUTPUT',m);
 const ys=m?[85,245,405]:[170,170,170];const xs=m?[xx,xx,xx]:[70,463,855];
 const labels=train?[['Examples','Inputs + target or objective'],['Model + loss','Evaluate the current output'],['Update state','Gradients → new parameters']]:[['Request','Input to the configured model'],['Model execution','Parameters + working memory'],['Response','Check output and quality']];
 labels.forEach(([a,b],i)=>{o+=box(xs[i],ys[i],w,110,a,b,m,i===2&&train?C.checkpoint:C.compute);if(i<2)o+=m?arrow(195,ys[i]+120,195,ys[i+1]-12):arrow(xs[i]+w+12,225,xs[i+1]-12,225);});
 if(train){if(m)o+=`<path d="M355 460H375V297H357" fill="none" stroke="${C.checkpoint}" stroke-width="3"/>`+arrow(375,297,357,297,C.checkpoint);else o+=`<path d="M992 298V379H600V298" fill="none" stroke="${C.checkpoint}" stroke-width="3"/>`+arrow(600,379,600,285,C.checkpoint)+t(790,415,'Keep state for the next update',25,C.checkpoint,'middle');}
 o+=note(train?['Training keeps more than weights.','Updates need supporting state.']:['Inference still needs working memory.','Request state can still change.'],m,m?580:465);
 return {markup:o,description:train?'Training passes examples through the model, evaluates an objective and updates parameters using gradients and optimizer state. The new parameters feed the next iteration.':'Inference runs a request through a configured model and produces a response for quality checks. It needs working memory but this depicted flow does not update the learned parameters.'};
}
function resourcePaths(s,m){
 const color=key=>s.resource===key?C.compute:C.line;let o=stamp('CAMPUS → IT HALL → COMPUTE SYSTEM',m);
 if(m){
 o+=box(95,67,200,80,'Storage','Inputs / restart state',true,C.checkpoint);
 o+=r(30,207,330,237,C.face)+t(47,235,'COMPUTE SYSTEM',14,C.muted)+box(56,265,130,120,'Memory',['Parameters','+ workspace'],true)+box(210,265,126,120,'Processor',['Execute','arithmetic'],true);
 o+=arrow(186,319,206,319,color('compute'))+arrow(145,152,145,258,color('input'))+arrow(252,204,252,154,color('checkpoint'));
 o+=t(75,185,'inputs',16,C.compute)+t(258,185,'save',16,C.checkpoint);
 o+=box(95,503,200,94,'Network','Other workers',true,C.communication)+arrow(272,445,272,498,color('exchange'));
 }else{
 o+=box(55,202,230,113,'Storage',['Inputs /','restart state'],false,C.checkpoint)+r(406,100,464,333,C.face)+t(431,137,'COMPUTE SYSTEM',18,C.muted)+box(438,210,178,113,'Memory',['Parameters +','workspace'],false)+box(663,210,176,113,'Processor','Arithmetic',false);
 o+=arrow(622,265,656,265,color('compute'))+arrow(285,237,430,237,color('input'))+arrow(430,306,293,306,color('checkpoint'))+t(350,218,'inputs',20,C.compute,'middle')+t(350,340,'checkpoint',19,C.checkpoint,'middle');
 o+=box(955,202,200,113,'Network','Other workers',false,C.communication)+arrow(875,260,945,260,color('exchange'));
 o+=t(635,391,'Electrical input → operation → heat removal',19,C.muted,'middle');
 }
 const payoff={input:['Late input data can stall compute.'],compute:['State must fit before arithmetic can run.'],exchange:['A worker may wait for its peers.'],checkpoint:['A completed save makes restart possible.']}[s.resource];
 o+=note(payoff,m,m?645:510);
 return {markup:o,description:`The compute system contains memory and processors; it connects to input/checkpoint storage and to other workers through the network. Selected phase: ${s.resource}. ${payoff[0]} Power and cooling support every active device.`};
}
function inferenceMemory(s,m){
 const a=memoryBudget({workspaceGB:s.workspace}),x=m?28:80,w=m?334:1040;let o=stamp('INFERENCE · ONE DEVICE · CAPACITY 80 GB',m);
 o+=t(m?195:600,m?99:103,'12 billion × 2 bytes = 24 GB',m?25:40,C.ink,'middle');
 const y=m?190:190,barH=m?110:108,scale=w/80;
 let bx=x;[[24,C.compute,'weights'],[s.workspace,C.communication,'workspace'],[8,C.checkpoint,'reserve']].forEach(([v,c,label])=>{o+=r(bx,y,v*scale,barH,c,c,0);o+=t(bx+v*scale/2,y+barH/2+8,String(v),m?22:35,C.paper,'middle');bx+=v*scale;});
 o+=r(bx,y,(80-a.totalGB)*scale,barH,C.face,C.line,0)+line(x+w,y-20,x+w,y+barH+20,C.ink,3);
 o+=t(x,y-24,'DECLARED BUDGET',m?14:18,C.muted)+t(x+w,y-24,'80 GB',m?17:23,C.ink,'end');
 const parts=m?[['24 GB weights',C.compute], [`${s.workspace} GB workspace / cache`,C.communication],['8 GB reservation',C.checkpoint]]:[['24 GB weights',C.compute],[`${s.workspace} GB workspace / cache`,C.communication],['8 GB reservation',C.checkpoint]];
 parts.forEach(([txt,c],i)=>o+=t(m?40:130+i*360,m?349+i*34:348,txt,m?19:24,c));
 o+=result(`${a.totalGB} GB used · ${a.aggregateHeadroomGB} GB left`,'Capacity screen passes',m,m?510:437);
 return {markup:`<g data-total-gb="${a.totalGB}" data-aggregate-capacity-gb="${a.aggregateCapacityGB}" data-aggregate-fits="${a.aggregateFits}" data-partition-fits="${a.partitionFits}">${o}</g>`,description:`Inference weights occupy 24 GB. Workspace/cache ${s.workspace} GB plus reservation 8 GB brings the total to ${a.totalGB} GB of the device's 80 GB, leaving ${a.aggregateHeadroomGB} GB. This is an arithmetic capacity screen, not a measured implementation fit.`};
}
function trainingMemory(s,m){
 const a=memoryBudget({kind:'training',deviceCount:s.devices});let o=stamp('TRAINING · SAME 12 BILLION PARAMETERS',m);
 o+=t(m?195:600,m?83:93,'12 billion × 16 bytes = 192 GB',m?24:38,C.ink,'middle');
 const x=m?30:160,w=m?330:880,y=m?143:153;
 o+=r(x,y,w*.75,90,C.compute,C.compute,0)+r(x+w*.75,y,w*.25,90,C.communication,C.communication,0);
 o+=t(x+w*.375,y+53,'192 GB',m?30:40,C.paper,'middle')+t(x+w*.875,y+53,'64 GB',m?22:34,C.paper,'middle');
 o+=lines(x,m?267:280,m?['Weights, gradients, optimizer state','+ 64 GB activations / workspace']:['Weights + gradients + optimizer state','64 GB of activations / workspace added separately'],m?17:23,C.muted);
 for(let i=0;i<s.devices;i++){const ww=m?70:165,xx=m?42+i*80:600-(s.devices*185-20)/2+i*185,yy=m?371:356;o+=r(xx,yy,ww,70,C.face)+t(xx+ww/2,yy+30,'80 GB',m?17:28,C.compute,'middle')+t(xx+ww/2,yy+54,`device ${i+1}`,m?12:16,C.muted,'middle');}
 o+=result(`${a.aggregateCapacityGB} GB ${a.aggregateFits?'≥':'<'} 256 GB`,a.aggregateFits?'Aggregate passes; partition still unproven':'Fails even with a perfect partition',m,m?529:478,a.aggregateFits?C.compute:C.checkpoint);
 return {markup:`<g data-total-gb="${a.totalGB}" data-aggregate-capacity-gb="${a.aggregateCapacityGB}" data-aggregate-fits="${a.aggregateFits}" data-partition-fits="${a.partitionFits}">${o}</g>`,description:`Training state is 192 GB, plus 64 GB activations and workspace, totaling 256 GB. ${s.devices} devices offer ${a.aggregateCapacityGB} GB aggregate. ${a.aggregateFits?'The aggregate screen passes; no partition has yet been supplied.':'The total capacity is insufficient even under perfect partitioning.'}`};
}
function partitionFit(s,m){
 const allocation=s.partition==='balanced'?[64,64,64,64]:[96,64,48,48],a=memoryBudget({kind:'training',allocationGB:allocation});let o=stamp('256 GB OF STATE → FOUR SEPARATE MEMORY POOLS',m);
 const y=m?145:156,h=m?287:225,scale=h/100,x0=m?37:195,gap=m?88:230,w=m?54:130;
 for(let i=0;i<4;i++){const x=x0+i*gap,bottom=y+h,hh=allocation[i]*scale,cap=80*scale,c=a.deviceFits[i]?C.compute:C.checkpoint;
 o+=r(x,bottom-cap,w,cap,C.face,C.line,0)+r(x,bottom-hh,w,hh,c,c,0)+line(x-8,bottom-cap,x+w+8,bottom-cap,C.ink,3,'5 4')+t(x+w/2,bottom+31,`D${i+1}`,m?19:26,C.ink,'middle')+t(x+w/2,bottom-hh-13,`${allocation[i]}`,m?22:33,c,'middle');}
 o+=t(m?195:600,m?85:82,'Dashed line: 80 GB on each device',m?18:25,C.muted,'middle');
 o+=result(a.partitionFits?'Each allocation fits':'Device 1 exceeds 80 GB',a.partitionFits?'16 GB headroom per device':'Same total; one device is 16 GB over',m,m?525:500,a.partitionFits?C.compute:C.checkpoint);
 return {markup:`<g data-total-gb="${a.totalGB}" data-aggregate-capacity-gb="${a.aggregateCapacityGB}" data-aggregate-fits="${a.aggregateFits}" data-partition-fits="${a.partitionFits}">${o}</g>`,description:`The four allocations are ${allocation.join(', ')} GB, totaling ${a.totalGB} GB. Every device has an 80 GB limit. ${a.partitionFits?'Each memory allocation fits, with 16 GB spare on each device. Implementation and performance still need validation.':'Device one exceeds its limit by 16 GB despite spare capacity on the others. Aggregate fit is insufficient.'}`};
}
function measuredProgress(s,m){
 let o=stamp('SUPPLIED MEASUREMENT → CONDITIONAL ESTIMATE',m);
 o+=t(m?195:600,m?95:116,'8 devices',m?30:40,C.compute,'middle');
 o+=t(m?195:600,m?174:215,'400 samples/s × 20 h',m?30:52,C.ink,'middle')+t(m?195:600,m?219:264,'× 3,600 seconds/hour',m?21:29,C.muted,'middle');
 o+=result('28.8 million','accepted samples, if the rate is sustained',m,m?319:365);
 o+=line(m?35:160,m?414:440,m?355:1040,m?414:440);
 o+=lines(m?195:600,m?466:485,m?['More samples ≠ a quality target.','64-device throughput needs','a scaling measurement.']:['More samples do not prove convergence.','A 64-device result needs a scaling measurement.'],m?21:24,C.muted,'middle');
 return {markup:o,description:'At a supplied sustained rate of 400 accepted samples per second on eight devices, 20 hours gives 28.8 million samples. This does not establish a training convergence target or predict performance on 64 devices.'};
}
function observed(s,m){
 const a=utilizationCase(s.observation),x=m?40:225,w=m?310:850,scale=w/60;let o=stamp('SAME CLOCK · ALLOCATION, POWER AND ACCEPTED OUTPUT',m);
 const y0=m?114:108,step=m?153:126;
 ['Allocated','System power','Accepted output'].forEach((label,i)=>{
  const y=y0+i*step;o+=t(m?40:63,m?y-42:y+15,label,m?18:23,C.muted);
  o+=line(x,y+70,x+w,y+70,C.line);a.phases.forEach(p=>{
   const px=x+p.startSeconds*scale,pw=p.seconds*scale,c=C[p.kind];let hh=i===0?(p.allocated?48:0):i===1?p.powerKW/60*65:p.kind==='compute'?65:0;
   if(hh)o+=r(px,y+70-hh,pw,hh,c,c,0);else o+=line(px,y+69,px+pw,y+69,C.muted,4,'5 4');
   if(i===1)o+=t(px+pw/2,y+70-hh-12,`${p.powerKW} kW`,m?17:23,c,'middle');
   if(i===2&&p.kind==='compute')o+=t(px+pw/2,y+35,'1,000/s',m?19:27,C.paper,'middle');
   if(i===0)o+=t(px+pw/2,y+48,p.kind==='compute'?'compute':p.kind,m?17:22,p.allocated?C.paper:C.muted,'middle');
  });
 });
 o+=t(x,m?y0+step*2+104:487,'0',m?16:20,C.muted)+t(x+w,m?y0+step*2+104:487,'60 s',m?16:20,C.muted,'end');
 o+=note(m?[`${n(a.allocationFraction*100)}% allocated · ${n(a.executionFraction*100)}% executing`,`${n(a.acceptedSamples)} accepted samples`]:`${n(a.allocationFraction*100)}% allocated · ${n(a.executionFraction*100)}% executing · ${n(a.acceptedSamples)} accepted samples`,m,m?613:533);
 return {markup:`<g data-case="${s.observation}" data-average-kw="${a.averageKW}" data-accepted-samples="${a.acceptedSamples}" data-allocation-fraction="${a.allocationFraction}" data-energy-kwh="${a.energyKWh}">${o}</g>`,description:`Case ${s.observation}: allocation ${n(a.allocationFraction*100)} percent, execution ${n(a.executionFraction*100)} percent. Average power ${n(a.averageKW,2)} kW. ${n(a.acceptedSamples)} accepted samples over sixty seconds. Waiting uses power with no accepted output; the no-job state has no allocated devices.`};
}
function energy(s,m){
 const a=utilizationCase('A'),b=utilizationCase(s.energyCase);let o=stamp('FULL-INTERVAL ENERGY ÷ ACCEPTED OUTPUT',m);
 const list=[['A',a],[s.energyCase==='idle'?'Idle':s.energyCase,b]];
 list.forEach(([label,v],i)=>{
 const x=m?28:75+i*560,y=m?79+i*230:83,w=m?334:490;
 o+=t(x,y,`CASE ${label}`,m?16:20,C.muted);
 const ss=v.phases.map(p=>`${p.powerKW} × ${p.seconds}`).join(' + ');
 o+=t(x,y+41,`${ss} = ${n(v.energyJ/1000)} kJ`,m?21:30);
 o+=line(x,y+62,x+w,y+62)+t(x,y+99,`${n(v.acceptedSamples)} accepted samples`,m?21:30,C.compute);
 const j=v.joulesPerAcceptedSample,txt=j===null?'Undefined':`${n(j,j===Math.round(j)?0:1)} J/sample`;
 o+=t(x,y+157,txt,m?38:51,j===null?C.muted:C.compute)+t(x,y+(m?189:212),`${n(v.averageKW,2)} kW mean · ${n(v.energyKWh,3)} kWh`,m?17:23,C.muted);
 });
 const change=b.joulesPerAcceptedSample===null?null:(b.joulesPerAcceptedSample/a.joulesPerAcceptedSample-1)*100;
 o+=note(change===null?['Zero output gives no energy-per-result ratio.','Idle energy still counts.']:[`${n(Math.abs(change),1)}% ${change>0?'more':'less'} energy per result`,change>0?'Waiting energy is shared by fewer results.':'Less waiting spreads energy over more results.'],m,m?591:470);
 return {markup:`<g data-comparison="${s.energyCase}" data-energy-kwh="${b.energyKWh}" data-joules-per-sample="${b.joulesPerAcceptedSample??'undefined'}">${o}</g>`,description:`Case A uses ${n(a.energyKWh,4)} kWh for ${n(a.acceptedSamples)} accepted samples, ${n(a.joulesPerAcceptedSample,1)} joules per sample. Case ${s.energyCase} uses ${n(b.energyKWh,4)} kWh for ${n(b.acceptedSamples)} samples; ${b.joulesPerAcceptedSample===null?'energy per sample is undefined because output is zero':n(b.joulesPerAcceptedSample,1)+' joules per accepted sample'}.`};
}
function batchExecution(s,m){
 const a=inferenceSchedule({batchSize:s.batch}),x=m?30:110,w=m?330:980,scale=w/40;let o=stamp('FULL QUEUE · SAME EXECUTION INSTANCE',m);
 o+=t(m?195:600,m?107:89,s.batch===1?'One request per execution':'Four requests per execution',m?25:34,C.compute,'middle');
 const count=s.batch===1?5:2;
 for(let i=0;i<count;i++){
 const xx=x+i*a.executionMs*scale,yy=m?199:152,hh=m?148:169,ww=a.executionMs*scale-7;o+=r(xx,yy,ww,hh,C.panel);
 for(let j=0;j<s.batch;j++){const cx=xx+ww/2,cy=yy+hh/2+(j-(s.batch-1)/2)*(m?26:30);o+=`<circle cx="${cx}" cy="${cy}" r="${m?8:10}" fill="${C.compute}"/>`;}
 o+=t(xx+ww/2,yy+hh+30,`${a.executionMs} ms`,m?16:22,C.muted,'middle');
 }
 o+=t(x,m?414:400,'0',m?17:22,C.muted)+line(x,m?387:374,x+w,m?387:374)+t(x+w,m?414:400,'40 ms',m?17:22,C.muted,'end');
 o+=result(`${a.capacityRps} requests/s`,`${s.batch} ÷ ${n(a.executionMs/1000,3)} seconds`,m,m?500:467);
 return {markup:`<g data-batch-size="${s.batch}" data-capacity-rps="${a.capacityRps}">${o}</g>`,description:`With a permanently full queue, batches of ${s.batch} execute in ${a.executionMs} milliseconds. Capacity is ${a.capacityRps} requests per second. This excludes time spent gathering requests.`};
}
function gathering(s,m){
 const a=inferenceSchedule({arrivalIntervalMs:s.arrivals}),x=m?80:165,w=m?222:780,max=60,scale=w/max;let o=stamp('LATENCY = GATHERING WAIT + EXECUTION',m);
 const yy=m?124:135,row=m?90:75;
 a.requests.forEach((q,i)=>{const y=yy+i*row;o+=t(m?22:66,y+23,`R${i+1}`,m?18:26,C.ink);o+=line(x+q.arrivalMs*scale,y+21,x+q.startMs*scale,y+21,C.checkpoint,m?9:12);o+=r(x+q.startMs*scale,y,20*scale,43,C.compute,C.compute,0);o+=`<circle cx="${x+q.arrivalMs*scale}" cy="${y+21}" r="6" fill="${C.checkpoint}"/>`;o+=t(m?361:1120,y+28,`${q.latencyMs} ms`,m?19:29,C.ink,'end');});
 const ay=m?491:458;o+=line(x,ay,x+w,ay);[0,18,38,60].forEach(v=>o+=t(x+v*scale,ay+28,String(v),m?15:19,C.muted,'middle'));o+=t(x+w+30,ay+28,'ms',m?13:17,C.muted);
 o+=t(m?30:200,m?562:78,'● Arrival / waiting',m?18:23,C.checkpoint)+t(m?220:700,m?562:78,'■ Execution',m?18:23,C.compute);
 o+=note(m?[`Batch starts at ${a.batches[0].startMs} ms; all finish at ${a.finishMs} ms.`,`Mean latency: ${n(a.meanLatencyMs)} ms`]:`Batch starts at ${a.batches[0].startMs} ms; all finish at ${a.finishMs} ms. Mean latency: ${n(a.meanLatencyMs)} ms.`,m,m?615:523);
 return {markup:`<g data-arrival-interval-ms="${s.arrivals}" data-mean-latency-ms="${a.meanLatencyMs}" data-max-latency-ms="${a.maxLatencyMs}">${o}</g>`,description:`Requests arrive at ${a.arrivalsMs.join(', ')} milliseconds. Execution starts at ${a.batches[0].startMs} and all finish at ${a.finishMs} milliseconds. Response times are ${a.requests.map(q=>q.latencyMs).join(', ')} milliseconds. The first request waits longest. Mean response time is ${a.meanLatencyMs} milliseconds.`};
}
function capacity(s,m){
 const a=inferenceSchedule({batchSize:s.batch,requestCount:8}),x=m?35:95,w=m?320:600;let o=stamp('ARRIVALS EVERY 6 ms → 166.7 REQUESTS/s',m);
 o+=t(x,m?96:107,'Offered arrivals',m?20:27)+r(x,m?118:131,w*166.6667/220,40,C.communication,C.communication,0)+t(x+w*166.6667/220+9,m?146:160,'166.7',m?16:22,C.communication);
 o+=t(x,m?214:252,'Execution capacity',m?20:27)+r(x,m?236:276,w*a.capacityRps/220,40,C.compute,C.compute,0)+t(x+w*a.capacityRps/220+9,m?264:305,String(a.capacityRps),m?16:22,C.compute);
 const xx=m?35:810,yy=m?339:92;o+=t(xx,yy,'FIRST 8 RESPONSE TIMES',m?16:19,C.muted);
 a.requests.forEach((q,i)=>{const cx=xx+(i%4)*(m?81:83),cy=yy+51+Math.floor(i/4)*83;o+=t(cx,cy,`${q.latencyMs}`,m?30:37,C.ink)+t(cx,cy+27,`R${i+1} · ms`,m?14:17,C.muted);});
 o+=note(a.overloaded?['Arrivals exceed capacity by 41.7/s.','The queue grows during sustained traffic.']:['Capacity exceeds arrivals.','The first request still takes 38 ms.'],m,m?590:475);
 return {markup:`<g data-batch-size="${s.batch}" data-overloaded="${a.overloaded}" data-capacity-rps="${a.capacityRps}">${o}</g>`,description:`Arrivals offer 166.7 requests per second. Batch ${s.batch} execution capacity is ${a.capacityRps} requests per second. ${a.overloaded?'Arrivals exceed capacity, so the sustained queue grows.':'The periodic offered load is within capacity.'} The first eight response times are ${a.requests.map(q=>q.latencyMs).join(', ')} milliseconds.`};
}
function phaseVisual(id,s,m){
 const single=id==='job-phases',staggered=id==='staggering-jobs'&&s.schedule==='staggered',offsets=single?[0]:staggered?[0,15,30,45]:[0,0,0,0],a=phaseSchedule({offsetsSeconds:offsets});let o=stamp(single?'ONE JOB · EACH PHASE HAS A DIFFERENT RESOURCE DEMAND':'FOUR JOBS · ADD VERTICALLY AT THE SAME INSTANT',m);
 const x=m?62:157,w=m?296:960,sc=w/60,top=m?104:85,row=single?(m?99:78):(m?49:47);
 const names={compute:'compute',communication:'exchange',checkpoint:'save'};
 for(let j=0;j<offsets.length;j++){
 const y=top+j*row;o+=t(m?20:69,y+25,single?'Job':`J${j+1}`,m?17:23,C.ink);
 for(const seg of a.segments){const ph=seg.jobPhases[j],xx=x+seg.startSeconds*sc,ww=(seg.endSeconds-seg.startSeconds)*sc;o+=r(xx,y,ww,row-8,C[ph.kind],C[ph.kind],0);if(ww>(m?65:100))o+=t(xx+ww/2,y+(row-8)/2+6,m?(ph.kind==='compute'?'C':ph.kind==='communication'?'↔':'S'):names[ph.kind],m?16:21,C.paper,'middle');}
 }
 const gy=single?(m?272:233):(m?370:322),gh=single?(m?196:184):(m?130:143),max=single?140:520,py=power=>gy+gh-power/max*gh;
 o+=t(m?25:66,gy-20,'kW',m?16:21,C.muted)+line(x,gy+gh,x+w,gy+gh);
 let d='';for(const seg of a.segments){const xx=x+seg.startSeconds*sc,xe=x+seg.endSeconds*sc,yy=py(seg.powerKW);d+=(d?'L':'M')+xx+' '+yy+'H'+xe;}
 o+=`<path d="${d}" fill="none" stroke="${C.compute}" stroke-width="5"/>`;
 const avgY=py(a.averageKW);o+=line(x,avgY,x+w,avgY,C.muted,2,'6 5');
 a.segments.forEach(seg=>{const yy=py(seg.powerKW),xx=x+(seg.startSeconds+seg.endSeconds)/2*sc;o+=t(xx,yy-12,String(seg.powerKW),m?20:28,C.compute,'middle');});
 [0,30,45,60].forEach(v=>o+=t(x+v*sc,gy+gh+29,`${v}${v===60?' s':''}`,m?15:21,C.muted,'middle'));
 if(single){o+=lines(m?28:80,m?550:487,m?['C: compute · 30 s at 120 kW','↔: exchange · 15 s at 40 kW','S: checkpoint · 15 s at 60 kW']:['Compute 120 kW · Exchange 40 kW · Checkpoint 60 kW'],m?17:23,C.muted);o+=t(m?195:1000,m?657:532,'85 kW mean',m?26:32,C.compute,m?'middle':'end');}
 else {o+=note(m?[`Peak ${a.peakKW} kW · mean ${n(a.averageKW)} kW`,`${n(a.energyKWh,3)} kWh per 60 s cycle`]:`Peak ${a.peakKW} kW · mean ${n(a.averageKW)} kW · ${n(a.energyKWh,3)} kWh per 60 s cycle`,m,m?577:534);o+=t(m?195:600,m?646:45,m?'C compute · ↔ exchange · S checkpoint':'',m?16:20,C.muted,'middle');}
 return {markup:`<g data-peak-kw="${a.peakKW}" data-average-kw="${a.averageKW}" data-energy-kwh="${a.energyKWh}" data-schedule="${staggered?'staggered':'sync'}">${o}</g>`,description:`${single?'One job':'Four '+(staggered?'independent jobs offset by fifteen seconds':'synchronized jobs')} has power plateaus ${a.segments.map(seg=>seg.powerKW).join(', ')} kW; peak ${a.peakKW} kW and mean ${n(a.averageKW)} kW. Energy is ${n(a.energyKWh,3)} kWh per sixty-second cycle. ${staggered?'At every instant two compute, one exchanges and one checkpoints. This requires independence, no contention and periodic steady operation.':''}`};
}
function independence(s,m){
 const coupled=s.relation==='coupled',x=m?72:205,w=m?278:790,top=m?146:135,row=m?84:71;let o=stamp(coupled?'ONE DISTRIBUTED JOB · SHARED EXCHANGE POINT':'FOUR INDEPENDENT JOBS · SEPARATE PROGRESS',m);
 const barrier=x+w*.75;
 for(let i=0;i<4;i++){
 const y=top+i*row,delay=i===3?45:0,computeW=coupled?w*.46:w*(.30+(i%2)*.13),start=coupled?x+(i===3?w*.26:0):x+i*w*.06;
 o+=t(m?20:67,y+24,coupled?`W${i+1}`:`J${i+1}`,m?18:24,C.ink)+r(start,y,computeW,42,C.compute,C.compute,0);
 if(coupled){const end=start+computeW;if(i<3)o+=r(end,y,barrier-end,42,C.checkpoint,C.checkpoint,0)+t(end+(barrier-end)/2,y+26,'wait',m?15:22,C.paper,'middle');o+=arrow(barrier+7,y+21,x+w,y+21,C.communication);}else o+=r(start+computeW,y,w*.18,42,C.communication,C.communication,0);
 }
 if(coupled)o+=line(barrier,top-36,barrier,top+3*row+53,C.communication,3,'5 5')+t(barrier,top-53,'exchange',m?17:25,C.communication,'middle');
 o+=note(coupled?['Delaying W4 makes W1–W3 wait.','The unchanged-phase assumption breaks.']:['Each job can reach its own exchange.','Check deadlines and shared resources.'],m,m?578:492);
 return {markup:o,description:coupled?'Four workers belong to one distributed job. Worker four starts late. The other three wait at a shared exchange point until worker four arrives. This is not the independent-job staggering model; completion time and energy would need to be measured again.':'Four jobs progress separately and each reaches its own exchange phase. Offsetting them can be considered only if deadlines, storage and network contention still allow the required accepted service.'};
}
function demand(s,m){
 const mean=s.resolution==='mean',x=m?55:170,w=m?290:930,y=m?123:95,h=m?320:305,p=v=>y+h-v/550*h;let o=stamp('MEAN AND TRANSITION ANSWER DIFFERENT QUESTIONS',m);
 o+=line(x,y+h,x+w,y+h)+line(x,y,x,y+h);
 if(mean){o+=line(x,p(340),x+w,p(340),C.muted,4,'9 7')+t(x+w/2,p(340)-22,'340 kW',m?32:46,C.muted,'middle');o+=t(x+w/2,y+h+36,'Complete ideal phase cycle',m?18:26,C.muted,'middle');}
 else{
 const xa=x+w*.3,xb=x+w*.7;
 o+=`<path d="M${x} ${p(480)}H${xa}L${xb} ${p(160)}H${x+w}" fill="none" stroke="${C.compute}" stroke-width="5"/>`;
 o+=t(x,p(480)-19,'480 kW',m?24:35,C.compute)+t(x+w,p(160)-20,'160 kW',m?24:35,C.compute,'end');
 o+=line(xa,y+h+16,xb,y+h+16,C.ink)+line(xa,y+h+8,xa,y+h+24,C.ink)+line(xb,y+h+8,xb,y+h+24,C.ink)+t((xa+xb)/2,y+h+52,'2 seconds',m?22:31,C.ink,'middle');
 }
 o+=note(mean?['The mean contains no transition time.','Recover the time-resolved trace.']:[`(160 − 480) ÷ 2 = ${transitionRate()} kW/s`,'320 kW drop over the assumed 2 s'],m,m?550:485);
 return {markup:`<g data-view="${s.resolution}" data-transition-rate-kw-per-second="${transitionRate()}">${o}</g>`,description:mean?'The mean is 340 kW over the ideal full phase cycle. It does not reveal peak power, the size of a phase change or the duration of that transition.':'The assumed transition drops from 480 to 160 kW in two seconds, a 320 kW decrease and an average rate of minus 160 kW per second. This separate ramp illustration does not recalculate the full-cycle energy.'};
}
function acceptance(s,m){
 const a=inferenceSchedule(),v=evaluateInferenceAcceptance({schedule:a,latencyLimitMs:s.latency}),reveal=s.acceptanceReveal;let o=stamp('SERVICE MUST SATISFY BOTH RATE AND RESPONSE TIME',m);
 const x=m?30:125,w=m?330:940,y=m?116:100;
 o+=t(x,y,'RATE REQUIREMENT',m?15:19,C.muted)+t(x,y+54,'≥120 requests/s',m?29:40,C.ink)+t(m?x:x+540,m?y+96:y+54,'166.7 arrive · capacity 200/s',m?20:27,C.compute);
 const yy=m?299:236;o+=t(x,yy,'EACH REQUEST’S RESPONSE TIME',m?15:19,C.muted);
 a.requests.forEach((q,i)=>{const ww=m?73:195,xx=x+i*(m?85:248),bad=q.latencyMs>s.latency,c=reveal&&bad?C.checkpoint:C.compute;o+=r(xx,yy+25,ww,100,C.face,c)+t(xx+ww/2,yy+51,`R${i+1}`,m?16:22,C.muted,'middle')+t(xx+ww/2,yy+109,`${q.latencyMs}`,m?32:45,c,'middle')+t(xx+ww/2,yy+153,'ms',m?17:22,C.muted,'middle');});
 o+=t(m?195:600,m?yy+205:443,`Every request ≤ ${s.latency} ms`,m?26:36,C.ink,'middle');
 o+=note(reveal?(v.meetsLatency?['Timing screens pass.','Quality, power and availability are untested.']:['R1 and R2 miss the latency limit.','A 29 ms mean does not meet this rule.']):['Does this service pass?','Predict, then reveal the reasoning.'],m,m?592:497);
 return {markup:`<g data-latency-limit-ms="${s.latency}" ${reveal?`data-meets-latency="${v.meetsLatency}" data-numerical-pass="${v.numericalPass}"`:''}>${o}</g>`,description:`The target is at least 120 requests per second and every request within ${s.latency} milliseconds. Arrivals offer 166.7 per second and execution capacity is 200. Response times are 38,32,26,20 milliseconds. ${reveal?(v.meetsLatency?'Numerical timing checks pass; quality, power and availability remain unverified.':'Requests one and two miss the limit even though the mean is 29 milliseconds.'):'Predict whether both requirements are met, then reveal the reasoning.'}`};
}
function nextBrief(s,m){
 const mem=memoryBudget({workspaceGB:44}),p=phaseSchedule(),a=inferenceSchedule();let o=stamp('CHANGED BRIEF · THREE SEPARATE BOUNDED SCREENS',m);
 const rows=[['MEMORY','24 + 44 + 8 GB','80 GB device',`${mem.totalGB} GB: capacity passes`,true],['REQUEST TIMING','Batch 4 · arrivals 6 ms','Every request ≤30 ms',`${a.maxLatencyMs} ms worst: misses limit`,false],['JOB POWER','Four synchronized jobs','400 kW peak limit',`${p.peakKW} kW peak: exceeds limit`,false]];
 rows.forEach(([a,b,c,d,pass],i)=>{const x=m?27:90,yy=m?87+i*164:97+i*127,w=m?336:1020;o+=t(x,yy,a,m?14:18,C.muted)+t(x,yy+34,b,m?22:29)+t(m?x:x+560,m?yy+63:yy+34,c,m?18:25,C.muted);o+=line(x,yy+(m?85:99),x+w,yy+(m?85:99));if(s.transferReveal)o+=t(x,yy+(m?118:81),d,m?23:29,pass?C.compute:C.checkpoint);else o+=t(x,yy+(m?118:81),'Pass, fail, or still unknown?',m?20:26,C.muted);});
 o+=note(s.transferReveal?['Next: supply and site conditions','for the supported service envelope.']:['Identify the failed mechanism.','Reveal before carrying the brief to D03.'],m,m?625:508);
 return {markup:`<g data-transfer-revealed="${s.transferReveal}">${o}</g>`,description:`Three separate screens: inference memory ${mem.totalGB} GB against 80 GB; batch-four maximum response time ${a.maxLatencyMs} ms against a 30 ms every-request limit; synchronized job peak ${p.peakKW} kW against a 400 kW job-power limit. ${s.transferReveal?'Memory capacity passes, request latency fails, and peak job power fails. Carry an explicit workload and failure envelope into D03 supply and siting.':'Predict each result, then reveal the reasoning.'}`};
}
export function renderWorkload(id,state,compact=false){
 const f={'success-brief':brief,'model-work':modelWork,'resource-paths':resourcePaths,'inference-memory':inferenceMemory,'training-memory':trainingMemory,'partition-fit':partitionFit,'measured-progress':measuredProgress,'occupied-waiting':observed,'energy-per-result':energy,'batching-throughput':batchExecution,'gathering-latency':gathering,'arrival-capacity':capacity,'independence':independence,'demand-transition':demand,'acceptance-envelope':acceptance,'next-brief':nextBrief}[id];
 const rendered=f?f(state,compact):['job-phases','synchronized-jobs','staggering-jobs'].includes(id)?phaseVisual(id,state,compact):null;
 if(!rendered)throw new RangeError(`Unknown workload scene: ${id}`);
 return rendered;
}
