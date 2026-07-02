#!/usr/bin/env python3
"""Adaugă temperatura în front matter și elimină câmpul transport."""

import re
from pathlib import Path

POSTS = Path(__file__).resolve().parent.parent / "_posts"

TEMPERATURI = {
    "barcelona": "+20°C",
    "berlin": "+4°C",
    "bucuresti": "+15°C",
    "budapesta": "+28°C",
    "cesky-krumlov": "+22°C",
    "delta-dunarii": "+16°C",
    "dresda": "+22°C",
    "katowice": "+10°C",
    "napoli": "+27°C",
    "praga": "+22°C",
    "procida": "+27°C",
    "roma": "+20°C",
    "transfagarsan": "+20°C",
    "varsovia": "+3°C",
    "venetia": "+22°C",
    "padova": "+22°C",
    "verona": "+22°C",
    "viena": "+10°C",
    "marmaris": "+27°C",
    "istanbul": "+20°C",
    "thassos": "+25°C",
    "skiathos": "+27°C",
    "skopelos": "+27°C",
    "olimp": "+25°C",
    "sithonia": "+25°C",
    "kassandra": "+25°C",
    "athos": "+25°C",
}


def slug_from_filename(name):
    stem = name.replace(".md", "")
    parts = stem.split("-", 3)
    return parts[3] if len(parts) >= 4 else stem


def patch_post(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False

    parts = text.split("---", 2)
    if len(parts) < 3:
        return False

    fm, body = parts[1], parts[2]
    changed = False

    if re.search(r"^\s*transport:", fm, re.MULTILINE):
        fm = re.sub(r"^\s*transport:.*\n", "", fm, flags=re.MULTILINE)
        changed = True

    slug = slug_from_filename(path.name)
    temp = TEMPERATURI.get(slug)
    if temp and "temperatura:" not in fm and "trip:" in fm:
        fm = re.sub(
            r"(trip:\n(?:  .+\n)+?)(  valuta:)",
            rf"\1  temperatura: {temp}\n\2",
            fm,
            count=1,
        )
        if "temperatura:" not in fm:
            fm = re.sub(r"(trip:\n)", rf"\1  temperatura: {temp}\n", fm, count=1)
        changed = True

    if not changed:
        return False

    path.write_text(f"---{fm}---{body}", encoding="utf-8")
    return True


def main():
    for path in sorted(POSTS.glob("*.md")):
        if patch_post(path):
            print(f"patched {path.name}")


if __name__ == "__main__":
    main()
