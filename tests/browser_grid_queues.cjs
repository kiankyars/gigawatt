const {webkit,chromium}=require('playwright');
const assert=require('node:assert/strict');
const {mkdirSync}=require('node:fs');
const base=process.argv[2]||'http://127.0.0.1:8878/_site/slides/grid-queues.html?teach=1';
const out=process.argv[3]||'/tmp/gigawatt-grid-queues-qa';
mkdirSync(out,{recursive:true});
(async()=>{
 for(const [name,engine] of [['webkit',webkit],['chromium',chromium]]){
  const browser=await engine.launch();const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const viewport of [{width:1280,height:720},{width:1440,height:900},{width:390,height:844}]){
   await page.setViewportSize(viewport);await page.goto(base);
   await page.waitForFunction(()=>document.querySelector('#scenes')?.options.length===12);
   const ids=await page.locator('#scenes option').evaluateAll(els=>els.map(e=>e.value));
   for(const id of ids){
    await page.selectOption('#scenes',id);
    await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
    const issues=await page.evaluate(()=>{
     const issues=[],visual=document.querySelector('#visual'),v=visual.getBoundingClientRect();
     if(document.documentElement.scrollWidth>innerWidth+2)issues.push('page horizontal overflow');
     if(innerWidth>800)for(const el of visual.children){const r=el.getBoundingClientRect();if(r.bottom>v.bottom+3)issues.push(`vertical overflow ${Math.round(r.bottom-v.bottom)}px`);}
     for(const i of document.images)if(!i.complete||!i.naturalWidth)issues.push('broken image');
     return issues;
    });
    assert.deepEqual(issues,[],`${name} ${viewport.width} ${id}`);
    if(name==='webkit'&&[390,1280].includes(viewport.width))await page.screenshot({path:`${out}/${id}-${viewport.width}.png`,fullPage:viewport.width<800});
   }
   await page.selectOption('#scenes','site-options');
   await page.getByRole('button',{name:'Choose B; withdraw A and C',exact:true}).click();
   assert.equal(await page.locator('.q-sites .withdrawn').count(),2);
   assert.match(await page.locator('.q-option-total').innerText(),/1 GW of active requests/);
  }
  await page.setViewportSize({width:1280,height:720});
  await page.goto(base+'#dominion-contracts');
  const [presenter]=await Promise.all([page.waitForEvent('popup'),page.getByRole('button',{name:'Presenter',exact:true}).click()]);
  await presenter.setViewportSize({width:1280,height:720});
  await presenter.waitForFunction(()=>document.querySelector('#workspace').dataset.notes==='true');
  await presenter.locator('#notes-content').getByText(/Dominion gives us/).waitFor();
  await presenter.frameLocator('#preview').locator('#scene[data-scene="dominion-demand"]').waitFor();
  assert.match(await presenter.locator('#chapter').innerText(),/^17\./);
  assert.equal(await page.locator('.toolbar').isVisible(),false);
  assert.equal(await page.locator('footer').isVisible(),false);
  await presenter.screenshot({path:`${out}/presenter-${name}.png`});
  await presenter.getByRole('button',{name:'Exit presenter'}).click();
  await page.waitForFunction(()=>!('presenterActive' in document.documentElement.dataset));
  assert.equal(await page.locator('.toolbar').isVisible(),true);
  await page.goto(new URL('integrated-cases.html?teach=1#watts-to-work',base).href);
  await page.getByRole('link',{name:/Next chapter/}).click();
  await page.waitForURL(/grid-queues\.html/);
  await page.waitForFunction(()=>document.querySelector('#scenes')?.options.length===12);
  await page.selectOption('#scenes','connection-terms');
  assert.equal(await page.locator('#next').isDisabled(),true);
  assert.deepEqual(errors,[]);
  console.log(`${name}: 12 slides at desktop, large desktop and phone; site choice, presenter notes/preview/exit, chapter handoff passed.`);
  await browser.close();
 }
})().catch(e=>{console.error(e);process.exit(1)});
