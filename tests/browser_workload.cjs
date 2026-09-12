const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const { pathToFileURL } = require("node:url");
const { resolve } = require("node:path");

const base = process.argv[2] || "http://127.0.0.1:8765/course/prototypes/workload-format.html";
const output = process.argv[3] || "/tmp/gigawatt-workload-qa";
const expectedScenes = [
  "success-brief", "model-work", "resource-paths", "inference-memory",
  "training-memory", "partition-fit", "measured-progress", "occupied-waiting",
  "energy-per-result", "batching-throughput", "gathering-latency", "arrival-capacity",
  "job-phases", "synchronized-jobs", "staggering-jobs", "independence",
  "demand-transition", "acceptance-envelope", "next-brief",
];

const close = (actual, expected, label) => assert.ok(
  Number.isFinite(actual) && Math.abs(actual - expected) < 1e-8,
  `${label}: ${actual} != ${expected}`,
);
const url = (id, teaching = false) => {
  const result = new URL(base);
  if (teaching) result.searchParams.set("teach", "1");
  else result.searchParams.delete("teach");
  result.hash = id;
  return result.href;
};
const button = (page, key, value) => page.locator(`[data-key="${key}"][data-value="${value}"]`);
const number = async (page, attribute, expected) => {
  const nodes = page.locator(`#diagram [${attribute}]`);
  assert.equal(await nodes.count(), 1, `One numeric account for ${attribute}`);
  close(Number(await nodes.getAttribute(attribute)), expected, attribute);
};
const flag = async (page, attribute, expected) => {
  const nodes = page.locator(`#diagram [${attribute}]`);
  assert.equal(await nodes.count(), 1, `One stated result for ${attribute}`);
  assert.equal(await nodes.getAttribute(attribute), String(expected), attribute);
};

async function checkQuantities(page, id, state) {
  const content = await page.locator("#diagram").textContent();
  assert.doesNotMatch(content, /\bNaN\b|\bInfinity\b/, "Invalid arithmetic cannot reach the visual");
  if (id === "inference-memory") {
    await number(page, "data-total-gb", 32 + state.workspace);
    await number(page, "data-aggregate-capacity-gb", 80);
    await flag(page, "data-aggregate-fits", true);
  }
  if (id === "training-memory") {
    await number(page, "data-total-gb", 256);
    await number(page, "data-aggregate-capacity-gb", 80 * state.devices);
    await flag(page, "data-aggregate-fits", state.devices === 4);
  }
  if (id === "partition-fit") {
    await number(page, "data-total-gb", 256);
    await number(page, "data-aggregate-capacity-gb", 320);
    await flag(page, "data-partition-fits", state.partition === "balanced");
  }
  if (id === "occupied-waiting") {
    const expected = { A: [51.25, 3075 / 3600, 45000, 1], B: [42.5, 2550 / 3600, 30000, 1], idle: [12, 0.2, 0, 0] }[state.observation];
    for (const [index, attribute] of ["data-average-kw", "data-energy-kwh", "data-accepted-samples", "data-allocation-fraction"].entries())
      await number(page, attribute, expected[index]);
  }
  if (id === "energy-per-result") {
    const expected = { B: [2550 / 3600, 85], C: [3250 / 3600, 65], idle: [0.2, null] }[state.energyCase];
    await number(page, "data-energy-kwh", expected[0]);
    if (expected[1] === null) await flag(page, "data-joules-per-sample", "undefined");
    else await number(page, "data-joules-per-sample", expected[1]);
  }
  if (["batching-throughput", "arrival-capacity"].includes(id))
    await number(page, "data-capacity-rps", state.batch === 1 ? 125 : 200);
  if (id === "arrival-capacity") await flag(page, "data-overloaded", state.batch === 1);
  if (id === "gathering-latency") {
    await number(page, "data-max-latency-ms", state.arrivals === 6 ? 38 : 56);
    await number(page, "data-mean-latency-ms", state.arrivals === 6 ? 29 : 38);
  }
  if (["job-phases", "synchronized-jobs", "staggering-jobs"].includes(id)) {
    const one = id === "job-phases";
    await number(page, "data-average-kw", one ? 85 : 340);
    await number(page, "data-peak-kw", one ? 120 : id === "staggering-jobs" && state.schedule === "staggered" ? 340 : 480);
    await number(page, "data-energy-kwh", one ? 17 / 12 : 17 / 3);
  }
  if (id === "acceptance-envelope" && state.acceptanceReveal) {
    await flag(page, "data-meets-latency", state.latency === 40);
    await flag(page, "data-numerical-pass", state.latency === 40);
  }
  if (id === "demand-transition")
    await number(page, "data-transition-rate-kw-per-second", -160);
}

