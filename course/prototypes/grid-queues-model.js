export const ercotSnapshot = Object.freeze({date:'June 2026',horizon:2033,totalGW:474.7,noStudiesGW:284.3,observedGW:5.9});
export const dominionSnapshot = Object.freeze({contractDate:'July 2025',engineeringGW:30.1,constructionGW:7.1,serviceGW:9.8,totalGW:47,coincidentPeakGW:4});
export function projectOptions(selected=false){return {plannedMW:1000,requestedMW:selected?1000:3000,activeSites:selected?['B']:['A','B','C']};}
export function securityFaceAmount(peakMW){if(!Number.isFinite(peakMW)||peakMW<=0)throw new RangeError('Positive peak MW required');return peakMW*50000;}
export function stagedLoad(generators){if(![0,1,2].includes(generators))throw new RangeError('Expected zero, one or two generators');return Math.min(1000,100+500*generators);}
