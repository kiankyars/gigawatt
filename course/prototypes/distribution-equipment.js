const ink='var(--text)', teal='var(--power)', orange='var(--heat)', muted='var(--muted)';
const tx=(x,y,t,size=22,color=ink)=>`<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}">${t}</text>`;
const ln=(d,color=teal,w=5,dash=false)=>`<path d="${d}" stroke="${color}" stroke-width="${w}" fill="none" stroke-linecap="round" ${dash?'stroke-dasharray="8 7"':''}/>`;
const panel=(x,y,w,h,stroke='var(--line)')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="var(--surface)" stroke="${stroke}" stroke-width="2"/>`;
const svg=(o,alt,h=460)=>`<svg class="mechanism equipment-diagram" viewBox="0 0 1120 ${h}" role="img" aria-label="${alt}">${o}</svg>`;
export function equipment(id,s,m){
 if(id==='switchgear-anatomy'){
  let o=panel(150,15,820,420)+tx(560,53,'Feeder switchgear',26);
  o+=ln('M195 105H925',teal,11)+tx(560,92,'Shared bus',19);
  o+=ln('M390 105V185')+panel(325,185,130,85,teal)+tx(390,220,'Circuit',22)+tx(390,250,'breaker',22)+ln('M390 270V400');
  o+=`<circle cx="390" cy="325" r="26" fill="var(--surface)" stroke="${orange}" stroke-width="6"/>`+ln('M390 299V351');
  o+=ln('M416 325H665V262',orange,3,true)+panel(605,180,260,82,orange)+tx(735,214,'Protection relay',24)+tx(735,244,'Evaluates measurements',16,muted);
  o+=ln('M605 215H485V226H455',orange,3,true)+tx(530,198,'Trip',16,orange);
  o+=tx(680,378,'Current transformer',21)+tx(680,406,'Measures feeder current',17,muted)+tx(390,427,'Outgoing feeder',19);
  return svg(o,'A shared bus feeds a circuit breaker and outgoing feeder. A current transformer sends a measurement to a protection relay, which sends a separate trip signal to the breaker.');
 }
 if(id==='protection-relay'){
  const fault=s.faultStage!=='normal',clear=s.faultStage==='cleared';
  let o=tx(560,40,clear?'Fault current interrupted':fault?'Fault current detected':'Feeder supplying its load',28);
  o+=ln('M65 270H470',fault&&!clear?orange:teal,7)+ln('M650 270H1050',clear?muted:fault?orange:teal,7);
  o+=panel(435,190,250,128)+tx(560,225,'Circuit breaker',21)+ln('M435 270H470',fault&&!clear?orange:teal,7)+ln('M650 270H685',clear?muted:fault?orange:teal,7);
  o+=ln(`M470 270L650 ${clear?240:270}`,clear?muted:fault?orange:teal,6)+`<circle cx="470" cy="270" r="5" fill="${teal}"/><circle cx="650" cy="270" r="5" fill="${clear?muted:fault?orange:teal}"/>`;
  o+=`<circle cx="280" cy="270" r="27" fill="none" stroke="${orange}" stroke-width="5"/>`;
  o+=panel(420,72,280,75,orange)+tx(560,104,'Protection relay',24)+tx(560,134,fault?'Trip command issued':'Monitoring current',17,muted);
  o+=ln('M280 243V111H420',orange,3,true)+ln('M560 147V190',orange,3,true);
  o+=tx(165,315,'Supply',22)+tx(208,197,'Sensor',17)+tx(935,315,fault?'Faulted feeder':'Load',22);
  o+=tx(560,410,clear?'The supply side remains energized':fault?'The command and physical interruption are separate events':'Measurements and trip signals are separate from the power path',22);
  return svg(o,'A current sensor informs the relay. The relay sends a trip signal; the breaker then opens its contacts and extinguishes the arc. A trip command alone does not establish that current has stopped.');
 }
 if(id==='isolation-surge'){
  return `<div class="device-comparison"><article><h2>Disconnector</h2><svg viewBox="0 0 480 230" role="img" aria-label="An isolating gap in a power conductor">${ln('M35 135H170 M305 135H445',muted,7)+ln('M170 135L278 66',teal,7)+tx(240,215,'Isolation gap',24)}</svg><p>Separates equipment for isolation.</p><small>Plain disconnector: no fault-breaking duty.</small></article><article><h2>Surge arrester</h2><svg viewBox="0 0 480 230" role="img" aria-label="A surge arrester connects in parallel from the phase conductor to earth">${ln('M35 45H445')+ln('M240 45V85',orange)+panel(210,85,60,65,orange)+ln('M240 150V182 M210 182H270 M220 195H260 M230 208H250',orange,4)+tx(122,121,'Surge',22,orange)+tx(385,48,'Load',20)}</svg><p>Limits transient overvoltage.</p><small>Diverts surge current to protect insulation.</small></article></div>`;
 }
 if(id==='phase-loading'){
  const allocation=s.balanced?[2,2,2]:[4,1,1];
  if(m)return `<div class="phase-cards">${allocation.map((count,i)=>`<article><h2>L${i+1} → neutral</h2><div class="phase-loads">${Array(count).fill('<span>PSU group<br>20 A</span>').join('')}</div><strong class="${count*20>60?'warm':''}">${count*20} A / 60 A</strong></article>`).join('')}</div><p class="inputs">Each group: 277 V phase-to-neutral · 20 A<br>Six groups total in either allocation</p>`;
  let o=tx(560,32,'Each single-phase PSU group draws 20 A at 277 V',25);
  allocation.forEach((count,i)=>{
   const y=110+i*125;
   o+=tx(75,y+8,`L${i+1}`,24)+ln(`M110 ${y}H930`,count*20>60?orange:teal,5);
   for(let j=0;j<count;j++){const x=280+j*160;o+=ln(`M${x} ${y}V${y+22}`,teal,3)+panel(x-60,y+22,120,50)+tx(x,y+53,'20 A',22)+ln(`M${x} ${y+72}V${y+88}H1000`,muted,2);}
   o+=tx(1030,y+8,`${count*20} A`,27,count*20>60?orange:teal);
  });
  o+=ln('M1000 198V455H1080',muted,3)+tx(1072,480,'N',20,muted)+tx(560,492,'60 A limit per phase · same six loads',23);
  return svg(o,'Six phase-to-neutral load groups each draw 20 amps. Two per phase gives 40/40/40 A; four/one/one gives 80/20/20 A and exceeds the 60 A limit on L1. Gray return paths join neutral.',515);
 }
 if(id==='feeder-diagnosis'){
  let o=`<div class="fault-evidence"><div><span>Relay event log</span><strong>TRIP issued</strong></div><div><span>Breaker indication</span><strong>Closed</strong></div><div><span>Current sensor</span><strong>Fault persists</strong></div></div>`;
  if(s.reveal)o+=`<div class="diagnosis-result"><h2>${s.diagnosis==='breaker'?'The feeder breaker has not cleared the fault.':s.diagnosis==='capacity'?'More campus capacity cannot clear this fault.':'A surge arrester cannot open this feeder.'}</h2><p>Backup protection may open an upstream breaker.</p><p class="inputs">That can remove supply from healthy branches too.</p></div>`;
  else o+=`<p class="prediction">What does this evidence identify?</p>`;
  return o;
 }
 throw new RangeError(`Unknown equipment scene: ${id}`);
}
