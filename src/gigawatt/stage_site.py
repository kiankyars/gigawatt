"""Stage the homepage, reader, presentations and assets for Pages.

The site publishes an explicit list of pages and documents. A link from a
published Markdown document to a repository file the site does not publish
points at that file on GitHub instead.

Large raster images are re-encoded as WebP at a visually lossless quality and
every staged reference is renamed to match. The lossless originals stay in the
repository.
"""

from __future__ import annotations

import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
from typing import NamedTuple
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_URL = "https://github.com/kiankyars/gigawatt/"

# Editable files remain grouped by curriculum concern; publication has one root.
SLIDE_NAMES = {
    "terminology-format": "primer",
    "orientation-format": "overview",
    "workload-format": "workloads",
    "siting-format": "siting",
    "site-format": "site-design",
    "distribution-format": "distribution",
    "continuity-format": "continuity",
    "rack-energy-format": "rack-energy",
    "networking-format": "networking",
    "cooling-format": "cooling",
}
SHARED_PRESENTATION_MODULES = (
    "electrical-renderer.js", "presentation-renderers.js",
    "reader-models.js", "presentation.css",
)
# Entry pages, plus the documents and data that published pages link to or load.
# Everything else, including the repository README, stays on GitHub.
PUBLISHED_FILES = (
    "course/404.html",
    "course/homepage.html",
    "course/index.html",
    "course/domain-map.html",
    "course/README.md",
    "course/COURSE_REVIEW.md",
    "course/DOMAIN_MAP.md",
    "course/EXPANDED_COURSE.md",
    "course/SPEAKER_NOTES.md",
    "course/TEACHING_STANDARD.md",
    "course/teaching-sequences.json",
    "research/INDEX.md",
    "research/README.md",
    "research/discovery-searches.md",
)
PUBLISHED_FOLDERS = ("course/lessons", "research/sources")  # files directly inside
PUBLISHED_TREES = ("course/assets", "course/home")  # every file, recursively
TEXT_SUFFIXES = {".html", ".js", ".css", ".json", ".md"}
QUOTED_URL = re.compile(
    r"([\"'`])((?:\.\.?/|course/|prototypes/|assets/|home/|lessons/|research/|web/|"
    r"[a-zA-Z0-9_-]+\.(?:html|js|css|json|md|png|webp|jpg|svg))[^\"'`\n<>]*?)\1"
)
MARKDOWN_URL = re.compile(r"(?<=\]\()([^\s)]+)(?=\))")
# Fenced blocks, then inline code spans (which cannot cross a blank line).
MARKDOWN_CODE = re.compile(r"^(```|~~~).*?^\1[^\n]*$|(`+)(?:(?!\n[ \t]*\n).)+?\2", re.M | re.S)

# Raster images above this size are published as WebP.
CONVERT_OVER = 300_000
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg"}
# Each image takes the first encoding whose RGB PSNR against the original
# reaches MIN_PSNR. Photographs and generated art usually pass at quality 90;
# diagrams with saturated colour edges move on to near-lossless.
MIN_PSNR = 40.0
CWEBP_LADDER = (
    ("-q", "90", "-m", "6", "-sharp_yuv"),
    ("-q", "95", "-m", "6", "-sharp_yuv"),
    ("-q", "100", "-m", "6", "-sharp_yuv"),
    ("-near_lossless", "40", "-m", "6"),
    ("-near_lossless", "60", "-m", "6"),
    ("-lossless", "-z", "9"),
)
PILLOW_LADDER = (90, 95, 100, "lossless")
# A WebP that saves less than this fraction is not worth a second lossy generation.
MIN_SAVING = 0.10
CWEBP_PSNR = re.compile(r"PSNR: B:\s*([\d.]+)\s+G:\s*([\d.]+)\s+R:\s*([\d.]+)")
# A folder of images named at run time, such as `../assets/generated/${name}.png`.
TEMPLATED_IMAGE = re.compile(r"([A-Za-z0-9_./-]*/)\$\{[^{}\n]*\}(\.(?:png|jpe?g))(?![\w-])")
# The start of a URL with a host (`https://…/` or `//…/`) earlier in the same token.
EXTERNAL_TOKEN = re.compile(r"//[^\s\"'`()<>]*\Z")


