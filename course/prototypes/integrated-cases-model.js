// Original teaching cases. Quantities stay at the boundaries named in each case.
const nonnegative=(name,value)=>{if(!Number.isFinite(value)||value<0)throw new RangeError(`${name} must be finite and nonnegative`);return value;};
const positive=(name,value)=>{nonnegative(name,value);if(value===0)throw new RangeError(`${name} must be positive`);return value;};
const efficiency=(name,value)=>{positive(name,value);if(value>1)throw new RangeError(`${name} cannot exceed one`);return value;};
const choice=(name,value,allowed)=>{if(!allowed.includes(value))throw new RangeError(`Unknown ${name}: ${value}`);};

export function coupledOutage({plan='existing',itMW=2,auxiliaryMW=.2,dcKWh=600,eta=.9,inverterMW=2.5,minutes=12}={}){
 choice('outage plan',plan,['existing','energy','auxiliaries']);
 positive('IT load',itMW);nonnegative('auxiliary load',auxiliaryMW);nonnegative('DC energy',dcKWh);efficiency('discharge efficiency',eta);positive('inverter',inverterMW);nonnegative('restoration minutes',minutes);
 const supportedMW=itMW+(plan==='auxiliaries'?auxiliaryMW:0),energyDC=dcKWh+(plan==='energy'?200:0),acKWh=energyDC*eta;
 const requiredKWh=supportedMW*1000*minutes/60,powerPass=supportedMW<=inverterMW,energyPass=requiredKWh<=acKWh;
 return {supportedMW,energyDC,acKWh,requiredKWh,reserveKWh:acKWh-requiredKWh,idealMinutes:acKWh/(supportedMW*1000)*60,powerPass,energyPass,electricalPass:powerPass&&energyPass,pumpSupplySurvives:plan==='auxiliaries',thermalSupport:'unestablished',serviceAccepted:false};
}

export function weatherCapacity({weather='hot',remedy='none',acceptedRacks=900,demandMW=58,siteMW=100,rackKW=100}={}){
 choice('weather',weather,['mild','hot']);choice('weather remedy',remedy,['none','auxiliaries','cooling']);
 positive('site capacity',siteMW);positive('rack duty',rackKW);nonnegative('accepted rack paths',acceptedRacks);nonnegative('demand',demandMW);
 if(!Number.isInteger(acceptedRacks))throw new RangeError('Accepted paths must be whole racks');
 const auxiliaryMW=(weather==='mild'?15:25)-(remedy==='auxiliaries'?10:0),coolingMW=(weather==='mild'?70:55)+(remedy==='cooling'?10:0);
 const electricalMW=Math.max(0,siteMW-auxiliaryMW),pathMW=acceptedRacks*rackKW/1000,capacityMW=Math.min(electricalMW,coolingMW,pathMW);
 const limits={electrical:electricalMW,cooling:coolingMW,paths:pathMW};
 return {auxiliaryMW,coolingMW,electricalMW,pathMW,capacityMW,racks:Math.floor((capacityMW*1000+1e-8)/rackKW),binding:Object.keys(limits).filter(key=>Math.abs(limits[key]-capacityMW)<1e-9),facilityMW:demandMW+auxiliaryMW,demandSupported:demandMW<=capacityMW,limits};
}

export function densityRetrofit({loadKW=120,etaA=.96,etaSidecar=.97,etaNear=.98,volts=800,feederKW=160,roomCoolingKW=140,architecture='a',route='blocked'}={}){
 positive('DC load',loadKW);efficiency('A efficiency',etaA);efficiency('sidecar efficiency',etaSidecar);efficiency('near-load efficiency',etaNear);positive('bus voltage',volts);positive('feeder capacity',feederKW);positive('room cooling',roomCoolingKW);
 choice('architecture',architecture,['a','b']);choice('service route',route,['blocked','clear']);
 const aInputKW=loadKW/etaA,intermediateKW=loadKW/etaNear,bInputKW=intermediateKW/etaSidecar;
 const inputKW=architecture==='a'?aInputKW:bInputKW,accessPass=architecture==='a'||route==='clear';
 return {aInputKW,bInputKW,intermediateKW,amps:intermediateKW*1000/volts,aLossKW:aInputKW-loadKW,sidecarLossKW:bInputKW-intermediateKW,nearLossKW:intermediateKW-loadKW,extraKW:bInputKW-aInputKW,inputKW,roomHeatKW:inputKW,electricalPass:inputKW<=feederKW,thermalPass:inputKW<=roomCoolingKW,accessPass,releaseCandidate:inputKW<=feederKW&&inputKW<=roomCoolingKW&&accessPass};
}

export function stalledJob({upgrade='none',payloadGB=800,computeSeconds=60,otherSeconds=10,endpointGBps=80,fabricGBps=40,receiverGBps=80}={}){
 choice('network upgrade',upgrade,['none','endpoint','fabric']);
 positive('payload',payloadGB);nonnegative('compute duration',computeSeconds);nonnegative('other serial duration',otherSeconds);positive('endpoint rate',endpointGBps);positive('fabric rate',fabricGBps);positive('receiver rate',receiverGBps);
 const rates={sender:endpointGBps*(upgrade==='endpoint'?2:1),fabric:fabricGBps*(upgrade==='fabric'?2:1),receiver:receiverGBps};
 const achievedGBps=Math.min(...Object.values(rates)),communicationSeconds=payloadGB/achievedGBps,cycleSeconds=computeSeconds+communicationSeconds+otherSeconds;
 const baselineSeconds=computeSeconds+payloadGB/Math.min(endpointGBps,fabricGBps,receiverGBps)+otherSeconds;
 return {rates,achievedGBps,communicationSeconds,cycleSeconds,baselineSeconds,throughputRatio:baselineSeconds/cycleSeconds,computeShare:computeSeconds/cycleSeconds,binding:Object.keys(rates).filter(key=>rates[key]===achievedGBps)};
}

export function phaseAcceptance({day=0,cTest='pass',bPass=true,cRetestPass=true,open='a'}={}){
 nonnegative('day',day);choice('C test result',cTest,['pass','fail']);choice('opening scope',open,['a','ab','all']);
 if(typeof bPass!=='boolean'||typeof cRetestPass!=='boolean')throw new RangeError('Acceptance results must be boolean');
 const bReadyDay=4+2,cReadyDay=cTest==='pass'?3+1+3:3+1+3+2+3;
 const groups=[{id:'A',racks:300,accepted:true},{id:'B',racks:250,accepted:day>=bReadyDay&&bPass},{id:'C',racks:250,accepted:day>=cReadyDay&&(cTest==='pass'||cRetestPass)}];
 const acceptedRacks=groups.filter(group=>group.accepted).reduce((sum,group)=>sum+group.racks,0),requestedGroups=open==='a'?['A']:open==='ab'?['A','B']:['A','B','C'];
 return {groups,acceptedRacks,acceptedMW:acceptedRacks*.1,installedRacks:800,installedMW:80,bReadyDay,cReadyDay,allReadyDay:Math.max(bReadyDay,cReadyDay),requestedRacks:groups.filter(group=>requestedGroups.includes(group.id)).reduce((sum,group)=>sum+group.racks,0),canOpen:groups.filter(group=>requestedGroups.includes(group.id)).every(group=>group.accepted)};
}
