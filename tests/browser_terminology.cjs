const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const { mkdirSync, readFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const base = process.argv[2] || 'http://127.0.0.1:8765/course/prototypes/terminology-format.html';
const output = process.argv[3] || '/tmp/gigawatt-terminology-qa';
const url = (id, teach = true) => { const u = new URL(base); if (teach) u.searchParams.set('teach','1'); u.hash=id; return u.href; };
async function geometry(page, size, context) {
  const result = await page.evaluate(() => {
    const svg=document.querySelector('#diagram'),vb=svg.viewBox.baseVal;
    const text=[...svg.querySelectorAll('text')],failures=[];
    for(const t of text) { const b=t.getBBox(); if(b.x < -1 || b.y < -1 || b.x+b.width > vb.width+1 || b.y+b.height > vb.height+1) failures.push(`Outside SVG: ${t.textContent}`); }
    for(let i=0;i<text.length;i++)for(let j=i+1;j<text.length;j++){const a=text[i].getBBox(),b=text[j].getBBox();if(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>1 && Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>1)failures.push(`Overlap: ${text[i].textContent} / ${text[j].textContent}`);}
    const diagram=svg.getBoundingClientRect(),head=document.querySelector('main>header').getBoundingClientRect(),footer=document.querySelector('footer').getBoundingClientRect(),actions=document.querySelector('#actions').getBoundingClientRect();
    if(head.bottom>diagram.top+1)failures.push('Title overlaps diagram');
    if(actions.height && diagram.bottom>actions.top+1)failures.push('Diagram overlaps actions');
    if(Math.max(diagram.bottom,actions.bottom)>footer.top+1)failures.push('Content overlaps footer');
    return {failures,width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight};
  });
  assert.deepEqual(result.failures,[],context);
  assert.ok(result.width<=size.width+1,`${context}: horizontal overflow`);
  if(size.width>=1024)assert.ok(result.height<=size.height+1,`${context}: desktop overflow`);
}
(async()=>{
  const {scenes,sceneAliases}=await import(pathToFileURL(path.resolve(__dirname,'../course/prototypes/terminology-scenes.js')));
  const lessons=JSON.parse(readFileSync(path.resolve(__dirname,'../course/expanded-course.json'),'utf8')).lessons;
  const ids=new Set(lessons.map(l=>l.id));
  for(const scene of scenes)assert.ok(ids.has(scene.reference),`Missing reading reference: ${scene.reference}`);
  assert.equal(scenes.length,16,'D00 goes straight into its sixteen substantive scenes');
  assert.equal(scenes.reduce((n,s)=>n+s.seconds,0),1110,'Planned scene pacing is 18:30, with about twenty minutes allowed for rehearsal');
  for(const id of Object.values(sceneAliases))assert.ok(scenes.some(scene=>scene.id===id),`Missing replacement scene: ${id}`);
  mkdirSync(output,{recursive:true});
  const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{})});
  try{
    const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    for(const colorScheme of ['light','dark'])for(const size of [{width:1280,height:720},{width:1024,height:768},{width:390,height:844},{width:844,height:390}]){
      await page.setViewportSize(size);await page.emulateMedia({colorScheme,reducedMotion:'reduce'});
      for(const scene of scenes){
        await page.goto(url(scene.id));await page.waitForSelector('#diagram text');
        assert.equal(await page.locator('#title').textContent(),scene.title);
        for(const [value]of scene.options||[[null]]){
          if(value!==null){await page.locator(`[data-setting="${scene.key}"][data-value="${value}"]`).click();assert.equal(await page.locator('#actions [aria-pressed="true"]').count(),1);}
          await geometry(page,size,`${scene.id}/${value}/${size.width}/${colorScheme}`);
          if(scene.id==='resistance'){const v=Number(value);assert.equal(Number(await page.locator('[data-heat-watts]').getAttribute('data-heat-watts')),v*v/6);}
          if(scene.id==='energy')assert.equal(await page.locator('[data-energy-kwh]').getAttribute('data-energy-kwh'),value);
          if(scene.id==='ac-dc')assert.equal(await page.locator('[data-ac-current-sign]').getAttribute('data-ac-current-sign'),value==='90'?'1':value==='180'?'0':'-1');
        }
        if(size.width===1280 || size.width===390)await page.screenshot({path:`${output}/${scene.id}-${size.width}-${colorScheme}.png`,fullPage:size.width<600});
      }
    }
    await page.setViewportSize({width:1280,height:720});
    await page.goto(url('welcome'));await page.waitForSelector('#diagram text');
    await page.waitForURL(/#circuit$/);
    assert.match(await page.locator('#primer-note').textContent(),/No memorization required/);
    assert.equal(await page.locator('#primer-note').isVisible(),true);
    await page.keyboard.press('ArrowRight');await page.waitForURL(/#voltage-current$/);
    assert.equal(await page.locator('#primer-note').isVisible(),false);
    await page.keyboard.press('ArrowLeft');await page.waitForURL(/#circuit$/);
    await page.locator('[data-value="open"]').click();
    assert.match(await page.locator('#diagram').textContent(),/No steady current/);
    assert.equal(await page.locator('#diagram path[marker-end]').count(),0,'Open circuit has no current arrows');
    await page.locator('#next').click();await page.locator('#previous').click();
    assert.equal(await page.locator('[data-value="open"]').getAttribute('aria-pressed'),'true');
    await page.locator('#explain').click();await page.keyboard.press('ArrowRight');assert.match(page.url(),/#circuit$/);
    assert.match(await page.locator('#explanation').textContent(),/Voltage can still exist/);
    await page.keyboard.press('Escape');assert.equal(await page.locator('#reading').evaluate(d=>d.open),false);
    await page.goto(url('ready'));await page.waitForURL(/#pue$/);
    assert.equal(await page.locator('#scenes').inputValue(),String(scenes.length-1));
    await page.locator('#next-section').click();await page.waitForURL(/orientation-format\.html\?teach=1#three-paths$/);
    await page.goto(url('welcome',false));assert.equal(await page.locator('#fullscreen').isVisible(),false);
    await page.locator('#skip-primer').click();await page.waitForURL(/orientation-format\.html#three-paths$/);
    assert.deepEqual(errors,[]);
    console.log('Passed D00 layouts in four viewports and both themes, all control states, example arithmetic, source lesson links, keyboard/dialog behavior and D01 handoff.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