async function checkSelection(page, scene, state) {
  for (const group of scene.controls || []) {
    const controls = page.locator(`#actions [data-key="${group.key}"]`);
    assert.equal(await controls.count(), group.options.length);
    assert.equal(await page.locator(`#actions [data-key="${group.key}"][aria-pressed="true"]`).count(), 1);
    assert.equal(await button(page, group.key, state[group.key]).getAttribute("aria-pressed"), "true");
    const styles = await controls.evaluateAll((elements) => elements.map((element) => ({
      selected: element.getAttribute("aria-pressed") === "true",
      background: getComputedStyle(element).backgroundColor,
    })));
    const selected = styles.find((item) => item.selected);
    assert.ok(styles.filter((item) => !item.selected).every((item) => item.background !== selected.background), "Selected control needs a visible state");
  }
  if (scene.reveal)
    assert.equal(await page.locator("#reveal").getAttribute("aria-expanded"), String(state[scene.reveal]));
}

async function checkGeometry(page, viewport) {
  const result = await page.evaluate(() => {
    const svg = document.querySelector("#diagram");
    const viewBox = svg.viewBox.baseVal;
    const failures = [];
    const fits = (a, b, margin = 0) => a.x >= b.x + margin && a.y >= b.y + margin
      && a.x + a.width <= b.x + b.width - margin && a.y + a.height <= b.y + b.height - margin;
    const texts = [...svg.querySelectorAll("text")];
    for (const label of texts) {
      if (!fits(label.getBBox(), viewBox, -1)) failures.push(`Text outside SVG: ${label.textContent}`);
      if (label.dataset.labelFor) {
        const owner = svg.querySelector(`#${CSS.escape(label.dataset.labelFor)}`);
        if (!owner || !fits(label.getBBox(), owner.getBBox(), 2))
          failures.push(`Text outside its object: ${label.textContent}`);
      }
    }
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].getBBox(), b = texts[j].getBBox();
      if (Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x) > 1
        && Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y) > 1)
        failures.push(`Overlapping labels: ${texts[i].textContent} / ${texts[j].textContent}`);
    }
    const rect = svg.getBoundingClientRect();
    const header = document.querySelector("main > header").getBoundingClientRect();
    const actions = document.querySelector("#actions").getBoundingClientRect();
    const footer = document.querySelector("footer").getBoundingClientRect();
    if (header.bottom > rect.top + 1) failures.push("Heading overlaps diagram");
    if (actions.height && rect.bottom > actions.top + 1) failures.push("Diagram overlaps controls");
    if (Math.max(rect.bottom, actions.bottom) > footer.top + 1) failures.push("Content overlaps footer");
    if ([...document.querySelectorAll("main .eyebrow, #boundary, main .subtitle")]
      .some((element) => element.getBoundingClientRect().height > 0))
      failures.push("A repeated subtitle or boundary layer is visible on the stage");
    return { failures, width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight, footerBottom: footer.bottom };
  });
  assert.deepEqual(result.failures, [], "SVG and control layout");
  assert.ok(result.width <= viewport.width + 1, "No horizontal page overflow");
  if (viewport.width >= 1024) {
    assert.ok(result.height <= viewport.height + 1, "Desktop presentation must fit vertically");
    assert.ok(result.footerBottom <= viewport.height + 1, "Desktop navigation stays visible");
  }
}

async function checkNavigation(page) {
  await page.goto(url("success-brief"));
  await page.waitForSelector("#diagram text");
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("ArrowLeft");
  assert.equal(new URL(page.url()).hash, "#success-brief");
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, "#model-work");
  await button(page, "service", "inference").focus();
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, "#model-work", "A focused control keeps its arrow keys");
  const selectConsumed = await page.locator("#scenes").evaluate((select) => {
    select.focus();
    const event = new KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true, cancelable: true });
    select.dispatchEvent(event);
    return event.defaultPrevented;
  });
  assert.equal(selectConsumed, false);
  await page.locator("#scenes").selectOption("next-brief");
  assert.equal(await page.locator("#next").isDisabled(), true);
  await page.locator("#previous").click();
  assert.equal(new URL(page.url()).hash, "#acceptance-envelope");
  const initial = await page.locator("#reveal").getAttribute("aria-expanded");
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("r");
  assert.notEqual(await page.locator("#reveal").getAttribute("aria-expanded"), initial);
  await page.locator("#explain").click();
  assert.equal(await page.locator("#reading").evaluate((dialog) => dialog.open), true);
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, "#acceptance-envelope");
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("#reading").evaluate((dialog) => dialog.open), false);
  await page.locator("#explain").click();
  await page.locator("#close-reading").click();
  assert.equal(await page.locator("#reading").evaluate((dialog) => dialog.open), false);
  assert.equal(await page.locator("#fullscreen").isVisible(), false);
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("f");
  assert.equal(await page.evaluate(() => !!document.fullscreenElement), false);
  await page.goto(url("success-brief", true));
  await page.waitForSelector("#diagram text");
  assert.equal(await page.locator("#fullscreen").isVisible(), true);
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !!document.fullscreenElement);
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !document.fullscreenElement);
}

