import { egressRouteModel } from "./site-model.js";

function plan(layout, incident) {
  const model=egressRouteModel({layout,incident});
  const has=exit=>model.reachable.includes(exit);
  const shared=layout==='shared';
  const common='M245 115V170H110V270';
  const west='M110 270H0';
  const east=shared?'M110 270H440V350':'M245 115H385V270H440V350';
  const line=(d,active,blocked=false)=>`<path d="${d}" class="egress-path ${blocked?'egress-blocked':active?'egress-connected':'egress-disconnected'}"/>`;
  const status=model.reachable.length===2?'Both exits connected':model.reachable.length===0?'Neither exit connected':has('east')?'East route remains':'West route remains';
  const hazard=incident==='clear'?'':`<g class="egress-incident" transform="translate(${incident==='west'?'110 215':'440 304'})"><title>${incident==='west'?'West corridor':'East exit'} unavailable</title><circle r="27"/><path d="M-10 -10L10 10M-10 10L10 -10"/></g>`;
  const corridors = [common, west, east];
  return `<article><h2>${shared?'Shared approach':'Separate approaches'}</h2>
    <svg class="egress-diagram" viewBox="0 0 500 380" role="img" aria-labelledby="egress-${layout}-title">
      <title id="egress-${layout}-title">${shared?'Both exit routes use the west corridor before dividing.':'The east route leaves the hall without using the west corridor.'} ${status}.</title>
      <rect x="20" y="15" width="460" height="315" class="egress-floor"/>
      ${corridors.map(d=>`<path d="${d}" class="egress-corridor-edge"/>`).join('')}
      ${corridors.map(d=>`<path d="${d}" class="egress-corridor"/>`).join('')}
      <rect x="140" y="35" width="200" height="100" class="egress-hall"/>
      <path d="M20 255V15H480V330H460M420 330H20V285" class="egress-wall"/>
      <path d="${shared?'M140 35H340V135H268M225 135H140V35':'M140 35H340V100M340 128V135H268M225 135H140V35'}" class="egress-partition"/>
      <text x="240" y="68" text-anchor="middle">People in data hall</text>
      <circle cx="245" cy="93" r="6" class="egress-person"/>
      <path d="M245 100V115M232 106H258M245 113L235 127M245 113L255 127" class="egress-person-lines"/>
      ${line(common,shared?model.reachable.length>0:has('west'),incident==='west')}
      ${line(west,has('west'))}${line(east,has('east'),incident==='east')}${hazard}
      ${has('west')?'<path d="M12 261L1 270L12 279" class="egress-arrow"/>':''}
      ${has('east')?'<path d="M431 338L440 351L449 338" class="egress-arrow"/>':''}
      <text x="62" y="307">West exit</text><text x="436" y="373" text-anchor="middle">East exit</text>
    </svg><p class="egress-status ${model.reachable.length?'':'egress-lost'}">${status}</p></article>`;
}

export function renderEgress(state={}) {
  const incident=state.egressIncident||'clear';
  const shared=egressRouteModel({layout:'shared',incident});
  const separate=egressRouteModel({layout:'separate',incident});
  return {
    markup:`<div class="egress-comparison" data-incident="${incident}">${plan('shared',incident)}${plan('separate',incident)}</div>`,
    description:`Two original floor-plan connectivity diagrams have the same two exterior exits. Incident zone: ${incident}. Shared approach retains ${shared.reachable.length} connected exits; separate approaches retain ${separate.reachable.length}. A west-corridor incident cuts both shared routes but leaves the separated east route. No smoke propagation, evacuation time or code compliance is calculated.`,
    format:'html'
  };
}
