import assert from "node:assert/strict";
import test from "node:test";
import {
  bypassModel,
  renderBypassDiagram,
} from "../course/prototypes/ups-bypass.js";

// Trace the rendered load-carrying network independently of the mode model.
function activeSegments(svg) {
  const segments = [];
  for (const [, d, classes] of svg.matchAll(
    /<path d="([^"]+)" class="([^"]+)"/g,
  )) {
    if (!classes.split(" ").includes("active")) continue;
    let point;
    for (const [, command, values] of d.matchAll(/([MLHV])([^MLHV]+)/g)) {
      const n = values.trim().split(/[ ,]+/).map(Number);
      const next =
        command === "H"
          ? [n[0], point[1]]
          : command === "V"
            ? [point[0], n[0]]
            : n;
      if (command !== "M") segments.push([point, next]);
      point = next;
    }
  }
  // Contact paths use local coordinates; replace those with their global bridges.
  const global = segments.filter(
    ([a, b]) => a[0] !== -14 || a[1] !== 0 || b[0] !== 14,
  );
  for (const [, xs, ys, rotation, closed, body] of svg.matchAll(
    /<g transform="translate\(([^ ]+) ([^)]+)\) rotate\(([^)]+)\)" data-contact="[^"]+" data-closed="([^"]+)">([\s\S]*?)<\/g>/g,
  )) {
    if (closed !== "true" || !body.includes("wire active")) continue;
    const x = +xs,
      y = +ys;
    global.push(
      +rotation === 90
        ? [
            [x, y - 14],
            [x, y + 14],
          ]
        : [
            [x - 14, y],
            [x + 14, y],
          ],
    );
  }
  return global;
}
function on(point, segment) {
  const [a, b] = segment;
  return (
    (a[0] === b[0] &&
      point[0] === a[0] &&
      point[1] >= Math.min(a[1], b[1]) &&
      point[1] <= Math.max(a[1], b[1])) ||
    (a[1] === b[1] &&
      point[1] === a[1] &&
      point[0] >= Math.min(a[0], b[0]) &&
      point[0] <= Math.max(a[0], b[0]))
  );
}
function connected(segments, start, end) {
  const reached = new Set(
    segments.flatMap((s, i) => (on(start, s) ? [i] : [])),
  );
  for (let changed = true; changed;) {
    changed = false;
    segments.forEach((s, i) => {
      if (reached.has(i)) return;
      if (
        [...reached].some(
          (j) =>
            s.some((p) => on(p, segments[j])) ||
            segments[j].some((p) => on(p, s)),
        )
      ) {
        reached.add(i);
        changed = true;
      }
    });
  }
  return [...reached].some((i) => on(end, segments[i]));
}
for (const mode of ["static", "maintenance"]) {
  for (const compact of [false, true]) {
    test(`${mode}, ${compact ? "portrait" : "landscape"}: source has a continuous bypass route to load`, () => {
      const { svg, model } = renderBypassDiagram({ mode, compact });
      const segments = activeSegments(svg);
      assert.equal(
        connected(
          segments,
          compact ? [105, 81] : [131, 188],
          compact ? [105, 632] : [1026, 188],
        ),
        true,
      );
      assert.equal(
        connected(
          segments,
          compact ? [253, 95] : [129, 354],
          compact ? [105, 632] : [1026, 188],
        ),
        false,
      );
      assert.equal(model.loadKW, 100);
      assert.equal(model.batteryCanSupplyLoad, false);
      assert.match(
        svg,
        /data-contact="inverter-unavailable" data-closed="false"/,
      );
      if (mode === "maintenance") {
        for (const name of [
          "ups-input",
          "bypass-input",
          "ups-output-isolation",
          "battery-disconnect",
        ]) {
          assert.match(
            svg,
            new RegExp(`data-contact="${name}" data-closed="false"`),
          );
        }
      }
    });
    test(`${mode}, ${compact ? "portrait" : "landscape"}: losing bypass source leaves demand unsupported`, () => {
      const { svg, model } = renderBypassDiagram({
        mode,
        compact,
        sourceAvailable: false,
      });
      assert.equal(activeSegments(svg).length, 0);
      assert.equal(model.loadPowered, false);
      assert.equal(model.loadKW, 0);
      assert.match(svg, /100 kW demand/);
    });
  }
}
test("an unspecified bypass mode cannot inherit forced-bypass assumptions", () => {
  assert.throws(
    () => bypassModel({ mode: "requested" }),
    /Unknown bypass mode/,
  );
});
