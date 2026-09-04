"""Validate the course source and build its single, network-independent page."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ("math.js", "diagrams.js", "course.js")
PLACEHOLDERS = ("__COURSE_DATA__", "__COURSE_CSS__", "__COURSE_SCRIPT__")


class CourseError(ValueError):
    """The editable sources do not form a complete course."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CourseError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CourseError(f"{location} must be nonempty text")
    return value


def _records(value: object, location: str) -> list[dict]:
    if not isinstance(value, list) or not value:
        raise CourseError(f"{location} must be a nonempty list")
    if any(not isinstance(item, dict) for item in value):
        raise CourseError(f"{location} must contain objects")
    return value


def validate_course(course: object, visual_ids: set[str]) -> dict:
    """Check relationships, usable evidence links, and answer integrity."""
    if not isinstance(course, dict):
        raise CourseError("The course must be a JSON object")
    for key in ("title", "subtitle"):
        _text(course.get(key), key)
    chapters = _records(course.get("chapters"), "chapters")
    lessons = _records(course.get("lessons"), "lessons")
    chapter_ids = set()
    for chapter in chapters:
        for key in ("id", "title", "kicker"):
            _text(chapter.get(key), f"chapter.{key}")
        if chapter["id"] in chapter_ids:
            raise CourseError(f"Duplicate chapter ID: {chapter['id']}")
        chapter_ids.add(chapter["id"])
    lesson_ids, used_chapters = set(), set()
    for lesson in lessons:
        for key in ("id", "chapter", "title", "eyebrow", "body", "visual", "takeaway"):
            _text(lesson.get(key), f"lesson.{key}")
        label = lesson["id"]
        if label in lesson_ids:
            raise CourseError(f"Duplicate lesson ID: {label}")
        lesson_ids.add(label)
        if lesson["chapter"] not in chapter_ids:
            raise CourseError(f"{label}: unknown chapter {lesson['chapter']}")
        used_chapters.add(lesson["chapter"])
        if lesson["visual"] not in visual_ids:
            raise CourseError(f"{label}: unknown visual {lesson['visual']}")
        notes = lesson.get("notes")
        if not isinstance(notes, list) or not notes:
            raise CourseError(f"{label}: notes must be a nonempty list")
        for note in notes:
            _text(note, f"{label}.notes")
        for source in _records(lesson.get("sources"), f"{label}.sources"):
            _text(source.get("title"), f"{label}.source.title")
            url = _text(source.get("url"), f"{label}.source.url")
            parsed = urlsplit(url)
            if (
                parsed.scheme not in {"https", "http"}
                or not parsed.netloc
                or any(character.isspace() for character in url)
            ):
                raise CourseError(f"{label}: source URL must be an absolute web URL")
        if "check" in lesson:
            check = lesson["check"]
            if not isinstance(check, dict):
                raise CourseError(f"{label}: check must be an object")
            for key in ("question", "explanation"):
                _text(check.get(key), f"{label}.check.{key}")
            options = check.get("options")
            if not isinstance(options, list) or len(options) < 2:
                raise CourseError(f"{label}: check needs at least two options")
            for option in options:
                _text(option, f"{label}.check.options")
            answer = check.get("answer")
            if type(answer) is not int or not 0 <= answer < len(options):
                raise CourseError(f"{label}: check answer must index an option")
    if used_chapters != chapter_ids:
        raise CourseError(
            f"Chapters without lessons: {sorted(chapter_ids - used_chapters)}"
        )
    return course


def declared_visual_ids(scripts: str) -> set[str]:
    """Read the renderer's public ID registry rather than maintaining a second one."""
    matches = re.findall(r"\bconst\s+VISUAL_IDS\s*=\s*(\[[^\]]*\])", scripts)
    if len(matches) != 1:
        raise CourseError("Declare one VISUAL_IDS JSON array in the JavaScript source")
    try:
        values = json.loads(matches[0])
    except json.JSONDecodeError as error:
        raise CourseError("VISUAL_IDS must use a JSON array of strings") from error
    if not values or any(not isinstance(value, str) or not value for value in values):
        raise CourseError("VISUAL_IDS must contain nonempty strings")
    if len(values) != len(set(values)):
        raise CourseError("VISUAL_IDS contains duplicates")
    return set(values)


def bundle_scripts(scripts: dict[str, str]) -> str:
    """Combine the small local ES modules while retaining their declaration bodies."""
    bundled = []
    import_pattern = re.compile(
        r"^[ \t]*import\s+\{([^}]*)\}"
        r"\s+from\s+['\"]\./(?:math|diagrams)\.js['\"];?[ \t]*(?:\n|$)",
        re.MULTILINE,
    )

    def remove_import(match: re.Match) -> str:
        if re.search(r"\bas\b", match[1]):
            raise CourseError("Bundled imports must use their original exported names")
        return ""

    for name in ASSETS:
        code = import_pattern.sub(remove_import, scripts[name])
        code = re.sub(
            r"^([ \t]*)export\s+(?=(?:async\s+)?(?:function|class|const|let|var)\b)",
            r"\1",
            code,
            flags=re.MULTILINE,
        )
        if re.search(r"^[ \t]*(?:import|export)\b", code, re.MULTILINE):
            raise CourseError(f"{name}: unsupported import or export declaration")
        bundled.append(f"// {name}\n{code.strip()}\n")
    return "\n".join(bundled)


def build(root: Path = ROOT) -> str:
    web = root / "course" / "web"
    try:
        source = (root / "course" / "lessons.json").read_text(encoding="utf-8")
        course = json.loads(source, object_pairs_hook=_unique_object)
        scripts = {name: (web / name).read_text(encoding="utf-8") for name in ASSETS}
        template = (web / "index.html").read_text(encoding="utf-8")
        css = (web / "course.css").read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CourseError(f"Cannot read course source: {error}") from error
    validate_course(course, declared_visual_ids("\n".join(scripts.values())))
    for placeholder in PLACEHOLDERS:
        if template.count(placeholder) != 1:
            raise CourseError(f"index.html must contain {placeholder} exactly once")
    if re.search(r"</style\b", css, re.IGNORECASE):
        raise CourseError("CSS must not contain a closing style tag")
    values = {
        "__COURSE_DATA__": json.dumps(
            course, ensure_ascii=False, separators=(",", ":")
        ).replace("<", "\\u003c"),
        "__COURSE_CSS__": css.strip(),
        "__COURSE_SCRIPT__": re.sub(
            r"</script", r"<\\/script", bundle_scripts(scripts), flags=re.IGNORECASE
        ),
    }
    return (
        re.sub(
            r"__COURSE_(?:DATA|CSS|SCRIPT)__", lambda match: values[match[0]], template
        ).rstrip()
        + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate source and require exact generated bytes",
    )
    args = parser.parse_args()
    try:
        result = build()
        destination = ROOT / "diagram" / "index.html"
        if args.check:
            if not destination.is_file() or destination.read_bytes() != result.encode(
                "utf-8"
            ):
                raise CourseError(
                    "diagram/index.html is stale; run uv run gigawatt-build"
                )
            print("Course source validated; diagram/index.html is current.")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(result, encoding="utf-8")
            print("Built diagram/index.html")
    except CourseError as error:
        parser.exit(1, f"Course build failed: {error}\n")


if __name__ == "__main__":
    main()
