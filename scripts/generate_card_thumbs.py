#!/usr/bin/env python3
"""Generează thumbnail-uri pentru carduri mici — downscale fin, fără sharpen."""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
IMAGES = ROOT / "assets" / "images"
THUMB_CROPS = ROOT / "_data" / "thumb_crops.yml"

# ~2x față de înălțimea cardului (240px) pentru ecrane retina
CARD_W = 800
CARD_H = 480


def load_thumb_crops() -> dict[str, str]:
    crops: dict[str, str] = {}
    if not THUMB_CROPS.exists():
        return crops
    for line in THUMB_CROPS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        slug, _, value = line.partition(":")
        crops[slug.strip()] = value.strip()
    return crops


def post_slug(path: Path) -> str:
    return path.stem.split("-", 3)[-1]


def cover_crop(
    img: Image.Image,
    target_w: int,
    target_h: int,
    position: str = "center",
) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        if position in {"right", "center-right"}:
            left = src_w - new_w
        elif position == "left":
            left = 0
        else:
            left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        new_h = int(src_w / target_ratio)
        if position == "top":
            top = 0
        elif position == "bottom":
            top = src_h - new_h
        else:
            top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)

    cropped = img.crop(box)
    return resize_soft(cropped, target_w, target_h)


def resize_soft(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    while w // 2 >= target_w * 1.5 and h // 2 >= target_h * 1.5:
        w //= 2
        h //= 2
        img = img.resize((w, h), Image.Resampling.LANCZOS)

    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)


def card_path_for(image_field: str) -> Path | None:
    if not image_field or "://" in image_field or not image_field.startswith("assets/images/"):
        return None
    rel = image_field.removeprefix("assets/images/")
    src = IMAGES / rel
    if not src.exists():
        return None
    stem = src.with_suffix("")
    return stem.parent / f"{stem.name}-card.webp"


def image_field_for(post: Path) -> str | None:
    for line in post.read_text(encoding="utf-8").splitlines():
        if line.startswith("image:"):
            return line.split(":", 1)[1].strip()
    return None


def generate_card(src: Path, dst: Path, position: str = "center") -> None:
    with Image.open(src) as img:
        thumb = cover_crop(img, CARD_W, CARD_H, position)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".webp.tmp")
    thumb.save(tmp, "WEBP", quality=88, method=6)
    tmp.replace(dst)
    print(f"  {dst.relative_to(ROOT)} ({position})")


def main():
    crops = load_thumb_crops()
    seen_src: set[Path] = set()
    for post in sorted(POSTS.glob("*.md")):
        image_field = image_field_for(post)
        if image_field is None:
            continue
        dst = card_path_for(image_field)
        if dst is None:
            continue
        src = IMAGES / image_field.removeprefix("assets/images/")
        if src in seen_src:
            continue
        seen_src.add(src)
        position = crops.get(post_slug(post), "center")
        generate_card(src, dst, position)
    print(f"done ({len(seen_src)} surse)")


if __name__ == "__main__":
    main()
