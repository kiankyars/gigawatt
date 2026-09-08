const { chromium } = require("playwright");
const { readFileSync, mkdirSync, writeFileSync, rmSync } = require("node:fs");
const { resolve } = require("node:path");
const assert = require("node:assert/strict");
const base = process.argv[2] || "http://127.0.0.1:8765/course/";
const output = resolve(process.argv[3] || "qa/presentation");
const data = JSON.parse(
  readFileSync("course/expansion/sample-presentation.json", "utf8"),
);
const revealKinds = new Set(["current", "loss", "energy", "paths"]);
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
  assert.equal(data.steps.length, 8);
  assert.ok(!JSON.stringify(data).toLowerCase().includes("recording setup"));
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
        for (const revealed of revealKinds.has(step.kind)
          ? [false, true]
          : [false]) {
          if (revealed) await page.locator("#reveal").click();
          const layout = await page.evaluate(() => ({
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight,
            text: document.querySelector("#scene").innerText,
            clipped: [
              ...document.querySelectorAll(
                ".unit,.metric-card,.ledger-card,.ledger-total",
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
          assert.deepEqual(
            layout.clipped,
            [],
            `${mode}/${step.id}: clipped labels`,
          );
          for (const note of step.notes) assert.ok(!layout.text.includes(note));
          assert.doesNotMatch(layout.text, /NaN|Infinity|150 kW|160 kW/);
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
  await fresh("teach", "current-prediction");
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
  await page.locator('#steps [data-step="6"]').click();
  await notes.waitForURL(/#energy-balance$/);
  assert.equal(
    await page
      .locator(".ledger-total strong")
      .allTextContents()
      .then((items) => items.every((s) => s.startsWith("?"))),
    true,
  );
  await notes.locator("#notes-reveal").click();
  await page.waitForFunction(() =>
    document.querySelector(".ledger-result").textContent.includes("4.325"),
  );
  assert.match(await page.locator("#visual").innerText(), /104\.34/);
  assert.match(await page.locator("#visual").innerText(), /100\.016/);
  assert.match(
    await page.locator("#visual").innerText(),
    /4\.325 kWh less input over 1 h/,
  );
  const models = await page.evaluate(() => ({
    low: dcConductorModel(100, 48, 0.001, 1),
    high: dcConductorModel(100, 800, 0.001, 1),
    ac: deliveryPathModel(100, 4, 1, 1),
    dc: deliveryPathModel(100, 3, 0.1, 1),
  }));
  near(models.low.inputKW, 104.34027777777777);
  near(models.high.inputKW, 100.015625);
  near(models.low.inputKWh - models.high.inputKWh, 4.32465277777777);
  for (const model of [models.low, models.high]) {
    near(model.inputKW, 100 + model.lossKW);
    near((model.sendingVolts * model.amps) / 1000, model.inputKW);
  }
  near(models.ac.inputKW, 105);
  near(models.dc.inputKW, 103.1);
  await page.screenshot({ path: resolve(output, "energy-balance-1280.png") });
  await notes.locator("#notes-next-button").click();
  await page.waitForURL(/#ac-dc-ledger$/);
  assert.equal(await page.locator("#next").isDisabled(), true);
  await page.locator("#reveal").click();
  await notes.waitForFunction(() =>
    document
      .querySelector("#narration")
      .textContent.includes("Live DC conversion loss: 3 kW"),
  );
  assert.match(
    await page.locator("#path-result").textContent(),
    /1\.9 kWh less/,
  );
  assert.match(await page.locator("#dc-path-card").innerText(), /103\.1/);
  await page.screenshot({ path: resolve(output, "ac-dc-default-1280.png") });
  const pathCases = [
    [1, 101.1, "DC uses 3.9 kWh less input over 1 h"],
    [4.9, 105, "Same input energy over 1 h"],
    [6, 106.1, "DC uses 1.1 kWh more input over 1 h"],
    [7, 107.1, "DC uses 2.1 kWh more input over 1 h"],
  ];
  for (const [conversion, input, result] of pathCases) {
    await setRange("dc-conversion", conversion);
    assert.equal(await page.locator("#path-result").textContent(), result);
    near(
      Number(
        (await page.locator("#dc-path-card .ledger-total strong").textContent())
          .replace("kW", "")
          .trim(),
      ),
      input,
    );
    await notes.waitForFunction(
      (value) =>
        document
          .querySelector("#narration")
          .textContent.includes(`Live DC conversion loss: ${value} kW`),
      conversion,
    );
  }
  await setRange("dc-conversion", 6);
  await notes.waitForFunction(() =>
    document.querySelector("#narration").textContent.includes("1.1 kWh more"),
  );
  await page.screenshot({ path: resolve(output, "ac-dc-reversed-1280.png") });
  await notes.screenshot({
    path: resolve(output, "presenter-notes.png"),
    fullPage: true,
  });
  await notes.locator("#notes-reveal").click();
  await page.locator("#reveal").waitFor();
  await notes.locator("#notes-reveal").click();
  await page.locator("#dc-conversion").waitFor();
  assert.equal(await page.locator("#dc-conversion").inputValue(), "6");
  await page.locator("#dc-loss-reset").click();
  assert.equal(await page.locator("#dc-conversion").inputValue(), "3");
  await notes.waitForFunction(() =>
    document
      .querySelector("#narration")
      .textContent.includes("Live DC conversion loss: 3 kW"),
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
  await fresh("student", "ac-dc-ledger");
  await page.locator("#reveal").click();
  await page.screenshot({
    path: resolve(output, "student-ledger-mobile.png"),
    fullPage: true,
  });
  for (const mode of ["teach", "student"]) {
    await fresh(mode, "feeder-transfer");
    assert.equal(
      await page.locator("#scene-title").textContent(),
      data.steps[7].headline,
    );
    assert.doesNotMatch(
      await page.locator("#visual").innerText(),
      /150 kW|160 kW|200 A/,
    );
  }
  await page.goto(`${base}sample-reading.html`);
  assert.ok(await page.locator("#prose").isVisible());
  assert.match(
    await page.locator("#title").textContent(),
    /What 800 V changes/,
  );
  assert.deepEqual(errors, []);
  rmSync(resolve(output, "transfer-1280.png"), { force: true });
  const report = {
    checked_on: "2026-09-08",
    browser: "Headless Chromium / Playwright",
    base,
    layout_states: layouts.length,
    layouts,
    checks: [
      "Eight visual steps in teaching and student modes at five viewport sizes",
      "Teaching notes excluded from visuals and no recording-setup instructions",
      "No teaching-view scroll at 1920×1080, 1280×720 or 1024×768",
      "No horizontal overflow or clipped labels on phone and short landscape",
      "Student explanations expand for all eight steps at all five sizes",
      "Student mode hides notes/fullscreen and P/F shortcuts do not activate them",
      "Prediction before reveal for currents, conductor loss and both energy ledgers",
      "DC current, I²R losses and source power balance checked numerically",
      "Complete-path default, break-even and reversed energy budgets",
      "Keyboard advance after reveal and slider keyboard ownership",
      "Separate presenter window with bidirectional navigation/reveal synchronization",
      "Voltage and DC-conversion slider state synchronized to notes",
      "Fullscreen entry and exit in teaching mode",
      "Old feeder-transfer hash routes to the complete-path comparison",
      "Source reading view preserved",
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
