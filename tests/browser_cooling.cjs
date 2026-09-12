const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const base =
  process.argv[2] ||
  "http://127.0.0.1:8765/course/prototypes/cooling-format.html";
const output = process.argv[3] || "/tmp/gigawatt-cooling-qa";
const variants = {
  "why-liquid": [null],
  "heat-path": [null],
  "capture-options": ["air", "coldplate", "rear-door", "immersion"],
  "cold-plate": [null],
  "water-balance": ["2.5", "5"],
  approach: [null],
  "coolit-cdu": ["true", "false"],
  rejection: [null],
  weather: ["dry", "humid"],
  "approach-outdoors": ["dry", "humid"],
  "plant-options": ["adiabatic", "air-chiller", "water-chiller", "economizer"],
  "lost-flow": ["none", "module", "shared-path"],
  "independent-cooling-paths": ["none", "shared-path"],
  "cooling-derating": [
    "full",
    "reduced",
    "full-lost",
    "reduced-lost",
    "reduced-restored",
  ],
};
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
    const continuity = svg.querySelector("[data-cooling-capacity]");
    if (continuity) {
      const labels = [...continuity.querySelectorAll("text")];
      for (let i = 0; i < labels.length; i++)
        for (let j = i + 1; j < labels.length; j++) {
          const a = labels[i].getBBox(),
            b = labels[j].getBBox();
          if (
            a.x < b.x + b.width &&
            a.x + a.width > b.x &&
            a.y < b.y + b.height &&
            a.y + a.height > b.y
          )
            issues.push(
              `Continuity labels overlap: ${labels[i].textContent} / ${labels[j].textContent}`,
            );
        }
      for (const arrow of continuity.querySelectorAll("path[marker-end]")) {
        const length = arrow.getTotalLength();
        for (const label of labels) {
          const b = label.getBBox();
          for (let distance = 0; distance <= length; distance += 2) {
            const point = arrow.getPointAtLength(distance);
            if (
              point.x >= b.x - 3 &&
              point.x <= b.x + b.width + 3 &&
              point.y >= b.y - 3 &&
              point.y <= b.y + b.height + 3
            ) {
              issues.push(
                `Continuity route overlaps text: ${label.textContent}`,
              );
              break;
            }
          }
        }
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
        for (const [id, states] of Object.entries(variants)) {
          await go(id);
          assert.equal(await page.locator("h1:visible").count(), 1);
          assert.equal(await page.locator("#fullscreen").isVisible(), false);
          assert.equal(await page.locator("#scenes option").count(), 14);
          if (id === "lost-flow") {
            assert.equal(
              await page
                .locator("[data-cooling-fault]")
                .getAttribute("data-cooling-fault"),
              "module",
            );
            assert.equal(
              await page
                .locator('[data-setting="cduFault"][data-value="module"]')
                .getAttribute("aria-pressed"),
              "true",
            );
          }
          if (id === "independent-cooling-paths")
            assert.equal(
              await page
                .locator("[data-cooling-fault]")
                .getAttribute("data-cooling-fault"),
              "shared-path",
            );
          for (const selected of states) {
            if (id === "cooling-derating") {
              const mode = selected.split("-")[0];
              const button = page.locator(
                `[data-setting="loadMode"][data-value="${mode}"]`,
              );
              await button.focus();
              await page.keyboard.press("Enter");
              assert.equal(await button.getAttribute("aria-pressed"), "true");
              const lost = selected.endsWith("-lost");
              const toggle = page.locator("#toggle-remaining-path");
              if ((await toggle.textContent()).startsWith("Restore") !== lost) {
                await toggle.focus();
                await page.keyboard.press("Enter");
              }
              assert.equal(
                (await toggle.textContent()).startsWith("Restore"),
                lost,
              );
            } else if (selected !== null) {
              const button = page.locator(`[data-value="${selected}"]`);
              await button.focus();
              await page.keyboard.press("Enter");
              assert.equal(await button.getAttribute("aria-pressed"), "true");
            }
            const name = `${id}-${selected || "default"}`;
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
            await page.screenshot({
              path: `${output}/${name}-${viewport.width}-${colorScheme}.png`,
              fullPage: true,
            });
            assert.ok(
              layout.width <= viewport.width + 1,
              `${name}: horizontal overflow`,
            );
            assert.ok(
              layout.title <= layout.svgTop + 1,
              `${name}: title overlaps SVG`,
            );
            assert.ok(
              layout.svgBottom <= layout.footer + 1,
              `${name}: footer overlaps SVG`,
            );
            if (viewport.width >= 1024)
              assert.ok(
                layout.height <= viewport.height + 1,
                `${name}: desktop scroll`,
              );
            assert.deepEqual(layout.clipped, [], `${name}: clipped SVG text`);
            await checkDiagramGeometry(page, name);
            const content = await page.locator("#diagram").textContent();
            if (id === "why-liquid") {
              for (const word of [
                "Steady-flow sensible-heat balance",
                "heat rate",
                "mass flow",
                "specific heat",
                "density",
                "volume flow",
                "ΔT",
                "8,292",
                "2.39",
              ])
                assert.ok(content.includes(word), `${name}: missing ${word}`);
            }
            if (id === "water-balance") {
              const m = await page
                .locator("[data-flow-kg-s]")
                .evaluate((e) => ({
                  flow: Number(e.dataset.flowKgS),
                  heat: Number(e.dataset.heatKw),
                  inlet: Number(e.dataset.inletC),
                  outlet: Number(e.dataset.outletC),
                  rise: Number(e.dataset.riseK),
                }));
              assert.equal(m.flow, Number(selected));
              assert.equal(m.heat, 100);
              assert.equal(m.inlet, 35);
              assert.ok(Math.abs(m.flow * 4.18 * m.rise - m.heat) < 1e-10);
              assert.ok(Math.abs(m.outlet - m.inlet - m.rise) < 1e-10);
              assert.match(content, /Steady-flow sensible-heat balance/);
              assert.ok(
                content.includes(selected === "5" ? "39.78°C" : "44.57°C"),
              );
              assert.ok(
                content.includes(selected === "5" ? "4.78 K" : "9.57 K"),
              );
            }
            if (id === "approach") assert.match(content, /35 − 30 = 5 K/);
            if (id === "capture-options" && selected === "air")
              assert.match(content, /CRAH/);
            if (id === "weather") {
              assert.match(content, /35°C/);
              assert.ok(content.includes(selected === "dry" ? "22°C" : "28°C"));
            }
            if (id === "approach-outdoors")
              assert.ok(content.includes(selected === "dry" ? "35°C" : "41°C"));
            if (id === "coolit-cdu") {
              assert.match(content, /2 MW/);
              assert.match(content, /2,125 L\/min/);
              const loaded = await page
                .locator("[data-product-photo]")
                .evaluate(async (el) => {
                  const img = new Image();
                  img.src = el.getAttribute("href");
                  await img.decode();
                  return img.naturalWidth;
                });
              assert.ok(loaded > 100);
            }
            if (
              [
                "lost-flow",
                "independent-cooling-paths",
                "cooling-derating",
              ].includes(id)
            ) {
              const m = await page
                .locator("[data-cooling-capacity]")
                .evaluate((el) => ({
                  capacity: Number(el.dataset.coolingCapacity),
                  load: Number(el.dataset.coolingLoad),
                  margin: Number(el.dataset.coolingMargin),
                  topology: el.dataset.coolingTopology,
                  fault: el.dataset.coolingFault,
                  supported: el.dataset.supported === "true",
                }));
              const isDerating = id === "cooling-derating";
              const expectedCapacity = isDerating
                ? selected.endsWith("-lost")
                  ? 0
                  : 600
                : id === "independent-cooling-paths"
                  ? 1200
                  : { none: 1800, module: 1200, "shared-path": 0 }[selected];
              assert.equal(
                m.capacity,
                expectedCapacity,
                `${name}: available heat-removal capacity`,
              );
              assert.equal(
                m.load,
                isDerating && selected.startsWith("reduced") ? 500 : 1000,
              );
              assert.equal(m.margin, m.capacity - m.load);
              assert.equal(m.supported, m.capacity >= m.load);
              assert.equal(
                m.topology,
                id === "independent-cooling-paths" ? "2n" : "n+1",
              );
              assert.equal(m.fault, isDerating ? "double-module" : selected);
              if (id === "independent-cooling-paths") {
                assert.equal((content.match(/Serving load/g) || []).length, 1);
                assert.equal(
                  (content.match(/Ready/g) || []).length,
                  selected === "none" ? 1 : 0,
                );
                assert.ok(
                  !content.includes("2,400 kW"),
                  "2N must not sum train ratings",
                );
              }
              if (isDerating) {
                if (selected.endsWith("-lost"))
                  assert.match(content, /No sustained heat-removal path/);
                else if (selected.startsWith("full"))
                  assert.match(content, /Heat accumulates at 400 kW/);
                else assert.match(content, /100 kW cooling margin/);
              }
            }
            layouts++;
          }
        }
        for (const [oldId, newId] of Object.entries({
          "less-flow": "water-balance",
          "two-loops": "heat-path",
          outdoors: "rejection",
          trace: "heat-path",
        })) {
          await go(oldId);
          assert.equal(
            await page.locator("#diagram").getAttribute("data-scene"),
            newId,
          );
        }
        await go("why-liquid");
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
        await page.locator("body").click({ position: { x: 2, y: 100 } });
        await page.keyboard.press("ArrowRight");
        await page.waitForURL(/#heat-path$/);
        await page.keyboard.press("ArrowLeft");
        await page.waitForURL(/#why-liquid$/);
        await page.goto(`${base}?teach=1#coolit-cdu`);
        assert.equal(await page.locator("#fullscreen").isVisible(), true);
        await page.close();
      }
    assert.deepEqual(errors, []);
    console.log(
      `Passed ${layouts} cooling scene/state layouts, labels, controls, real product images, legacy links, keyboard and audience modes.`,
    );
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
