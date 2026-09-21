export const ercotSnapshot = Object.freeze({date:'June 2026',horizon:2033,totalGW:474.7,noStudiesGW:284.3,underReviewGW:135.5,studiesOnlyGW:9.9,requirementsMetGW:36.0,approvedNotOperationalGW:3.2,observedGW:5.9});
export const dominionSnapshot = Object.freeze({contractDate:'July 2026',engineeringGW:32.4,constructionGW:9.4,serviceGW:12.0,totalGW:53.8,coincidentPeakGW:4,peakYear:2025});
// ERCOT's six status rows collapse into three groups; rounded rows sum to 474.8 against a displayed 474.7.
export function ercotGroups(m=ercotSnapshot){const round=v=>Math.round(v*10)/10;return [{key:'none',label:'No study submitted to ERCOT',gw:m.noStudiesGW},{key:'review',label:'Study under ERCOT review',gw:m.underReviewGW},{key:'approved',label:'Study approved or further',gw:round(m.studiesOnlyGW+m.requirementsMetGW+m.approvedNotOperationalGW+m.observedGW)}];}
export function projectOptions(){const sites=['A','B','C'],plannedMW=1000;return {plannedMW,sites,requestedMW:sites.length*plannedMW};}
export function securityFaceAmount(peakMW){if(!Number.isFinite(peakMW)||peakMW<=0)throw new RangeError('Positive peak MW required');return peakMW*50000;}
export function stagedLoad(generators){if(![0,1,2].includes(generators))throw new RangeError('Expected zero, one or two generators');return Math.min(1000,100+500*generators);}
