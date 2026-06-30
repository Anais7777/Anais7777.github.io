#!/usr/bin/env python3
"""Generează postări Jekyll structurate din datele Excel."""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
IMAGES = ROOT / "assets" / "images"
EXCEL = ROOT / "excel datas"

PLACEHOLDER = "*Urmează să completez cu povestea mea.*"


def fmt(n):
    if n is None:
        return None
    return f"{int(round(n)):,}".replace(",", " ")


def transport_label(t):
    parts = []
    if t.get("masina"):
        parts.append("cu mașina")
    if t.get("avion"):
        parts.append("avion")
    if t.get("tren"):
        parts.append("tren")
    return " · ".join(parts) if parts else None


def yaml_trip(t):
    lines = ["trip:"]
    for key in (
        "plecare",
        "intoarcere",
        "durata",
        "persoane",
        "valuta",
        "buget_actual",
        "cazare",
        "cheltuieli_masina",
        "bilete_avion",
        "transport_intern",
        "restaurante",
        "alimente",
        "bilete_locatii",
        "cumparaturi",
        "suvenire",
        "temperatura",
    ):
        if t.get(key) is not None:
            lines.append(f"  {key}: {t[key]}")
    return "\n".join(lines)


def body_sections(t, has_car, has_cazare, intro=None):
    parts = []
    if intro:
        parts.append(intro.strip())
        parts.append("")

    if has_cazare:
        parts.append("## Cazare")
        if t.get("cazare"):
            parts.append(
                f"Cheltuieli cazare (din Excel): **{fmt(t['cazare'])} MDL**."
            )
        parts.append("")
        parts.append(PLACEHOLDER)
        parts.append("")

    parts.append("## Buget")
    parts.append("")

    expense_rows = []
    labels = [
        ("cazare", "Cazare"),
        ("bilete_avion", "Bilete avion"),
        ("cheltuieli_masina", "Cheltuieli mașină"),
        ("transport_intern", "Transport intern"),
        ("bilete_locatii", "Bilete locații"),
        ("restaurante", "Restaurante"),
        ("alimente", "Alimente"),
        ("cumparaturi", "Cumpărături"),
        ("suvenire", "Suvenire"),
    ]
    for key, label in labels:
        val = t.get(key)
        if val and val > 0:
            expense_rows.append(f"- {label}: {fmt(val)} MDL")
    if expense_rows:
        parts.append("**Detalii cheltuieli:**")
        parts.extend(expense_rows)
        parts.append("")

    if has_car:
        parts.append("## Trip cu mașina")
        if t.get("cheltuieli_masina"):
            parts.append(
                f"Cheltuieli mașină (din Excel): **{fmt(t['cheltuieli_masina'])} MDL**."
            )
        parts.append("")
        parts.append(PLACEHOLDER)
        parts.append("")

    parts.append("## Jurnal de călătorie")
    parts.append("")
    parts.append(PLACEHOLDER)
    return "\n".join(parts)


