const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");
const base =
  process.argv[2] ||
  "http://127.0.0.1:8765/course/prototypes/cooling-format.html";
const output = process.argv[3] || "/tmp/gigawatt-cooling-qa";
const variants = {
  "why-liquid": [null],
  "capture-options": [null],
  "rack-coolant-entry": [null],
  "capture-rear-door": [null],
  "capture-immersion": [null],
  "cold-plate": [null],
  "local-heat-flux": [null],
  "device-temperature": [null],
  "water-balance": ["2.5", "5"],
  "pump-operating-point": [null],
  approach: [null],
  "coolit-cdu": ["true", "false"],
  "lost-flow": [null],
  "independent-cooling-paths": ["none", "shared-path"],
  "cooling-derating": [null],
  "cooling-retrofit": [null],
};
const controlSettings = {
  "water-balance": "flow",
  "coolit-cdu": "interior",
  "independent-cooling-paths": "pathFault",
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
    const continuity = svg.querySelector("[data-continuity-diagram]");
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
          await page.waitForSelector("#diagram > title", { state: "attached" });
        };
        for (const [id, states] of Object.entries(variants)) {
          await go(id);
          assert.equal(await page.locator("h1:visible").count(), 1);
          assert.equal(await page.locator("#fullscreen").isVisible(), false);
          assert.equal(await page.locator("#scenes option").count(), 16);
          assert.equal(
            await page.locator("#diagram").getAttribute("data-scene"),
            id,
            `${id}: requested scene renders instead of falling back`,
          );
          assert.equal(
            await page.locator("#scenes").inputValue(),
            String(Object.keys(variants).indexOf(id)),
            `${id}: chapter order`,
          );
          const setting = controlSettings[id];
          assert.equal(
            await page.locator("#actions button").count(),
            setting ? states.length : 0,
            `${id}: only the intended action controls remain`,
          );
          if (id === "independent-cooling-paths")
            assert.equal(
              await page.locator("[data-cooling-fault]").getAttribute("data-cooling-fault"),
              "shared-path",
            );
          for (const selected of states) {
            if (setting) {
              const button = page.locator(
                `#actions [data-setting="${setting}"][data-value="${selected}"]`,
              );
              await button.focus();
              await page.keyboard.press("Enter");
              assert.equal(await button.getAttribute("aria-pressed"), "true");
              assert.equal(
                await page.locator(`#actions [data-setting="${setting}"][aria-pressed="true"]`).count(),
                1,
              );
              const colors = await page
                .locator(`#actions [data-setting="${setting}"]`)
                .evaluateAll((buttons) =>
                  buttons.map((button) => getComputedStyle(button).backgroundColor),
                );
              assert.notEqual(colors[0], colors[1], `${id}: selected state looks distinct`);
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
            const content = (await page.locator("#diagram text").allTextContents()).join(" ");
            if (id === "why-liquid") {
              for (const word of ["Q̇ = ṁ cₚ ΔT = ρ V̇ cₚ ΔT", "8,292", "2.39"])
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
                content.includes(selected === "5" ? "4.78°C" : "9.57°C"),
              );
            }
            if (id === "approach") {
              assert.match(content, /35°C − 30°C = 5°C/);
              assert.match(content, /fluids stay separate/);
            }
            if (id === "capture-options") assert.match(content, /CRAH/);
            if (id === "capture-options") {
              for (const phrase of ["CRAH", "CDU", "Facility water"])
                assert.ok(content.includes(phrase), `${name}: missing ${phrase}`);
            }
            if (id === "device-temperature") {
              for (const phrase of ["35°C + 32°C = 67°C", "35°C + 48°C = 83°C", "80°C limit"])
                assert.ok(content.includes(phrase), `${name}: missing ${phrase}`);
            }
            if (id === "pump-operating-point") {
              assert.deepEqual(
                await page.locator("#diagram [data-curve]").evaluateAll((curves) =>
                  curves.map((curve) => curve.dataset.curve),
                ),
                ["pump", "clean", "restricted"],
                "Both circuit curves remain visible with the common pump curve",
              );
              for (const flow of ["2 L/s", "1.41 L/s"])
                assert.ok(content.includes(flow), `${name}: missing operating flow ${flow}`);
            }
            if (id === "coolit-cdu") {
              assert.match(content, /2 MW/);
              assert.match(content, /2,125 L\/min/);
              assert.match(
                await page.locator("[data-product-photo]").getAttribute("href"),
                selected === "true" ? /cooling-chx2000-inside\.jpeg$/ : /cooling-chx2000-front\.png$/,
                "The photo follows the cabinet/interior selection",
              );
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
            if (id === "lost-flow") {
              assert.deepEqual(
                await page.locator("[data-redundancy-case]").evaluateAll((cases) =>
                  cases.map((el) => ({
                    name: el.dataset.redundancyCase,
                    installed: Number(el.dataset.installedCdus),
                    required: Number(el.dataset.requiredCdus),
                  })),
                ),
                [
                  { name: "n", installed: 2, required: 2 },
                  { name: "n-plus-one", installed: 3, required: 2 },
                  { name: "two-n", installed: 4, required: 2 },
                ],
              );
              assert.match(content, /Facility path is still shared/);
              assert.match(content, /Either train can carry the load/);
            }
            if (id === "independent-cooling-paths") {
              const m = await page.locator("[data-cooling-capacity]").evaluate((el) => ({
                capacity: Number(el.dataset.coolingCapacity),
                load: Number(el.dataset.coolingLoad),
                margin: Number(el.dataset.coolingMargin),
                topology: el.dataset.coolingTopology,
                fault: el.dataset.coolingFault,
                supported: el.dataset.supported === "true",
              }));
              assert.deepEqual(m, {
                capacity: 1200,
                load: 1000,
                margin: 200,
                topology: "2n",
                fault: selected,
                supported: true,
              });
              assert.equal((content.match(/Serving load/g) || []).length, 1);
              assert.equal((content.match(/Ready/g) || []).length, selected === "none" ? 1 : 0);
              assert.ok(!content.includes("2,400 kW"), "2N must not sum train ratings");
            }
            if (id === "cooling-derating") {
              assert.deepEqual(
                await page.locator("[data-load-case]").evaluateAll((cases) =>
                  cases.map((el) => ({
                    name: el.dataset.loadCase,
                    heat: Number(el.dataset.caseHeat),
                    capacity: Number(el.dataset.caseCapacity),
                    margin: Number(el.dataset.caseMargin),
                    supported: el.dataset.caseSupported === "true",
                  })),
                ),
                [
                  { name: "full", heat: 1000, capacity: 600, margin: -400, supported: false },
                  { name: "reduced", heat: 500, capacity: 600, margin: 100, supported: true },
                ],
                "Original and reduced load stay visible together",
              );
              assert.match(content, /400 kW excess heat/);
              assert.match(content, /100 kW cooling margin/);
            }
            if (id === "cooling-retrofit") {
              for (const phrase of ["100 kW", "85 kW", "15 kW", "20 kW capacity", "5 kW"])
                assert.ok(content.includes(phrase), `${name}: missing heat split or air allowance ${phrase}`);
            }
            layouts++;
          }
        }
        for (const [oldId, newId] of Object.entries({
          "heat-path": "capture-options",
          "capture-coldplates": "capture-options",
          "crah-cdu": "capture-options",
          "branch-flow": "pump-operating-point",
          "coolant-interfaces": "cooling-retrofit",
        })) {
          await go(oldId);
          assert.equal(
            await page.locator("#diagram").getAttribute("data-scene"),
            newId,
          );
        }
        await go("why-liquid");
        assert.match(
          await page.locator(".reading-link").getAttribute("href"),
          /index\.html#d10-local-thermal-paths$/,
        );
        await page.locator("body").click({ position: { x: 2, y: 100 } });
        await page.keyboard.press("ArrowRight");
        await page.waitForURL(/#capture-options$/);
        await page.keyboard.press("ArrowLeft");
        await page.waitForURL(/#why-liquid$/);
        await go("cooling-retrofit");
        assert.equal(await page.locator("#next").isDisabled(), true);
        assert.match(
          await page.locator(".reading-link").getAttribute("href"),
          /index\.html#d10-cdu-interfaces$/,
        );
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
