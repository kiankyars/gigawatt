import {procurementCommissioningVisual} from './procurement-commissioning.js';
import {deliverySchedule, rackInterfaces} from './procurement-model.js';

const arrow='<span class="p-arrow" aria-hidden="true">→</span>';
const result=(value,label,cls='')=>`<div class="p-result ${cls}"><strong>${value}</strong><span>${label}</span></div>`;
const photo=(file,alt,credit,url)=>`<figure class="p-photo"><img src="../assets/references/${file}" alt="${alt}"><figcaption><a href="${url}" target="_blank" rel="noreferrer">${credit}</a></figcaption></figure>`;
const rack=(large=false)=>`<span class="p-rack ${large?'large':''}" aria-hidden="true"><i></i><i></i><i></i><i></i></span>`;
const racks=(count,large=false)=>`<div class="p-rack-row" aria-hidden="true">${Array.from({length:count},()=>rack(large)).join('')}</div>`;
const sourceCEI='https://www.cei.com/core-markets/modular';
const sourceCompass='https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/';

function dependencyComparison(){
 const scenarios=[
  {label:'Baseline',detail:'Switchgear sets the date',electricalProcurement:18,coolingProcurement:10,utilityReady:16},
  {label:'Cooling arrives 4 weeks earlier',detail:'No change to the opening date',electricalProcurement:18,coolingProcurement:6,utilityReady:16},
  {label:'Switchgear arrives 4 weeks earlier',detail:'Testing can begin earlier',electricalProcurement:14,coolingProcurement:10,utilityReady:16},
  {label:'Grid connection slips to week 30',detail:'Utility work takes over the critical path',electricalProcurement:18,coolingProcurement:10,utilityReady:30},
 ];
 const scale=36;
 const color={electrical:'power',cooling:'water',utility:'grid'};
 return `<div class="p-stack p-delivery-compare">
  <div class="p-delivery-legend"><span class="power">Electrical installed</span><span class="water">Cooling installed</span><span class="grid">Utility ready</span><span class="test">Integrated tests</span></div>
  <div class="p-delivery-axis"><span>Delivery scenario</span><div>${[0,9,18,27,36].map(n=>`<span>${n}</span>`).join('')}</div><span>Online</span></div>
  ${scenarios.map(s=>{const m=deliverySchedule(s);return `<section class="p-delivery-row"><div class="p-delivery-label"><h2>${s.label}</h2><p>${s.detail}</p></div><div class="p-delivery-track" role="img" aria-label="Electrical ready week ${m.electrical}; cooling ready week ${m.cooling}; utility ready week ${m.utility}; testing from week ${m.join} to ${m.finish}">${['electrical','cooling','utility'].map((key,i)=>`<span class="p-readiness ${color[key]}" style="--lane:${i};width:${m[key]/scale*100}%"><b>${m[key]}</b></span>`).join('')}<span class="p-test-window" style="left:${m.join/scale*100}%;width:${4/scale*100}%">Test</span></div><strong class="p-online">W${m.finish}</strong></section>`;}).join('')}
  <p class="p-delivery-unit">Weeks from project start</p>
 </div>`;
}

function meter(value,limit,max,unit){return `<div class="p-meter"><div class="p-meter-track"><span style="width:${value/max*100}%" class="${value>limit?'over':''}"></span><i style="left:${limit/max*100}%"></i></div><div class="p-meter-labels"><span>0</span><b style="left:${limit/max*100}%">${limit} ${unit} branch limit</b><span>${max}</span></div></div>`;}
function electrical(){
 const before=rackInterfaces({rackKW:100}),after=rackInterfaces({rackKW:200});
 return `<div class="p-stack"><div class="p-two p-compare">${[[before,'100 kW rack'],[after,'200 kW rack']].map(([m,label])=>`<section><h2>${label}</h2><div class="p-branch-load">${rack(true)}${result(`${Math.round(m.amps)} A`,'Per branch',m.electricalPass?'':'warning')}</div>${meter(m.amps,160,300,'A')}</section>`).join('')}</div><div class="p-case-equation">I = P / (√3 × V × PF)<span>480 V three-phase · PF = 1</span></div></div>`;
}
function hydraulic(){
 const before=rackInterfaces({rackKW:100}),after=rackInterfaces({rackKW:200});
 return `<div class="p-stack"><div class="p-two p-compare"><section><h2>One rack’s coolant branch</h2><div class="p-compare-values"><span>100 kW<b>${before.flow.toFixed(1)} kg/s</b></span><span>200 kW<b>${after.flow.toFixed(1)} kg/s</b></span></div>${meter(after.flow,3,6,'kg/s')}<div class="p-case-equation">ṁ = Q̇ / (cₚ × ΔT)<span>Water · 10°C rise</span></div></section><section><h2>Pressure difference across the connection</h2><div class="p-compare-values"><span>Original flow<b>${before.pressure} kPa</b></span><span>Double flow<b>${after.pressure} kPa</b></span></div>${meter(after.pressure,60,100,'kPa')}<div class="p-case-equation">Δp ∝ ṁ²<span>Δp = inlet − outlet · same hardware</span></div></section></div></div>`;
}
function ocpInterface(){
 return `<div class="p-stack p-ocp"><div class="p-ocp-example"><div class="p-coupling-pair" role="img" aria-label="A supplier A coolant plug and supplier B socket use the same nominal UQD size"><section><h2>Supplier A</h2><div class="p-coupling plug" aria-hidden="true"><i></i><i></i><i></i></div><p>UQD plug</p></section><div class="p-coupling-joint"><b>Same nominal size</b><span aria-hidden="true">⇄</span></div><section><h2>Supplier B</h2><div class="p-coupling socket" aria-hidden="true"><i></i><i></i><i></i></div><p>UQD socket</p></section></div><div class="p-ocp-duty"><h2>Now connect the 200 kW rack</h2><div><span>Required flow<strong>4.8 kg/s</strong></span><span>Existing branch limit<strong>3.0 kg/s</strong></span></div><p>The connectors mate. The branch still needs redesign.</p></div></div><p class="p-ocp-name">Open Compute Project · Universal Quick Disconnect (UQD)</p></div>`;
}