TRIPS = [
    {
        "slug": "barcelona",
        "file": "2025-05-06-barcelona.md",
        "title": "Barcelona",
        "categories": ["Spania"],
        "date": "2025-05-06",
        "image": "barcelona.png",
        "excel": "barcelona.png",
        "trip": {
            "plecare": "2025-05-06",
            "intoarcere": "2025-05-11",
            "durata": "5 nopți și 6 zile",
            "persoane": 4,
            "valuta": "EUR",
            "buget_actual": 64300.65,
            "cazare": 32225.50,
            "cheltuieli_masina": 2262.00,
            "bilete_avion": 11382.01,
            "transport_intern": 1003.00,
            "restaurante": 1499.61,
            "alimente": 3244.02,
            "bilete_locatii": 4723.08,
            "cumparaturi": 7847.35,
            "masina": True,
            "avion": True,
        },
    },
    {
        "slug": "berlin",
        "file": "2024-12-19-berlin.md",
        "title": "Berlin",
        "categories": ["Germania"],
        "date": "2024-12-19",
        "image": "berlin.png",
        "excel": "berlin.png",
        "trip": {
            "plecare": "2024-12-19",
            "intoarcere": "2024-12-22",
            "durata": "3 nopți și 4 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 12704.87,
            "cazare": 3910.85,
            "transport_intern": 4987.14,
            "bilete_locatii": 2004.54,
            "suvenire": 1041.88,
            "alimente": 760.46,
            "avion": False,
        },
    },
    {
        "slug": "bucuresti",
        "file": "2023-06-28-bucuresti.md",
        "title": "București",
        "categories": ["România"],
        "date": "2023-06-28",
        "image": "bucuresti.png",
        "excel": "bucuresti.png",
        "trip": {
            "plecare": "2023-06-28",
            "intoarcere": "2023-06-29",
            "durata": "1 noapte și 2 zile",
            "persoane": 2,
            "valuta": "RON",
            "buget_actual": 7509.12,
            "cazare": 868.24,
            "transport_intern": 2398.77,
            "bilete_locatii": 2398.34,
            "restaurante": 228.96,
            "alimente": 1083.56,
            "cumparaturi": 531.25,
        },
    },
    {
        "slug": "budapesta",
        "file": "2026-06-16-budapesta.md",
        "title": "Budapesta",
        "categories": ["Ungaria"],
        "date": "2026-06-16",
        "image": "budapesta.png",
        "excel": "budapesta.png",
        "trip": {
            "plecare": "2026-06-16",
            "intoarcere": "2026-06-20",
            "durata": "4 nopți și 5 zile",
            "persoane": 4,
            "valuta": "HUF",
            "buget_actual": 37264.77,
            "cazare": 5185.38,
            "bilete_avion": 5379.81,
            "bilete_locatii": 13833.93,
            "restaurante": 5222.00,
            "transport_intern": 1579.51,
            "alimente": 1750.54,
            "cumparaturi": 4313.61,
            "avion": True,
        },
    },
    {
        "slug": "cesky-krumlov",
        "file": "2026-06-05-cesky-krumlov.md",
        "title": "Český Krumlov",
        "categories": ["Cehia"],
        "date": "2026-06-05",
        "image": "cesky.png",
        "excel": "cesky.png",
        "trip": {
            "plecare": "2026-06-05",
            "intoarcere": "2026-06-05",
            "durata": "1 zi",
            "persoane": 2,
            "valuta": "CZK",
            "buget_actual": 2715.97,
            "transport_intern": 936.14,
            "restaurante": 919.48,
            "bilete_locatii": 371.48,
            "suvenire": 168.81,
            "alimente": 320.06,
            "masina": True,
        },
    },
    {
        "slug": "delta-dunarii",
        "file": "2024-05-24-delta-dunarii.md",
        "title": "Delta Dunării",
        "categories": ["România"],
        "date": "2024-05-24",
        "image": "delta-dunarii.png",
        "excel": "delta dunarii.png",
        "trip": {
            "plecare": "2024-05-24",
            "intoarcere": "2024-05-26",
            "durata": "2 nopți și 3 zile",
            "persoane": 4,
            "valuta": "RON",
            "buget_actual": 12838.60,
            "cazare": 3600.00,
            "cheltuieli_masina": 2392.80,
            "restaurante": 1520.00,
            "cumparaturi": 3157.40,
            "alimente": 168.40,
            "masina": True,
        },
    },
    {
        "slug": "dresda",
        "file": "2026-06-03-dresda.md",
        "title": "Dresda",
        "categories": ["Germania"],
        "date": "2026-06-03",
        "image": "dresda.png",
        "excel": "dresda.png",
        "trip": {
            "plecare": "2026-06-03",
            "intoarcere": "2026-06-07",
            "durata": "4 nopți și 5 zile",
            "persoane": 2,
            "valuta": "CZK",
            "buget_actual": 4142.61,
            "transport_intern": 1813.13,
            "restaurante": 1000.00,
            "bilete_locatii": 733.73,
            "cumparaturi": 528.90,
            "alimente": 66.85,
            "masina": True,
        },
    },
    {
        "slug": "katowice",
        "file": "2025-06-07-katowice.md",
        "title": "Katowice",
        "categories": ["Polonia"],
        "date": "2025-06-07",
        "image": "katowice.png",
        "excel": "katowice.png",
        "trip": {
            "plecare": "2025-06-07",
            "intoarcere": "2025-06-10",
            "durata": "3 nopți și 4 zile",
            "persoane": 2,
            "valuta": "PLN",
            "buget_actual": 13415.67,
            "cazare": 3129.08,
            "bilete_avion": 1713.96,
            "transport_intern": 5142.23,
            "bilete_locatii": 1224.60,
            "restaurante": 1129.89,
            "alimente": 522.48,
            "cumparaturi": 553.42,
            "avion": True,
        },
    },
    {
        "slug": "napoli",
        "file": "2025-08-03-napoli.md",
        "title": "Napoli",
        "categories": ["Italia"],
        "date": "2025-08-03",
        "image": "napoli.png",
        "excel": "napoli.png",
        "trip": {
            "plecare": "2025-08-03",
            "intoarcere": "2025-08-05",
            "durata": "2 nopți și 3 zile",
            "persoane": 4,
            "valuta": "EUR",
            "buget_actual": 20406.27,
            "cazare": 3225.60,
            "bilete_avion": 8266.25,
            "transport_intern": 2280.96,
            "restaurante": 1263.24,
            "alimente": 909.20,
            "cumparaturi": 2671.02,
            "suvenire": 190.00,
            "avion": True,
        },
    },
    {
        "slug": "praga",
        "file": "2026-06-03-praga.md",
        "title": "Praga",
        "categories": ["Cehia"],
        "date": "2026-06-03",
        "image": "praga.png",
        "excel": "praga.png",
        "trip": {
            "plecare": "2026-06-03",
            "intoarcere": "2026-06-07",
            "durata": "4 nopți și 5 zile",
            "persoane": 2,
            "valuta": "CZK",
            "buget_actual": 20619.09,
            "cazare": 11939.42,
            "bilete_avion": 2634.68,
            "transport_intern": 574.61,
            "bilete_locatii": 720.00,
            "restaurante": 2593.88,
            "alimente": 390.28,
            "cumparaturi": 342.86,
            "suvenire": 165.48,
            "avion": True,
        },
    },
    {
        "slug": "procida",
        "file": "2025-07-29-procida.md",
        "title": "Procida",
        "categories": ["Italia"],
        "date": "2025-07-29",
        "image": "procida.png",
        "excel": "procida.png",
        "trip": {
            "plecare": "2025-07-29",
            "intoarcere": "2025-08-03",
            "durata": "5 nopți și 6 zile",
            "persoane": 4,
            "valuta": "EUR",
            "buget_actual": 26771.64,
            "cazare": 17352.00,
            "transport_intern": 1374.64,
            "restaurante": 5591.80,
            "alimente": 2133.20,
        },
    },
    {
        "slug": "roma",
        "file": "2025-11-04-roma.md",
        "title": "Roma",
        "categories": ["Italia"],
        "date": "2025-11-04",
        "image": "roma.png",
        "excel": "roma.png",
        "trip": {
            "plecare": "2025-11-04",
            "intoarcere": "2025-11-08",
            "durata": "4 nopți și 5 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 22549.79,
            "cazare": 7683.00,
            "bilete_avion": 1714.42,
            "transport_intern": 1598.46,
            "bilete_locatii": 2427.50,
            "restaurante": 4045.66,
            "alimente": 950.04,
            "cumparaturi": 3674.29,
            "suvenire": 456.42,
            "avion": True,
        },
    },
    {
        "slug": "transfagarsan",
        "file": "2024-07-25-transfagarsan.md",
        "title": "Transfăgărășan + Praid + Argeș",
        "categories": ["România"],
        "date": "2024-07-25",
        "image": "transfagarsan.png",
        "excel": "transfagarsan.png",
        "trip": {
            "plecare": "2024-07-25",
            "intoarcere": "2024-07-30",
            "durata": "5 nopți și 6 zile",
            "persoane": 4,
            "valuta": "RON",
            "buget_actual": 18632.40,
            "cazare": 8270.00,
            "cheltuieli_masina": 3104.00,
            "bilete_locatii": 1360.00,
            "restaurante": 1104.00,
            "alimente": 1680.20,
            "cumparaturi": 3086.20,
            "masina": True,
        },
    },
    {
        "slug": "varsovia",
        "file": "2024-12-23-varsovia.md",
        "title": "Varșovia",
        "categories": ["Polonia"],
        "date": "2024-12-23",
        "image": "varsovia.png",
        "excel": "varsovia.png",
        "trip": {
            "plecare": "2024-12-23",
            "intoarcere": "2024-12-26",
            "durata": "3 nopți și 4 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 16329.91,
            "cazare": 4875.31,
            "bilete_avion": 6104.74,
            "transport_intern": 3594.85,
            "bilete_locatii": 405.30,
            "suvenire": 711.61,
            "alimente": 638.10,
            "avion": True,
        },
    },
    {
        "slug": "venetia",
        "file": "2026-05-05-venetia.md",
        "title": "Veneția, Verona, Padova și Bassano",
        "categories": ["Italia"],
        "date": "2026-05-05",
        "image": "venetia.png",
        "excel": "venetia.png",
        "trip": {
            "plecare": "2026-05-05",
            "intoarcere": "2026-05-12",
            "durata": "7 nopți și 8 zile",
            "persoane": 2,
            "valuta": "CZK",
            "buget_actual": 15687.85,
            "transport_intern": 1311.66,
            "bilete_locatii": 870.12,
            "restaurante": 2098.57,
            "cumparaturi": 10996.27,
            "suvenire": 102.01,
            "alimente": 309.22,
        },
    },
    {
        "slug": "viena",
        "file": "2024-10-30-viena.md",
        "title": "Viena",
        "categories": ["Austria"],
        "date": "2024-10-30",
        "image": "viena.png",
        "excel": "viena.png",
        "trip": {
            "plecare": "2024-10-30",
            "intoarcere": "2024-11-04",
            "durata": "5 nopți și 6 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 27579.60,
            "cazare": 8431.00,
            "bilete_avion": 2400.00,
            "transport_intern": 1336.00,
            "bilete_locatii": 5236.00,
            "restaurante": 3050.00,
            "cumparaturi": 3341.60,
            "suvenire": 3687.00,
            "alimente": 98.00,
            "avion": True,
        },
    },
]

