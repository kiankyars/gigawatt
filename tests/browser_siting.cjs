const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const base =
  process.argv[2] ||
  "http://127.0.0.1:8841/course/prototypes/siting-format.html";
const output = process.argv[3] || "/tmp/gigawatt-siting-qa";
const url = (id, teach = false) => {
  const u = new URL(base);
  u.hash = id;
  if (teach) u.searchParams.set("teach", "1");
  else u.searchParams.delete("teach");
  return u.href;
};
const button = (page, key, value) =>
  page.locator(`[data-key="${key}"][data-value="${value}"]`);
const close = (a, b, label) =>
  assert.ok(
    Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(b)),
    `${label}: ${a} != ${b}`,
  );

async function checkSelection(page, scene, values) {
  for (const group of scene.controls || []) {
    const buttons = page.locator(`[data-key="${group.key}"]`);
    assert.equal(await buttons.count(), group.options.length);
    assert.equal(
      await buttons.locator('css=:scope[aria-pressed="true"]').count(),
      1,
    );
    assert.equal(
      await button(page, group.key, values[group.key]).getAttribute(
        "aria-pressed",
      ),
      "true",
    );
    const styles = await buttons.evaluateAll((elements) =>
      elements.map((e) => ({
        selected: e.getAttribute("aria-pressed") === "true",
        fill: getComputedStyle(e).backgroundColor,
      })),
    );
    const active = styles.find((s) => s.selected);
    for (const inactive of styles.filter((s) => !s.selected))
      assert.notEqual(
        active.fill,
        inactive.fill,
        "Selected state must be visually distinct",
      );
  }
}