(async () => {
  const { scenes, initialState } = await import(pathToFileURL(resolve(__dirname, "../course/prototypes/workload-scenes.js")));
  assert.deepEqual(scenes.map((scene) => scene.id), expectedScenes);
  mkdirSync(output, { recursive: true });
  const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
  const browser = await chromium.launch(executablePath ? { executablePath } : {});
  const errors = [], failures = [];
  let layouts = 0;
  try {
    for (const colorScheme of ["light", "dark"]) for (const viewport of [
      { width: 1280, height: 720 }, { width: 1440, height: 900 },
      { width: 390, height: 844 }, { width: 844, height: 390 },
    ]) {
      const touch = viewport.width === 390;
      const page = await browser.newPage({ viewport, colorScheme, hasTouch: touch, reducedMotion: "reduce" });
      page.on("pageerror", (error) => errors.push(String(error)));
      page.on("response", (response) => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
      page.on("requestfailed", (request) => errors.push(`${request.failure()?.errorText} ${request.url()}`));
      const state = { ...initialState };
      await page.goto(url(scenes[0].id));
      await page.waitForSelector("#diagram text");
      assert.equal(await page.locator("#scenes option").count(), 19);
      for (const scene of scenes) {
        await page.locator("#scenes").selectOption(scene.id);
        const configurations = (scene.controls || []).flatMap((group) => group.options.map(([value]) => ({ key: group.key, value })));
        if (!configurations.length) configurations.push({});
        if (scene.reveal) {
          configurations.push({ reveal: true });
          // Change the limit while the verdict is visible; the earlier choices
          // alone exercise only the prediction view and could miss a stale result.
          configurations.push(...(scene.controls || []).flatMap((group) =>
            group.options.map(([value]) => ({ key: group.key, value, afterReveal: true }))));
        }
        for (const configuration of configurations) {
          const name = `${scene.id}-${configuration.value ?? (configuration.reveal ? "revealed" : "default")}${configuration.afterReveal ? "-revealed" : ""}-${viewport.width}-${colorScheme}`;
          try {
            if (configuration.key) {
              const control = button(page, configuration.key, configuration.value);
              if (touch) await control.tap();
              else { await control.focus(); await page.keyboard.press("Enter"); }
              state[configuration.key] = configuration.value;
              if (!touch) assert.equal(await control.evaluate((element) => element === document.activeElement), true, "Changing state preserves focus");
              if (touch) await control.tap(); else await page.keyboard.press("Space");
            }
            if (configuration.reveal) {
              await page.locator("#reveal").click();
              state[scene.reveal] = !state[scene.reveal];
            }
            assert.equal(await page.locator("h1:visible").count(), 1);
            assert.ok((await page.locator("#diagram-description").textContent()).length > 30, "The visual has a useful text alternative");
            await checkSelection(page, scene, state);
            await checkQuantities(page, scene.id, state);
            await checkGeometry(page, viewport);
            if ([1280, 390].includes(viewport.width) && (configuration === configurations.at(-1)))
              await page.screenshot({ path: `${output}/${name}.png`, fullPage: true });
            layouts++;
          } catch (error) {
            failures.push(`${name}: ${error.message}`);
            await page.screenshot({ path: `${output}/FAIL-${name}.png`, fullPage: true });
          }
        }
        // Settings and reveal state survive leaving and restoring the scene.
        if (scene.controls || scene.reveal) {
          await page.locator("#scenes").selectOption(scene.id === scenes[0].id ? scenes.at(-1).id : scenes[0].id);
          await page.locator("#scenes").selectOption(scene.id);
          await checkSelection(page, scene, state);
          await checkQuantities(page, scene.id, state);
        }
      }
      try { await checkNavigation(page); }
      catch (error) { failures.push(`Navigation ${viewport.width}-${colorScheme}: ${error.message}`); }
      await page.close();
    }
    assert.deepEqual(errors, [], "No browser errors or failed resources");
    assert.deepEqual(failures, [], "Workload regression failures");
    console.log(`Passed ${layouts} workload scene/state layouts across four viewports and both themes, quantitative states, control restoration, touch, keyboard, reveals, dialogs and teaching fullscreen.`);
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exit(1); });