class Conversion(NamedTuple):
    """One staged image published as WebP, with sizes in bytes and RGB PSNR in dB."""

    source: str
    target: str
    before: int
    after: int
    psnr: float
    setting: str


def public_path(source):
    """Map a repository source path to its stable location in the published site."""
    source = PurePosixPath(source)
    parts = source.parts
    if source == PurePosixPath("course/homepage.html"):
        return PurePosixPath("index.html")
    if source == PurePosixPath("course/index.html"):
        return PurePosixPath("read.html")
    if parts[:2] == ("course", "prototypes"):
        if len(parts) == 2:
            return PurePosixPath("slides")
        name = source.name
        if source.suffix == ".html":
            name = SLIDE_NAMES.get(source.stem, source.stem.removesuffix("-format")) + ".html"
        return PurePosixPath("slides", *parts[2:-1], name)
    if source == PurePosixPath("course/README.md"):
        return PurePosixPath("SOURCE_INDEX.md")
    if parts[:1] == ("course",):
        return PurePosixPath(*parts[1:])
    return source


def published_url(value, source):
    """Rebase local links and module imports when their containing file moves."""
    if not value or value[0] in "#?" or any(c in value for c in "\n\r\t"):
        return value
    try:
        route = urlsplit(value)
    except ValueError:
        return value
    if route.scheme or route.netloc or route.path.startswith("/"):
        return value
    if not (route.path.startswith(("./", "../", "course/", "prototypes/", "assets/", "home/", "lessons/", "research/", "web/"))
            or re.fullmatch(r"[a-zA-Z0-9_-]+\.(?:html|js|css|json|md|png|webp|jpg|svg)", route.path)):
        return value
    source = PurePosixPath(source)
    original = PurePosixPath(posixpath.normpath(str(source.parent / route.path)))
    target = public_path(original)
    relative = posixpath.relpath(str(target), str(public_path(source).parent))
    if route.path.endswith("/") and not relative.endswith("/"):
        relative += "/"
    if value.startswith("./") and not relative.startswith("."):
        relative = "./" + relative
    # Empty delimiters can be prefixes for a JavaScript URL concatenation.
    if "?" in value.split("#", 1)[0]:
        relative += "?" + route.query
    if "#" in value:
        relative += "#" + route.fragment
    return relative


def markdown_url(value, source, published=None, root=ROOT):
    """Rebase a Markdown link, or send it to GitHub when the site omits its file.

    Pages and folders under course/ keep their site address, so a link to a retired
    page reaches the 404 page. Other repository files and folders the site omits
    link to GitHub, and a missing target stays as written.
    """
    route = urlsplit(value)
    if published is None or route.scheme or route.netloc or not route.path or route.path.startswith("/"):
        return published_url(value, source)
    original = PurePosixPath(posixpath.normpath(str(PurePosixPath(source).parent / route.path)))
    if original in published or original.parts[:1] == ("..",):
        return published_url(value, source)
    in_course = original.parts[:1] == ("course",)
    fragment = "#" + route.fragment if route.fragment else ""
    if (root / original).is_file() and not (in_course and original.suffix == ".html"):
        return REPOSITORY_URL + "blob/main/" + str(original) + fragment
    if (root / original).is_dir() and not in_course:
        folder = "" if original == PurePosixPath(".") else str(original)
        return REPOSITORY_URL + "tree/main/" + folder + fragment
    return published_url(value, source)


