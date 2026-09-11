const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");

const base =
  process.argv[2] || "http://127.0.0.1:8765/course/prototypes/ups-format.html";
const output = process.argv[3] || "/tmp/gigawatt-ups-qa";
const sceneIds = [
  "capacity-n",
  "capacity-n1",
  "capacity-n2",
  "shared-bus",
  "two-n",
  "two-n-plus-one",
  "load-growth",
];

(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ reducedMotion: "reduce" });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(String(error)));
    const navigate = async (id, query = "") => {
      await page.goto(`${base}${query}#${id}`);
      await page.waitForSelector("#scene-jump");
      const menuFits = await page.locator("#scene-jump").evaluate((select) => {
        const style = getComputedStyle(select);
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        ctx.font = style.font;
        const longest = Math.max(
          ...Array.from(
            select.options,
            (option) => ctx.measureText(option.text).width,
          ),
        );
        return (
          longest +
            parseFloat(style.paddingLeft) +
            parseFloat(style.paddingRight) <=
          select.clientWidth + 1
        );
      });
      assert.ok(menuFits, `${id}: navigation label clips`);
      assert.equal(
        await page.locator("#caption").count(),
        0,
        `${id}: bottom subtitle returned`,
      );
      assert.equal(
        await page.locator("#location").count(),
        0,
        `${id}: secondary teaching subtitle returned`,
      );
      assert.equal(
        await page.locator(".image-label").count(),
        0,
        `${id}: generated illustration label returned`,
      );
      assert.equal(
        await page.locator("#viewer h1:visible").count(),
        1,
        `${id}: expected one audience headline`,
      );
      assert.doesNotMatch(
        await page.locator("#viewer").innerText(),
        /Generated spatial illustration|placement and scale are schematic|An interruption upstream does not have to stop the load|Conversion electronics maintain the output/,
      );
    };
    const svg = () => page.locator("#redundancy-view svg");
    const action = (key) =>
      page.locator(`#exercise-controls [data-action="${key}"]`);
    const supported = async (expected) =>
      assert.equal(
        await svg().getAttribute("data-supported"),
        String(expected),
      );
    const unavailableCount = async (state) =>
      page.locator(`#redundancy-view [data-state="${state}"]`).count();

    for (const size of [
      { width: 1440, height: 900 },
      { width: 1280, height: 720 },
      { width: 390, height: 844 },
      { width: 844, height: 390 },
    ]) {
      await page.setViewportSize(size);
      for (const id of sceneIds) {
        await navigate(id);
        const bounds = await page.evaluate(() => {
          const rect = (selector) => {
            const r = document.querySelector(selector).getBoundingClientRect();
            return {
              top: r.top,
              bottom: r.bottom,
              left: r.left,
              right: r.right,
            };
          };
          const svg = document.querySelector("#redundancy-view svg");
          const outer = rect("#redundancy-view svg");
          return {
            title: rect("#title"),
            stage: rect("#stage"),
            svg: outer,
            controls: rect("#exercise-controls"),
            footer: rect("footer"),
            strip: rect(".state-strip"),
            width: document.documentElement.scrollWidth,
            clippedText: [...svg.querySelectorAll("text")]
              .filter((element) => {
                const r = element.getBoundingClientRect();
                return (
                  r.left < outer.left - 1 ||
                  r.right > outer.right + 1 ||
                  r.top < outer.top - 1 ||
                  r.bottom > outer.bottom + 1
                );
              })
              .map((element) => element.textContent),
          };
        });
        const name = `${id} at ${size.width}×${size.height}`;
        assert.ok(
          bounds.width <= size.width + 1,
          `${name}: horizontal overflow`,
        );
        assert.ok(
          bounds.title.bottom <= bounds.stage.top + 1,
          `${name}: stage overlaps heading`,
        );
        assert.ok(
          bounds.strip.top >= bounds.stage.top - 1,
          `${name}: state strip clipped above stage`,
        );
        assert.ok(
          bounds.svg.top >= bounds.stage.top - 1,
          `${name}: SVG clipped above stage`,
        );
        assert.ok(
          bounds.svg.bottom <= bounds.controls.top + 1,
          `${name}: controls overlap SVG`,
        );
        assert.ok(
          bounds.controls.bottom <= bounds.footer.top + 1,
          `${name}: footer overlaps controls`,
        );
        assert.ok(
          bounds.stage.bottom <= bounds.footer.top + 1,
          `${name}: footer overlaps stage`,
        );
        assert.deepEqual(bounds.clippedText, [], `${name}: SVG text clips`);
        assert.equal(
          await page.locator("#circuit").isVisible(),
          false,
          `${name}: old SVG remains visible`,
        );
        assert.equal(
          await svg().isVisible(),
          true,
          `${name}: redundancy SVG absent`,
        );
        assert.equal(await page.locator("#notes").isVisible(), false);
        assert.equal(await page.locator("#open-notes").isVisible(), false);
        await page.screenshot({
          path: `${output}/${id}-${size.width}x${size.height}.png`,
          fullPage: true,
        });
      }
      for (const id of [
        "campus",
        "electrical-room",
        "equipment",
        "normal",
        "outage",
        "capacitors",
        "generator",
        "static-bypass",
        "maintenance-bypass",
        "return",
      ]) {
        await navigate(id);
        const circuitScene = [
          "normal",
          "outage",
          "capacitors",
          "generator",
          "static-bypass",
          "maintenance-bypass",
        ].includes(id);
        const bounds = await page.evaluate((circuitScene) => {
          const rect = (selector) => {
            const r = document.querySelector(selector).getBoundingClientRect();
            return {
              top: r.top,
              bottom: r.bottom,
              left: r.left,
              right: r.right,
            };
          };
          const diagram = circuitScene ? rect("#circuit") : null;
          return {
            width: document.documentElement.scrollWidth,
            stage: rect("#stage"),
            title: rect("#title"),
            footer: rect("footer"),
            strip: circuitScene ? rect(".state-strip") : null,
            diagram,
            foot: circuitScene ? rect(".diagram-foot") : null,
            clipped: circuitScene
              ? [...document.querySelectorAll("#circuit text")]
                  .filter((t) => {
                    const r = t.getBoundingClientRect();
                    return (
                      r.left < diagram.left - 1 ||
                      r.right > diagram.right + 1 ||
                      r.top < diagram.top - 1 ||
                      r.bottom > diagram.bottom + 1
                    );
                  })
                  .map((t) => t.textContent)
              : [],
          };
        }, circuitScene);
        const name = `${id} at ${size.width}×${size.height}`;
        assert.ok(
          bounds.width <= size.width + 1,
          `${name}: horizontal overflow`,
        );
        assert.ok(
          bounds.title.bottom <= bounds.stage.top + 1,
          `${name}: title overlap`,
        );
        assert.ok(
          bounds.stage.bottom <= bounds.footer.top + 1,
          `${name}: footer overlaps stage`,
        );
        assert.deepEqual(bounds.clipped, [], `${name}: clipped diagram labels`);
        if (circuitScene) {
          assert.ok(
            bounds.strip.top >= bounds.stage.top - 1,
            `${name}: clipped state`,
          );
          assert.ok(
            bounds.diagram.top >= bounds.strip.bottom - 1,
            `${name}: diagram overlaps state`,
          );
          assert.ok(
            bounds.diagram.bottom <= bounds.foot.top + 1,
            `${name}: diagram overlaps controls`,
          );
          assert.ok(
            bounds.foot.bottom <= bounds.footer.top + 1,
            `${name}: footer overlaps controls`,
          );
        }
        if (id === "equipment") {
          const photo = page.locator(".product-photo img");
          assert.equal(
            await photo.isVisible(),
            true,
            `${name}: actual product photograph absent`,
          );
          const product = await photo.evaluate((img) => ({
            loaded:
              img.complete &&
              img.naturalWidth >= 300 &&
              img.naturalHeight >= 300,
            height: img.getBoundingClientRect().height,
            width: img.getBoundingClientRect().width,
            caption: img.closest("figure").querySelector("figcaption")
              .textContent,
            bottom: img.closest("figure").getBoundingClientRect().bottom,
          }));
          assert.equal(
            product.loaded,
            true,
            `${name}: product photograph did not load`,
          );
          assert.ok(
            product.height >= 200 && product.width >= 250,
            `${name}: product photograph reduced to a thumbnail`,
          );
          assert.match(product.caption, /Schneider Easy UPS 3-Phase Modular/);
          assert.match(
            product.caption,
            /both pictured cabinets are UPS\s+units/,
          );
          assert.ok(
            product.bottom <= bounds.stage.bottom + 1,
            `${name}: equipment caption clips below stage`,
          );
          const battery = await page
            .locator(".battery-schematic")
            .boundingBox();
          assert.ok(
            battery.y + battery.height <= bounds.stage.bottom + 1,
            `${name}: battery cabinet caption clips below stage`,
          );
          assert.match(
            await page.locator(".battery-schematic").textContent(),
            /UPS battery cabinet/,
          );
        }
        if (id.endsWith("bypass")) {
          await page.locator("#toggle-supply").click();
          assert.match(
            await page.locator("#circuit").textContent(),
            /No supply/,
          );
          assert.equal(await page.locator("#circuit .wire.active").count(), 0);
          await page.locator("#toggle-supply").click();
          assert.ok((await page.locator("#circuit .wire.active").count()) > 0);
        }
        assert.equal(await page.locator("#open-notes").isVisible(), false);
        await page.screenshot({
          path: `${output}/${id}-${size.width}x${size.height}.png`,
          fullPage: true,
        });
      }
    }

    for (const size of [
      { width: 1440, height: 900 },
      { width: 390, height: 844 },
    ]) {
      await page.setViewportSize(size);
      for (const colorScheme of ["light", "dark"]) {
        await page.emulateMedia({ colorScheme });
        for (const id of [
          "campus",
          "electrical-room",
          "equipment",
          "capacitors",
        ]) {
          await navigate(id);
          const theme = await page.evaluate(() => ({
            declared: getComputedStyle(document.documentElement).colorScheme,
            titleColor: getComputedStyle(document.querySelector("#title"))
              .color,
            background: getComputedStyle(document.documentElement)
              .backgroundColor,
          }));
          assert.equal(
            theme.declared,
            colorScheme,
            `${id}: device theme not applied`,
          );
          assert.notEqual(
            theme.titleColor,
            theme.background,
            `${id}: heading invisible in ${colorScheme}`,
          );
          if (id === "capacitors") {
            const choose = (mode) =>
              page.locator(
                `#exercise-controls [data-capacitor-mode="${mode}"]`,
              );
            assert.equal(
              await choose("alone").getAttribute("aria-pressed"),
              "true",
            );
            assert.match(await page.locator("#circuit").textContent(), /15 kJ/);
            assert.match(await page.locator("#circuit").textContent(), /49 kJ/);
            await choose("ramp").click();
            assert.equal(
              await choose("ramp").getAttribute("aria-pressed"),
              "true",
            );
            assert.match(await page.locator("#circuit").textContent(), /5 kJ/);
            assert.match(
              await page.locator("#circuit").textContent(),
              /768.1 V/,
            );
            assert.match(
              await page.locator(".state-strip").innerText(),
              /Separate DC bus.*1 MW load/s,
            );
            const activeColor = await choose("ramp").evaluate(
              (e) => getComputedStyle(e).backgroundColor,
            );
            const idleColor = await choose("alone").evaluate(
              (e) => getComputedStyle(e).backgroundColor,
            );
            assert.notEqual(
              activeColor,
              idleColor,
              "Capacitor scenario selection must be visible",
            );
            await choose("alone").click();
            assert.match(await page.locator("#circuit").textContent(), /15 kJ/);
          }
          if (id === "equipment") {
            assert.equal(
              await page
                .locator(".product-photo img")
                .evaluate((img) => img.complete && img.naturalWidth > 0),
              true,
            );
          }
          await page.screenshot({
            path: `${output}/${id}-${size.width}-${colorScheme}.png`,
            fullPage: true,
          });
        }
      }
      await page.emulateMedia({ colorScheme: "light" });
      await navigate("capacity-n");
      await action("fault").click();
      await supported(false);
      assert.match(
        await svg().textContent(),
        /50 kW available · 100 kW required/,
      );

      await navigate("capacity-n1");
      assert.equal(
        await unavailableCount("fault"),
        0,
        "previous-scene fault persists",
      );
      await action("maintenance").click();
      await supported(true);
      await action("fault").click();
      await supported(false);
      assert.equal(await unavailableCount("maintenance"), 1);
      assert.equal(await unavailableCount("fault"), 1);

      await navigate("capacity-n2");
      await action("maintenance").click();
      await action("fault").click();
      await supported(true);
      assert.match(
        await svg().textContent(),
        /100 kW available · 100 kW required/,
      );

      await navigate("shared-bus");
      await action("busFault").click();
      await supported(false);
      assert.match(await svg().textContent(), /Bus fault/);
      assert.match(
        await svg().textContent(),
        /0 kW available · 100 kW required/,
      );
      assert.equal(
        await unavailableCount("available"),
        4,
        "bus fault incorrectly marks all UPS modules failed",
      );
      await action("busFault").click();
      await supported(true);

      await navigate("two-n");
      await action("maintenance").click();
      await supported(true);
      assert.equal(await unavailableCount("maintenance"), 2);
      await action("fault").click();
      await supported(false);
      assert.match(
        await svg().textContent(),
        /0\/2 paths can carry the whole load/,
      );

      await navigate("two-n-plus-one");
      await action("maintenance").click();
      await action("fault").click();
      await supported(true);
      assert.equal(await unavailableCount("maintenance"), 3);
      assert.equal(await unavailableCount("fault"), 1);
      assert.match(
        await svg().textContent(),
        /1\/2 paths can carry the whole load/,
      );

      await navigate("load-growth");
      assert.equal(await page.locator("#supply-state").innerText(), "2(N+1)");
      await supported(true);
      await action("loadKW").click();
      await supported(false);
      assert.equal(await page.locator("#supply-state").innerText(), "2N");
      assert.match(await page.locator(".ur-rack").textContent(), /150 kW/);
      assert.match(await svg().textContent(), /Insufficient UPS capacity/);
      assert.doesNotMatch(
        await svg().textContent(),
        /50 kW delivered|100 kW delivered/,
      );
      await page.screenshot({
        path: `${output}/load-growth-changed-${size.width}.png`,
        fullPage: true,
      });
    }

    await page.setViewportSize({ width: 1440, height: 900 });
    await navigate("normal");
    assert.equal(await page.locator("#circuit").isVisible(), true);
    assert.equal(await page.locator("#redundancy-view").isVisible(), false);
    await page.locator("#title").click();
    await page.keyboard.press("ArrowRight");
    await page.waitForURL(/#outage$/);
    await page.keyboard.press("PageDown");
    await page.waitForURL(/#capacitors$/);
    await page.keyboard.press("PageDown");
    await page.waitForURL(/#generator$/);
    await page.keyboard.press("PageDown");
    await page.waitForURL(/#static-bypass$/);
    assert.equal(await page.locator("#circuit").isVisible(), true);
    assert.equal(await page.locator("#redundancy-view").isVisible(), false);
    await page.keyboard.press("r");
    assert.match(
      await page.locator("#supply-state").innerText(),
      /UNAVAILABLE/,
    );
    await page.keyboard.press("PageDown");
    await page.waitForURL(/#maintenance-bypass$/);
    await page.keyboard.press("ArrowRight");
    await page.waitForURL(/#capacity-n$/);
    assert.equal(await page.locator("#circuit").isVisible(), false);
    assert.equal(await svg().isVisible(), true);
    await page.keyboard.press("ArrowLeft");
    await page.waitForURL(/#maintenance-bypass$/);
    assert.equal(await page.locator("#circuit").isVisible(), true);
    assert.equal(await page.locator("#redundancy-view").isVisible(), false);

    await navigate("capacity-n1", "?rehearse=1");
    assert.equal(await page.locator("#open-notes").isVisible(), true);
    const opened = context.waitForEvent("page");
    await page.locator("#open-notes").click();
    const notes = await opened;
    notes.on("pageerror", (error) => errors.push(String(error)));
    await notes.waitForSelector("#note-points li");
    assert.equal(await notes.locator("#viewer").isVisible(), false);
    assert.equal(await notes.locator("#notes").isVisible(), true);
    assert.ok((await notes.locator("#note-points li").count()) <= 5);
    await notes.locator('[data-action="maintenance"]').click();
    await page.waitForFunction(
      () =>
        document.querySelector('[data-module="M1"]').dataset.state ===
        "maintenance",
    );
    await notes.locator('[data-action="fault"]').click();
    await page.waitForFunction(
      () => document.querySelector(".ur-svg").dataset.supported === "false",
    );
    await notes.locator("#note-next").click();
    await page.waitForURL(/#capacity-n2$/);
    assert.equal(await unavailableCount("maintenance"), 0);
    await page.locator("#title").click();
    await page.keyboard.press("PageDown");
    await notes.waitForURL(/#shared-bus$/);
    await action("busFault").click();
    await notes.waitForFunction(
      () =>
        document
          .querySelector('[data-action="busFault"]')
          .getAttribute("aria-pressed") === "true",
    );
    await notes.close();
    for (const viewport of [
      { width: 1280, height: 720 },
      { width: 390, height: 844 },
    ]) {
      await page.setViewportSize(viewport);
      for (const colorScheme of ["light", "dark"]) {
        await page.emulateMedia({ colorScheme });
        await navigate("generator");
        for (const stage of ["utility", "waiting", "generator"]) {
          await page
            .locator(
              `#exercise-controls button[data-generator-stage="${stage}"]`,
            )
            .click();
          for (const [path, active] of [
            ["utility-input", stage === "utility"],
            ["generator-input", stage === "generator"],
            ["battery-to-dc-link", stage === "waiting"],
            ["dc-link", true],
            ["inverter-output", true],
          ]) {
            assert.equal(
              await page
                .locator(`#circuit [data-path="${path}"]`)
                .evaluate((el) => el.classList.contains("active")),
              active,
            );
          }
          assert.equal(
            await page
              .locator('#circuit [data-contact="utility"]')
              .getAttribute("data-closed"),
            String(stage === "utility"),
          );
          assert.equal(
            await page
              .locator('#circuit [data-contact="generator"]')
              .getAttribute("data-closed"),
            String(stage === "generator"),
          );
          assert.match(await page.locator("#circuit").textContent(), /100 kW/);
          if (stage === "generator")
            assert.match(
              await page.locator("#supply-state").innerText(),
              /UTILITY UNAVAILABLE/,
            );
          await page.screenshot({
            path: `${output}/generator-${stage}-${viewport.width}-${colorScheme}.png`,
            fullPage: true,
          });
        }
      }
    }
    assert.deepEqual(errors, []);
    console.log(
      "Passed 68 scene layouts, 16 theme views and capacitor scenario controls, real product photograph and caption visibility, no competing subtitles, bypass-source loss/restoration, 14 redundancy cases, SVG exclusivity, optional notes sync and keyboard navigation.",
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
