const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const base = process.argv[2] || "http://127.0.0.1:8765/course/";
const output = process.argv[3] || "/tmp/gigawatt-primer-qa";
const scenes = ["dc-circuit", "ac-cycle", "three-phase", "voltage-basis"];
(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(String(error)));
    for (const size of [
      { width: 1280, height: 720 },
      { width: 1024, height: 768 },
      { width: 1920, height: 1080 },
      { width: 390, height: 844 },
      { width: 844, height: 390 },
    ]) {
      await page.setViewportSize(size);
      for (const id of scenes) {
        await page.goto(`${base}teach.html#${id}`);
        const bounds = await page.evaluate(() => {
          const rect = (selector) => {
            const r = document.querySelector(selector).getBoundingClientRect();
            return { top: r.top, bottom: r.bottom };
          };
          return {
            title: rect(".scene-heading"),
            visual: rect("#visual"),
            footer: rect(".transport"),
            width: document.documentElement.scrollWidth,
          };
        });
        assert.ok(bounds.width <= size.width + 1, `${id}: horizontal overflow`);
        assert.ok(
          bounds.title.bottom <= bounds.visual.top + 1,
          `${id}: visual overlaps title`,
        );
        assert.ok(
          bounds.visual.bottom <= bounds.footer.top + 1,
          `${id}: visual overlaps footer`,
        );
        assert.equal(await page.locator("#caption").count(), 0);
        if (id !== "voltage-basis")
          assert.match(
            await page.locator(".energy-band").innerText(),
            /100 kW average at the load/,
          );
        await page.screenshot({
          path: `${output}/${id}-${size.width}.png`,
          fullPage: size.width < 800,
        });
      }
    }
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto(`${base}teach.html#ac-cycle`);
    const opened = context.waitForEvent("page");
    await page.locator("#open-notes").click();
    const notes = await opened;
    await notes.waitForSelector("#notes-cycle");
    async function angle(degrees) {
      await page.locator("#cycle-angle").fill(String(degrees));
      await notes.waitForFunction(
        (d) =>
          document.querySelector("#notes-cycle").textContent.includes(`${d}°`),
        degrees,
      );
    }
    await angle(90);
    assert.match(await page.locator(".wave-result").innerText(), /200 kW now/);
    assert.match(
      await page.locator(".current-circuit").getAttribute("aria-label"),
      /200 kilowatts/,
    );
    await angle(270);
    assert.match(await page.locator(".wave-result").innerText(), /200 kW now/);
    assert.match(
      await page.locator(".current-circuit").getAttribute("aria-label"),
      /reverses/,
    );
    assert.match(
      await page.locator(".current-circuit").textContent(),
      /−?678\.8|-678\.8/,
    );
    await angle(180);
    assert.match(await page.locator(".wave-result").innerText(), /0 kW now/);
    assert.match(
      await page.locator(".current-circuit").textContent(),
      /0 kW/,
    );
    await page.locator("#cycle-angle").focus();
    await page.keyboard.press("ArrowRight");
    assert.equal(await page.locator("#cycle-angle").inputValue(), "181");
    assert.ok(page.url().endsWith("#ac-cycle"));
    await page.locator('#steps [data-step="3"]').click();
    await notes.waitForURL(/#three-phase$/);
    for (const degrees of [0, 30, 90, 180, 270, 360]) {
      await page.locator("#cycle-angle").fill(String(degrees));
      assert.match(
        await page.locator(".wave-result").innerText(),
        /100 kW total at every instant/,
      );
      assert.match(
        await page.locator(".current-circuit").textContent(),
        /i₁ \+ i₂ \+ i₃ = 0 A/,
      );
    }
    await page.goto(`${base}teach.html#voltage-basis`);
    assert.equal(await page.locator("#cycle-angle").count(), 0);
    assert.match(
      await page.locator(".voltage-measurement").innerText(),
      /480 V/,
    );
    assert.match(
      await page.locator(".voltage-measurement").innerText(),
      /L1 to L2/,
    );
    assert.match(
      await page.locator(".phase-measurement-note").innerText(),
      /All three phases are live/,
    );
    assert.match(
      await page.locator(".voltage-measurement svg title").textContent(),
      /L3 is also live and is not ground/,
    );
    const voltageRelations = await page.evaluate(() =>
      [0, 90, 180, 270].map((degrees) => {
        const v = waveView(degrees);
        return v.lineVoltage - (v.phaseVoltage1 - v.phaseVoltage2);
      }),
    );
    for (const difference of voltageRelations)
      assert.ok(Math.abs(difference) < 1e-9);
    await page.goto(`${base}teach.html#dc-circuit`);
    assert.equal(await page.locator(".wave-chart").count(), 0);
    assert.match(
      await page.locator(".equation-block").innerText(),
      /800 V × 125 A/,
    );
    assert.deepEqual(errors, []);
    console.log(
      "Passed 20 primer layouts, fixed energy reference, polarity reversal, phase balance, voltage subtraction, keyboard and notes synchronization.",
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
