const assert = require('node:assert/strict');
const { mkdirSync, readFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const staticOnly = process.argv.includes('--static');
const args = process.argv.slice(2).filter(arg => arg !== '--static');
const base = args[0] || 'http://127.0.0.1:8765/course/prototypes/terminology-format.html';
const output = args[1] || '/tmp/gigawatt-terminology-qa';
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
  const {renderTerminology}=await import(pathToFileURL(path.resolve(__dirname,'../course/prototypes/terminology-visuals.js')));
  const html=readFileSync(path.resolve(__dirname,'../course/prototypes/terminology-format.html'),'utf8');
  const forwardPointer=/\bD\d{2}\b|later (?:lesson|section|chapter|sequence|comparison|calculation)|(?:next|other) (?:chapter|section)|(?:explain|introduce|meet|revisit).*again|returns in context|first exposure|optional primer|prelude|Skip to|Read the later|Continue to/i;
  assert.equal(scenes.length,19,'Primer goes straight into its nineteen substantive scenes');
  assert.equal(scenes.reduce((n,s)=>n+s.seconds,0),1205,'Planned scene pacing is 20:05, pending an aloud rehearsal');
  for(const [before,after] of [['ac-dc','ac-shapes'],['three-phase','power-factor'],['backup','ups-types']]) {
    assert.equal(scenes.findIndex(s=>s.id===after),scenes.findIndex(s=>s.id===before)+1,`${after} immediately follows the concept it develops`);
  }
  assert.match(html,/<h2 id="reading-title">Primer<\/h2>/);
  assert.doesNotMatch(html,forwardPointer,'Presentation contains a course-forward pointer');
  assert.doesNotMatch(html,/<a\b|\bhref=|source-list|lesson-reference|skip-primer|next-section/,'Standalone primer has no reference or course links');
  for(const id of Object.values(sceneAliases))assert.ok(scenes.some(scene=>scene.id===id),`Missing replacement scene: ${id}`);
  for(const scene of scenes){
    assert.equal('returns' in scene || 'reference' in scene || 'sources' in scene,false,`${scene.id}: reference metadata belongs outside the presentation`);
    assert.doesNotMatch(JSON.stringify(scene),forwardPointer,`${scene.id}: course-forward pointer`);
    assert.doesNotMatch(scene.title,/;/,`${scene.id}: title uses simple English without a semicolon`);
    for(const compact of [false,true])for(const [value]of scene.options||[[null]]){
      const state={circuit:'closed',resistanceVoltage:'12',hours:'1',angle:'90',upsSupply:'normal',bandwidth:'100',...(scene.key?{[scene.key]:value}:{})};
      const svg=renderTerminology(scene.id,state,compact);
      assert.match(svg,/<text\b/,`${scene.id}: visible teaching content`);
      assert.doesNotMatch(svg,/NaN|undefined/,`${scene.id}: invalid diagram value`);
      assert.doesNotMatch(svg,forwardPointer,`${scene.id}: diagram contains a course-forward pointer`);
      if(scene.id==='resistance')assert.match(svg,new RegExp(`data-heat-watts="${Number(value)**2/6}"`));
      if(scene.id==='energy')assert.match(svg,new RegExp(`data-energy-kwh="${value}"`));
      if(scene.id==='ac-dc')assert.match(svg,new RegExp(`data-ac-current-sign="${value==='90'?1:value==='180'?0:-1}"`));
      if(scene.id==='circuit'&&value==='open')assert.doesNotMatch(svg,/marker-end=/,'Open circuit has no current arrows');
      if(scene.id==='power-factor') {
        const rows=[...svg.matchAll(/data-power-factor="([^"]+)" data-real-kw="([^"]+)" data-apparent-kva="([^"]+)"/g)];
        assert.equal(rows.length,2,'Power factor compares two loads');
        for(const [,pf,kw,kva] of rows)assert.equal(Number(kw)/Number(kva),Number(pf),'Power factor is real divided by apparent power');
        assert.equal(Number(rows[1][3])/Number(rows[0][3]),1.25,'Current demand rises 25% at fixed voltage and phase arrangement');
        assert.match(svg,/Same voltage and phase arrangement/,'Current comparison states its fixed electrical conditions');
      }
      if(scene.id==='ups-types') {
        assert.match(svg,new RegExp(`data-standby-path="${value==='interrupted'?'battery-inverter-switch':'utility-switch'}"`),'Standby supply switches between utility and inverter');
        assert.match(svg,new RegExp(`data-online-path="${value==='interrupted'?'battery-dclink-inverter':'utility-rectifier-dclink-inverter'}"`),'Online inverter stays in the load path');
      }
      if(scene.id==='memory-storage')assert.match(svg,/data-loading-path="storage-ram-gpu-memory-gpu-cores"/,'The memory example shows the saved model loading into GPU memory');
      if(scene.id==='network') {
        const attr=name=>Number(svg.match(new RegExp(`data-${name}="([^"]+)"`))[1]);
        assert.equal(attr('sending-ms'),8*8/Number(value)*1000,'Serialization time uses bits, bytes and the selected payload rate');
        assert.equal(attr('travel-ms'),20,'First-bit travel stays fixed');
        assert.equal(attr('arrival-ms'),attr('sending-ms')+attr('travel-ms'),'Last-bit arrival includes sending and travel');
      }
      if(scene.id==='heat-temperature') {
        assert.match(svg,/data-heat-watts="500" data-chip-celsius="70" data-plate-celsius="45" data-inlet-celsius="30" data-outlet-celsius="35"/,'The heat path labels temperatures and transfer rate separately');
      }
    }
  }
  console.log('Passed Primer static checks: nineteen scenes, all diagram/control states, circuit and new example arithmetic, UPS supply paths, follow-up sequence, legacy aliases, and zero course-forward or reference pointers.');
  if(staticOnly)return;
  const { chromium } = require('playwright');
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
    await page.keyboard.press('ArrowRight');await page.waitForURL(/#voltage-current$/);
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
    assert.equal(await page.locator('#next').isDisabled(),true);
    assert.equal(await page.locator('a').count(),0);
    await page.goto(url('welcome',false));assert.equal(await page.locator('#fullscreen').isVisible(),false);
    await page.locator('#explain').click();assert.equal(await page.locator('#reading-title').textContent(),'Primer');
    assert.equal(await page.locator('a').count(),0);
    assert.deepEqual(errors,[]);
    console.log('Passed Primer layouts in four viewports and both themes, all control states, example arithmetic, keyboard/dialog behavior and standalone navigation.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
