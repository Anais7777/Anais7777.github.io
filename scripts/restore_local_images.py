#!/usr/bin/env python3
"""Restaurează pozele locale pentru destinațiile vechi; Unsplash doar pentru cele noi."""

import re
from pathlib import Path

POSTS = Path(__file__).resolve().parent.parent / "_posts"

# Destinații — poze proprii din assets/images/
LOCAL_IMAGES = {
    "marmaris": "assets/images/marmaris.webp",
    "istanbul": "assets/images/istanbul.webp",
    "muntenegru": "assets/images/muntenegru.webp",
    "thassos": "assets/images/thassos.webp",
    "skiathos": "assets/images/skiathos.webp",
    "skopelos": "assets/images/skopelos.webp",
    "olimp": "assets/images/olimp.webp",
    "sithonia": "assets/images/sithonia.webp",
    "kassandra": "assets/images/sithonia.webp",
    "athos": "assets/images/sithonia.webp",
    "creta": "assets/images/creta.webp",
    "arges": "assets/images/Arges/arges.jpg",
    "auschwitz": "assets/images/Auschwitz/auschwitz.jpg",
    "barcelona": "assets/images/Barcelona/barcelona.jpg",
    "bassano-del-grappa": "assets/images/Bassano/bassano.jpg",
    "budapesta": "assets/images/Budapesta/budapesta.jpg",
    "cesky-krumlov": "assets/images/CeskyKrumlov/cesky-krumlov.jpg",
    "delta-dunarii": "assets/images/DeltaDunarii/delta-dunarii.jpg",
    "dresda": "assets/images/Dresda/dresda.jpg",
    "katowice": "assets/images/Katowice/katowice.jpg",
    "napoli": "assets/images/Napoli/napoli.jpg",
    "padova": "assets/images/Padova/padova.jpg",
    "praga": "assets/images/Praga/praga.jpg",
    "praid": "assets/images/Praid/praid.jpg",
    "procida": "assets/images/Procida/procida.jpg",
    "roma": "assets/images/Roma/roma.jpg",
    "transfagarsan": "assets/images/Transfagarasan/transfagarsan.jpg",
    "varsovia": "assets/images/Varsovia/varsovia.jpg",
    "vatican": "assets/images/Vatican/vatican.jpg",
    "venetia": "assets/images/Venetia/venetia.jpg",
    "verona": "assets/images/Verona/verona.jpg",
    "viena": "assets/images/Viena/viena.jpg",
}


def slug_from_filename(name):
    stem = name.replace(".md", "")
    parts = stem.split("-", 3)
    return parts[3] if len(parts) >= 4 else stem


def main():
    for path in sorted(POSTS.glob("*.md")):
        slug = slug_from_filename(path.name)
        local = LOCAL_IMAGES.get(slug)
        if not local:
            continue

        text = path.read_text(encoding="utf-8")
        new_text, count = re.subn(
            r"^image: .+$",
            f"image: {local}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if count:
            path.write_text(new_text, encoding="utf-8")
            print(f"restored {path.name} -> {local}")


if __name__ == "__main__":
    main()
