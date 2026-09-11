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
            caption: rect("#caption"),
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
          bounds.visual.bottom <= bounds.caption.top + 1,
          `${id}: visual overlaps caption`,
        );
        assert.ok(
          bounds.caption.bottom <= bounds.footer.top + 1,
          `${id}: footer overlaps caption`,
        );
        assert.match(
          await page.locator(".energy-band").innerText(),
          /100 kW average at the load/,
        );
        assert.match(
          await page.locator(".energy-band").innerText(),
          /100 kWh received/,
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
      /Zero power at this instant/,
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
    for (const degrees of [0, 90, 180, 270]) {
      await page.locator("#cycle-angle").fill(String(degrees));
      const values = await page.evaluate(() => {
        const v = waveView(state.cycleDegrees);
        return [v.lineVoltage, v.phaseVoltage1 - v.phaseVoltage2];
      });
      assert.ok(Math.abs(values[0] - values[1]) < 1e-9);
    }
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
