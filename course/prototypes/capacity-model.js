// Original teaching scenarios from the D15 reader. No named-site estimates.
const nonnegative=(value,name)=>{if(!Number.isFinite(value)||value<0)throw new RangeError(`${name} must be finite and nonnegative`);return value;};
const positive=(value,name)=>{nonnegative(value,name);if(value===0)throw new RangeError(`${name} must be positive`);return value;};
const fraction=(value,name)=>{nonnegative(value,name);if(value>1)throw new RangeError(`${name} must be at most one`);return value;};
export const capacityInputs=Object.freeze({siteMW:100,overheadFactor:1.2,fixedMW:5,nonComputeMW:5,rackMW:.1,electricalMW:70,coolingMW:60,network:600,space:750,accepted:520});

export function capacityLedger(options={}){
 const p={...capacityInputs,...options};
 for(const [key,value]of Object.entries(p))nonnegative(value,key);
 positive(p.rackMW,'rackMW');positive(p.overheadFactor,'overheadFactor');
 if(p.overheadFactor<1)throw new RangeError('overheadFactor cannot remove IT input');
 for(const key of ['network','space','accepted'])if(!Number.isInteger(p[key]))throw new RangeError(`${key} must count whole rack equivalents`);
 const whole=value=>Math.max(0,Math.floor(value+1e-9));
 const ceilings=[
  {key:'site',label:'Site input',value:whole(((p.siteMW-p.fixedMW)/p.overheadFactor-p.nonComputeMW)/p.rackMW)},
  {key:'electrical',label:'IT electrical',value:whole((p.electricalMW-p.nonComputeMW)/p.rackMW)},
  {key:'cooling',label:'Heat removal',value:whole((p.coolingMW-p.nonComputeMW)/p.rackMW)},
  {key:'network',label:'Network',value:p.network},{key:'space',label:'Space',value:p.space},{key:'accepted',label:'Accepted paths',value:p.accepted}
 ];
 const racks=Math.min(...ceilings.map(item=>item.value)),computeMW=racks*p.rackMW,itMW=computeMW+p.nonComputeMW,siteMW=itMW*p.overheadFactor+p.fixedMW;
 // The shared IT and fixed plant must also fit when zero compute racks fit.
 const baseLoadFits=p.siteMW>=p.nonComputeMW*p.overheadFactor+p.fixedMW&&p.electricalMW>=p.nonComputeMW&&p.coolingMW>=p.nonComputeMW;
 return {inputs:p,ceilings,racks,binding:ceilings.filter(item=>item.value===racks).map(item=>item.key),computeMW,itMW,siteMW,headroomMW:p.siteMW-siteMW,baseLoadFits};
}

export function capacityStage(stage='current'){
 const stages={current:{},acceptance:{accepted:700},cooling:{accepted:700,coolingMW:70},network:{accepted:700,coolingMW:70,network:800}};
 if(!(stage in stages))throw new RangeError('Unknown capacity stage');
 return capacityLedger(stages[stage]);
}

export function presentValue(amount,year,rate=.08){
 if(!Number.isFinite(amount))throw new RangeError('amount must be finite');
 nonnegative(year,'year');nonnegative(rate,'rate');
 return amount/(1+rate)**year;
}

export function costComparison({energyPrice=80,rate=.08,years=3,initialMillions=20,operationsMillions=3,energyMWh=50000,residualMillions=5,contractMillions=11}={}){
 for(const [key,value]of Object.entries({energyPrice,rate,initialMillions,operationsMillions,energyMWh,residualMillions,contractMillions}))nonnegative(value,key);
 if(!Number.isInteger(years)||years<1)throw new RangeError('years must be a positive integer');
 const energyMillions=energyPrice*energyMWh/1e6,annualMillions=operationsMillions+energyMillions;
 const factors=Array.from({length:years},(_,index)=>presentValue(1,index+1,rate));
 const recurringFactor=factors.reduce((sum,value)=>sum+value,0),residualPV=presentValue(residualMillions,years,rate);
 const ownPV=initialMillions+annualMillions*recurringFactor-residualPV,contractPV=contractMillions*recurringFactor;
 return {energyMillions,annualMillions,factors,recurringFactor,residualPV,ownPV,contractPV,savingMillions:ownPV-contractPV,years,rate,energyPrice};
}

export function usefulCost({costMillions,resultsMillions=10}={}){
 nonnegative(costMillions,'costMillions');positive(resultsMillions,'resultsMillions');
 return {perResult:costMillions/resultsMillions,resultsMillions,costMillions};
}

export function upgradeScreen({coolingDelay=1,demand=1,years=3,hoursPerYear=8000}={}){
 nonnegative(coolingDelay,'coolingDelay');fraction(demand,'demand');positive(years,'years');positive(hoursPerYear,'hoursPerYear');
 const option=(capitalMillions,rate,delay)=>{
  const activeYears=Math.max(0,years-delay),results=rate*hoursPerYear*activeYears*demand;
  return {capitalMillions,rate,delay,activeYears,results,perResult:results>0?capitalMillions*1e6/results:null};
 };
 const network=option(4,80,0),cooling=option(6,150,coolingDelay);
 const preferred=network.perResult===null?'none':cooling.perResult===null?'network':Math.abs(network.perResult-cooling.perResult)<1e-9?'tie':network.perResult<cooling.perResult?'network':'cooling';
 const equalCostDelay=years-(cooling.capitalMillions*network.results)/(network.capitalMillions*cooling.rate*hoursPerYear*(demand||1));
 return {network,cooling,preferred,years,hoursPerYear,demand,equalCostDelay:demand>0?equalCostDelay:null};
}
