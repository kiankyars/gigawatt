import { phaseSchedule, llamaMemory, sameWorkEnergy, interactivityMetrics, decodeSlots } from './workload-model.js';
const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',panel:'var(--panel)',paper:'var(--paper)',face:'var(--surface)',compute:'var(--power)',communication:'var(--data)',checkpoint:'var(--heat)',wait:'var(--heat)',idle:'var(--muted)'};
const esc=v=>String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const n=(v,d=0)=>v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const t=(x,y,s,size=22,color=C.ink,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${esc(s)}</text>`;
const lines=(x,y,a,size=22,color=C.ink,anchor='start',step=size*1.4)=>a.map((s,i)=>t(x,y+i*step,s,size,color,anchor)).join('');
const r=(x,y,w,h,fill=C.panel,stroke=C.line,rx=9)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}"/>`;
const line=(x,y,xx,yy,color=C.line,width=2,dash='')=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
const arrow=(x,y,xx,yy,color=C.compute)=>`${line(x,y,xx,yy,color,3)}<path d="M${xx-9} ${yy-6}L${xx} ${yy}L${xx-9} ${yy+6}" transform="rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI} ${xx} ${yy})" fill="none" stroke="${color}" stroke-width="3"/>`;
const result=(markup,description)=>({markup,description});
const split=(m)=>m?line(25,334,365,334):line(600,55,600,505);
const panel=(i,m)=>({x:m?28:60+i*600,y:m?40+i*335:70,w:m?334:480});
function purpose(s,m){
 const w=m?390:1200,h=m?247:560;
 const o=`<image href="../assets/references/jensen-huang-tokens-per-watt.png" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/>`;
 return result(o,'Jensen Huang beside an AI factory revenue graphic showing a tokens-per-watt annotation. The supplied screenshot is shown in full.');}
function interactivity(s,m){const a=interactivityMetrics({tokensPerSecond:s.tokensPerSecond});let o='';
 const x=m?28:72,y=m?48:49;
 o+=t(x,y,'ONE USER',m?19:23,C.communication)+t(x,y+60,`${a.tokensPerSecond} tokens/s/user`,m?32:48,C.communication);
 const gx=m?28:72,gy=m?159:162,cols=m?20:40,cw=m?16:21,ch=m?14:26;
 for(let i=0;i<a.tokensPerSecond;i++)o+=r(gx+(i%cols)*cw,gy+Math.floor(i/cols)*(ch+5),cw-4,ch,C.communication,C.communication,2);
 o+=t(x,m?274:259,'Output tokens generated in one second',m?17:24,C.muted)+t(x,m?325:313,`${a.millisecondsPerToken} ms between tokens`,m?26:36);
 o+=line(m?28:72,m?365:354,m?361:1130,m?365:354);
 o+=t(x,m?412:405,'THROUGHPUT',m?19:23,C.compute)+t(x,m?455:449,'Tokens/s across all users',m?25:32,C.compute);
 return result(`<g data-tokens-per-user="${a.tokensPerSecond}" data-token-interval-ms="${a.millisecondsPerToken}">${o}</g>`,`Interactivity is output tokens per second per user. At ${a.tokensPerSecond} tokens per second, the average gap between tokens is ${a.millisecondsPerToken} milliseconds. Each block is an output token generated in one second. Throughput counts output tokens across all users. Batching can increase total throughput while slowing each answer. Time to first token is the separate initial wait.`);}
function frontier(s,m){const target=s.minInteractivity??100;let o='';
 const x=m?8:49,y=m?75:0,w=m?374:830,h=w*2/3;
 o+=`<image href="../assets/references/nvidia-gb300-interactivity.webp" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"><title>NVIDIA GB300 NVL72 Qwen3.8 performance, Figure 2, August 2026</title></image>`;
 // The original image is 1536 by 1024; its plot spans x=375..1394 for 0..350 TPS/user.
 const scale=w/1536,xx=x+(375+target/350*(1394-375))*scale,yt=y+244*scale,yb=y+817*scale;
 o+=line(xx,yt,xx,yb,C.communication,m?2:3,'7 5');
 const tx=m?28:905,ty=m?393:147;
 o+=t(tx,ty,'I WANT AT LEAST',m?17:19,C.muted)+t(tx,ty+45,`${target} tokens/s/user`,m?29:28,C.communication);
 o+=t(m?195:450,m?42:551,'NVIDIA · GB300 NVL72 · Qwen3.8 FP8 · Aug 2026',m?11:16,C.muted,'middle');
 return result(`<g data-min-interactivity="${target}">${o}</g>`,`NVIDIA’s original Qwen3.8-2.4T-A95B FP8 curve on GB300 NVL72, with 8k input and 1k output, TensorRT-LLM and multi-token prediction. Horizontal axis: tokens per second per user, or interactivity. Vertical axis: throughput in tokens per second per GPU. A dashed line marks the ${target} tokens per second per user requirement. Only the curve to its right meets the minimum. Higher interactivity corresponds to lower available throughput on this curve.`);}
function modelWork(s,m){let o=split(m);
 [['TRAINING','Learn parameters',['Forward pass → loss','Backward pass → gradients','Optimizer → updated weights'],['Training compute: FLOPs']],['INFERENCE','Produce tokens',['Prompt → prefill + KV cache','Decode → next output token','Scheduler → active requests'],['Throughput: tokens/s across all users','Per user: first-token + inter-token latency']]].forEach(([name,sub,steps,payoff],i)=>{const {x,y}=panel(i,m);o+=t(x,y,name,m?21:30,i?C.communication:C.compute)+t(x,y+42,sub,m?24:34);steps.forEach((v,j)=>o+=t(x,y+99+j*(m?38:54),v,m?18:25));o+=lines(x,y+(m?244:300),payoff,m?15:22,C.muted);});
 return result(o,'Training learns parameters through forward, backward and optimizer work. FLOPs count the floating-point operations in that computation. Inference uses configured parameters to prefill prompts and decode output tokens. Throughput counts tokens across all users; first-token and inter-token latency describe each user’s response.');}
function memoryCompare(s,m){let o=split(m);
 [['SERVING WEIGHTS','2 bytes / parameter','≈140 GB',['BF16 weights','Add KV cache + runtime workspace']],['FP16/FP32 ADAM STATE','16 bytes / parameter','≈1,120 GB',['FP16/FP32 · 2 weights + 2 gradients','+ 4 master + 8 moments; add activations']]].forEach(([a,b,c,d],i)=>{const {x,y}=panel(i,m);o+=t(x,y,a,m?20:27,i?C.checkpoint:C.compute)+t(x,y+44,'70B × '+b,m?18:27)+t(x,y+(m?115:145),c,m?45:64,i?C.checkpoint:C.compute)+lines(x,y+(m?166:219),d,m?15:22,C.muted,'start',m?30:37);});
 return result(o,'Rounded 70 billion parameters: serving BF16 weights use about 140 GB. A classic mixed-precision Adam account at 16 bytes per parameter uses about 1,120 GB of training state before activations and buffers. Optimizer, precision and partition choices can change it. Decimal GB.');}
function kv(s,m){let o='';
 o+=t(m?195:600,m?53:53,'One cached token in Llama 3.1 70B',m?22:31,C.ink,'middle');
 const cols=m?2:5,items=[['2','K + V'],['80','layers'],['8','KV heads'],['128','head width'],['2 B','BF16 element']];
 items.forEach(([a,b],i)=>{const x=m?35+(i%2)*174:74+i*219,y=m?99+Math.floor(i/2)*121:130;o+=t(x,y,a,m?39:56,C.compute)+t(x,y+36,b,m?17:22,C.muted);if(!m&&i<4)o+=t(x+151,y,'×',30,C.muted);});
 o+=t(m?195:600,m?494:314,'327,680 bytes = 320 KiB / token',m?22:40,C.compute,'middle')+t(m?195:600,m?563:399,'KV memory = cached tokens × 320 KiB',m?18:28,C.ink,'middle')+t(m?195:600,m?623:482,'Excludes block overhead',m?16:20,C.muted,'middle');
 return result(o,'Two K and V vectors times 80 layers times eight KV heads times 128 elements times two bytes equals 327,680 bytes, or 320 KiB, per cached token. Multiply by all cached context tokens in every active request.');}
function context(s,m){let o='';
 o+=t(m?195:55,m?33:51,'Llama 3.1 70B',m?24:29,C.ink,m?'middle':'start')+t(m?195:55,m?66:86,'64 GiB allocated to KV cache',m?18:22,C.muted,m?'middle':'start');
 [8192,32768].forEach((tokens,i)=>{const a=llamaMemory({contextTokens:tokens}),x=m?22+i*190:55,y=m?121:163+i*193;
  o+=t(x,y,n(tokens)+' tokens',m?21:29)+t(x,y+(m?38:43),`${a.requestGiB} GiB / request`,m?17:25,C.communication)+t(x,y+(m?82:97),`${a.concurrentRequests} requests`,m?24:35,C.compute);
 });
 if(m)o+=line(22,244,368,244);else o+=line(484,30,484,515);
 o+=`<image href="../assets/references/deepseek-kv-cache.png" x="${m?12:525}" y="${m?302:26}" width="${m?366:636}" height="${m?285:495}" preserveAspectRatio="xMidYMid meet"><title>DeepSeek V4 report: accumulated KV cache versus sequence length for V3.2, V4-Pro and V4-Flash</title></image>`;
 o+=t(m?195:843,m?280:549,'DeepSeek V4 · compressed attention',m?17:21,C.muted,'middle');
 return result(o,'For Llama 3.1 70B at BF16, a 64 GiB KV pool holds 25 requests with 8,192 cached tokens each or six with 32,768, using 2.5 or 10 GiB per request. The supplied DeepSeek report chart separately compares V4-Pro and V4-Flash compressed-attention KV state with V3.2 as sequence length grows. Its model architectures and KV storage differ from the Llama calculation.');}
function prefill(s,m){let o=split(m);
 [['PREFILL','Process the prompt',['Many prompt tokens in parallel','Large matrix operations'],'Usually compute-bound','Time to first token'],['DECODE','Stream the answer',['Read weights + cached context','Generate the next token'],'Often memory-bandwidth-bound','Time between output tokens']].forEach(([a,b,c,bound,d],i)=>{const {x,y}=panel(i,m);o+=t(x,y,a,m?23:31,i?C.communication:C.compute)+t(x,y+49,b,m?26:38)+lines(x,y+108,c,m?18:25,C.ink,'start',m?35:49)+t(x,y+(m?193:234),bound,m?19:27,i?C.communication:C.compute)+t(x,y+(m?240:300),d,m?17:25,C.muted);});return result(o,'Prefill processes many prompt tokens together, forming large matrix operations that are usually compute-bound. Decode repeatedly reads weights and cached context to extend the answer and is often memory-bandwidth-bound, especially at low batch sizes. The first phase affects the wait for an answer; the second affects how quickly it streams.');}
function disaggregated(s,m){let o='';
 const photo='../assets/references/nvidia-groq-3-lpx.webp';
 o+=`<image href="${photo}" x="${m?18:30}" y="${m?4:82}" width="${m?354:565}" height="${m?199:318}" preserveAspectRatio="xMidYMid meet"><title>NVIDIA Groq 3 LPX official product render</title></image>`;
 o+=t(m?195:310,m?228:449,'NVIDIA Groq 3 LPX',m?22:29,C.ink,'middle')+t(m?195:310,m?255:480,'NVIDIA product render',m?12:17,C.muted,'middle');
 const x=m?30:657,y=m?313:65;
 o+=t(x,y,'PREFILL',m?17:20,C.compute)+t(x,y+38,'Vera Rubin NVL72',m?28:35)+t(x,y+75,'GPUs process the prompt',m?19:25);
 o+=arrow(x+20,y+103,x+20,y+160,C.communication)+t(x+43,y+138,'Transfer the KV cache',m?18:23,C.communication);
 o+=t(x,y+204,'DECODE',m?17:20,C.communication)+t(x,y+242,'Groq 3 LPX',m?28:35)+t(x,y+279,'LPUs stream the answer',m?19:25)+t(x,y+315,'Fast SRAM feeds token generation',m?16:23,C.muted);
 return result(o,'NVIDIA Groq 3 LPX product render. In NVIDIA’s standard prefill–decode configuration, Vera Rubin NVL72 GPUs process the prompt and transfer the KV cache to the separate Groq 3 LPX rack. SRAM-based Groq LPUs generate the answer tokens. These are two rack platforms connected by the state handoff.');}
function continuous(s,m){
 let o=`<image href="../assets/generated/batching-bus.png" x="${m?20:380}" y="0" width="${m?350:440}" height="${m?175:220}" preserveAspectRatio="xMidYMid meet"><title>A city bus, used as a visual cue for the batching analogy</title></image>`;
 o+=m?line(24,409,366,409):line(600,264,600,535);
 [false,true].forEach((policy,i)=>{const a=decodeSlots(policy),x=m?28:60+i*600,y=m?208+i*224:275,gx=x+(m?52:58),cell=m?33:47,rowStep=m?42:50;
  o+=t(x,y,policy?'CONTINUOUS BATCH':'FIXED BATCH',m?20:27,policy?C.communication:C.compute)+t(x,y+(m?28:36),policy?'C fills A’s released slot':'C waits for the batch',m?17:23,C.muted);
  a.rows.forEach((row,j)=>{const yy=y+(m?47:60)+j*rowStep;o+=t(x,yy+25,`Slot ${j+1}`,m?13:17,C.muted);row.forEach((job,k)=>{const xx=gx+k*cell,col=job==='A'?C.compute:job==='B'?C.communication:job==='C'?C.checkpoint:C.panel;o+=r(xx,yy,cell-4,m?34:39,col,col,4);if(job)o+=t(xx+(cell-4)/2,yy+25,job,m?18:23,C.paper,'middle');});});
  for(let k=0;k<8;k++)o+=t(gx+k*cell+(cell-4)/2,y+(m?151:180),k+1,m?12:16,C.muted,'middle');
  o+=t(x,y+(m?183:223),'Decode iterations',m?15:21,C.muted);
 });
 return result(o,'A bus accompanies the batching analogy. Two decode slots: A needs two steps, B five and queued C three. The fixed batch starts C only after B finishes. Continuous batching starts C in the released slot while B continues. The numbered columns show decode iterations.');}
function energy(s,m){const a=sameWorkEnergy();let o='';const x=m?25:92,w=m?340:1016,col1=x+(m?177:556),col2=x+(m?267:826);
 o+=t(x,m?43:53,'Same completed tokens and quality',m?22:32)+t(col1,m?115:135,'Run A',m?22:29,C.compute,'middle')+t(col2,m?115:135,'Run B',m?22:29,C.communication,'middle');
 [['Mean power',`${a.runA.powerKW} kW`,`${a.runB.powerKW} kW`],['Time to finish',`${a.runA.minutes} min`,`${a.runB.minutes} min`],['Total energy',`${n(a.runA.energyKWh,1)} kWh`,`${a.runB.energyKWh} kWh`]].forEach(([name,av,bv],i)=>{const y=(m?181:211)+i*91;o+=line(x,y+30,x+w,y+30)+t(x,y,name,m?18:28)+t(col1,y,av,m?23:39,C.compute,'middle')+t(col2,y,bv,m?23:39,i===2?C.checkpoint:C.communication,'middle');});
 o+=t(m?195:600,m?523:504,'Five extra minutes → 20% more energy',m?21:31,C.checkpoint,'middle');
 return result(o,'Run A completes the token workload in ten minutes at a mean 100 kW, using 16.7 kWh. Run B completes the same work and quality in fifteen minutes at 80 kW, using 20 kWh. The extra five minutes outweigh the lower power: total energy rises 20 percent.');}
function resource(s,m){let o=''; const x=m?77:240,w=m?280:870,top=m?113:120,row=m?107:96;
 ['GPU group A','GPU group B','GPU group C'].forEach((name,i)=>{const y=top+i*row;o+=t(m?24:66,y-18,name,m?17:25);o+=r(x,y,w*.48,42,C.compute,C.compute,0)+r(x+w*.48,y,w*.28,42,C.checkpoint,C.checkpoint,0)+r(x+w*.76,y,w*.24,42,C.communication,C.communication,0);});
 o+=t(x+w*.24,m?485:443,'Compute',m?16:23,C.compute,'middle')+t(x+w*.62,m?522:443,'Exchange / wait',m?16:23,C.checkpoint,'middle')+t(x+w*.88,m?559:443,'Next step',m?15:23,C.communication,'middle')+line(x+w*.76,top-36,x+w*.76,top+2*row+52,C.muted,2,'5 5');o+=t(m?195:600,m?635:521,'Less compute during the exchange → lower GPU power',m?13:23,C.muted,'middle');return result(o,'Three training groups compute, participate in or wait for a required exchange, then begin the next dependent step. The shared dependency can expose a low-compute period. Align collective timings, GPU activity, storage events and power to diagnose the stall.');}
function evidence(s,m){let o='';const src='https://arxiv.org/html/2508.14318v1/Fig1.svg';o+=r(m?14:40,m?94:79,m?362:1120,m?234:374,'white','white',0)+`<image href="${src}" x="${m?14:40}" y="${m?94:79}" width="${m?362:1120}" height="${m?234:374}" preserveAspectRatio="xMidYMid meet"><title>Figure 1: power readings from an at-scale training job on DGX-H100 racks, Choukse et al., 2025</title></image>`;o+=t(m?195:600,m?420:494,'DGX-H100 production training · normalized power',m?16:25,C.ink,'middle')+t(m?195:600,m?479:535,'Choukse et al. (2025), Fig. 1 · Microsoft / OpenAI / NVIDIA',m?11:18,C.muted,'middle')+t(195,m?549:580,m?'Read peaks, cycle rhythm and transition speed.':'',m?14:19,C.muted,'middle');return result(o,'Published Figure 1 shows normalized production training power from DGX-H100 racks over time. The curve shows repeated power swings during synchronized training work.');}
function phaseVisual(id,s,m){
 const single=id==='job-phases',staggered=id==='staggering-jobs',offsets=single?[0]:staggered?[0,15,30,45]:[0,0,0,0],a=phaseSchedule({offsetsSeconds:offsets});let o='';
 const x=m?62:157,w=m?296:960,sc=w/60,top=m?104:85,row=single?(m?99:78):(m?49:47);
 const names={compute:'compute',communication:'exchange',checkpoint:'save'};
 for(let j=0;j<offsets.length;j++){
 const y=top+j*row;o+=t(m?8:35,y+25,single?'Group':`G${j+1}`,m?17:23,C.ink);
 for(const seg of a.segments){const ph=seg.jobPhases[j],xx=x+seg.startSeconds*sc,ww=(seg.endSeconds-seg.startSeconds)*sc;o+=r(xx,y,ww,row-8,C[ph.kind],C[ph.kind],0);if(ww>(m?65:100))o+=t(xx+ww/2,y+(row-8)/2+6,m?(ph.kind==='compute'?'C':ph.kind==='communication'?'↔':'S'):names[ph.kind],m?16:21,C.paper,'middle');}
 }
 const gy=single?(m?272:233):(m?370:322),gh=single?(m?196:184):(m?130:143),max=single?140:520,py=power=>gy+gh-power/max*gh;
 o+=line(x,gy+gh,x+w,gy+gh);
 let d='';for(const seg of a.segments){const xx=x+seg.startSeconds*sc,xe=x+seg.endSeconds*sc,yy=py(seg.powerKW);d+=(d?'L':'M')+xx+' '+yy+'H'+xe;}
 o+=`<path d="${d}" fill="none" stroke="${C.compute}" stroke-width="5"/>`;
 const avgY=py(a.averageKW);o+=line(x,avgY,x+w,avgY,C.muted,2,'6 5');
 a.segments.forEach(seg=>{const yy=py(seg.powerKW),xx=x+(seg.startSeconds+seg.endSeconds)/2*sc;o+=t(xx,yy-12,String(seg.powerKW),m?20:28,C.compute,'middle');});
 [0,30,45,60].forEach(v=>o+=t(x+v*sc,gy+gh+29,`${v}${v===60?' s':''}`,m?15:21,C.muted,'middle'));
 o+=t(x+w,avgY+(staggered?28:-25),`${n(a.averageKW)} kW mean`,m?16:22,C.muted,'end');
 if(!staggered)o+=line(x+w,avgY-18,x+w,avgY,C.muted,1);
 if(m)o+=t(195,single?232:317,'C compute · ↔ exchange · S checkpoint',16,C.muted,'middle');
 if(!single)o+=t(x+w,m?574:530,`${n(a.energyKWh,3)} kWh / 60 s cycle`,m?19:25,C.ink,'end');
 return {markup:`<g data-peak-kw="${a.peakKW}" data-average-kw="${a.averageKW}" data-energy-kwh="${a.energyKWh}" data-schedule="${staggered?'staggered':'sync'}">${o}</g>`,description:`${single?'One job':'Four '+(staggered?'independent jobs offset by fifteen seconds':'synchronized jobs')} has power plateaus ${a.segments.map(seg=>seg.powerKW).join(', ')} kW; peak ${a.peakKW} kW and mean ${n(a.averageKW)} kW. Energy is ${n(a.energyKWh,3)} kWh per sixty-second cycle. ${staggered?'At every instant two compute, one exchanges and one checkpoints. This requires independence, no contention and periodic steady operation.':''}`};
}
function nextBrief(s,m){
 const image='../assets/generated/workload-handoff.png';
 const trace='<path d="M566 582H973M566 582V373" fill="none" stroke="#667e81" stroke-width="3"/><path d="M566 474H608V405H716V550H768V511H820V405H925V550H973" fill="none" stroke="#086e83" stroke-width="7"/><text x="576" y="367" fill="#193139" font-size="24">P(t)</text><text x="973" y="611" text-anchor="end" fill="#193139" font-size="24">Time</text>';
 const art=`<image href="${image}" width="1672" height="941"/>${trace}`;
 let o='';
 if(m){
  const views=[['Workload','Model · context · token service','0 95 505 700'],['Power trace','Peak · energy · transition speed','505 250 580 450'],['Supply','Grid · generation · local storage','1080 165 592 620']];
  views.forEach(([heading,detail,view],i)=>{const y=i*220,[,,vw,vh]=view.split(' ').map(Number),scale=Math.min(235/vw,167/vh),w=vw*scale,h=vh*scale;const figure=`<image href="${image}" width="1672" height="941"/>${i===1?trace:''}`;o+=t(24,y+25,heading,23)+`<svg x="${130+(235-w)/2}" y="${y+8}" width="${w}" height="${h}" viewBox="${view}" overflow="hidden">${figure}</svg>`+t(24,y+198,detail,15,C.muted);if(i<2)o+=line(24,y+216,365,y+216);});
 }else{
  o+=`<svg x="30" y="68" width="1140" height="400" viewBox="0 100 1672 720" preserveAspectRatio="xMidYMid meet">${art}</svg>`;
  [['Workload','Model · context · token service',225],['Power trace','Peak · energy · transition speed',600],['Supply','Grid · generation · local storage',987]].forEach(([a,b,x])=>{o+=t(x,43,a,29,C.ink,'middle')+t(x,520,b,20,C.muted,'middle');});
 }
 return result(o,'A generic workload rack, a schematic power trace and supply equipment form a visual handoff. Define the model, context and token service; measure peak demand, energy and transition speed; use those measurements to design grid, generation and local storage. ');
}

export function renderWorkload(id,state,compact=false){
 const f={'workload-purpose':purpose,'interactivity':interactivity,'serving-frontier':frontier,'model-work':modelWork,'memory-comparison':memoryCompare,'kv-cache':kv,'context-capacity':context,'prefill-decode':prefill,'disaggregated-serving':disaggregated,'continuous-batching':continuous,'energy-per-result':energy,'resource-paths':resource,'training-power-evidence':evidence,'next-brief':nextBrief}[id];
 const rendered=f?f(state,compact):['job-phases','synchronized-jobs','staggering-jobs'].includes(id)?phaseVisual(id,state,compact):null;
 if(!rendered)throw new RangeError(`Unknown workload scene: ${id}`);return rendered;
}
