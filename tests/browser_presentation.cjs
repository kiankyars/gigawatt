const { chromium } = require("playwright");
const { readFileSync, mkdirSync, writeFileSync } = require("node:fs");
const { resolve } = require("node:path");
const assert = require("node:assert/strict");
const base = process.argv[2] || "http://127.0.0.1:8765/course/";
const output = resolve(process.argv[3] || "qa/presentation");
const data = JSON.parse(
  readFileSync("course/expansion/sample-presentation.json", "utf8"),
);
let browser;
(async () => {
  mkdirSync(output, { recursive: true });
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ reducedMotion: "reduce" });
  const page = await context.newPage();
  const errors = [];
  context.on("page", observe);
  observe(page);
  function observe(p) {
    p.on("pageerror", (e) => errors.push(String(e)));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
    });
  }
  const layouts = [];
  for (const viewport of [
    { width: 1920, height: 1080 },
    { width: 1280, height: 720 },
    { width: 1024, height: 768 },
    { width: 390, height: 844 },
    { width: 844, height: 390 },
  ]) {
    await page.setViewportSize(viewport);
    for (const step of data.steps) {
      await page.goto(`${base}sample.html#${step.id}`);
      await page.reload();
      assert.equal(
        await page.locator("#scene-title").textContent(),
        step.headline,
      );
      assert.equal(await page.locator("#presenter").isVisible(), false);
      let states = [false];
      if (["current", "loss", "transfer"].includes(step.kind))
        states.push(true);
      for (const revealed of states) {
        if (revealed) await page.locator("#reveal").click();
        const layout = await page.evaluate(() => ({
          width: document.documentElement.scrollWidth,
          height: document.documentElement.scrollHeight,
          text: document.querySelector("#scene").innerText,
          clipped: [...document.querySelectorAll(".unit,.metric-card")]
            .filter((e) => e.scrollWidth > e.clientWidth + 1)
            .map((e) => e.textContent),
        }));
        assert.ok(
          layout.width <= viewport.width + 1,
          `${step.id} ${viewport.width}: horizontal overflow ${layout.width}`,
        );
        if (viewport.width >= 1024 && viewport.height >= 720)
          assert.ok(
            layout.height <= viewport.height + 1,
            `${step.id}: recording view scrolls`,
          );
        assert.deepEqual(layout.clipped, [], `${step.id}: clipped labels`);
        assert.ok(
          layout.text.split(/\s+/).length < 90,
          `${step.id}: excessive audience text`,
        );
        for (const note of step.notes) assert.ok(!layout.text.includes(note));
        layouts.push({
          step: step.id,
          viewport,
          revealed,
          horizontal_overflow: false,
        });
      }
    }
  }
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto(`${base}sample.html#current-prediction`);
  await page.reload();
  assert.ok(!(await page.locator("#visual").innerText()).includes("125"));
  await page.locator("#reveal").click();
  assert.match(await page.locator("#variable-current").textContent(), /125 A/);
  assert.equal(await page.evaluate(() => document.activeElement.id), "scene");
  await page.keyboard.press("ArrowRight");
  assert.match(page.url(), /#conductor-loss$/);
  await page.keyboard.press("ArrowLeft");
  await page.locator("#voltage").focus();
  await page.keyboard.press("Home");
  assert.equal(await page.locator("#variable-voltage").textContent(), "48");
  assert.match(
    await page.locator("#variable-current").textContent(),
    /2,083\.3/,
  );
  await page.keyboard.press("End");
  assert.match(await page.locator("#variable-current").textContent(), /125/);
  await page.screenshot({ path: resolve(output, "current-1280.png") });
  const opened = context.waitForEvent("page");
  await page.locator("#open-notes").click();
  const notes = await opened;
  await notes.waitForLoadState();
  await notes.waitForFunction(() =>
    document.querySelector("#connection").textContent.startsWith("Connected"),
  );
  assert.equal(await notes.locator("#audience").isVisible(), false);
  assert.match(
    await notes.locator("#narration").textContent(),
    /one hundred and twenty-five/,
  );
  await notes.locator("#notes-next-button").click();
  await page.waitForURL(/#conductor-loss$/);
  await notes.locator("#notes-reveal").click();
  await page.waitForFunction(() =>
    document.querySelector("#visual").textContent.includes("0.36"),
  );
  assert.match(
    await page.locator("#caption").textContent(),
    /Same conductor resistance/,
  );
  await page.screenshot({ path: resolve(output, "loss-1280.png") });
  await notes.locator('#notes-outline [data-step="1"]').click();
  await page.waitForURL(/#current-prediction$/);
  await page.locator("#voltage").focus();
  await page.keyboard.press("Home");
  await notes.waitForFunction(() =>
    document
      .querySelector("#narration")
      .textContent.includes("Live comparison: 48 V"),
  );
  await notes.screenshot({
    path: resolve(output, "presenter-notes.png"),
    fullPage: true,
  });
  await page.locator('#steps [data-step="6"]').click();
  await notes.waitForURL(/#feeder-transfer$/);
  assert.ok(!(await page.locator("#visual").innerText()).includes("200 A"));
  await page.locator("#reveal").click();
  assert.match(await page.locator("#visual").innerText(), /200 A/);
  assert.match(
    await page.locator("#visual").innerText(),
    /cannot supply 160 kW/,
  );
  assert.equal(await page.locator("#next").isDisabled(), true);
  await page.screenshot({ path: resolve(output, "transfer-1280.png") });
  await notes.close();
  await page.goto(`${base}sample.html#one-load`);
  await page.locator(".hero img").waitFor();
  await page.waitForFunction(
    () => document.querySelector(".hero img").complete,
  );
  assert.ok(
    await page.locator(".hero img").evaluate((e) => e.naturalWidth > 0),
  );
  await page.screenshot({ path: resolve(output, "intro-1280.png") });
  await page.bringToFront();
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => Boolean(document.fullscreenElement));
  assert.ok(await page.evaluate(() => Boolean(document.fullscreenElement)));
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !document.fullscreenElement);
  await page.goto(`${base}sample.html#conversion-in-rack`);
  await page.screenshot({ path: resolve(output, "architecture-1280.png") });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({
    path: resolve(output, "architecture-mobile.png"),
    fullPage: true,
  });
  await page.goto(`${base}sample-reading.html`);
  assert.ok(await page.locator("#prose").isVisible());
  assert.match(
    await page.locator("#title").textContent(),
    /What 800 V changes/,
  );
  assert.deepEqual(errors, []);
  const report = {
    checked_on: "2026-09-06",
    browser: "Headless Chromium / Playwright",
    base,
    layout_states: layouts.length,
    layouts,
    checks: [
      "One visual at a time; audience notes excluded",
      "No desktop scroll at recording sizes",
      "Mobile and short landscape overflow",
      "Prediction before reveal",
      "DC arithmetic and units",
      "Keyboard advance after reveal",
      "Slider keyboard ownership",
      "Separate presenter window",
      "Bidirectional step, reveal and voltage synchronization",
      "Fullscreen entry and exit",
      "Source reading view preserved",
    ],
    errors,
  };
  writeFileSync(
    resolve(output, "browser-report.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  console.log(
    `Passed ${layouts.length} presentation layout states, arithmetic, keyboard, fullscreen and separate-window synchronization.`,
  );
  await browser.close();
})().catch(async (error) => {
  console.error(error);
  await browser?.close();
  process.exitCode = 1;
});
