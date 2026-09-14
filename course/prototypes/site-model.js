const positive=(v,name)=>{if(!Number.isFinite(v)||v<=0)throw new RangeError(`${name} must be positive and finite`);return v;};
export function movingLoad({massKg=2200,contacts=4,gravity=9.81}={}){positive(massKg,'mass');positive(contacts,'contacts');positive(gravity,'gravity');if(!Number.isInteger(contacts))throw new RangeError('contacts must be an integer');const totalKN=massKg*gravity/1000;return{totalKN,perContactKN:totalKN/contacts};}
export function survivingFiber({arrangement='shared',crossingFailed=true}={}){if(!['shared','separate'].includes(arrangement))throw new RangeError('Unknown arrangement');return crossingFailed?(arrangement==='shared'?[]:['B']):['A','B'];}
export function controlResponse(command='normal'){if(!['normal','stop'].includes(command))throw new RangeError('Unknown command');return{trainA:command==='normal',trainB:command==='normal',commonDependency:'Shared controller'};}

export function egressRouteModel({layout='shared',incident='clear'}={}) {
  if (!['shared','separate'].includes(layout)) throw new RangeError('Unknown exit layout');
  if (!['clear','west','east'].includes(incident)) throw new RangeError('Unknown incident zone');
  const paths=layout==='shared'
    ? {west:['common-corridor','west-exit'],east:['common-corridor','east-exit']}
    : {west:['west-corridor','west-exit'],east:['east-corridor','east-exit']};
  const blocked=incident==='west'?['common-corridor','west-corridor']:incident==='east'?['east-exit']:[];
  const reachable=Object.entries(paths).filter(([,edges])=>edges.every(edge=>!blocked.includes(edge))).map(([exit])=>exit);
  return {layout,incident,paths,blocked,reachable};
}
