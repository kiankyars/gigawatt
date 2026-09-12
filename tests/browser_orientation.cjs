const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");

const base =
  process.argv[2] ||
  "http://127.0.0.1:8765/course/prototypes/orientation-format.html";
const output = process.argv[3] || "/tmp/gigawatt-orientation-qa";
const scenes = [
  { id: "three-paths", setting: "path", values: ["power", "heat", "data"] },
  { id: "white-grey", setting: "cduLocation", values: ["hall", "gallery"] },
  { id: "rack-boundary", setting: "rackDetail", values: ["false", "true"] },
  { id: "facility-meter", setting: "boundary", values: ["it", "facility"] },
  { id: "heat-account", values: [null] },
  { id: "power-energy", setting: "schedule", values: ["stepped", "flat"] },
  { id: "meter-average", setting: "trace", values: ["steady", "spike"] },
  { id: "useful-work", setting: "efficiency", values: ["baseline", "extra"] },
];
const close = (actual, expected, label) =>
  assert.ok(
    Math.abs(actual - expected) < 1e-8,
    `${label}: ${actual} != ${expected}`,
  );
const url = (id, teaching = false) => {
  const result = new URL(base);
  if (teaching) result.searchParams.set("teach", "1");
  else result.searchParams.delete("teach");
  result.hash = id;
  return result.href;
};
const selectedButton = (page, setting, value) =>
  page.locator(`[data-setting="${setting}"][data-value="${value}"]`);

async function checkSelection(page, scene, selected) {
  if (!scene.setting) {
    assert.equal(await page.locator("#actions button").count(), 0);
    return;
  }
  assert.equal(
    await page.locator(`#actions [aria-pressed="true"]`).count(),
    1,
    "Exactly one option should visibly describe the current state",
  );
  assert.equal(
    await selectedButton(page, scene.setting, selected).getAttribute(
      "aria-pressed",
    ),
    "true",
  );
  const styles = await page.locator("#actions button").evaluateAll((buttons) =>
    buttons.map((button) => ({
      selected: button.getAttribute("aria-pressed") === "true",
      fill: getComputedStyle(button).backgroundColor,
    })),
  );
  const active = styles.find((s) => s.selected);
  for (const inactive of styles.filter((s) => !s.selected))
    assert.notEqual(
      active.fill,
      inactive.fill,
      "Selection must be visually distinct",
    );
}

async function checkGeometry(page, viewport) {
  const result = await page.evaluate(() => {
    const svg = document.querySelector("#diagram");
    const svgRect = svg.getBoundingClientRect();
    const viewBox = svg.viewBox.baseVal;
    const failures = [];
    const fits = (inner, outer, padding = 0) =>
      inner.x >= outer.x + padding &&
      inner.y >= outer.y + padding &&
      inner.x + inner.width <= outer.x + outer.width - padding &&
      inner.y + inner.height <= outer.y + outer.height - padding;
    const texts = [...svg.querySelectorAll("text")];
    for (const label of texts) {
      if (!fits(label.getBBox(), viewBox, -1))
        failures.push(`Text outside viewBox: ${label.textContent}`);
      const r = label.getBoundingClientRect();
      if (
        r.left < svgRect.left - 1 ||
        r.right > svgRect.right + 1 ||
        r.top < svgRect.top - 1 ||
        r.bottom > svgRect.bottom + 1
      )
        failures.push(`Text clipped by rendered SVG: ${label.textContent}`);
      if (label.dataset.labelFor) {
        const owner = svg.querySelector(
          `#${CSS.escape(label.dataset.labelFor)}`,
        );
        if (!owner || !fits(label.getBBox(), owner.getBBox(), 3))
          failures.push(`Label outside its object: ${label.textContent}`);
      }
    }
    for (let i = 0; i < texts.length; i++)
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i].getBBox(),
          b = texts[j].getBBox();
        const overlapX =
          Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
        const overlapY =
          Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
        if (overlapX > 1 && overlapY > 1)
          failures.push(
            `Overlapping labels: ${texts[i].textContent} / ${texts[j].textContent}`,
          );
      }
    const header = document
      .querySelector("main > header")
      .getBoundingClientRect();
    const actions = document.querySelector("#actions").getBoundingClientRect();
    const footer = document.querySelector("footer").getBoundingClientRect();
    if (header.bottom > svgRect.top + 1)
      failures.push("Header overlaps diagram");
    if (actions.height > 0 && svgRect.bottom > actions.top + 1)
      failures.push("Diagram overlaps controls");
    if (Math.max(svgRect.bottom, actions.bottom) > footer.top + 1)
      failures.push("Content overlaps footer");
    for (const button of document.querySelectorAll(
      "#actions button, footer button, #scenes",
    )) {
      const r = button.getBoundingClientRect();
      const parent = button.closest("footer") ? footer : actions;
      if (r.top < parent.top - 1 || r.bottom > parent.bottom + 1)
        failures.push(`Control escapes its bar: ${button.textContent}`);
    }
    return {
      failures,
      width: document.documentElement.scrollWidth,
      height: document.documentElement.scrollHeight,
      footerBottom: footer.bottom,
    };
  });
  assert.deepEqual(result.failures, [], "Diagram and UI geometry");
  assert.ok(
    result.width <= viewport.width + 1,
    "Page must not scroll horizontally",
  );
  if (viewport.width >= 1024) {
    assert.ok(
      result.height <= viewport.height + 1,
      "Desktop teaching view must fit vertically",
    );
    assert.ok(
      result.footerBottom <= viewport.height + 1,
      "Desktop footer must remain visible",
    );
  }
}