export function procurementVisual(id,state){
 const commissioning=procurementCommissioningVisual(id,state);
 if(commissioning!==null)return commissioning;
 switch(id){
 case 'delivery-purpose':return '';
 case 'rack-case-brief':return `<div class="p-case-intro"><strong>20 MW IT</strong><p>A data center is under construction.</p><p>The rack design changes from<br><b>100 kW to 200 kW.</b></p></div>`;
 case 'schedule-case-brief':return `<div class="p-case-intro p-schedule-intro"><p>The site needs electrical equipment,<br>cooling equipment and utility power.</p><p><b>Which delivery should we expedite?</b></p><div class="p-case-regimes"><span>Baseline</span><span>Earlier cooling</span><span>Earlier switchgear</span><span>Later grid connection</span></div></div>`;
 case 'critical-path':return dependencyComparison();
 case 'epc-and-prefab':return `<div class="p-epc-project"><div class="p-epc-step"><span>E</span><section><h2>Engineering</h2><p>Size the switchgear, transformer and connections.</p></section></div><div class="p-epc-step"><span>P</span><section><h2>Procurement</h2><p>Order the coordinated package and reserve factory capacity.</p></section></div><div class="p-epc-step"><span>C</span><section><h2>Construction</h2><p>Build the foundations, place the skid and connect the plant.</p></section></div></div>`;
 case 'factory-and-site':return '<figure class="procurement-meme"><a class="full-size-figure" href="../assets/references/prefab-factory-site-user.png" target="_blank" rel="noopener" aria-label="Open full-size prefabrication diagram"><img src="../assets/references/prefab-factory-site-user.png" alt="Prefab shifts assembly into the factory: distribution, coolant manifolds, wiring and controls are assembled before delivery; foundations, utility and cooling plant, field joints and integrated tests remain on site."></a></figure>';
 case 'aws-houdini-prefab':return `<div class="p-case">${photo('cei-modular-factory-edgerton.jpg','Cupertino Electric’s Edgerton factory with electrical equipment and modular infrastructure assemblies.','Cupertino Electric · Edgerton factory',sourceCEI)}<div class="p-case-copy"><h2>AWS prefabricated data-hall skids</h2><p>Power and cooling infrastructure is assembled off-site.</p><div class="p-parallel-pair"><section><b>Factory</b><span>Assemble + test</span></section><section><b>Site</b><span>Prepare + connect</span></section></div><p class="p-credit"><a href="https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters" target="_blank" rel="noreferrer">SemiAnalysis · July 29, 2026</a></p></div></div>`;
 case 'compass-package':return `<div class="p-case">${photo('distribution-compass-switchgear.jpg','Siemens medium-voltage switchgear for the jointly developed Compass skid.','Siemens × Compass · switchgear portion',sourceCompass)}<div class="p-case-copy"><h2>One factory-built package</h2><div class="p-skid-assembly"><span>8DJH 36<br>switchgear</span><span aria-hidden="true">+</span><span>Transformer</span></div><p>Internal connections and assembly move into the factory.</p><p class="p-credit">Co-developed by Siemens and Compass Datacenters.</p></div></div>`;
 case 'interface-owner':return ocpInterface();
 case 'ocp-rack-example':return '<figure class="procurement-meme ocp-rack-image"><a class="full-size-figure" href="../assets/references/ocp-rack-basics-user.png" target="_blank" rel="noopener" aria-label="Open full-size rack power comparison"><img src="../assets/references/ocp-rack-basics-user.png" alt="Conventional rack with server-level PSUs beside an open-source rack with consolidated rack-level PSUs."></a></figure>';
 case 'rack-change':return `<div class="p-stack"><div class="p-two p-rack-comparison"><section><h2>Before: one 2 MW zone</h2>${racks(20)}${result('20 × 100 kW','20 racks in this zone')}</section><section><h2>After: one 2 MW zone</h2>${racks(10,true)}${result('10 × 200 kW','10 racks in this zone')}</section></div></div>`;
 case 'electrical-interface':return electrical();
 case 'hydraulic-interface':return hydraulic();
 case 'spatial-interface':return `<div class="p-stack"><div class="p-two p-supports"><section><h2>Original rack</h2><div class="p-supported-rack">${rack(true)}<div class="p-feet">${Array.from({length:4},()=>'<span class="p-load-blocks"><i></i></span>').join('')}</div></div>${result('1× load per foot','20 racks in one zone')}</section><section><h2>Twice the mass, same four feet</h2><div class="p-supported-rack heavy">${rack(true)}<div class="p-feet">${Array.from({length:4},()=>'<span class="p-load-blocks"><i></i><i></i></span>').join('')}</div></div>${result('2× load per foot','10 racks in one zone')}</section></div></div>`;
 default:throw new Error(`Unknown procurement scene: ${id}`);
 }
}
