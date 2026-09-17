/** Original teaching models from the D11 reader; these are not equipment curves. */
const nonnegative=(value,name)=>{if(!Number.isFinite(value)||value<0)throw new RangeError(`${name} must be finite and non-negative.`);};
export function chillerBalance({dutyMW=10,compressorMW=2,auxiliaryMW=.5}={}){
 for(const [name,value]of Object.entries({dutyMW,compressorMW,auxiliaryMW}))nonnegative(value,name);
 if(compressorMW===0)throw new RangeError('Compressor input must be positive.');
 return {dutyMW,compressorMW,auxiliaryMW,condenserMW:dutyMW+compressorMW,plantInputMW:compressorMW+auxiliaryMW,compressorCOP:dutyMW/compressorMW,plantCOP:dutyMW/(compressorMW+auxiliaryMW)};
}
export const WEATHER_POINTS=Object.freeze({cool:Object.freeze({cop:8,thermalMW:9}),hot:Object.freeze({cop:4,thermalMW:8.5})});
export function operatingPoint({condition='hot',requestedITMW=8,siteMW=10,otherMW=.4}={}){
 const point=WEATHER_POINTS[condition];if(!point)throw new RangeError('Unknown weather condition.');
 for(const [name,value]of Object.entries({requestedITMW,siteMW,otherMW}))nonnegative(value,name);
 if(otherMW>siteMW)throw new RangeError('Other demand exceeds site supply.');
 const electricalMW=(siteMW-otherMW)/(1+1/point.cop),feasibleMW=Math.min(electricalMW,point.thermalMW);
 const coolingMW=requestedITMW/point.cop,totalMW=requestedITMW+coolingMW+otherMW;
 return {...point,condition,requestedITMW,siteMW,otherMW,electricalMW,feasibleMW,coolingMW,totalMW,electricalFits:totalMW<=siteMW+1e-10,thermalFits:requestedITMW<=point.thermalMW};
}
export function weatherDay(){
 const bins=['cool','hot'].map(condition=>{const ceiling=operatingPoint({condition});const itMW=Math.min(8,ceiling.feasibleMW);return {condition,hours:12,itMW,coolingMW:itMW/ceiling.cop,otherMW:.4};});
 const energy=key=>bins.reduce((sum,bin)=>sum+bin[key]*bin.hours,0);
 const itMWh=energy('itMW'),coolingMWh=energy('coolingMW'),otherMWh=energy('otherMW');
 return {bins,itMWh,coolingMWh,otherMWh,facilityMWh:itMWh+coolingMWh+otherMWh};
}
export function towerLedger({evaporationM3=100,cycles=5,itMWh=100,facilityMWh=120,returnKnown=true}={}){
 for(const [name,value]of Object.entries({evaporationM3,itMWh,facilityMWh}))nonnegative(value,name);
 if(!Number.isFinite(cycles)||cycles<=1)throw new RangeError('Concentration ratio must exceed one.');
 if(itMWh===0||facilityMWh<itMWh)throw new RangeError('Energy boundaries require positive IT and no smaller facility energy.');
 if(typeof returnKnown!=='boolean')throw new TypeError('Return-flow evidence must be boolean.');
 const blowdownM3=evaporationM3/(cycles-1),makeupM3=evaporationM3+blowdownM3;
 return {evaporationM3,cycles,itMWh,facilityMWh,blowdownM3,makeupM3,consumptionM3:returnKnown?evaporationM3:null,intakeLitresPerKWh:makeupM3/itMWh,consumptionLitresPerKWh:returnKnown?evaporationM3/itMWh:null,energyRatio:facilityMWh/itMWh};
}
export function heatReuse({availableMW=4,receiverMW=2,receiverHours=6,dayHours=24}={}){
 for(const [name,value]of Object.entries({availableMW,receiverMW,receiverHours,dayHours}))nonnegative(value,name);
 if(dayHours===0||receiverHours>dayHours)throw new RangeError('Receiver hours must fit a positive observation period.');
 const generatedMWh=availableMW*dayHours,acceptedMWh=Math.min(availableMW,receiverMW)*receiverHours;
 return {availableMW,receiverMW,receiverHours,dayHours,generatedMWh,acceptedMWh,remainingMWh:generatedMWh-acceptedMWh,acceptedFraction:generatedMWh?acceptedMWh/generatedMWh:0};
}
export function decisionFeedback(choice){
 if(choice==='reduce')return {correct:true,text:'7.68 MW fits both limits: 7.68 + 1.92 + 0.40 = 10 MW, below the 8.5 MW thermal ceiling. Use the qualified air-cooled path; retain fill and maintenance in its water account.'};
 if(choice==='full')return {correct:false,text:'Eight MW fits the 8.5 MW thermal ceiling, but 8 + 2 + 0.4 = 10.4 MW exceeds the electrical limit.'};
 if(choice==='tower')return {correct:false,text:'A closed rack loop does not supply makeup to a separate tower circuit. That heat path is unavailable during the stated restriction.'};
 return {correct:false,text:'Choose an operating plan, then check the complete heat and power paths.'};
}