async function checkValues(page, scene, values, revealed) {
  const attr = async (name) =>
    Number(await page.locator(`[${name}]`).getAttribute(name));
  const description = await page.locator("#diagram-description").textContent();
  assert.ok(
    description.length >= 40 && !description.includes("undefined"),
    "A useful description must accompany every visual state",
  );
  assert.ok(
    !/(?:NaN|Infinity|\[object Object\])/.test(
      await page.locator("#diagram").textContent(),
    ),
    "No unresolved numbers or objects",
  );
  if (scene.id === "site-ready")
    assert.equal(await attr("data-ready-month"), values.site === "A" ? 22 : 21);
  if (scene.id === "storage-match") {
    assert.equal(
      await attr("data-returned-mwh"),
      values.storage === "losses" ? 108 : 120,
    );
    assert.equal(
      await attr("data-output-mw"),
      values.storage === "power" ? 2 : 10,
    );
  }
  if (
    ["btm-import", "import-contingency", "island-boundary"].includes(scene.id)
  ) {
    const generation =
      scene.id === "btm-import"
        ? Number(values.generation)
        : scene.id === "import-contingency" && values.generator === "stopped"
          ? 0
          : 6;
    const storage =
      scene.id === "island-boundary" && values.island === "supported" ? 2 : 0;
    assert.equal(await attr("data-generation-mw"), generation);
    assert.equal(await attr("data-storage-mw"), storage);
    assert.equal(
      await attr("data-grid-mw"),
      scene.id === "island-boundary" ? 0 : 8 - generation,
    );
  }
  if (scene.id === "island-duration") {
    const deficit = Number(values.protectedLoad) - 6;
    assert.equal(await attr("data-deficit-mw"), deficit);
    assert.equal(
      await attr("data-duration-hours"),
      deficit ? Math.min(4 / deficit, 4) : 4,
    );
  }
  if (scene.id === "procurement-route")
    assert.equal(
      await page.locator("[data-route]").getAttribute("data-route"),
      values.route,
    );
  if (scene.id === "transport-current") {
    close(
      await attr("data-line-current-a"),
      200000 / (Math.sqrt(3) * Number(values.voltage)),
      "Transport current",
    );
    assert.equal(await attr("data-voltage-kv"), Number(values.voltage));
    assert.equal(await attr("data-power-mw"), 200);
  }
  if (scene.id === "parallel-circuits") {
    const n = Number(values.circuits);
    assert.equal(await attr("data-circuits"), n);
    close(
      await attr("data-power-per-circuit-mw"),
      200 / n,
      "Power per circuit",
    );
    close(
      await attr("data-line-current-a"),
      200000 / (n * Math.sqrt(3) * 34.5),
      "Current per line",
    );
  }
  if (scene.id === "procurement-decision")
    assert.equal(
      await page
        .locator("[data-decision-revealed]")
        .getAttribute("data-decision-revealed"),
      String(revealed),
    );
  if (scene.reveal)
    assert.equal(
      await page.locator("#reveal").getAttribute("aria-expanded"),
      String(revealed),
    );
  const stageWords = (
    await page
      .locator("#diagram")
      .evaluate((svg) =>
        [...svg.querySelectorAll("text")].map((t) => t.textContent).join(" "),
      )
  )
    .trim()
    .split(/\s+/).length;
  assert.ok(
    stageWords <= 150,
    `The diagram has ${stageWords} words; review visual density`,
  );
  assert.ok(
    (await page.locator("#title").textContent()).split(/\s+/).length <= 22,
    "Heading should remain one short claim",
  );
}
async function checkGeometry(page, viewport) {
  const result = await page.evaluate(() => {
    const svg = document.querySelector("#diagram");
    const viewBox = svg.viewBox.baseVal;
    const failures = [];
    const fits = (a, b, margin = 0) =>
      a.x >= b.x + margin &&
      a.y >= b.y + margin &&
      a.x + a.width <= b.x + b.width - margin &&
      a.y + a.height <= b.y + b.height - margin;
    const texts = [...svg.querySelectorAll("text")];
    for (const label of texts) {
      if (!fits(label.getBBox(), viewBox, -1))
        failures.push(`Text outside SVG: ${label.textContent}`);
      if (label.dataset.labelFor) {
        const owner = svg.querySelector(
          `#${CSS.escape(label.dataset.labelFor)}`,
        );
        if (!owner || !fits(label.getBBox(), owner.getBBox(), 2))
          failures.push(`Text outside its object: ${label.textContent}`);
      }
    }
    for (let i = 0; i < texts.length; i++)
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i].getBBox(),
          b = texts[j].getBBox();
        if (
          Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x) > 1 &&
          Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y) > 1
        )
          failures.push(
            `Overlapping labels: ${texts[i].textContent} / ${texts[j].textContent}`,
          );
      }
    const rect = svg.getBoundingClientRect();
    const header = document
      .querySelector("main > header")
      .getBoundingClientRect();
    const actions = document.querySelector("#actions").getBoundingClientRect();
    const footer = document.querySelector("footer").getBoundingClientRect();
    if (header.bottom > rect.top + 1) failures.push("Heading overlaps diagram");
    if (actions.height && rect.bottom > actions.top + 1)
      failures.push("Diagram overlaps controls");
    if (Math.max(rect.bottom, actions.bottom) > footer.top + 1)
      failures.push("Content overlaps footer");
    if (
      [
        ...document.querySelectorAll(
          "main .eyebrow, #boundary, main .subtitle",
        ),
      ].some((element) => element.getBoundingClientRect().height > 0)
    )
      failures.push(
        "A repeated subtitle or boundary layer is visible on the stage",
      );
    return {
      failures,
      width: document.documentElement.scrollWidth,
      height: document.documentElement.scrollHeight,
      footerBottom: footer.bottom,
    };
  });
  assert.deepEqual(result.failures, [], "SVG and control layout");
  assert.ok(result.width <= viewport.width + 1, "No horizontal page overflow");
  if (viewport.width >= 1024) {
    assert.ok(
      result.height <= viewport.height + 1,
      "Desktop presentation must fit vertically",
    );
    assert.ok(
      result.footerBottom <= viewport.height + 1,
      "Desktop navigation stays visible",
    );
  }
}