async function checkQuantities(page, id, value) {
  const content = await page.locator("#diagram").textContent();
  const attributeNumber = async (attribute) =>
    Number(await page.locator(`[${attribute}]`).getAttribute(attribute));
  if (id === "three-paths") {
    assert.equal(
      await page.locator('[data-path][data-selected="true"]').count(),
      1,
    );
    assert.equal(
      await page
        .locator('[data-path][data-selected="true"]')
        .getAttribute("data-path"),
      value,
    );
  }
  if (id === "white-grey") {
    assert.equal(
      await page
        .locator("[data-cdu-location]")
        .getAttribute("data-cdu-location"),
      value,
    );
    assert.match(content, /WHITE SPACE/);
    assert.match(content, /GREY SPACE/);
  }
  if (id === "rack-boundary") {
    assert.equal(await attributeNumber("data-rack-inlet"), 100);
    assert.equal(
      await page.locator("[data-rack-detail]").getAttribute("data-rack-detail"),
      value,
    );
    if (value === "true") {
      assert.match(content, /8 kW/);
      assert.match(content, /92 kW/);
      assert.match(content, /8 \+ 92 = 100 kW/);
    }
  }
  if (id === "facility-meter") {
    assert.equal(await attributeNumber("data-facility-kw"), 1320);
    assert.equal(
      await attributeNumber("data-meter-kw"),
      value === "it" ? 1100 : 1320,
    );
  }
  if (id === "heat-account")
    assert.equal(await attributeNumber("data-heat-kw"), 1320);
  if (id === "power-energy") {
    close(await attributeNumber("data-energy-mwh"), 184, "Daily energy");
    close(await attributeNumber("data-average-mw"), 184 / 24, "Daily average");
    close(
      await attributeNumber("data-peak-mw"),
      value === "flat" ? 184 / 24 : 10,
      "Daily peak",
    );
  }
  if (id === "meter-average") {
    close(
      await attributeNumber("data-energy-mwh"),
      2 / 3,
      "Five-minute energy",
    );
    close(await attributeNumber("data-average-mw"), 8, "Five-minute average");
    close(
      await attributeNumber("data-peak-mw"),
      value === "spike" ? 12 : 8,
      "Five-minute peak",
    );
  }
  if (id === "useful-work") {
    close(
      await attributeNumber("data-pue"),
      value === "extra" ? 7 / 6 : 1.2,
      "PUE",
    );
    assert.equal(
      await attributeNumber("data-energy-per-job"),
      value === "extra" ? 14 : 12,
    );
  }
}

