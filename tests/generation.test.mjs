import test from 'node:test';
import assert from 'node:assert/strict';
import {generationBalance,dispatchDay,generationCosts,generationScenes,generationInitialState,renderGeneration} from '../course/prototypes/siting-generation.js';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
test('equal net output closes both fuel balances without a free-energy remainder',()=>{
 for(const cycle of ['simple','combined']){const a=generationBalance(cycle);near(a.netMW,100);near(a.fuelMW,a.netMW+a.remainderMW);near(a.fuelMW*a.efficiency,100);assert.ok(a.remainderMW>0);}
 near(generationBalance('simple').fuelMW,250);near(generationBalance('combined').fuelMW,500/3);
 assert.throws(()=>generationBalance('unknown'),RangeError);
});
test('every hourly dispatch balance preserves demand and source limits',()=>{
 for(const campus of [0,50,200])for(const a of dispatchDay(campus)){
  near(a.baseMW+a.combinedMW+a.peakerMW+a.shortfallMW,a.demandMW);
  assert.ok(a.baseMW<=100&&a.combinedMW<=120&&a.peakerMW<=80);
  assert.ok(a.combinedMW>=0&&a.peakerMW>=0&&a.shortfallMW>=0);
 }
 const original=dispatchDay(0),added=dispatchDay(50);
 near(Math.max(...original.map(a=>a.demandMW)),260);
 near(Math.max(...added.map(a=>a.demandMW)),310);
 near(Math.max(...added.map(a=>a.shortfallMW)),10);
 near(original.reduce((n,a)=>n+a.shortfallMW,0),0);
 near(added.reduce((n,a)=>n+a.demandMW,0)-original.reduce((n,a)=>n+a.demandMW,0),1200);
 assert.throws(()=>dispatchDay(-1),RangeError);
});
test('cost crossover follows independent marginal fuel saving',()=>{
 near(generationCosts(0).simpleTotal,8e6);near(generationCosts(0).combinedTotal,16e6);
 const a=generationCosts(500),b=generationCosts(7000),cross=generationCosts(4800);
 near(a.simpleTotal,10.5e6);near(a.combinedTotal,16e6+100*500*20/.6);
 near(b.simpleTotal,43e6);near(b.combinedTotal,16e6+100*7000*20/.6);
 assert.equal(a.winner,'simple');assert.equal(b.winner,'combined');assert.equal(cross.winner,'equal');
 near(cross.crossoverHours,4800);near(cross.simpleTotal,cross.combinedTotal);
 assert.throws(()=>generationCosts(8761),RangeError);assert.throws(()=>generationCosts(NaN),RangeError);
});
test('generation scenes render all declared control and reveal states in both layouts',()=>{
 assert.equal(new Set(generationScenes.map(s=>s.id)).size,generationScenes.length);
 for(const scene of generationScenes){const variants=[{...generationInitialState}];for(const c of scene.controls??[])for(const [v] of c.options)variants.push({...generationInitialState,[c.key]:v});if(scene.reveal)variants.push({...generationInitialState,[scene.reveal]:true});
  for(const state of variants)for(const compact of [false,true]){const a=renderGeneration(scene.id,state,compact);assert.ok(a.markup.length>100&&a.description.length>80);assert.doesNotMatch(a.markup,/NaN|undefined|Infinity/);}
 }
 assert.throws(()=>renderGeneration('unknown',{}));
});