def markdown_links(content, rewrite):
    """Apply rewrite to each Markdown link target outside code blocks and code spans."""
    pieces, start = [], 0
    for code in MARKDOWN_CODE.finditer(content):
        pieces.append(MARKDOWN_URL.sub(lambda match: rewrite(match[1]), content[start:code.start()]))
        pieces.append(code[0])
        start = code.end()
    pieces.append(MARKDOWN_URL.sub(lambda match: rewrite(match[1]), content[start:]))
    return "".join(pieces)


def published_text(content, source, published=None, root=ROOT):
    """Rebase the links in one staged text file.

    Markdown rewrites only real link targets, so code spans keep repository paths.
    """
    if PurePosixPath(source).suffix == ".md":
        return markdown_links(content, lambda value: markdown_url(value, source, published, root))
    return QUOTED_URL.sub(
        lambda match: match[1] + published_url(match[2], source) + match[1], content
    )


def has_alpha(path):
    """Whether a PNG can carry transparency (an alpha channel or a tRNS chunk)."""
    with open(path, "rb") as image:
        if image.read(8) != b"\x89PNG\r\n\x1a\n":
            return False
        while header := image.read(8):
            length, kind = int.from_bytes(header[:4], "big"), header[4:]
            if kind == b"IHDR":
                colour = image.read(length)[9]
                if colour in (4, 6):
                    return True
                image.seek(4, 1)
            elif kind == b"tRNS":
                return True
            elif kind == b"IDAT":
                return False
            else:
                image.seek(length + 4, 1)
    return False


def combined_psnr(channel_psnrs):
    """PSNR over all colour channels, from per-channel PSNRs in dB."""
    mse = sum(255 ** 2 / 10 ** (value / 10) for value in channel_psnrs) / len(channel_psnrs)
    return math.inf if mse == 0 else 10 * math.log10(255 ** 2 / mse)


def encode_cwebp(source, target, attempt, alpha):
    """Encode with cwebp and return the RGB PSNR it reports against the source."""
    # -exact keeps colour under transparent pixels, so PSNR measures only real change.
    command = ["cwebp", *attempt, *(["-exact"] if alpha else []), "-print_psnr", str(source), "-o", str(target)]
    result = subprocess.run(command, capture_output=True, text=True)
    match = CWEBP_PSNR.search(result.stderr + result.stdout)
    if result.returncode or not match:
        raise RuntimeError(f"cwebp could not convert {source}:\n{result.stderr.strip()}")
    return combined_psnr([float(value) for value in match.groups()])


def encode_pillow(source, target, attempt, alpha):
    """Encode with Pillow and return the RGB PSNR of the result against the source."""
    from PIL import Image, ImageChops, ImageStat

    with Image.open(source) as original:
        original = original.convert("RGBA" if alpha else "RGB")
    options = {"lossless": True} if attempt == "lossless" else {"quality": attempt, "method": 6}
    original.save(target, "WEBP", exact=alpha, **options)
    with Image.open(target) as encoded:
        encoded = encoded.convert(original.mode)
    squares = ImageStat.Stat(ImageChops.difference(original.convert("RGB"), encoded.convert("RGB"))).sum2
    mse = sum(squares) / (3 * original.width * original.height)
    return math.inf if mse == 0 else 10 * math.log10(255 ** 2 / mse)


def webp_encoder():
    """Prefer cwebp; fall back to Pillow when it can write WebP."""
    if shutil.which("cwebp"):
        return "cwebp"
    try:
        from PIL import features
    except ImportError:
        return None
    return "pillow" if features.check("webp") else None


def encode_webp(source, target, encoder):
    """Try each quality in turn until the WebP is visually lossless.

    Returns the PSNR in dB and the encoder setting that reached it.
    """
    alpha = source.suffix.lower() == ".png" and has_alpha(source)
    encode, ladder = (encode_cwebp, CWEBP_LADDER) if encoder == "cwebp" else (encode_pillow, PILLOW_LADDER)
    for attempt in ladder:
        psnr = encode(source, target, attempt, alpha)
        if psnr >= MIN_PSNR:
            return psnr, " ".join(attempt) if isinstance(attempt, tuple) else f"quality {attempt}"
    raise RuntimeError(f"No WebP encoding of {source} reached {MIN_PSNR} dB")


