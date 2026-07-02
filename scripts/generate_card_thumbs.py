#!/usr/bin/env python3
"""Generează thumbnail-uri optimizate pentru carduri (fără over-sharpen la downscale)."""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
IMAGES = ROOT / "assets" / "images"

# ~2x față de înălțimea cardului (240px) pentru ecrane retina
CARD_W = 800
CARD_H = 480


def cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)

    cropped = img.crop(box)
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def card_path_for(image_field: str) -> Path | None:
    if not image_field or "://" in image_field or not image_field.startswith("assets/images/"):
        return None
    rel = image_field.removeprefix("assets/images/")
    src = IMAGES / rel
    if not src.exists():
        return None
    stem = src.with_suffix("")
    return stem.parent / f"{stem.name}-card.webp"


def generate_card(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        thumb = cover_crop(img, CARD_W, CARD_H)
    dst.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(dst, "WEBP", quality=82, method=6)
    print(f"  {dst.relative_to(ROOT)}")


def collect_image_fields() -> set[str]:
    fields = set()
    for post in POSTS.glob("*.md"):
        text = post.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("image:"):
                fields.add(line.split(":", 1)[1].strip())
                break
    return fields


def main():
    seen_src: set[Path] = set()
    for image_field in sorted(collect_image_fields()):
        dst = card_path_for(image_field)
        if dst is None:
            continue
        src = IMAGES / image_field.removeprefix("assets/images/")
        if src in seen_src:
            continue
        seen_src.add(src)
        generate_card(src, dst)
    print(f"done ({len(seen_src)} surse)")


if __name__ == "__main__":
    main()
