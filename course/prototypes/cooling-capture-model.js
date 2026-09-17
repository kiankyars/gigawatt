const positive=(v,n)=>{if(!Number.isFinite(v)||v<=0)throw new RangeError(`${n} must be positive`);return v;};
export function deviceTemperature({watts=400,fluidC=35,resistance=.08,limitC=80}={}){positive(watts,'Heat');positive(resistance,'Thermal resistance');if(!Number.isFinite(fluidC)||!Number.isFinite(limitC))throw new RangeError('Temperatures must be finite');const junctionC=fluidC+watts*resistance;return {junctionC,marginK:limitC-junctionC,passes:junctionC<=limitC};}
export function hydraulicPoint({resistance=30,heatKW=84,cp=4.2}={}){positive(resistance,'Circuit resistance');positive(heatKW,'Heat');positive(cp,'Specific heat');const flowLs=Math.sqrt(160/(10+resistance)),pressureKPa=resistance*flowLs**2,hydraulicW=pressureKPa*flowLs;return {flowLs,pressureKPa,hydraulicW,inputW:hydraulicW/.6,deltaK:heatKW/(flowLs*cp)};}
export function parallelBranches(restricted=false){if(typeof restricted!=='boolean')throw new TypeError('Restriction must be boolean');const flows=restricted?[.5,1.5]:[1,1],returns=flows.map(q=>35+42/(4.2*q));return {flows,returns,totalLs:2,mixedReturnC:returns.reduce((t,r,i)=>t+r*flows[i],0)/2};}
export const retrofitAnswers={
 air:{correct:false,text:'Air-only needs 100 kW of room cooling; only 20 kW is available.'},
 coldplate:{correct:true,text:'85 kW enters liquid and 15 kW enters air. Confirm flow, pressure, coolant compatibility and the service route before release.'},
 'rear-door':{correct:false,text:'Establish rear-door duty, compatible server airflow and the hose and door service clearance before comparing it.'},
 immersion:{correct:false,text:'The existing servers are not qualified for immersion. Cooling capacity alone cannot establish compatibility.'}
};