EXISTING_UPDATES = {
    "2022-07-20-marmaris.md": {
        "title": "Marmaris",
        "categories": ["Turcia"],
        "date": "2022-07-20",
        "image": "marmaris.png",
        "excel": "marmaris.png",
        "intro": "Mai am olecuță de lucru și termin și ghidul despre Marmaris 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2022-07-20",
            "intoarcere": "2022-07-26",
            "durata": "6 nopți și 7 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 52868.00,
            "cazare": 52868.00,
        },
    },
    "2023-11-05-istanbul.md": {
        "title": "Istanbul - palatul pescărușilor și a libertății",
        "categories": ["Turcia"],
        "date": "2023-11-05",
        "image": "istanbul.webp",
        "intro": "Mai am olecuță de lucru și termin și ghidul despre Istanbul 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2023-11-05",
            "intoarcere": "2023-11-10",
            "durata": "5 nopți și 6 zile",
            "persoane": 4,
            "valuta": "TRY",
            "buget_actual": 10667.61,
            "cazare": 4233.60,
            "bilete_avion": 1504.00,
            "transport_intern": 1374.00,
            "bilete_locatii": 1364.00,
            "restaurante": 1171.17,
            "suvenire": 427.80,
            "cumparaturi": 316.20,
            "alimente": 109.44,
            "avion": True,
        },
    },
    "2019-07-27-thassos.md": {
        "title": "Thassos",
        "categories": ["Grecia"],
        "date": "2019-07-27",
        "image": "thassos.webp",
        "intro": "Mai am olecuță de lucru și termin și ghidul despre Thassos 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2019-07-27",
            "intoarcere": "2019-08-05",
            "durata": "9 nopți și 10 zile",
            "persoane": 4,
            "valuta": "EUR",
            "buget_actual": 34995.57,
            "cazare": 21036.36,
            "cheltuieli_masina": 4822.34,
            "restaurante": 1516.00,
            "alimente": 5156.03,
            "cumparaturi": 2282.84,
            "masina": True,
        },
    },
    "2023-06-29-skiathos.md": {
        "title": "Skiathos",
        "categories": ["Grecia"],
        "date": "2023-06-29",
        "image": "skiathos.webp",
        "intro": "Mai am olecuță de lucru și termin ghidul despre Skiathos 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2023-06-29",
            "intoarcere": "2023-07-06",
            "durata": "2 nopți și 3 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 11689.00,
            "cazare": 2610.00,
            "bilete_avion": 5499.00,
            "transport_intern": 1275.75,
            "restaurante": 1154.25,
            "suvenire": 222.75,
            "cumparaturi": 587.25,
            "alimente": 340.00,
            "avion": True,
        },
    },
    "2023-06-30-skopelos.md": {
        "title": "Skopelos - insula unde îngerii fac amiaza",
        "categories": ["Grecia"],
        "date": "2023-06-30",
        "image": "skopelos.webp",
        "intro": "Mai am olecuță de lucru și termin și ghidul despre Skopelos 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2023-06-30",
            "intoarcere": "2023-07-05",
            "durata": "5 nopți și 6 zile",
            "persoane": 2,
            "valuta": "EUR",
            "buget_actual": 11185.75,
            "cazare": 5100.00,
            "transport_intern": 635.24,
            "restaurante": 3358.25,
            "bilete_locatii": 202.50,
            "suvenire": 50.63,
            "alimente": 1839.13,
        },
    },
    "2017-07-28-olimp.md": {
        "title": "Riviera Olimpului",
        "categories": ["Grecia"],
        "date": "2017-07-28",
        "image": "olimp.webp",
        "intro": "Mai am olecuță de lucru și termin și ghidul despre Riviera Olimpului 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙",
        "trip": {
            "plecare": "2017-07-28",
            "intoarcere": "2017-08-07",
            "durata": "9 nopți și 10 zile",
            "persoane": 4,
            "valuta": "EUR",
            "buget_actual": 29940.40,
            "cazare": 29400.00,
            "cheltuieli_masina": 540.40,
            "masina": True,
        },
    },
}


