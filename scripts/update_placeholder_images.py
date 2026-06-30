#!/usr/bin/env python3
"""Actualizează imaginile postărilor cu URL-uri Unsplash placeholder."""

import re
from pathlib import Path

POSTS = Path(__file__).resolve().parent.parent / "_posts"

# Unsplash — imagini reprezentative per destinație
IMAGES = {
    "barcelona": "https://images.unsplash.com/photo-1583422409516-2895c77bed99?w=900&auto=format&fit=crop&q=80",
    "berlin": "https://images.unsplash.com/photo-1560969184-10fe6639e047?w=900&auto=format&fit=crop&q=80",
    "bucuresti": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=900&auto=format&fit=crop&q=80",
    "budapesta": "https://images.unsplash.com/photo-1549297126-59e4d6094d10?w=900&auto=format&fit=crop&q=80",
    "cesky-krumlov": "https://images.unsplash.com/photo-1600725666056-101fd9d24dda?w=900&auto=format&fit=crop&q=80",
    "delta-dunarii": "https://images.unsplash.com/photo-1596484552834-064416301d85?w=900&auto=format&fit=crop&q=80",
    "dresda": "https://images.unsplash.com/photo-1569949385872-10f403266a75?w=900&auto=format&fit=crop&q=80",
    "katowice": "https://images.unsplash.com/photo-1615460549969-36fa19521a21?w=900&auto=format&fit=crop&q=80",
    "napoli": "https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=900&auto=format&fit=crop&q=80",
    "praga": "https://images.unsplash.com/photo-1541849546-216549fe1262?w=900&auto=format&fit=crop&q=80",
    "procida": "https://images.unsplash.com/photo-1523906834658-5e2c750b082e?w=900&auto=format&fit=crop&q=80",
    "roma": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=900&auto=format&fit=crop&q=80",
    "transfagarsan": "https://images.unsplash.com/photo-1596423132593-2e2c4f5c9eaf?w=900&auto=format&fit=crop&q=80",
    "varsovia": "https://images.unsplash.com/photo-1519197924294-8895fa5e2b66?w=900&auto=format&fit=crop&q=80",
    "venetia": "https://images.unsplash.com/photo-1514890546007-1f5739927117?w=900&auto=format&fit=crop&q=80",
    "viena": "https://images.unsplash.com/photo-1601918774946-304208d1a0d4?w=900&auto=format&fit=crop&q=80",
}


def slug_from_filename(name):
    stem = name.replace(".md", "")
    parts = stem.split("-", 3)
    return parts[3] if len(parts) >= 4 else stem


def main():
    for path in sorted(POSTS.glob("*.md")):
        slug = slug_from_filename(path.name)
        url = IMAGES.get(slug)
        if not url:
            print(f"skip {path.name}")
            continue

        text = path.read_text(encoding="utf-8")
        new_text, count = re.subn(
            r"^image: .+$",
            f"image: {url}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if count:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.name}")


if __name__ == "__main__":
    main()
