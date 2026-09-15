const ink='var(--text)', power='var(--power)', measurement='var(--heat)', trip='var(--data)', muted='var(--muted)';
const text=(x,y,label,size=22,color=ink)=>`<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}">${label}</text>`;
const path=(d,color=power,width=5)=>`<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round"/>`;
const box=(x,y,w,h,color='var(--line)')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="var(--surface)" stroke="${color}" stroke-width="2"/>`;
const circle=(x,y,r,color=measurement)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="${color}" stroke-width="4"/>`;
const signal=(d,command=false)=>`<path d="${d}" fill="none" stroke="${command?trip:measurement}" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round" marker-end="url(#instrument-${command?'trip':'measurement'})"/>`;
const earth=(x,y)=>path(`M${x} ${y}v14m-20 0h40m-33 9h26m-20 9h14`,power,3);
const contact=(x,y,open=false,color=power)=>path(`M${x-40} ${y}L${x+(open?25:40)} ${y-(open?28:0)}`,color,5)+`<circle cx="${x-40}" cy="${y}" r="4" fill="${color}"/><circle cx="${x+40}" cy="${y}" r="4" fill="${color}"/>`;
const markers=`<defs>${[['measurement',measurement],['trip',trip]].map(([id,color])=>`<marker id="instrument-${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9Z" fill="${color}"/></marker>`).join('')}</defs>`;
const figure=(body,description,m,height)=>`<svg class="mechanism equipment-system" viewBox="0 0 ${m?390:1120} ${height}" role="img" aria-label="${description}">${markers}${body}</svg>`;

export function relayProtection(state,m){
 if(state.faultStage==='measurements')return highVoltageMeasurements(m);
 const fault=state.faultStage!=='normal',cleared=state.faultStage==='cleared';
 const upstream=fault&&!cleared?measurement:power,downstream=cleared?muted:upstream;
 const relayState=fault?'Trip command sent':'Monitoring current';
 const breakerState=cleared?'Open':fault?'Trip received':'Closed';
 const description=`A current transformer (CT) surrounds the feeder conductor and sends a scaled current measurement to the protection relay. A separate trip signal connects the relay to the circuit breaker. ${cleared?'The breaker has opened and interrupted the fault current; its supply side remains energized.':fault?'The relay has detected the fault and sent a trip command, but the breaker contacts have not yet separated.':'The breaker is closed and the feeder supplies the load.'}`;
 if(m){
  let body=text(80,32,'Supply',21)+path('M80 51V155',upstream,6)+circle(80,180,25)+path('M80 155V345',upstream,6);
  body+=text(240,139,'Current transformer',18)+text(240,164,'(CT)',18);
  body+=signal('M105 180H287V225')+text(180,206,'Scaled current',16,measurement);
  body+=box(197,225,180,85,measurement)+text(287,258,'Protection relay',19)+text(287,286,relayState,16,muted);
  body+=box(26,345,108,110)+path('M80 345V365',upstream,6)+`<g transform="translate(80 405) rotate(90)">${contact(0,0,cleared,downstream)}</g>`+path('M80 445V541',downstream,6);
  body+=signal('M287 310H350V400H134',true)+text(286,383,'Trip',19,trip);
  body+=text(254,443,'Circuit breaker',21)+text(254,470,breakerState,18,cleared?muted:power);
  body+=text(80,572,fault?'Faulted feeder':'Load',20,cleared?muted:ink);
  return figure(body,description,m,590);
 }
 let body=path('M45 280H720',upstream,7)+path('M900 280H1080',downstream,7);
 body+=circle(230,280,28)+text(230,351,'Current transformer',23)+text(230,383,'(CT)',22);
 body+=signal('M230 252V130H390')+text(306,111,'Scaled current',18,measurement);
 body+=box(390,85,280,88,measurement)+text(530,121,'Protection relay',25)+text(530,151,relayState,18,muted);
 body+=box(720,215,180,128)+text(810,242,'Circuit breaker',22)+path('M720 280H770',upstream,7)+contact(810,280,cleared,downstream)+path('M850 280H900',downstream,7);
 body+=signal('M670 130H810V215',true)+text(741,111,'Trip',20,trip);
 body+=text(85,322,'Supply',22)+text(1012,322,fault?'Faulted feeder':'Load',22,cleared?muted:ink)+text(810,384,breakerState,23,cleared?muted:power);
 return figure(body,description,m,440);
}

function highVoltageMeasurements(m){
 const description='At a 345 kV connection, the phase conductor passes through a current transformer (CT). A capacitor voltage transformer (CVT) connects in parallel from the phase to earth. Separate scaled current and voltage signals reach the protection relay; a different trip signal commands the circuit breaker. These instrument transformers measure the high-voltage circuit.';
 if(m){
  let body=text(195,28,'345 kV connection',24,power)+path('M35 145H240M340 145H360',power,6);
  body+=circle(80,145,24)+text(80,70,'Current transformer',16)+text(80,95,'(CT)',17);
  body+=box(240,111,100,78)+path('M240 145H250M330 145H340',power,6)+contact(290,145)+text(290,70,'Circuit breaker',18);
  body+=path('M180 145V250',power,5)+`<circle cx="180" cy="145" r="5" fill="${power}"/>`+box(140,250,80,100,power)+text(180,307,'CVT',23,power)+earth(180,350);
  body+=text(195,407,'Capacitor voltage',18)+text(195,429,'transformer (CVT)',18);
  body+=signal('M80 121V112H20V470H155V515')+text(111,454,'Scaled current',16,measurement);
  body+=signal('M220 300H360V489H265V515')+text(279,474,'Scaled voltage',16,measurement);
  body+=box(100,515,200,90,measurement)+text(200,554,'Protection relay',22)+text(200,581,'Current + voltage',17,muted);
  body+=signal('M300 560H378V211H290V189',true)+text(325,237,'Trip',18,trip);
  return figure(body,description,m,630);
 }
 let body=text(560,31,'345 kV connection',27,power)+path('M45 145H650M860 145H1080',power,7);
 body+=circle(250,145,28)+text(250,85,'Current transformer (CT)',22);
 body+=box(650,93,210,121)+text(755,76,'Circuit breaker',23)+path('M650 145H715M795 145H860',power,7)+contact(755,145);
 body+=path('M490 145V280',power,6)+`<circle cx="490" cy="145" r="5" fill="${power}"/>`+box(440,280,100,100,power)+text(490,337,'CVT',25,power)+earth(490,380);
 body+=text(675,384,'Capacitor voltage',22)+text(675,413,'transformer (CVT)',22);
 body+=signal('M250 173V470H950V385')+text(701,454,'Scaled current',20,measurement);
 body+=signal('M540 330H830')+text(683,312,'Scaled voltage',20,measurement);
 body+=box(830,285,240,100,measurement)+text(950,328,'Protection relay',25)+text(950,357,'Current + voltage',19,muted);
 body+=signal('M950 285V234H755V214',true)+text(870,216,'Trip',21,trip);
 return figure(body,description,m,505);
}