def image_references(destination, renamed, templated):
    """Rename converted images in every staged text file except the asset records.

    JSON files under assets/ record the repository originals and their hashes, a
    course/ path names a repository file, a URL with a host names a remote file, and
    Markdown prose and code spans describe the repository, so all of these keep the
    original names. Markdown links follow the published files.
    """
    names = {PurePosixPath(old).name: PurePosixPath(new).name for old, new in renamed.items()}
    reference = re.compile(
        r"(?<![\w.-])((?:[\w.-]+/)*)(" + "|".join(map(re.escape, sorted(names, key=len, reverse=True)))
        + r")(?![\w-]|\.\w)"
    )

    def rename(match):
        prefix = match[1]
        # Only the text just before a match can hold its scheme and host.
        remote = EXTERNAL_TOKEN.search(match.string, max(0, match.start() - 2048), match.start())
        return match[0] if prefix.startswith("course/") or remote else prefix + names[match[2]]

    def template(match, folder):
        target = PurePosixPath(posixpath.normpath(str(folder / match[1])))
        return match[1] + match[0][len(match[1]):-len(match[2])] + ".webp" if (target, match[2]) in templated else match[0]

    for path in sorted(destination.rglob("*")):
        relative = PurePosixPath(path.relative_to(destination).as_posix())
        if path.suffix not in TEXT_SUFFIXES or (path.suffix == ".json" and relative.parts[0] == "assets"):
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            updated = markdown_links(content, lambda value: reference.sub(rename, value) if names else value)
        else:
            updated = reference.sub(rename, content) if names else content
            updated = TEMPLATED_IMAGE.sub(lambda match: template(match, relative.parent), updated)
        if updated != content:
            path.write_text(updated, encoding="utf-8")


def convert_images(destination, convert_over=CONVERT_OVER, encoder=None):
    """Publish large PNG and JPEG images as WebP and rename their references.

    Returns one Conversion per published WebP, with paths relative to the destination.
    """
    files = [p for p in destination.rglob("*") if p.is_file()]
    templated = set()
    for path in files:
        if path.suffix in TEXT_SUFFIXES and not (path.suffix == ".json" and path.relative_to(destination).parts[0] == "assets"):
            folder = PurePosixPath(path.parent.relative_to(destination).as_posix())
            for match in TEMPLATED_IMAGE.finditer(path.read_text(encoding="utf-8")):
                templated.add((PurePosixPath(posixpath.normpath(str(folder / match[1]))), match[2]))

    def forced(path):
        relative = PurePosixPath(path.relative_to(destination).as_posix())
        return (relative.parent, path.suffix) in templated

    images = [
        p for p in files
        if p.suffix.lower() in RASTER_SUFFIXES and (p.stat().st_size > convert_over or forced(p))
    ]
    if not images:
        return []
    encoder = encoder or webp_encoder()
    if encoder is None:
        raise RuntimeError(
            f"{len(images)} images need WebP conversion, but neither cwebp nor Pillow with WebP "
            "support is available. Install the webp package (for example apt-get install webp)."
        )
    for image in images:
        if image.with_suffix(".webp").exists():
            raise ValueError(f"Cannot publish {image} as WebP: {image.with_suffix('.webp')} already exists")

    with tempfile.TemporaryDirectory() as scratch:
        def convert(image):
            target = Path(scratch) / (str(image.relative_to(destination)).replace(os.sep, "__") + ".webp")
            return (image, target, *encode_webp(image, target, encoder))

        with ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as pool:
            results = list(pool.map(convert, images))
        conversions = []
        for image, target, psnr, setting in results:
            before, after = image.stat().st_size, target.stat().st_size
            if forced(image) or after <= (1 - MIN_SAVING) * before:
                shutil.move(target, image.with_suffix(".webp"))
                image.unlink()
                conversions.append(Conversion(
                    image.relative_to(destination).as_posix(),
                    image.with_suffix(".webp").relative_to(destination).as_posix(),
                    before, after, psnr, setting,
                ))
        renamed = {conversion.source: conversion.target for conversion in conversions}

    kept = {PurePosixPath(p.relative_to(destination).as_posix()).name for p in destination.rglob("*") if p.is_file()}
    for original in renamed:
        if PurePosixPath(original).name in kept:
            raise ValueError(f"Another staged file shares the name of {original}, so its references are ambiguous")
    converted_folders = {(PurePosixPath(old).parent, PurePosixPath(old).suffix) for old in renamed}
    for folder, suffix in templated & converted_folders:
        if (destination / folder).is_dir() and any((destination / folder).glob("*" + suffix)):
            raise ValueError(f"{folder}/*{suffix} is named at run time but was not converted completely")
    image_references(destination, renamed, templated & converted_folders)
    return conversions