async function checkNavigation(page) {
  await page.goto(url("three-paths"));
  await page.waitForSelector("#diagram text");
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("ArrowLeft");
  assert.equal(new URL(page.url()).hash, "#three-paths");
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, "#white-grey");
  await page.keyboard.press("ArrowLeft");
  assert.equal(new URL(page.url()).hash, "#three-paths");
  const button = selectedButton(page, "path", "heat");
  await button.focus();
  await page.keyboard.press("ArrowRight");
  assert.equal(
    new URL(page.url()).hash,
    "#three-paths",
    "Arrows on a control must not turn a page",
  );
  const selectConsumed = await page.locator("#scenes").evaluate((select) => {
    select.focus();
    const event = new KeyboardEvent("keydown", {
      key: "ArrowRight",
      bubbles: true,
      cancelable: true,
    });
    select.dispatchEvent(event);
    return event.defaultPrevented;
  });
  assert.equal(
    selectConsumed,
    false,
    "Scene navigation must not consume select's keys",
  );
  assert.equal(new URL(page.url()).hash, "#three-paths");
  await page.locator("#scenes").selectOption("7");
  assert.equal(new URL(page.url()).hash, "#useful-work");
  assert.equal(await page.locator("#next").isDisabled(), true);
  await page.locator("#previous").click();
  assert.equal(new URL(page.url()).hash, "#meter-average");
  await page.locator("#explain").click();
  assert.equal(
    await page.locator("#reading").evaluate((dialog) => dialog.open),
    true,
  );
  await page.keyboard.press("ArrowRight");
  assert.equal(
    new URL(page.url()).hash,
    "#meter-average",
    "Dialog reading must not navigate slides",
  );
  await page.keyboard.press("Escape");
  assert.equal(
    await page.locator("#reading").evaluate((dialog) => dialog.open),
    false,
  );
  await page.locator("#explain").click();
  await page.locator("#close-reading").click();
  assert.equal(
    await page.locator("#reading").evaluate((dialog) => dialog.open),
    false,
  );
  assert.equal(await page.locator("#fullscreen").isVisible(), false);
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("f");
  assert.equal(await page.evaluate(() => !!document.fullscreenElement), false);
  await page.goto(url("three-paths", true));
  await page.waitForSelector("#diagram text");
  assert.equal(await page.locator("#fullscreen").isVisible(), true);
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !!document.fullscreenElement);
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !document.fullscreenElement);
}

(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch();
  const errors = [],
    failures = [];
  let layouts = 0;
  try {
    for (const colorScheme of ["light", "dark"])
      for (const viewport of [
        { width: 1280, height: 720 },
        { width: 1440, height: 900 },
        { width: 390, height: 844 },
        { width: 844, height: 390 },
      ]) {
        const touch = viewport.width === 390;
        const page = await browser.newPage({
          viewport,
          colorScheme,
          hasTouch: touch,
          reducedMotion: "reduce",
        });
        page.on("pageerror", (error) => errors.push(String(error)));
        page.on("response", (response) => {
          if (response.status() >= 400)
            errors.push(`${response.status()} ${response.url()}`);
        });
        page.on("requestfailed", (request) =>
          errors.push(`${request.failure()?.errorText} ${request.url()}`),
        );
        for (const scene of scenes) {
          await page.goto(url(scene.id));
          await page.waitForSelector("#diagram text");
          assert.equal(await page.locator("h1:visible").count(), 1);
          assert.equal(await page.locator("#scenes option").count(), 8);
          assert.equal(await page.locator("#fullscreen").isVisible(), false);
          for (const value of scene.values) {
            const name = `${scene.id}-${value ?? "default"}-${viewport.width}-${colorScheme}`;
            try {
              if (scene.setting) {
                const button = selectedButton(page, scene.setting, value);
                if (touch) await button.tap();
                else {
                  await button.focus();
                  await page.keyboard.press("Enter");
                }
                await checkSelection(page, scene, value);
                assert.equal(
                  await selectedButton(page, scene.setting, value).evaluate(
                    (el) => el === document.activeElement,
                  ),
                  true,
                  "Rerender must preserve keyboard focus on the selected control",
                );
                // Selecting the active choice repeatedly is idempotent.
                if (touch)
                  await selectedButton(page, scene.setting, value).tap();
                else await page.keyboard.press("Space");
                await checkSelection(page, scene, value);
              }
              await checkQuantities(page, scene.id, value);
              await checkGeometry(page, viewport);
              if (
                value === scene.values[0] ||
                ["power-energy", "useful-work", "rack-boundary"].includes(
                  scene.id,
                )
              )
                await page.screenshot({
                  path: `${output}/${name}.png`,
                  fullPage: true,
                });
              layouts++;
            } catch (error) {
              failures.push(`${name}: ${error.message}`);
              await page.screenshot({
                path: `${output}/FAIL-${name}.png`,
                fullPage: true,
              });
            }
          }
          if (scene.setting) {
            const value = scene.values.at(-1);
            const index = scenes.indexOf(scene);
            await page
              .locator("#scenes")
              .selectOption(String(index === 7 ? 0 : 7));
            await page.locator("#scenes").selectOption(String(index));
            await checkSelection(page, scene, value);
            await checkQuantities(page, scene.id, value);
          }
        }
        try {
          await checkNavigation(page);
        } catch (error) {
          failures.push(
            `Navigation ${viewport.width}-${colorScheme}: ${error.message}`,
          );
        }
        await page.close();
      }
    assert.deepEqual(errors, [], "Page errors and unsuccessful requests");
    assert.deepEqual(failures, [], "Orientation regression failures");
    console.log(
      `Passed ${layouts} orientation scene/state layouts across four viewports and both themes, numerical boundaries, visible selections, mouse/touch/keyboard controls, dialog and teaching mode.`,
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
