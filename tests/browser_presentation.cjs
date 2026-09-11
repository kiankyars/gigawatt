const { chromium } = require("playwright");
const { readFileSync, mkdirSync, writeFileSync, rmSync } = require("node:fs");
const { resolve } = require("node:path");
const assert = require("node:assert/strict");
const base = process.argv[2] || "http://127.0.0.1:8765/course/";
const output = resolve(process.argv[3] || "qa/presentation");
const data = JSON.parse(
  readFileSync("course/expansion/sample-presentation.json", "utf8"),
);
const revealKinds = new Set(["current", "loss", "conversion-loss"]);
const stepById = (id) => {
  const step = data.steps.find((item) => item.id === id);
  assert.ok(step, `Unknown step: ${id}`);
  return step;
};
const stepSelector = (container, id) =>
  `${container} [data-step="${data.steps.indexOf(stepById(id))}"]`;
const near = (actual, expected) =>
  assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} ≠ ${expected}`);
let browser;
(async () => {
  mkdirSync(output, { recursive: true });
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ reducedMotion: "reduce" });
  const errors = [];
  context.on("page", (p) => {
    p.on("pageerror", (e) => errors.push(String(e)));
    p.on("response", (r) => {
      if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
    });
  });
  const page = await context.newPage();
  async function fresh(mode, id) {
    await page.goto(
      `${base}${mode === "teach" ? "teach" : "sample"}.html#${id}`,
    );
    await page.reload();
  }
  async function setRange(id, value) {
    await page.locator(`#${id}`).evaluate((input, next) => {
      input.value = String(next);
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }, value);
  }
  const layouts = [];
  assert.deepEqual(
    data.steps.slice(1, 5).map((s) => s.kind),
    ["dc-basics", "ac-basics", "three-phase", "voltage-basis"],
  );
  assert.equal(data.steps.at(-1).id, "conversion-farther-upstream");
  assert.equal(data.steps.at(-1).kind, "facility");
  assert.ok(!JSON.stringify(data).toLowerCase().includes("recording setup"));
  const pathStep = stepById("ac-dc-ledger");
  assert.doesNotMatch(
    JSON.stringify(pathStep),
    /\b103\.1\b|\b106\.1\b|\b4\.9\b|\b1\.9\b|\b1\.1\b/,
    "Complete-path narration must use the calculated conductor losses",
  );
  for (const mode of ["teach", "student"]) {
    for (const viewport of [
      { width: 1920, height: 1080 },
      { width: 1280, height: 720 },
      { width: 1024, height: 768 },
      { width: 390, height: 844 },
      { width: 844, height: 390 },
    ]) {
      await page.setViewportSize(viewport);
      for (const step of data.steps) {
        await fresh(mode, step.id);
        assert.equal(
          await page.locator("body").getAttribute("data-view"),
          mode,
        );
        assert.equal(await page.locator("#caption").count(), 0);
        assert.equal(
          await page.locator("#scene-title").textContent(),
          step.headline,
        );
        assert.equal(await page.locator("#presenter").isVisible(), false);
        assert.equal(
          await page.locator("#open-notes").isVisible(),
          mode === "teach",
        );
        assert.equal(
          await page.locator("#fullscreen").isVisible(),
          mode === "teach",
        );
        assert.equal(
          await page.locator("#student-context").isVisible(),
          mode === "student",
        );
        assert.equal(
          await page.locator("#steps button").count(),
          data.steps.length,
        );
        assert.equal(
          await page.locator("#next").isDisabled(),
          step.id === "conversion-farther-upstream",
        );
        if (step.kind === "conversion-loss") {
          assert.equal(await page.locator(".stepdown-path section").count(), 3);
          const supplyBounds = await page.evaluate(() => ({
            width: document.documentElement.scrollWidth,
            bottom: document
              .querySelector(".stepdown-example")
              .getBoundingClientRect().bottom,
            footer: document.querySelector(".transport").getBoundingClientRect()
              .top,
            titleBottom: document
              .querySelector("#scene-title")
              .getBoundingClientRect().bottom,
            controlsTop: document
              .querySelector(".conversion-views")
              .getBoundingClientRect().top,
          }));
          assert.ok(
            supplyBounds.width <= viewport.width + 1,
            "Step-down diagram overflows horizontally",
          );
          assert.ok(
            supplyBounds.bottom <= supplyBounds.footer + 1,
            "Step-down diagram overlaps navigation",
          );
          assert.ok(
            supplyBounds.titleBottom <= supplyBounds.controlsTop + 1,
            "Step-down controls overlap headline",
          );
          await page.screenshot({
            path: `${output}/${mode}-stepdown-${viewport.width}.png`,
            fullPage: true,
          });
          await page.locator('[data-converter-view="heat"]').click();
          assert.equal(
            await page.locator("#scene-title").textContent(),
            step.heat_headline,
          );
        }
        for (const revealed of revealKinds.has(step.kind)
          ? [false, true]
          : [false]) {
          if (revealed) await page.locator("#reveal").click();
          const layout = await page.evaluate(() => ({
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight,
            text: document.querySelector("#scene").innerText,
            equationBottom:
              document
                .querySelector(".converter-example .equation-block")
                ?.getBoundingClientRect().bottom ?? 0,
            footerTop: document
              .querySelector(".transport")
              .getBoundingClientRect().top,
            clipped: [
              ...document.querySelectorAll(
                ".unit,.metric-card,.ledger-card,.ledger-total,.copper-result,.capacity-result,.capacity-row > *,#steps,.transport",
              ),
            ]
              .filter((e) => e.scrollWidth > e.clientWidth + 1)
              .map((e) => e.textContent),
          }));
          assert.ok(
            layout.width <= viewport.width + 1,
            `${mode}/${step.id} ${viewport.width}: horizontal overflow ${layout.width}`,
          );
          if (
            mode === "teach" &&
            viewport.width >= 1024 &&
            viewport.height >= 720
          )
            assert.ok(
              layout.height <= viewport.height + 1,
              `${step.id} ${viewport.width}×${viewport.height}: teaching view scrolls (${layout.height})`,
            );
          assert.ok(
            layout.equationBottom <= layout.footerTop + 1,
            `${mode}/${step.id}: converter equation overlaps navigation`,
          );
          assert.deepEqual(
            layout.clipped,
            [],
            `${mode}/${step.id}: clipped labels`,
          );
          for (const note of step.notes) assert.ok(!layout.text.includes(note));
          assert.doesNotMatch(
            layout.text,
            /NaN|Infinity|150 kW|160 kW|\b48 V DC\b|2,?083|0\.36\s*%/,
          );
          layouts.push({
            mode,
            step: step.id,
            viewport,
            revealed,
            horizontal_overflow: false,
            document_height: layout.height,
          });
        }
        if (mode === "student") {
          await page.locator("#student-context summary").click();
          assert.equal(
            await page.locator("#student-explanation").isVisible(),
            true,
          );
          assert.ok(
            (await page.locator("#student-explanation").textContent()).includes(
              step.explanation[0],
            ),
          );
          assert.ok(
            await page.evaluate(
              () => document.documentElement.scrollWidth <= innerWidth + 1,
            ),
          );
        }
      }
    }
  }
  await page.setViewportSize({ width: 1280, height: 720 });
  await fresh("student", "one-load");
  const pagesBefore = context.pages().length;
  await page.keyboard.press("p");
  await page.keyboard.press("f");
  assert.equal(context.pages().length, pagesBefore);
  assert.equal(
    await page.evaluate(() => Boolean(document.fullscreenElement)),
    false,
  );
  await page.locator("#student-context summary").click();
  await page.screenshot({
    path: resolve(output, "student-explanation-1280.png"),
    fullPage: true,
  });
  await fresh("teach", "conductor-copper");
  assert.equal(
    await page.locator('.copper-bundle[data-supply="ac"] .copper-bar').count(),
    3,
  );
  assert.equal(
    await page.locator('.copper-bundle[data-supply="dc"] .copper-bar').count(),
    2,
  );
  const copperGeometry = await page.locator(".copper-bar").evaluateAll((bars) =>
    bars.map((bar) => {
      const bounds = bar.getBoundingClientRect();
      return { width: bounds.width, height: bounds.height };
    }),
  );
  for (const conductor of copperGeometry) {
    near(conductor.width, copperGeometry[0].width);
    near(conductor.height, copperGeometry[0].height);
  }
  assert.equal(await page.locator(".copper-result").count(), 0);
  assert.match(
    await page.locator(".copper-bundle").first().getAttribute("aria-label"),
    /equal length and cross-section/,
  );
  assert.equal(await page.locator("#reveal").count(), 0);
  assert.match(
    await page.locator(".model-top").innerText(),
    /Equal length, cross-section and material/,
  );
  await page.screenshot({ path: resolve(output, "copper-1280.png") });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({
    path: resolve(output, "copper-mobile.png"),
    fullPage: true,
  });
  await page.setViewportSize({ width: 1280, height: 720 });
  await fresh("teach", "current-prediction");
  assert.equal(
    await page
      .locator(".metric-card")
      .first()
      .locator(".conductor-lines > div")
      .count(),
    3,
  );
  assert.equal(
    await page.locator(".metric-card.changed .conductor-lines > div").count(),
    2,
  );
  assert.ok(!(await page.locator("#visual").innerText()).includes("125"));
  await page.locator("#reveal").click();
  assert.match(await page.locator("#variable-current").textContent(), /125 A/);
  assert.equal(await page.evaluate(() => document.activeElement.id), "scene");
  await page.keyboard.press("ArrowRight");
  assert.match(page.url(), /#conductor-loss$/);
  await page.keyboard.press("ArrowLeft");
  await page.locator("#voltage").focus();
  await page.keyboard.press("Home");
  assert.equal(await page.locator("#variable-voltage").textContent(), "400");
  assert.match(await page.locator("#variable-current").textContent(), /250 A/);
  await page.keyboard.press("End");
  assert.match(await page.locator("#variable-current").textContent(), /100 A/);
  await setRange("voltage", 480);
  assert.match(
    await page.locator("#variable-current").textContent(),
    /208\.3 A/,
  );
  assert.match(
    await page.locator(".metric-card").first().innerText(),
    /120\.3 A/,
  );
  await page.locator("#reset-voltage").click();
  assert.match(await page.locator("#variable-current").textContent(), /125 A/);
  await page.screenshot({ path: resolve(output, "current-1280.png") });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({
    path: resolve(output, "current-mobile.png"),
    fullPage: true,
  });
  await page.setViewportSize({ width: 1280, height: 720 });
  const opened = context.waitForEvent("page");
  await page.locator("#open-notes").click();
  const notes = await opened;
  await notes.waitForLoadState();
  await notes.waitForFunction(() =>
    document.querySelector("#connection").textContent.startsWith("Connected"),
  );
  assert.equal(await notes.locator("#audience").isVisible(), false);
  assert.match(await notes.locator("#narration").textContent(), /125 A/);
  assert.equal(await notes.locator(".speaker-points li").count(), 4);
  assert.doesNotMatch(
    await notes.locator("body").innerText(),
    /recording setup/i,
  );
  assert.match(
    await notes.locator("#audience-link").getAttribute("href"),
    /^teach\.html\?session=/,
  );
  await notes.locator("#notes-next-button").click();
  await page.waitForURL(/#conductor-loss$/);
  await notes.locator("#notes-reveal").click();
  await page.waitForFunction(() =>
    document.querySelector("#visual").textContent.includes("312.5"),
  );
  assert.match(
    await page.locator("#visual").textContent(),
    /10 mΩ per conductor/,
  );
  await page.screenshot({ path: resolve(output, "loss-1280.png") });
  await notes
    .locator(stepSelector("#notes-outline", "current-prediction"))
    .click();
  await page.waitForURL(/#current-prediction$/);
  await page.locator("#voltage").focus();
  await setRange("voltage", 480);
  await notes.waitForFunction(() =>
    document
      .querySelector("#narration")
      .textContent.includes("Live DC comparison: 480 V"),
  );
  const models = await page.evaluate(() => ({
    feeder: acdcConductorModel(100, 480, 800, 1, 0.01, 1),
    equalVoltage: acdcConductorModel(100, 480, 480, 1, 0.01, 1),
    complete: acdcDeliveryModel(100, 480, 800, 1, 0.01, 1, 4, 3, 1),
    crossover: acdcDeliveryModel(
      100,
      480,
      800,
      1,
      0.01,
      1,
      4,
      4.137030473977177,
      1,
    ),
  }));
  near(models.feeder.ac.amps, 120.28130608117203);
  near(models.feeder.dc.amps, 125);
  assert.equal(models.feeder.ac.conductors, 3);
  assert.equal(models.feeder.dc.conductors, 2);
  near(models.feeder.ac.lossKW, 0.4340277777777778);
  near(models.feeder.dc.lossKW, 0.3125);
  near(models.feeder.ac.inputKW, 100.43402777777777);
  near(models.feeder.dc.inputKW, 100.3125);
  near(models.feeder.ac.inputKWh - models.feeder.dc.inputKWh, 0.12152777777777);
  near(models.feeder.lossRatio, 0.72);
  for (const model of [models.feeder.ac, models.feeder.dc]) {
    near(model.inputKW, 100 + model.lossKW);
    near(model.inputKWh, model.deliveredKWh + model.lossKWh);
  }
  near(models.equalVoltage.dc.amps, 208.33333333333334);
  near(models.equalVoltage.dc.lossKW, 2 * models.equalVoltage.ac.lossKW);
  near(models.complete.ac.inputKW, 104.46944444444445);
  near(models.complete.dc.inputKW, 103.325125);
  near(models.complete.ac.feederKW, 104);
  near(models.complete.dc.feederKW, 102);
  near(models.crossover.ac.inputKW, models.crossover.dc.inputKW);
  await page.locator(stepSelector("#steps", "ac-dc-ledger")).click();
  await notes.waitForURL(/#ac-dc-ledger$/);
  assert.equal(await page.locator("#dc-conversion").count(), 0);
  assert.equal(await page.locator("#next").isDisabled(), false);
  await page.locator('[data-converter-view="heat"]').click();
  assert.match(await page.locator(".power-port").first().innerText(), /\?/);
  await notes.locator("#notes-reveal").click();
  await page.waitForFunction(() =>
    document.querySelector(".converter-heat").textContent.includes("2.04"),
  );
  assert.match(await page.locator(".power-port").first().innerText(), /102.04/);
  assert.match(await page.locator(".power-port").last().innerText(), /100/);
  assert.match(
    await page.locator(".converter-heat").innerText(),
    /2.04 kW\s+converter heat/,
  );
  assert.match(
    await page.locator(".converter-example").innerText(),
    /One AC\/DC power supply.*98% efficiency assumed/,
  );
  const conversion = await page.evaluate(() => ({
    input: DEFAULTS.power_kw / DEFAULTS.converter_efficiency,
    output: DEFAULTS.power_kw,
    efficiency: DEFAULTS.converter_efficiency,
  }));
  near(conversion.input, 102.04081632653062);
  near(conversion.output / conversion.input, 0.98);
  near(conversion.input - conversion.output, 2.040816326530617);
  assert.match(
    await page.locator(".power-port").first().innerText(),
    /480 V three-phase AC input/,
  );
  assert.match(
    await page.locator(".power-port").last().innerText(),
    /800 V DC output/,
  );
  await page.screenshot({ path: resolve(output, "converter-loss-1280.png") });
  await notes.screenshot({
    path: resolve(output, "presenter-notes.png"),
    fullPage: true,
  });
  await notes.locator("#notes-reveal").click();
  await page.locator("#reveal").waitFor();
  await notes.locator("#notes-reveal").click();
  await page.waitForFunction(() =>
    document.querySelector(".converter-heat").textContent.includes("2.04"),
  );
  await page
    .locator(stepSelector("#steps", "conversion-farther-upstream"))
    .click();
  await notes.waitForURL(/#conversion-farther-upstream$/);
  assert.equal(await page.locator("#next").isDisabled(), true);
  assert.doesNotMatch(
    await page.locator("#visual").innerText(),
    /200 kW|250 A/,
  );
  await notes.close();
  await fresh("teach", "one-load");
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
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !document.fullscreenElement);
  await fresh("teach", "conversion-in-rack");
  await page.screenshot({ path: resolve(output, "architecture-1280.png") });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({
    path: resolve(output, "architecture-mobile.png"),
    fullPage: true,
  });
  for (const [id, filename] of [
    ["conversion-in-sidecar", "sidecar"],
    ["conversion-farther-upstream", "facility-dc"],
  ]) {
    await page.setViewportSize({ width: 1280, height: 720 });
    await fresh("teach", id);
    assert.match(await page.locator(".rack-space").innerText(), /Freed/);
    assert.equal(await page.locator(".zone.rack .unit.converter").count(), 1);
    assert.match(
      await page.locator(".roadmap-context").innerText(),
      id === "conversion-in-sidecar"
        ? /Phases 1–2.*2026\/27 and 2027\/28/
        : /Phase 3.*late 2028\/2029/,
    );
    assert.match(
      await page.locator(".roadmap-context").innerText(),
      /SemiAnalysis forecast/,
    );
    const zones = page.locator(".zone");
    if (id === "conversion-in-sidecar") {
      assert.match(await zones.nth(0).innerText(), /Facility AC/);
      assert.match(await zones.nth(1).innerText(), /AC → DC/);
    } else {
      assert.match(await zones.nth(0).innerText(), /AC → DC/);
      assert.match(await zones.nth(1).innerText(), /800 V DC/);
    }
    await page.screenshot({ path: resolve(output, `${filename}-1280.png`) });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({
      path: resolve(output, `${filename}-mobile.png`),
      fullPage: true,
    });
  }
  await fresh("student", "ac-dc-ledger");
  await page.locator('[data-converter-view="heat"]').click();
  await page.locator("#reveal").click();
  await page.screenshot({
    path: resolve(output, "student-ledger-mobile.png"),
    fullPage: true,
  });
  for (const mode of ["teach", "student"]) {
    await fresh(mode, "feeder-transfer");
    assert.equal(
      await page.locator("#scene-title").textContent(),
      pathStep.headline,
    );
    assert.doesNotMatch(
      await page.locator("#visual").innerText(),
      /150 kW|160 kW|200 A/,
    );
  }
  await fresh("teach", "capacity-check");
  assert.equal(
    await page.locator("#scene-title").textContent(),
    stepById("conversion-farther-upstream").headline,
  );
  await fresh("teach", "energy-balance");
  assert.equal(
    await page.locator("#scene-title").textContent(),
    stepById("conductor-loss").headline,
  );
  await page.goto(`${base}sample-reading.html`);
  assert.ok(await page.locator("#prose").isVisible());
  assert.match(
    await page.locator("#title").textContent(),
    /800 V DC: less copper, room for compute/,
  );
  for (const viewport of [
    { width: 390, height: 844 },
    { width: 1440, height: 1000 },
  ]) {
    await page.setViewportSize(viewport);
    assert.ok(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
      "AC/DC reading lab must not overflow horizontally",
    );
  }
  await page
    .locator("#lab")
    .screenshot({ path: resolve(output, "reading-acdc-lab.png") });
  assert.equal(await page.locator("#lab-volts").inputValue(), "800");
  assert.equal(await page.locator("#lab-pf").inputValue(), "1");
  assert.match(
    await page.locator("#lab-boundary").innerText(),
    /480 V AC line-to-line RMS/,
  );
  assert.match(await page.locator("#lab-output").innerText(), /72% of AC loss/);
  assert.doesNotMatch(
    await page.locator("#lab").innerText(),
    /\b48 V DC\b|2,?083|0\.36\s*%/,
  );
  await setRange("lab-volts", 480);
  assert.match(
    await page.locator("#lab-output").innerText(),
    /200% of AC loss/,
  );
  await page.locator('[data-arch="hybrid"]').click();
  assert.equal(await page.locator("#lab-volts").inputValue(), "480");
  for (const control of ["lab-kw", "lab-volts", "lab-pf", "lab-resistance"]) {
    await page.locator(`#${control}`).focus();
    await page.keyboard.press("Home");
    assert.doesNotMatch(
      await page.locator("#lab-output").innerText(),
      /NaN|Infinity|undefined/,
    );
    await page.keyboard.press("End");
    assert.doesNotMatch(
      await page.locator("#lab-output").innerText(),
      /NaN|Infinity|undefined/,
    );
  }
  assert.equal(
    layouts.length,
    10 *
      data.steps.reduce(
        (n, step) => n + (revealKinds.has(step.kind) ? 2 : 1),
        0,
      ),
  );
  assert.deepEqual(errors, []);
  rmSync(resolve(output, "transfer-1280.png"), { force: true });
  const report = {
    checked_on: new Date().toISOString().slice(0, 10),
    browser: "Headless Chromium / Playwright",
    base,
    layout_states: layouts.length,
    layouts,
    checks: [
      "Twelve visual steps and three reveal states in teaching and student modes at five viewport sizes",
      "Teaching notes excluded from visuals and no recording-setup instructions",
      "No teaching-view scroll at 1920×1080, 1280×720 or 1024×768",
      "No horizontal overflow or clipped labels on phone and short landscape",
      "Student explanations expand for all twelve steps at all five sizes",
      "Student mode hides notes/fullscreen and P/F shortcuts do not activate them",
      "Prediction before reveal for currents, conductor loss, the single converter energy balance",
      "Equal-geometry copper comparison: three bars versus two, 33.3% less conductor copper",
      "Moved conversion: sidecar retains upstream AC and nearby footprint; facility DC moves conversion to power room",
      "All twelve footer steps remain accessible without horizontal overflow; upstream conversion resolves the architecture question",
      "480 V balanced three-phase AC versus 800 V DC: current, conductor count, 72% heat ratio and energy balance",
      "Single converter balance at an explicit illustrative 98% efficiency",
      "Keyboard advance after reveal and slider keyboard ownership",
      "Separate presenter window with bidirectional navigation/reveal synchronization",
      "Voltage and answer state synchronized to notes",
      "Fullscreen entry and exit in teaching mode",
      "Old feeder-transfer hash routes to the converter-loss example",
      "Reading view uses the AC/DC calculator, including the equal-voltage counterexample and control endpoints",
    ],
    errors,
  };
  writeFileSync(
    resolve(output, "browser-report.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  console.log(
    `Passed ${layouts.length} layout states, student explanations, loss budgets, keyboard, mode separation and notes synchronization.`,
  );
  await browser.close();
})().catch(async (error) => {
  console.error(error);
  await browser?.close();
  process.exitCode = 1;
});