def published_files(root):
    """The repository files the site publishes, as paths relative to the root."""
    catalog = json.loads((root / "course/teaching-sequences.json").read_text())
    presentation_html = {
        Path("course") / urlsplit(chapter["href"]).path
        for presentation in catalog["presentations"]
        for chapter in presentation["chapters"]
    }
    presentation_html.update({
        Path("course/prototypes/presenter.html"),
        Path("course/prototypes/case-studies.html"),
    })
    paths = {Path(name) for name in PUBLISHED_FILES}
    paths.update(
        p.relative_to(root) for p in (root / "course/prototypes").glob("*")
        if p.is_file() and (p.suffix in {".js", ".css"} or p.relative_to(root) in presentation_html)
    )
    paths.update(Path("course/web") / name for name in SHARED_PRESENTATION_MODULES)
    for directory in PUBLISHED_FOLDERS:
        paths.update(p.relative_to(root) for p in (root / directory).glob("*") if p.is_file())
    for directory in PUBLISHED_TREES:
        paths.update(p.relative_to(root) for p in (root / directory).rglob("*") if p.is_file())
    return sorted(path for path in paths if (root / path).is_file())


def stage(root=ROOT, destination=None, convert_over=CONVERT_OVER, encoder=None, conversions=None):
    """Stage the site into destination (default _site) and return its path.

    Pass a list as conversions to receive the record of each image published as WebP.
    """
    destination = destination or root / "_site"
    # Rebuild our generated directory so retired routes cannot survive a later stage.
    if destination.exists() and any(destination.iterdir()):
        if not (destination / ".nojekyll").is_file():
            raise ValueError(f"Refusing to replace a non-staged directory: {destination}")
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    # Mark the directory first, so a stage that stops partway can still be replaced.
    (destination / ".nojekyll").touch()
    paths = published_files(root)
    published = {PurePosixPath(path.as_posix()) for path in paths}
    for path in paths:
        target = destination / public_path(path.as_posix())
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in TEXT_SUFFIXES:
            content = published_text((root / path).read_text(), path.as_posix(), published, root)
            target.write_text(content, encoding="utf-8")
        else:
            shutil.copyfile(root / path, target)
    converted = convert_images(destination, convert_over, encoder)
    if conversions is not None:
        conversions.extend(converted)
    return destination


def size_of(directory):
    return sum(p.stat().st_size for p in directory.rglob("*") if p.is_file())


if __name__ == "__main__":
    converted = []
    site = stage(conversions=converted)
    if converted:
        before, after = sum(c.before for c in converted), sum(c.after for c in converted)
        lowest = min(converted, key=lambda c: c.psnr)
        print(
            f"Published {len(converted)} images as WebP: {before / 1e6:.1f} MB became {after / 1e6:.1f} MB; "
            f"lowest PSNR {lowest.psnr:.1f} dB ({lowest.target})"
        )
    print(f"Staged course at {site} ({size_of(site) / 1e6:.1f} MB)")
