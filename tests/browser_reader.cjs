/* Run with Playwright available through NODE_PATH or a local installation. */
const { chromium } = require("playwright");
const { readFileSync, mkdirSync, writeFileSync } = require("node:fs");
const { resolve } = require("node:path");
const assert = require("node:assert/strict");
const base = process.argv[2] || "http://127.0.0.1:8765/course/";
const output = resolve(process.argv[3] || "qa/expansion");
const course = JSON.parse(readFileSync("course/expanded-course.json", "utf8"));
(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  const errors = [];
  const checks = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("response", (r) => {
    if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
  });
  async function lesson(id) {
    await page.goto(`${base}index.html#${id}`);
    await page.locator("#title").waitFor();
    await page.waitForFunction(
      () =>
        document.querySelector("#teaching-image").closest("figure").hidden ||
        document.querySelector("#teaching-image").complete,
    );
  }
  for (const viewport of [
    { width: 1440, height: 1000 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    for (const l of course.lessons) {
      await lesson(l.id);
      assert.equal(await page.locator("#title").textContent(), l.title);
      const state = await page.evaluate(() => ({
        width: innerWidth,
        scroll: document.documentElement.scrollWidth,
        image: document.querySelector("#teaching-image").naturalWidth,
        imageVisible: !document
          .querySelector("#teaching-image")
          .closest("figure").hidden,
        sections: document.querySelectorAll(".reading-section").length,
        steps: document.querySelectorAll("#worked ol li").length,
      }));
      assert.ok(
        state.scroll <= state.width + 1,
        `${l.id}: horizontal overflow ${JSON.stringify(state)}`,
      );
      assert.equal(
        state.imageVisible,
        l.image === "campus",
        `${l.id}: unreviewed illustration shown`,
      );
      if (state.imageVisible)
        assert.ok(state.image > 0, `${l.id}: missing image`);
      const figures = l.sections.flatMap((s) => s.figures || []);
      assert.equal(
        await page.locator(".source-figure img").count(),
        figures.length,
      );
      for (const figure of await page.locator(".source-figure img").all()) {
        await figure.scrollIntoViewIfNeeded();
        await figure.evaluate((img) => img.decode());
        assert.ok(await figure.evaluate((img) => img.naturalWidth > 0));
      }
      assert.ok(state.sections >= 2 && state.steps >= 2);
      await page.locator("#practice summary").click();
      assert.ok(
        (await page.locator("#practice .answer").textContent()).length > 15,
      );
      checks.push({
        id: l.id,
        width: viewport.width,
        overflow: false,
        image: state.imageVisible ? "orientation" : "omitted",
        answer: true,
      });
    }
  }
  await page.setViewportSize({ width: 1440, height: 1000 });
  await lesson(course.lessons[0].id);
  await page.screenshot({ path: resolve(output, "desktop-course.png") });
  await page.locator("#search").fill("800 V");
  assert.ok((await page.locator(".lesson-link").count()) > 0);
  await page.locator("#search").fill("zzzz-no-match");
  assert.equal(await page.locator(".lesson-link").count(), 0);
  await page.locator("#search").fill("");
  await page.locator("#lookup-toggle").click();
  assert.equal(
    await page.locator(".glossary-card").count(),
    course.glossary.length,
  );
  await page.locator(".glossary-card button").first().click();
  assert.ok(await page.locator("#lesson").isVisible());
  const sampleByDomain = [
    "D01",
    "D02",
    "D04",
    "D05",
    "D08",
    "D09",
    "D10",
    "D15",
  ];
  for (const domain of sampleByDomain) {
    await lesson(course.lessons.find((l) => l.domain === domain).id);
    for (const input of await page.locator("#lab input").all()) {
      await input.focus();
      await input.press("Home");
      assert.doesNotMatch(
        await page.locator("#lab-output").textContent(),
        /NaN|Infinity|undefined/,
      );
      await input.press("End");
      assert.doesNotMatch(
        await page.locator("#lab-output").textContent(),
        /NaN|Infinity|undefined/,
      );
    }
  }
  await lesson("d06-eight-hundred-volt-architectures");
  await page.locator('[data-arch="hybrid"]').click();
  assert.match(
    await page.locator("#architecture").textContent(),
    /Existing facility AC/,
  );
  await page.locator('[data-arch="facility"]').click();
  assert.match(
    await page.locator("#architecture").textContent(),
    /Facility conversion/,
  );
  await page
    .locator("#lab")
    .screenshot({ path: resolve(output, "architecture-lab.png") });
  await page.goto(`${base}sample-reading.html`);
  await page.waitForFunction(
    () => document.querySelector("#teaching-image").complete,
  );
  assert.match(await page.title(), /800 V/);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: resolve(output, "mobile-sample.png") });
  await page
    .locator("#lab")
    .screenshot({ path: resolve(output, "mobile-lab.png") });
  await page.locator("#contents-toggle").click();
  assert.equal(
    await page.locator("#contents-toggle").getAttribute("aria-expanded"),
    "true",
  );
  await page.keyboard.press("Escape");
  assert.equal(
    await page.locator("#contents-toggle").getAttribute("aria-expanded"),
    "false",
  );
  for (const viewport of [
    { width: 1024, height: 768 },
    { width: 844, height: 390 },
  ]) {
    await page.setViewportSize(viewport);
    assert.ok(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 1,
      ),
    );
  }
  assert.deepEqual(errors, []);
  writeFileSync(
    resolve(output, "browser-report.json"),
    JSON.stringify(
      {
        checked_on: "2026-09-06",
        browser: "Headless Chromium / Playwright",
        lesson_states: checks.length,
        checks,
        errors,
        additional_checks: [
          "Search match and empty states",
          "Glossary entry to lesson",
          "Eight model types at all slider endpoints",
          "AC/sidecar/facility selector",
          "Practice answer reveal in every lesson",
          "Sample page",
          "Mobile contents and Escape",
          "Tablet and short-landscape sample overflow",
          "Reduced-motion context",
        ],
      },
      null,
      2,
    ),
  );
  await browser.close();
  console.log(
    `Passed ${checks.length} lesson viewport states, eight interactive model types, search/glossary/practice and sample checks.`,
  );
})().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
