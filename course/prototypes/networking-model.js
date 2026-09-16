function positive(value,label){if(!Number.isFinite(value)||value<=0)throw new RangeError(`${label} must be positive.`);return value;}
export function fabricBudget({endpointsPerLeaf=4,leaves=4,uplinksPerLeaf=2,linkGbps=400,payloadGB=32}={}){
 for(const [k,v]of Object.entries({endpointsPerLeaf,leaves,uplinksPerLeaf,linkGbps,payloadGB}))positive(v,k);
 const downGbps=endpointsPerLeaf*linkGbps,upGbps=uplinksPerLeaf*linkGbps,bottleneckGbps=Math.min(downGbps,upGbps);
 const endpointCables=endpointsPerLeaf*leaves,uplinkCables=uplinksPerLeaf*leaves;
 return {downGbps,upGbps,oversubscription:downGbps/upGbps,transferSeconds:payloadGB*8/bottleneckGbps,endpointCables,uplinkCables,cables:endpointCables+uplinkCables,switchPorts:endpointCables+2*uplinkCables};
}
export function messageTime({bytes,gbps=400,startupUs=5}){positive(bytes,'bytes');positive(gbps,'gbps');if(startupUs<0||!Number.isFinite(startupUs))throw new RangeError('Startup must be nonnegative.');const serializationUs=bytes*8/gbps/1e3;return {serializationUs,totalUs:startupUs+serializationUs};}
export function communicationTime({communicationMs=30,computeMs=200,overlapMs=20}={}){
 for(const [k,v]of Object.entries({communicationMs,computeMs}))positive(v,k);
 if(!Number.isFinite(overlapMs)||overlapMs<0||overlapMs>computeMs)throw new RangeError('Overlap must fit within the compute interval.');
 const exposedMs=Math.max(0,communicationMs-overlapMs);
 return {communicationMs,computeMs,overlapMs,exposedMs,communicationStartMs:computeMs-overlapMs,sequentialStepMs:computeMs+communicationMs,overlappedStepMs:computeMs+exposedMs};
}
export function propagation(routeKm,speedKmPerSecond=200000){if(routeKm<0||!Number.isFinite(routeKm))throw new RangeError('Route length must be nonnegative.');positive(speedKmPerSecond,'Speed');return {oneWayMs:routeKm/speedKmPerSecond*1e3,roundTripMs:routeKm/speedKmPerSecond*2e3};}
