const positive=(v,label)=>{if(!Number.isFinite(v)||v<=0)throw new RangeError(`${label} must be positive`);return v;};
export function rentalRevenue({gpus=1024,hours=8760,committedRate=2.5,marketRate=4,occupancy=.5}={}){
 for(const [name,value] of Object.entries({gpus,hours,committedRate,marketRate}))positive(value,name);
 if(!Number.isInteger(gpus))throw new RangeError('gpus must be an integer');
 if(!Number.isFinite(occupancy)||occupancy<0||occupancy>1)throw new RangeError('occupancy must be between zero and one');
 const availableHours=gpus*hours,billedHours=availableHours*occupancy;
 return {gpus,hours,occupancy,availableHours,billedHours,committed:availableHours*committedRate,market:billedHours*marketRate,breakEven:committedRate/marketRate,committedRate,marketRate};
}
export function electricityPerBilledHour({rentedSiteKWPerGPU=1,idleSiteKWPerGPU=.2,tariffPerMWh=80,occupancy=.8}={}){
 positive(rentedSiteKWPerGPU,'rentedSiteKWPerGPU');positive(tariffPerMWh,'tariffPerMWh');positive(occupancy,'occupancy');
 if(!Number.isFinite(idleSiteKWPerGPU)||idleSiteKWPerGPU<0)throw new RangeError('idleSiteKWPerGPU cannot be negative');
 if(occupancy>1)throw new RangeError('occupancy cannot exceed one');
 const averageSiteKWPerGPU=occupancy*rentedSiteKWPerGPU+(1-occupancy)*idleSiteKWPerGPU;
 return averageSiteKWPerGPU*tariffPerMWh/1000/occupancy;
}
export const h100Ranges=Object.freeze([
 {period:'Oct 2025',low:1.45,high:1.95},
 {period:'Jan 2026',low:1.50,high:2.05},
 {period:'Apr 2026',low:2.10,high:2.70}
]);
