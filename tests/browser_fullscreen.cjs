const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const { mkdirSync } = require("node:fs");

// The staged slides folder, served at the site root.
const base = process.argv[2] || "http://127.0.0.1:8878/slides/";
const output = process.argv[3] || "/tmp/gigawatt-fullscreen-qa";
// One deck that puts its #viewer in full screen and one that uses the whole page.
const lessons = [
  {
    name: "overview",
    path: "overview.html?teach=1#three-paths",
    target: "viewer",
  },
  {
    name: "cooling",
    path: "cooling.html?teach=1#why-liquid",
    target: "HTML",
  },
];

async function appearance(page) {
  return page.evaluate(() => {
    const root = getComputedStyle(document.documentElement);
    const element = document.fullscreenElement;
    const fullscreen = element && getComputedStyle(element);
    return {
      prefersDark: matchMedia("(prefers-color-scheme: dark)").matches,
      rootScheme: root.colorScheme,
      rootColor: root.color,
      rootBackground: root.backgroundColor,
      target: element ? element.id || element.tagName : null,
      fullscreenScheme: fullscreen?.colorScheme,
      fullscreenColor: fullscreen?.color,
      fullscreenBackground: fullscreen?.backgroundColor,
      backdrop: element
        ? getComputedStyle(element, "::backdrop").backgroundColor
        : null,
    };
  });
}

function assertTheme(state, theme, lesson, fullscreen) {
  const description = `${lesson.name} / ${theme}`;
  assert.equal(state.prefersDark, theme === "dark", description);
  assert.equal(state.rootScheme, theme, description);
  if (!fullscreen) {
    assert.equal(state.target, null, description);
    return;
  }
  assert.equal(state.target, lesson.target, description);
  assert.equal(state.fullscreenScheme, state.rootScheme, description);
  assert.equal(state.fullscreenColor, state.rootColor, description);
  assert.equal(
    state.fullscreenBackground,
    state.rootBackground,
    `${description}: the fullscreen surface must paint the device theme background`,
  );
  if (lesson.target === "viewer")
    assert.equal(
      state.backdrop,
      state.rootBackground,
      `${description}: any area behind the viewer must use the same theme`,
    );
}

(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    let cases = 0;
    for (const theme of ["light", "dark"]) {
      for (const lesson of lessons) {
        const page = await browser.newPage({
          viewport: { width: 1280, height: 720 },
          colorScheme: theme,
          reducedMotion: "reduce",
        });
        try {
          await page.goto(new URL(lesson.path, base).href);
          await page.locator("#fullscreen").waitFor({ state: "visible" });
          const before = await appearance(page);
          assertTheme(before, theme, lesson, false);
          await page.locator("#fullscreen").click();
          await page.waitForFunction(() => !!document.fullscreenElement);
          const entered = await appearance(page);
          assertTheme(entered, theme, lesson, true);
          assert.equal(entered.rootBackground, before.rootBackground);
          assert.equal(entered.rootColor, before.rootColor);
          await page.screenshot({
            path: `${output}/${lesson.name}-${theme}-fullscreen.png`,
          });

          const opposite = theme === "light" ? "dark" : "light";
          await page.emulateMedia({ colorScheme: opposite });
          assertTheme(await appearance(page), opposite, lesson, true);
          await page.emulateMedia({ colorScheme: theme });
          assertTheme(await appearance(page), theme, lesson, true);
          await page.locator("#fullscreen").click();
          await page.waitForFunction(() => !document.fullscreenElement);
          const exited = await appearance(page);
          assertTheme(exited, theme, lesson, false);
          assert.equal(exited.rootBackground, before.rootBackground);
          cases += 1;
        } finally {
          await page.close();
        }
      }
    }
    console.log(
      `Passed ${cases} real-fullscreen cases across ${lessons.length} decks: theme persistence, live device-theme changes and exit.`,
    );
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