def write_post(path, meta, body):
    cats = ", ".join(meta["categories"])
    trip_block = ""
    if meta.get("trip"):
        trip_block = yaml_trip(meta["trip"]) + "\n"
    content = f"""---
layout: post
title: "{meta['title']}"
categories: [ {cats} ]
date: {meta['date']}
image: assets/images/{meta['image']}
toc: true
beforetoc: "Cuprins"
{trip_block}---

{body}
"""
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.name}")


def main():
    IMAGES.mkdir(parents=True, exist_ok=True)

    for trip in TRIPS:
        src = EXCEL / trip["excel"]
        dst = IMAGES / trip["image"]
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"  image {dst.name}")

    for trip in TRIPS:
        t = trip["trip"]
        has_car = bool(t.get("masina") or (t.get("cheltuieli_masina") or 0) > 0)
        has_cazare = bool((t.get("cazare") or 0) > 0)
        body = body_sections(t, has_car, has_cazare)
        write_post(POSTS / trip["file"], trip, body)

    for filename, meta in EXISTING_UPDATES.items():
        src = EXCEL / meta.get("excel", meta["image"])
        dst = IMAGES / meta["image"]
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

        t = meta["trip"]
        has_car = bool(t.get("masina") or (t.get("cheltuieli_masina") or 0) > 0)
        has_cazare = bool((t.get("cazare") or 0) > 0)
        body = body_sections(t, has_car, has_cazare, intro=meta.get("intro"))
        write_post(POSTS / filename, meta, body)

    # Istanbul: copy png if only webp exists - skip
    # Sitonia: special handling - preserve long content
    sitonia_path = POSTS / "2023-07-22-sitonia.md"
    if sitonia_path.exists():
        original = sitonia_path.read_text(encoding="utf-8")
        # keep content after front matter
        if original.startswith("---"):
            parts = original.split("---", 2)
            old_body = parts[2].strip() if len(parts) > 2 else ""
        else:
            old_body = original

        meta = {
        "title": "Halikidiki - trei perle într-o scoică",
            "categories": ["Grecia"],
            "date": "2023-07-23",
            "image": "sithonia.webp",
            "trip": {
                "plecare": "2023-07-23",
                "intoarcere": "2023-08-04",
                "durata": "12 nopți și 13 zile",
                "persoane": 4,
                "valuta": "EUR",
                "buget_actual": 58813.64,
                "cazare": 36000.00,
                "cheltuieli_masina": 4714.52,
                "bilete_locatii": 2800.00,
                "restaurante": 3970.00,
                "alimente": 7845.56,
                "cumparaturi": 1589.56,
                "suvenire": 884.00,
                "masina": True,
            },
        }

        # Prepend buget/trip sections if missing, enable toc in front matter
        budget_block = """## Buget

**Detalii cheltuieli:** cazare 36 000 · cheltuieli mașină 4 715 · restaurante 3 970 · alimente 7 846 · bilete locații 2 800 · suvenire 884 · cumpărături 1 590 MDL

## Trip cu mașina

*Completează aici detaliile drumului spre Halkidiki.*

"""
        if "## Buget" not in old_body:
            # insert after first paragraph block / before ## Jurnal
            if "## Jurnal de călătorie" in old_body:
                old_body = old_body.replace(
                    "## Jurnal de călătorie", budget_block + "## Jurnal de călătorie", 1
                )
            else:
                old_body = budget_block + old_body

        cats = ", ".join(meta["categories"])
        new_content = f"""---
layout: post
title: "{meta['title']}"
categories: [ {cats} ]
date: {meta['date']}
image: assets/images/{meta['image']}
toc: true
beforetoc: "Cuprins"
{yaml_trip(meta['trip'])}
---

{old_body}
"""
        sitonia_path.write_text(new_content, encoding="utf-8")
        print("  updated sitonia (preserved content)")

    # Muntenegru & Creta - structure only, no excel
    for filename, title, cat, date, img in [
        ("2018-07-09-muntenegru.md", "Muntenegru", "Muntenegru", "2018-07-09", "muntenegru.webp"),
        ("2021-08-14-creta.md", "Creta", "Grecia", "2021-08-14", "creta.webp"),
    ]:
        intro = (
            "Mai am olecuță de lucru și termin și ghidul despre "
            + title
            + " 😉\n\nÎți mulțumesc pentru răbdare și că vei mai reveni aici când e gata totul 💙"
        )
        body = f"""{intro}

## Cazare

{PLACEHOLDER}

## Buget

{PLACEHOLDER}

## Jurnal de călătorie

{PLACEHOLDER}
"""
        write_post(
            POSTS / filename,
            {
                "title": title,
                "categories": [cat],
                "date": date,
                "image": img,
            },
            body,
        )

    old_istanbul = POSTS / "2023-01-02-istanbul.md"
    if old_istanbul.exists():
        old_istanbul.unlink()

    # Copy remaining excel images as placeholders
    for trip in TRIPS + list(EXISTING_UPDATES.values()):
        excel_name = trip.get("excel") or trip.get("image")
        if excel_name and (EXCEL / excel_name).exists():
            target = IMAGES / trip["image"]
            if not target.exists():
                shutil.copy2(EXCEL / excel_name, target)


if __name__ == "__main__":
    main()
