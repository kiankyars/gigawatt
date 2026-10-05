const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const {mkdirSync}=require('node:fs');
// The staged site root.
const base=process.argv[2]||'http://127.0.0.1:8878/';
const out=process.argv[3]||'/tmp/gigawatt-homepage-qa';
mkdirSync(out,{recursive:true});
const stopIs=(page,n)=>page.waitForFunction(label=>document.querySelector('#stop-count').textContent.startsWith(label),String(n).padStart(2,'0'));
const settle=page=>page.waitForFunction(()=>window.datacenter?.isSettled(),null,{timeout:30000});
(async()=>{
 const browser=await chromium.launch({args:['--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()}: ${r.url()}`)});
 const stills=[];page.on('request',r=>{if(/campus-cutaway/.test(r.url()))stills.push(r.url())});
 await page.goto(base);
 await page.waitForFunction(()=>document.body.dataset.world==='ready');
 await page.waitForFunction(()=>document.querySelectorAll('.chapter-link').length===17);
 assert.deepEqual(stills,[],'The still campus image loads only when the 3D view cannot start');
 assert.equal(await page.locator('.campus-fallback').count(),0);
 assert.equal(await page.locator('#chapter-title').innerText(),'Inside an AI\ndata center.');
 assert.equal(await page.getByRole('button',{name:'Play motion',exact:true}).isVisible(),true);
 const chapterLinks=await page.locator('.chapter-link').evaluateAll(nodes=>nodes.map(n=>n.href));
 for(const href of chapterLinks){const response=await page.request.get(href);assert.equal(response.status(),200,href);assert.match(new URL(href).pathname,/\/slides\/[^/]+\.html$/);}
 // Every tour stop's course links reach a published slide deck.
 const deckLinks=new Set();
 for(let stop=1;stop<=6;stop++){
  await page.keyboard.press(String(stop));await stopIs(page,stop);
  for(const href of await page.locator('.chapter-links a').evaluateAll(nodes=>nodes.map(n=>n.href)))if(!href.includes('#'))deckLinks.add(href);
 }
 assert.ok(deckLinks.size>=9,`Expected course links at every stop, found ${deckLinks.size}`);
 for(const href of deckLinks){const response=await page.request.get(href);assert.equal(response.status(),200,href);assert.match(new URL(href).pathname,/\/slides\/[^/]+\.html$/);}
 for(const size of [{width:1440,height:1000},{width:1280,height:720},{width:390,height:844}]){
  await page.setViewportSize(size);
  await page.keyboard.press('1');await stopIs(page,1);await settle(page);
  await page.screenshot({path:`${out}/tour-1-${size.width}.png`});
  for(let stop=2;stop<=6;stop++){
   await page.locator('#next').click();await stopIs(page,stop);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,`stop ${stop}: page fits ${size.width}`);
   const copy=await page.locator('#chapter-copy').boundingBox();
   assert.ok(copy.y>=0&&copy.y+copy.height<=size.height+1,`stop ${stop}: copy fits the viewport at ${size.width}`);
   if(size.width===1440||stop===3){await settle(page);await page.screenshot({path:`${out}/tour-${stop}-${size.width}.png`});}
  }
  // The header keeps a visible link to the reader at every width.
  await page.keyboard.press('1');await stopIs(page,1);
  const read=page.locator('.site-header nav a[href$="read.html"]');
  assert.equal(await read.isVisible(),true,`Reader link hidden at ${size.width}`);
  assert.match((await read.innerText()).trim(),size.width<=760?/^Read\b/:/^Reading & glossary/);
  const box=await read.boundingBox();
  assert.ok(box.x+box.width<=size.width+1,`Reader link leaves the header at ${size.width}`);
 }
 // Follow the power, open its equipment guide, and open a piece of equipment.
 await page.setViewportSize({width:1440,height:1000});
 await page.keyboard.press('2');await stopIs(page,2);
 await page.locator('#trace').click();assert.equal(await page.locator('#trace').getAttribute('aria-pressed'),'true');
 await page.locator('#open-guide').click();await page.locator('#equipment-dialog[open]').waitFor();
 await page.locator('#equipment-content [data-equipment="ups"]').click();
 assert.equal(await page.locator('#equipment-title').innerText(),'UPS & batteries');
 assert.equal(await page.locator('#trace').getAttribute('aria-pressed'),'false');
 await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'Play motion',exact:true}).click();
 await page.getByRole('button',{name:'Pause motion',exact:true}).click();
 // The course directory follows the tour, and the tour's controls step aside for it.
 await page.locator('.site-header nav a[href="#chapters"]').click();
 await page.waitForFunction(()=>document.body.classList.contains('past-journey'));
 await page.locator('#chapters h2').waitFor();
 await page.screenshot({path:`${out}/directory-1440.png`});
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
 await page.locator('.mast .brand').click();await page.waitForURL(/index\.html$/);await page.locator('#chapter-title').waitFor();
 // Missing WebGL uses the still image and keeps the tour text and the course directory.
 const fallback=await context.newPage();await fallback.addInitScript(()=>{const old=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(kind,...args){return /webgl/i.test(kind)?null:old.call(this,kind,...args);};});
 await fallback.goto(base);await fallback.waitForFunction(()=>document.body.dataset.world==='fallback');
 assert.equal(await fallback.locator('.campus-fallback').isVisible(),true);await fallback.waitForFunction(()=>document.querySelectorAll('.chapter-link').length===17);
 // Staging publishes the still image as WebP.
 assert.match(await fallback.locator('.campus-fallback').getAttribute('src'),/campus-cutaway\.(?:webp|png)$/);
 assert.ok(await fallback.locator('.campus-fallback').evaluate(async img=>{await img.decode();return img.naturalWidth>0;}));
 await fallback.keyboard.press('4');await stopIs(fallback,4);
 await fallback.screenshot({path:`${out}/fallback.png`});
 assert.deepEqual(errors,[]);
 await browser.close();console.log('Homepage passed: tour stops, course links, flow and equipment, responsive fit, directory, reader/home links and WebGL fallback.');
})().catch(e=>{console.error(e);process.exit(1)});
