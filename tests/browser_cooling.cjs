const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const base =
  process.argv[2] ||
  "http://127.0.0.1:8765/course/prototypes/cooling-format.html";
const output = process.argv[3] || "/tmp/gigawatt-cooling-qa";
const ids = [
  "heat-path",
  "cold-plate",
  "two-loops",
  "outdoors",
  "water-balance",
  "less-flow",
  "lost-flow",
  "trace",
];
async function checkDiagramGeometry(page, state) {
  const issues = await page.locator("#diagram").evaluate((svg) => {
    const issues = [];
    const fits = (inner, outer, padding) =>
      inner.x >= outer.x + padding &&
      inner.y >= outer.y + padding &&
      inner.x + inner.width <= outer.x + outer.width - padding &&
      inner.y + inner.height <= outer.y + outer.height - padding;
    for (const label of svg.querySelectorAll("[data-label-for]")) {
      const owner = svg.querySelector(`#${label.dataset.labelFor}`);
      if (!owner || !fits(label.getBBox(), owner.getBBox(), 3))
        issues.push(`Label outside its object: ${label.textContent}`);
    }
    for (const shape of svg.querySelectorAll("[data-inside]")) {
      const owner = svg.querySelector(`#${shape.dataset.inside}`);
      if (!owner || !fits(shape.getBBox(), owner.getBBox(), 3))
        issues.push(`Object crosses its container: ${shape.id}`);
    }
    for (const arrow of svg.querySelectorAll("[data-heat-from]")) {
      const source = svg.querySelector(`#${arrow.dataset.heatFrom}`);
      const box = source?.getBBox();
      const start = arrow.getPointAtLength(0);
      if (
        !box ||
        Math.abs(start.x - (box.x + box.width)) > 4.1 ||
        start.y < box.y ||
        start.y > box.y + box.height
      )
        issues.push(`Heat arrow misses its source: ${arrow.dataset.heatFrom}`);
      const pathBox = arrow.getBBox();
      for (const label of svg.querySelectorAll("[data-label-for]")) {
        const b = label.getBBox();
        if (
          pathBox.x < b.x + b.width &&
          pathBox.x + pathBox.width > b.x &&
          pathBox.y - 3 < b.y + b.height &&
          pathBox.y + pathBox.height + 3 > b.y
        )
          issues.push(`Heat arrow crosses a label: ${label.textContent}`);
      }
    }
    return issues;
  });
  assert.deepEqual(issues, [], `${state}: diagram geometry`);
}
(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch();
  const errors = [];
  let layouts = 0;
  try {
    for (const colorScheme of ["light", "dark"])
      for (const viewport of [
        { width: 1440, height: 900 },
        { width: 1280, height: 720 },
        { width: 390, height: 844 },
        { width: 844, height: 390 },
      ]) {
        const page = await browser.newPage({
          viewport,
          colorScheme,
          reducedMotion: "reduce",
        });
        page.on("pageerror", (e) => errors.push(String(e)));
        page.on("response", (r) => {
          if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
        });
        const go = async (id) => {
          await page.goto(`${base}?qa=${colorScheme}-${viewport.width}#${id}`);
          await page.waitForSelector("#diagram text");
        };
        for (const id of ids) {
          await go(id);
          assert.equal(await page.locator("h1:visible").count(), 1);
          assert.equal(await page.locator("#fullscreen").isVisible(), false);
          assert.equal(await page.locator("#scenes option").count(), 8);
          const layout = await page.evaluate(() => {
            const svg = document
              .querySelector("#diagram")
              .getBoundingClientRect();
            return {
              width: document.documentElement.scrollWidth,
              height: document.documentElement.scrollHeight,
              title: document.querySelector("h1").getBoundingClientRect()
                .bottom,
              svgTop: svg.top,
              svgBottom: svg.bottom,
              footer: document.querySelector("footer").getBoundingClientRect()
                .top,
              clipped: [...document.querySelectorAll("#diagram text")]
                .filter((t) => {
                  const r = t.getBoundingClientRect();
                  return (
                    r.left < svg.left - 1 ||
                    r.right > svg.right + 1 ||
                    r.top < svg.top - 1 ||
                    r.bottom > svg.bottom + 1
                  );
                })
                .map((t) => t.textContent),
            };
          });
          assert.ok(
            layout.width <= viewport.width + 1,
            `${id}: horizontal overflow`,
          );
          assert.ok(
            layout.title <= layout.svgTop + 1,
            `${id}: title overlaps diagram`,
          );
          assert.ok(
            layout.svgBottom <= layout.footer + 1,
            `${id}: navigation overlaps diagram`,
          );
          if (viewport.width >= 1024)
            assert.ok(
              layout.height <= viewport.height + 1,
              `${id}: desktop requires scrolling`,
            );
          assert.deepEqual(layout.clipped, [], `${id}: clipped SVG labels`);
          await checkDiagramGeometry(page, id);
          if (["heat-path", "two-loops", "outdoors", "lost-flow"].includes(id))
            assert.equal(
              await page.locator('[data-label-for="rack-heat-source"]').count(),
              1,
            );
          await page.screenshot({
            path: `${output}/${id}-${viewport.width}-${colorScheme}.png`,
            fullPage: true,
          });
          layouts++;
        }
        await go("less-flow");
        await page.locator('[data-flow="2.5"]').click();
        assert.equal(
          await page.locator('[data-flow="2.5"]').getAttribute("aria-pressed"),
          "true",
        );
        assert.match(await page.locator("#diagram").textContent(), /9\.57/);
        await page.locator('[data-flow="5"]').focus();
        await page.keyboard.press("Enter");
        assert.equal(
          await page.locator('[data-flow="5"]').getAttribute("aria-pressed"),
          "true",
        );
        assert.match(await page.locator("#diagram").textContent(), /4\.78/);
        await page.screenshot({
          path: `${output}/less-flow-restored-${viewport.width}-${colorScheme}.png`,
          fullPage: true,
        });
        await go("lost-flow");
        assert.ok((await page.locator("#diagram .stopped").count()) > 0);
        assert.match(
          await page.locator("#diagram").textContent(),
          /accumulate/,
        );
        await page.locator("#toggle-facility").click();
        assert.equal(await page.locator("#diagram .stopped").count(), 0);
        await checkDiagramGeometry(page, "facility-restored");
        await page.screenshot({
          path: `${output}/facility-restored-${viewport.width}-${colorScheme}.png`,
          fullPage: true,
        });
        assert.match(
          await page.locator("h1").innerText(),
          /Restoring facility flow/,
        );
        await page.locator("#toggle-facility").click();
        assert.ok((await page.locator("#diagram .stopped").count()) > 0);
        await go("trace");
        const before = await page.locator("#diagram path.heat").count();
        await page.locator("#toggle-trace").click();
        assert.ok((await page.locator("#diagram path.heat").count()) > before);
        await checkDiagramGeometry(page, "trace-revealed");
        assert.equal(
          await page.locator('[data-label-for="rack-heat-source"]').count(),
          1,
        );
        await page.screenshot({
          path: `${output}/trace-revealed-${viewport.width}-${colorScheme}.png`,
          fullPage: true,
        });
        await page.locator("#evidence").click();
        assert.equal(
          await page.locator("#reading").evaluate((e) => e.open),
          true,
        );
        await page.keyboard.press("Escape");
        assert.equal(
          await page.locator("#reading").evaluate((e) => e.open),
          false,
        );
        await go("heat-path");
        await page.locator("body").click({ position: { x: 2, y: 100 } });
        await page.keyboard.press("ArrowRight");
        await page.waitForURL(/#cold-plate$/);
        await page.keyboard.press("ArrowLeft");
        await page.waitForURL(/#heat-path$/);
        await page.goto(`${base}?teach=1#heat-path`);
        assert.equal(await page.locator("#fullscreen").isVisible(), true);
        await page.close();
      }
    assert.deepEqual(errors, []);
    console.log(
      `Passed ${layouts} cooling layouts, object/label containment, heat-arrow origins, flow and failure controls, heat trace, source dialog, keyboard and teaching-mode separation.`,
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
