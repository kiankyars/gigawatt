const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const {mkdirSync}=require('node:fs');
const base=process.argv[2]||'http://127.0.0.1:8878/_site/';
const out=process.argv[3]||'/tmp/gigawatt-homepage-qa';
mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({args:['--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()}: ${r.url()}`)});
 await page.goto(base);
 await page.waitForFunction(()=>document.querySelector('#campus-mount')?.dataset.ready==='true');
 await page.waitForFunction(()=>document.querySelectorAll('.chapter-link').length===17);
 assert.equal(await page.locator('#campus-mount').getAttribute('data-motion'),'false');
 assert.equal(await page.getByRole('button',{name:'Play motion',exact:true}).isVisible(),true);
 const chapterLinks=await page.locator('.chapter-link').evaluateAll(nodes=>nodes.map(n=>n.href));
 for(const href of chapterLinks){const response=await page.request.get(href);assert.equal(response.status(),200,href);assert.match(new URL(href).pathname,/\/slides\/[^/]+\.html$/);}
 for(const size of [{width:1440,height:1000},{width:1280,height:720},{width:390,height:844}]){
  await page.setViewportSize(size);
  for(const view of ['campus','power','compute','cooling']){
   const button=page.locator(`[data-view="${view}"]`);await button.focus();await page.keyboard.press('Enter');
   assert.equal(await page.locator('#campus-mount').getAttribute('data-focus'),view);
   assert.equal(await button.getAttribute('aria-pressed'),'true');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,`${view}: page fits ${size.width}`);
   const bounds=await page.evaluate(()=>{
    const work=document.querySelector('.campus-workspace').getBoundingClientRect();
    const controls=document.querySelector('.campus-controls').getBoundingClientRect();
    const strip=document.querySelector('.explore-strip').getBoundingClientRect();
    return {bottom:work.bottom,controlsBottom:controls.bottom,stripTop:strip.top};
   });
   assert.ok(bounds.controlsBottom<=bounds.stripTop+1,`Controls overlap next section: ${JSON.stringify(bounds)}`);
   if(view==='campus'||size.width===1440)await page.screenshot({path:`${out}/${view}-${size.width}.png`,fullPage:size.width===390});
  }
 }
 await page.getByRole('button',{name:'Electricity',exact:true}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-flow'),'heat');
 await page.getByRole('button',{name:'Heat',exact:true}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-flow'),'none');
 await page.getByRole('button',{name:'Electricity',exact:true}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-flow'),'power');
 await page.getByRole('button',{name:'Heat',exact:true}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-flow'),'all');
 await page.getByRole('button',{name:'Play motion',exact:true}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-motion'),'true');
 await page.getByRole('button',{name:'Pause motion',exact:true}).click();
 await page.getByRole('button',{name:'Reset campus view'}).click();assert.equal(await page.locator('#campus-mount').getAttribute('data-focus'),'campus');
 // All chapters keep their current scene-aware reading links and return home.
 await page.setViewportSize({width:1280,height:720});
 for(const href of chapterLinks){
  await page.goto(href);
  const reading=page.locator('.toolbar a[data-course-reading]');await reading.waitFor();
  assert.equal(new URL(await reading.getAttribute('href'),page.url()).pathname,new URL('read.html',base).pathname,href);
  const home=page.locator('.toolbar .back-to-course, .toolbar .course-link, .toolbar .brand').first();
  assert.equal(new URL(await home.getAttribute('href'),page.url()).pathname,new URL('index.html',base).pathname,href);
 }
 await page.goto(new URL('read.html#d04-conversion-placement',base).href);
 await page.locator('#title').getByText('Moving a converter moves an interface',{exact:true}).waitFor();
 await page.locator('#lookup-toggle').click();assert.equal(await page.locator('#lookup').isVisible(),true);
 await page.locator('.mast .brand').click();await page.waitForURL(/index\.html$/);await page.locator('#hero-title').waitFor();
 // Missing WebGL uses the image without blocking the course directory.
 const fallback=await context.newPage();await fallback.addInitScript(()=>{const old=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(kind,...args){return /webgl/i.test(kind)?null:old.call(this,kind,...args);};});
 await fallback.goto(base);await fallback.waitForFunction(()=>document.querySelector('#campus-mount').dataset.fallback==='true');
 assert.equal(await fallback.locator('.campus-fallback').isVisible(),true);await fallback.waitForFunction(()=>document.querySelectorAll('.chapter-link').length===17);
 await fallback.screenshot({path:`out/fallback.png`.replace('out/',out+'/')});
 assert.deepEqual(errors,[]);
 await browser.close();console.log('Homepage passed: 3D views, keyboard, flow/motion, responsive fit, all chapter/reader/home links, glossary and WebGL fallback.');
})().catch(e=>{console.error(e);process.exit(1)});
