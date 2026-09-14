import test from 'node:test';
import assert from 'node:assert/strict';
import {loadFromDc,reservedOutput,phaseLedger,conversionPath,rowBudget,traceLoad} from '../course/prototypes/distribution-model.js';
const close=(a,b,e=1e-7)=>assert.ok(Math.abs(a-b)<e,`${a} != ${b}`);

test('converter losses, apparent power and line current preserve their boundaries',()=>{
 const d=loadFromDc();close(d.inputKW,937.5);close(d.lossKW,37.5);close(d.apparentKVA,1041.6666666667);
 close(d.currentA,1252.9302716789,1e-5);assert.equal(d.passes,false);
 const improved=loadFromDc({powerFactor:.99});assert.equal(improved.passes,true);close(improved.lossKW,d.lossKW);close(improved.inputKW,d.inputKW);
 assert.ok(improved.currentA<d.currentA);
});
test('reservation, power factor and efficiency each apply once',()=>{
 const r=reservedOutput();close(r.budgetKVA,960);close(r.inputKW,864);close(r.outputKW,829.44);
 close(reservedOutput({reserve:0}).outputKW,1036.8);
});
test('the phase model identifies independent service and branch limits',()=>{
 const base=phaseLedger();close(base.inputMW,5.8);assert.deepEqual(base.limits,[]);
 const hot=phaseLedger({auxiliaryMW:1.4});close(hot.inputMW,6.2);assert.deepEqual(hot.limits,['service']);
 const growth={itMW:5.1,auxiliaryMW:1.1,lossMW:.22};close(phaseLedger(growth).inputMW,6.42);
 assert.deepEqual(phaseLedger(growth).limits,['service','IT branch']);
 assert.deepEqual(phaseLedger({...growth,serviceMW:10}).limits,['IT branch']);
 assert.deepEqual(phaseLedger({...growth,branchMW:5.5}).limits,['service']);
 assert.deepEqual(phaseLedger({...growth,serviceMW:10,branchMW:5.5}).limits,[]);
});
test('complete conversion paths balance stage by stage and reverse the ranking',()=>{
 const a=conversionPath(1000,[.98,.96]),b=conversionPath(1000,[.975,.99]),worse=conversionPath(1000,[.94,.99]);
 close(a.inputKW,1062.925170068);close(b.inputKW,1036.001036001);assert.ok(b.inputKW<a.inputKW);assert.ok(worse.inputKW>a.inputKW);
 for(const p of [a,b,worse]){close(p.stages.reduce((sum,s)=>sum+s.lossKW,0),p.lossKW);close(p.inputKW-p.outputKW,p.lossKW);close(p.stages[0].outputKW,p.stages[1].inputKW);}
});
test('busway segment current sums downstream branches',()=>{
 const r=rowBudget([40,40,40,40]);close(r.currentA,r.branchA.reduce((a,b)=>a+b,0));
 close(r.segmentsA[1],3*r.branchA[0]);assert.ok(r.currentA<250);assert.ok(rowBudget([40,40,40,40,40]).currentA>250);
});
test('open future feeder stops supply without erasing the physical route',()=>{
 assert.equal(traceLoad('future').energized,false);assert.equal(traceLoad('future').stopsAt,'future-feeder');
 assert.equal(traceLoad('future',{futureClosed:true}).energized,true);
 assert.ok(traceLoad('row').path.includes('high-voltage-grid'));assert.ok(traceLoad('row').path.includes('campus-transformer'));
 assert.ok(traceLoad('row').path.includes('transformer'));assert.ok(traceLoad('cooling').path.includes('transformer'));
 assert.ok(!traceLoad('cooling').path.includes('it-feeder'));
});
test('reject invalid ratings, efficiencies, reserve and demand inputs',()=>{
 for(const options of [{outputKW:-1},{voltageLL:0},{efficiency:1.1},{powerFactor:0},{limitKVA:NaN}])assert.throws(()=>loadFromDc(options),RangeError);
 for(const reserve of [-.1,1,Infinity])assert.throws(()=>reservedOutput({reserve}),RangeError);
 assert.throws(()=>phaseLedger({lossMW:-.1}),RangeError);assert.throws(()=>conversionPath(1000,[]),RangeError);assert.throws(()=>conversionPath(1000,[.98,0]),RangeError);
 assert.throws(()=>rowBudget([]),RangeError);assert.throws(()=>rowBudget([-40]),RangeError);assert.throws(()=>traceLoad('unknown'),RangeError);
});
