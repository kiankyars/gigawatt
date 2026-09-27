// The reader's Primer vocabulary is the Primer deck's reading target.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";
import { scenes } from "../course/prototypes/terminology-scenes.js";

const read = (path) => readFileSync(new URL(path, import.meta.url), "utf8");
const source = read("../course/web/reader.js");
const start = source.indexOf("const PRIMER_VOCABULARY = [");
const vocabulary = vm.runInNewContext(
  `${source.slice(start, source.indexOf("\n];\n", start) + 3)}\nPRIMER_VOCABULARY;`,
);
const course = JSON.parse(read("../course/expanded-course.json"));
const lessons = new Set(course.lessons.map((lesson) => lesson.id));
const glossary = new Set(course.glossary.map((entry) => entry.term));

test("the vocabulary follows the Primer's slides in order", () => {
  assert.deepEqual(Array.from(vocabulary, ([topic]) => topic), scenes.map((scene) => scene.label));
});

test("every term has a two-sentence definition and somewhere to go next", () => {
  const terms = vocabulary.flatMap(([, entries]) => entries);
  for (const [term, definition, glossaryTerm, lesson] of terms) {
    const sentences = definition.split(/(?<=[.!?])\s+(?=[A-Z0-9])/);
    assert.equal(sentences.length, 2, `${term}: ${definition}`);
    assert.doesNotMatch(definition, /—/, `${term}: no em-dashes`);
    assert.ok(lessons.has(lesson), `${term}: ${lesson} is a lesson`);
    if (glossaryTerm !== null) assert.ok(glossary.has(glossaryTerm), `${term}: glossary has ${glossaryTerm}`);
  }
  const named = terms.map(([term]) => term).join(" | ");
  for (const acronym of ["CDU (coolant distribution unit)", "RMS (root mean square)", "Power supply unit (PSU)"])
    assert.ok(named.includes(acronym), `${acronym} is defined`);
});

test("the Primer deck's Reading link opens the vocabulary, never a default lesson", () => {
  const chrome = read("../course/prototypes/slide-chrome.js");
  assert.match(chrome, /terminology: 'primer-vocabulary'/);
  assert.match(chrome, /primer: 'primer-vocabulary'/);
  assert.match(chrome, /if \(!reading && nav && \(sourceLink \|\| references\[deck\]\)\)/);
  assert.match(source, /const PRIMER_VIEW = "primer-vocabulary";/);
  assert.match(source, /if \(id === "primer" \|\| id === PRIMER_VIEW\)/);
});