async function checkNavigation(page, scenes, colorScheme) {
  const first = scenes[0],
    last = scenes.at(-1);
  await page.goto(url(first.id));
  await page.reload();
  await page.waitForSelector("#diagram text");
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("ArrowLeft");
  assert.equal(new URL(page.url()).hash, `#${first.id}`);
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, `#${scenes[1].id}`);
  const control = page.locator("[data-key]").first();
  await control.focus();
  await page.keyboard.press("ArrowRight");
  assert.equal(
    new URL(page.url()).hash,
    `#${scenes[1].id}`,
    "Focused controls retain arrow keys",
  );
  await page.locator("#scenes").selectOption(first.id);
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("r");
  assert.equal(
    await page.locator("#reveal").getAttribute("aria-expanded"),
    "true",
  );
  await page.keyboard.press("r");
  assert.equal(
    await page.locator("#reveal").getAttribute("aria-expanded"),
    "false",
  );
  const consumed = await page.locator("#scenes").evaluate((e) => {
    e.focus();
    const k = new KeyboardEvent("keydown", {
      key: "ArrowRight",
      bubbles: true,
      cancelable: true,
    });
    e.dispatchEvent(k);
    return k.defaultPrevented;
  });
  assert.equal(consumed, false);
  await page.locator("#explain").click();
  assert.equal(await page.locator("#reading").evaluate((e) => e.open), true);
  await page.keyboard.press("ArrowRight");
  assert.equal(new URL(page.url()).hash, `#${first.id}`);
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("#reading").evaluate((e) => e.open), false);
  await page.locator("#explain").click();
  await page.locator("#close-reading").click();
  assert.equal(await page.locator("#reading").evaluate((e) => e.open), false);
  await page.locator("#scenes").selectOption(last.id);
  assert.equal(await page.locator("#next").isDisabled(), true);
  const checkin = page.locator("#actions a");
  const href = new URL(await checkin.getAttribute("href"), page.url());
  assert.equal(href.searchParams.get("checkin"), "1");
  assert.equal(href.hash, "#d03-service-and-siting");
  assert.equal((await page.request.get(href.href)).status(), 200);
  assert.equal(await page.locator("#fullscreen").isVisible(), false);
  await page.locator("body").click({ position: { x: 2, y: 100 } });
  await page.keyboard.press("f");
  assert.equal(await page.evaluate(() => !!document.fullscreenElement), false);
  await page.goto(url(first.id, true));
  await page.waitForSelector("#diagram text");
  assert.equal(await page.locator("#fullscreen").isVisible(), true);
  const bg = await page
    .locator("#viewer")
    .evaluate((e) => getComputedStyle(e).backgroundColor);
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !!document.fullscreenElement);
  assert.equal(
    await page
      .locator("#viewer")
      .evaluate((e) => getComputedStyle(e).backgroundColor),
    bg,
  );
  assert.notEqual(
    bg,
    "rgba(0, 0, 0, 0)",
    "Fullscreen must have an opaque theme background",
  );
  const opposite = colorScheme === "light" ? "dark" : "light";
  await page.emulateMedia({ colorScheme: opposite });
  assert.notEqual(
    await page
      .locator("#viewer")
      .evaluate((e) => getComputedStyle(e).backgroundColor),
    bg,
    "Fullscreen follows device theme changes",
  );
  await page.emulateMedia({ colorScheme });
  await page.locator("#fullscreen").click();
  await page.waitForFunction(() => !document.fullscreenElement);
  await page.goto(url("unknown-scene"));
  await page.waitForSelector("#diagram text");
  assert.equal(await page.locator("#scenes").inputValue(), first.id);
  await page.goto(url(last.id));
  await page.locator("#actions a").click();
  await page.waitForSelector("#checkin-response", { state: "visible" });
  assert.equal(new URL(page.url()).hash, "#d03-service-and-siting");
  assert.equal(await page.locator("#domain-checkin").isVisible(), true);
  assert.ok(
    (await page.locator("#domain-checkin h3").first().textContent()).length >
      10,
  );
  assert.ok(await page.locator("#checkin-continue").getAttribute("href"));
}

