/* Physical water circuits for the reader's stipulated 84 kW example.
 * Warm/cool colours indicate temperature within each loop, not different fluids.
 * Direction is also carried by arrowheads and moving dashes; motion is optional.
 */
const labels=['Collect','Transfer','Release','Return'];
const text=(x,y,value,cls='',anchor='middle')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${value}</text>`;
const group=(active,body)=>`<g class="h-water-part${active?' is-active':''}">${body}</g>`;
const pipe=(d,kind='warm',active=false)=>`<path d="${d}" class="h-water-pipe h-water-${kind}"/>${active?`<path d="${d}" class="h-water-motion"/>`:''}`;
const arrow=(x,y,dir,kind='warm')=>`<path d="M-7 -5L1 0L-7 5" transform="translate(${x} ${y}) rotate(${dir})" class="h-water-arrow h-water-${kind}"/>`;
const pump=(x,y,vertical=false)=>`<g transform="translate(${x} ${y})${vertical?' rotate(90)':''}"><circle r="12" class="h-water-pump"/><path d="M5 -7L-7 0L5 7Z" class="h-water-pump-blade"/></g>`;
const defs=`<defs><pattern id="h-tower-fill" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M0 0L14 14M-7 7L7 21M7 -7L21 7" class="h-water-fin"/></pattern></defs>`;
function exchanger(x,y,name,active,vertical=false){
  const shape=vertical
    ? `<rect x="${x-83}" y="${y-47}" width="166" height="94" rx="10" class="h-water-shell"/><path d="M${x-70} ${y}H${x+70}" class="h-water-divider"/>${pipe(`M${x+60} ${y-25}H${x-60}`,'warm',active)}${pipe(`M${x-60} ${y+25}H${x+60}`,'cool',active)}${arrow(x-25,y-25,180)}${arrow(x+25,y+25,0,'cool')}${text(x+110,y+7,'↓','h-water-heat')}`
    : `<rect x="${x-48}" y="${y-87}" width="96" height="174" rx="10" class="h-water-shell"/><path d="M${x} ${y-72}V${y+72}" class="h-water-divider"/>${pipe(`M${x-25} ${y-60}V${y+60}`,'warm',active)}${pipe(`M${x+25} ${y+60}V${y-60}`,'cool',active)}${arrow(x-25,y+20,90)}${arrow(x+25,y-20,270,'cool')}${text(x,y+7,'→','h-water-heat')}`;
  return group(active,shape)+text(x,vertical?y-64:y-111,name,'h-water-equipment')+text(x,vertical?y+75:y+114,'Separate channels','h-water-small');
}
function rack(x,y,active,vertical=false){
  return group(active,`<rect x="${x-62}" y="${y-88}" width="124" height="176" rx="9" class="h-water-shell"/>${[-56,-11,34].map(offset=>`<rect x="${x-46}" y="${y+offset}" width="69" height="31" rx="3" class="h-water-server"/><circle cx="${x-35}" cy="${y+offset+15}" r="3" class="h-water-chip"/>`).join('')}${vertical?pipe(`M${x-35} ${y+48}V${y-55}H${x+35}V${y+48}`,'warm',active):pipe(`M${x+35} ${y+60}V${y-60}`,'warm',active)}${text(x-11,y+6,'→','h-water-heat')}`)+text(x,y-111,'Rack','h-water-equipment');
}
function dryCooler(x,y,active,vertical=false){
  const coil=vertical?`M${x+60} ${y-65}V${y-20}H${x-48}Q${x-64} ${y-20} ${x-64} ${y-4}T${x-48} ${y+12}H${x+48}Q${x+64} ${y+12} ${x+64} ${y+28}T${x+48} ${y+44}H${x-60}V${y-65}`:`M${x-76} ${y-60}H${x+56}Q${x+73} ${y-60} ${x+73} ${y-40}T${x+56} ${y-20}H${x-53}Q${x-70} ${y-20} ${x-70} ${y}T${x-53} ${y+20}H${x+56}Q${x+73} ${y+20} ${x+73} ${y+40}T${x+56} ${y+60}H${x-76}`;
  return group(active,`<rect x="${x-96}" y="${y-85}" width="192" height="170" rx="10" class="h-water-shell"/>${Array.from({length:10},(_,i)=>`<path d="M${x-65+i*14} ${y-69}V${y+69}" class="h-water-fin"/>`).join('')}${[-32,32].map(dx=>`${pipe(`M${x+dx} ${y+75}V${y-78}`,'air',active)}${arrow(x+dx,y-78,270,'air')}`).join('')}${pipe(coil,'warm',active)}<circle cx="${x}" cy="${y-115}" r="20" class="h-water-fan"/><path d="M${x-16} ${y-115}H${x+16}M${x} ${y-131}V${y-99}" class="h-water-fin"/>${text(x,y-151,'Heat to air ↑','h-water-air-label')}`)+text(x,y+115,'Sealed coil','h-water-equipment')+text(x,y+143,'Water inside · air outside','h-water-small');
}
function tower(x,y,active,makeup=false){
  return group(active,`<path d="M${x-102} ${y+100}V${y-86}L${x-49} ${y-113}H${x+49}L${x+102} ${y-86}V${y+100}Z" class="h-water-shell"/><rect x="${x-80}" y="${y-15}" width="160" height="67" fill="url(#h-tower-fill)" class="h-water-fill"/><path d="M${x-101} ${y+71}Q${x-50} ${y+62} ${x} ${y+71}T${x+101} ${y+71}V${y+100}H${x-101}Z" class="h-water-basin"/>${pipe(`M${x-108} ${y-57}H${x+72}`,'warm',active)}${[-63,0,63].map(offset=>`<path d="M${x+offset-5} ${y-53}H${x+offset+5}L${x+offset} ${y-46}Z" class="h-water-nozzle"/>${pipe(`M${x+offset} ${y-36}V${y+59}`,'drops',active)}${arrow(x+offset,y+58,90,'cool')}`).join('')}${pipe(`M${x+146} ${y+52}H${x+91}M${x+38} ${y+35}V${y-95}M${x-27} ${y-88}V${y-153}`,'air',active)}${arrow(x+91,y+52,180,'air')}${arrow(x-27,y-153,270,'air')}<circle cx="${x}" cy="${y-120}" r="18" class="h-water-fan"/><path d="M${x-14} ${y-120}H${x+14}M${x} ${y-134}V${y-106}" class="h-water-fin"/>${text(x,y-170,'Heat + water vapour ↑','h-water-air-label')}${text(x,y+24,'Fill','h-water-small h-water-on-pipe')}${text(x,y+123,'Basin','h-water-small')}`)+group(makeup,`${pipe(`M${x+152} ${y+91}H${x+104}`,'cool',makeup)}${arrow(x+105,y+91,180,'cool')}${text(x+152,y+116,'Makeup','h-water-small')}`);
}
function temp(x,y,value,kind,show){return show?text(x,y,`${value}°C`,`h-water-temperature h-water-${kind}`):'';}
function desktop(wet,step,wb){
  const rackX=100,cdu=wet?355:470,hx=640,out=wet?1000:967,y=265;
  const active=(...steps)=>steps.includes(step),supply=wet?wb+13:45;
  let body=rack(rackX,y,active(0,3))+exchanger(cdu,y,'CDU',active(1,3));
  body+=group(active(0,1,3),`${pipe(`M135 205H${cdu-25}`,'warm',active(0,1))}${arrow((135+cdu-25)/2,205,0)}${pipe(`M${cdu-25} 325H135`,'cool',active(3))}${arrow((135+cdu-25)/2,325,180,'cool')}${pump((135+cdu-25)/2+48,325)}${temp((135+cdu-25)/2,188,supply+10,'warm',step===0||step===3)}${temp((135+cdu-25)/2,367,supply,'cool',step===3)}`);
  body+=text((135+cdu-25)/2,415,'Rack circuit','h-water-circuit');
  const target=wet?hx-25:out-76;
  body+=group(active(1,3),`${pipe(`M${cdu+25} 205H${target}`,'warm',active(1))}${arrow((cdu+25+target)/2,205,0)}${pipe(`M${target} 325H${cdu+25}`,'cool',active(3))}${arrow((cdu+25+target)/2,325,180,'cool')}${pump((cdu+25+target)/2+46,325)}${temp((cdu+25+target)/2,188,supply+5,'warm',step===1||step===3)}${temp((cdu+25+target)/2,367,supply-5,'cool',step===3)}`);
  body+=text((cdu+25+target)/2,415,'Facility circuit','h-water-circuit');
  if(wet){
    body+=exchanger(hx,y,'Heat exchanger',active(1,3))+tower(out,240,active(2,3),active(3));
    body+=group(active(1,2,3),`${pipe(`M${hx+25} 205H775V183H${out-108}`,'warm',active(1,2))}${arrow(831,183,0)}${pipe(`M${out-102} 325H${hx+25}`,'cool',active(3))}${arrow(795,325,180,'cool')}${pump(829,325)}${temp(785,166,wb+13,'warm',step===1||step===3)}${temp(775,367,wb+3,'cool',step===3)}`);
    body+=text(788,415,'Tower circuit','h-water-circuit')+text(1138,217,`${wb}°C wet bulb`,'h-water-air-reading')+text(1138,242,'Incoming air','h-water-small')+text(out,397,'Open tower','h-water-equipment');
  }else{
    body+=dryCooler(out,y,active(2,3))+text(out,56,'35°C dry bulb','h-water-air-reading')+text(out,81,'Incoming air','h-water-small');
  }
  return `<svg class="h-water-diagram" viewBox="0 0 ${wet?1230:1160} 450" role="img" aria-label="${wet?'Three separate water circuits: rack, facility and open tower. Warm water moves right, cooler water returns left. Air crosses exposed water in the fill; some water evaporates.':'Two separate water circuits: rack and facility. Warm water moves right, cooler water returns left. Facility water flows inside the dry cooler coil; outdoor air passes outside.'}">${defs}${body}</svg>`;
}
function mobile(wet,step,wb){
  const active=(...steps)=>steps.includes(step),supply=wet?wb+13:45,cy=335,hy=570,oy=wet?870:643;
  let body=`<g data-water-focus="collect">${rack(200,131,active(0,3),true)}</g><g data-water-focus="transfer">${exchanger(200,cy,'CDU',active(1,3),true)}</g>`;
  body+=group(active(0,1,3),`${pipe('M235 179H350V310H260','warm',active(0,1))}${arrow(350,246,90)}${pipe('M140 310H50V179H165','cool',active(3))}${arrow(50,244,270,'cool')}${pump(50,275,true)}${text(200,241,'Rack circuit','h-water-circuit')}${temp(346,173,supply+10,'warm',step===0||step===3)}${temp(60,173,supply,'cool',step===3)}`);
  const end=wet?hy-25:oy-65;
  body+=group(active(1,3),`${pipe(`M260 360H350V${end}H260`,'warm',active(1))}${arrow(350,445,90)}${pipe(`M140 ${end}H50V360H140`,'cool',active(3))}${arrow(50,445,270,'cool')}${pump(50,484,true)}${text(200,wet?477:449,'Facility circuit','h-water-circuit')}${temp(345,406,supply+5,'warm',step===1||step===3)}${temp(53,406,supply-5,'cool',step===3)}`);
  if(wet){
    body+=exchanger(200,hy,'Heat exchanger',active(1,3),true)+`<g data-water-focus="release">${tower(200,oy,active(2,3),active(3))}</g>`;
    body+=group(active(1,2,3),`${pipe(`M260 ${hy+25}H370V${oy-57}H92`,'warm',active(1,2))}${arrow(370,744,90)}${pipe(`M98 ${oy+85}H50V${hy+25}H140`,'cool',active(3))}${arrow(50,737,270,'cool')}${pump(50,810,true)}${text(200,669,'Tower circuit','h-water-circuit')}${temp(353,687,wb+13,'warm',step===1||step===3)}${temp(52,687,wb+3,'cool',step===3)}`);
    body+=text(200,1046,`${wb}°C wet bulb · incoming air`,'h-water-air-reading');
  }else{
    body+=`<g data-water-focus="release">${dryCooler(200,oy,active(2,3),true)}</g>`+text(200,843,'35°C dry bulb · incoming air','h-water-air-reading');
  }
  return `<svg class="h-water-diagram" viewBox="0 0 410 ${wet?1070:873}" role="img" aria-label="${wet?'Three separate circuits, arranged vertically: rack, facility and open tower.':'Two separate circuits, arranged vertically: rack and facility.'} Warm water moves down the right pipes; cooler water returns up the left pipes. Exchanger channels stay separate.">${defs}${body}</svg>`;
}
export function outdoorWaterVisual(id,state,compact=false){
  const wet=id==='approach-wet',step=wet?state.wetStep:state.interfaceStep,wb=state.humidity==='humid'?28:22;
  const supply=wet?wb+13:45,passes=supply<=35;
  const captions=wet?[
    'Chips warm the rack coolant.',
    'Heat crosses two exchangers. The three water circuits stay separate.',
    'Water falls over fill. Air takes heat; some water evaporates.',
    `Rack coolant supply ${supply}°C · ${passes?'meets':'exceeds'} the 35°C coolant limit.`,
  ]:[
    'Chips warm the rack coolant.',
    'The CDU passes heat into a separate facility-water circuit.',
    'Air passes outside the coil. Water stays inside.',
    'Rack coolant supply 45°C · exceeds the 35°C coolant limit.',
  ];
  return `<div class="h-outdoor-water" data-water-route="${wet?'wet':'dry'}" data-water-phase="${step}"><div class="h-water-key" aria-hidden="true"><span><i class="h-water-key-warm"></i>Warm water ${compact?'↓':'→'}</span><span><i class="h-water-key-cool"></i>${compact?'↑':'←'} Cooler water</span><span><i class="h-water-key-air"></i>Air</span></div>${compact?mobile(wet,step,wb):desktop(wet,step,wb)}<p class="h-water-caption ${step===3?passes?'h-pass-text':'h-warning':''}" role="status">${captions[step]}</p><div class="h-water-controls" role="group" aria-label="Follow the water">${labels.map((label,i)=>`<button type="button" data-water-step="${i}" aria-pressed="${step===i}"><span>${i+1}</span>${label}</button>`).join('')}<button type="button" id="approach-next" aria-label="${step===3?'Restart water sequence':'Show next water phase'}">${step===3?'Restart ↺':'Next phase →'}</button></div><details class="h-water-assumptions"><summary>Example assumptions</summary><p>84 kW · water flows ≈ 2 kg/s · 10°C rise in each loop. ${wet?'Tower approach 3°C; each exchanger 5°C.':'Dry-cooler and CDU approaches 5°C each.'} Stipulated values, not equipment ratings. All circuits run together; highlighting follows the heat. Pumps shown schematically; pump heat is excluded.</p></details></div>`;
}