(async () => {
  const { scenes, initialState } =
    await import("../course/prototypes/siting-scenes.js");
  assert.equal(scenes.length, 18);
  assert.equal(new Set(scenes.map((s) => s.id)).size, scenes.length);
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
        const touch = viewport.width === 390,
          page = await browser.newPage({
            viewport,
            colorScheme,
            hasTouch: touch,
            reducedMotion: "reduce",
          });
        page.on("pageerror", (e) => errors.push(String(e)));
        page.on("response", (r) => {
          if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
        });
        for (const scene of scenes) {
          await page.goto(url(scene.id));
          await page.waitForSelector("#diagram text");
          assert.equal(
            await page.locator("#scenes option").count(),
            scenes.length,
          );
          assert.equal(await page.locator("h1:visible").count(), 1);
          let variants = [{ ...initialState }];
          for (const group of scene.controls || [])
            variants = variants.flatMap((v) =>
              group.options.map(([value]) => ({ ...v, [group.key]: value })),
            );
          const previousFrames = new Map();
          for (const values of variants) {
            for (const group of scene.controls || []) {
              const target = button(page, group.key, values[group.key]);
              if (touch) await target.tap();
              else {
                await target.focus();
                await page.keyboard.press("Enter");
              }
              assert.equal(
                await target.evaluate((e) => e === document.activeElement),
                true,
              );
              const chosenFrame = await page.locator("#diagram").innerHTML();
              if (touch) await target.tap();
              else await page.keyboard.press("Space");
              assert.equal(
                await page.locator("#diagram").innerHTML(),
                chosenFrame,
                "Selecting an active option again must leave its visual state unchanged",
              );
            }
            for (const revealed of scene.reveal ? [false, true] : [false]) {
              if (
                scene.reveal &&
                (await page
                  .locator("#reveal")
                  .getAttribute("aria-expanded")) !== String(revealed)
              )
                await page.locator("#reveal").click();
              const name = `${scene.id}-${(scene.controls || []).map((g) => values[g.key]).join("-") || "default"}${scene.reveal ? (revealed ? "-revealed" : "-hidden") : ""}-${viewport.width}-${colorScheme}`;
              try {
                await checkSelection(page, scene, values);
                await checkValues(page, scene, values, revealed);
                await checkGeometry(page, viewport);
                const frame = await page.locator("#diagram").innerHTML();
                if (previousFrames.has(revealed))
                  assert.notEqual(
                    frame,
                    previousFrames.get(revealed),
                    "Each changed control choice must change the visual state",
                  );
                previousFrames.set(revealed, frame);
                layouts++;
              } catch (e) {
                failures.push(`${name}: ${e.message}`);
              }
              await page.screenshot({
                path: `${output}/${name}.png`,
                fullPage: true,
              });
            }
          }
          if (scene.controls?.length) {
            const values = variants.at(-1);
            await page
              .locator("#scenes")
              .selectOption(
                scene.id === scenes[0].id ? scenes.at(-1).id : scenes[0].id,
              );
            await page.locator("#scenes").selectOption(scene.id);
            try {
              await checkSelection(page, scene, values);
            } catch (e) {
              failures.push(`State restoration ${scene.id}: ${e.message}`);
            }
          }
        }
        try {
          await checkNavigation(page, scenes, colorScheme);
        } catch (e) {
          failures.push(
            `Navigation ${viewport.width}-${colorScheme}: ${e.message}`,
          );
        }
        await page.close();
      }
    assert.deepEqual(errors, [], "No JavaScript or HTTP errors");
    assert.deepEqual(failures, [], "Siting browser regressions");
    console.log(
      `Passed ${layouts} siting scene/state layouts across 18 scenes, four viewports and both themes; controls, reveals, numerical results, keyboard, dialog, fullscreen and reader check-in.`,
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
