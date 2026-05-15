from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter


COMMONS_API_URL = "https://commons.wikimedia.org/w/api.php"
OUTPUT_DIR = Path("sample_data/images/tomato_web")
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"
ATTRIBUTION_PATH = OUTPUT_DIR / "ATTRIBUTION.md"
USER_AGENT = "GemmaGardenGuardian/0.1 (sample image collection for Kaggle demo)"


@dataclass(frozen=True)
class SampleSpec:
    key: str
    condition: str
    output_name: str
    commons_title: str | None = None
    derive_from: str | None = None
    transform: str | None = None
    note: str = ""


SAMPLES = [
    SampleSpec(
        key="whole_plant",
        condition="1. トマト全体",
        output_name="01_tomato_whole_plant.jpg",
        commons_title="File:Tomato plants in home garden.jpg",
        note="Whole tomato plants in a home garden.",
    ),
    SampleSpec(
        key="leaf_closeup",
        condition="2. 葉のアップ",
        output_name="02_tomato_leaf_closeup.jpg",
        commons_title="File:Healthy tomato leaves (7871755330).jpg",
        note="Close-up healthy tomato leaves.",
    ),
    SampleSpec(
        key="soil_condition",
        condition="3. 土の状態",
        output_name="03_tomato_soil_condition.jpg",
        commons_title="File:Tomatoseedlings.jpg",
        note="Tomato seedlings in soil/peat pots.",
    ),
    SampleSpec(
        key="weeds_context",
        condition="4. 雑草がある状態",
        output_name="04_tomato_weeds_context.jpg",
        commons_title="File:20240906Solanum lycopersicum.jpg",
        note="Wild tomato plant with surrounding vegetation; useful as weed/context sample.",
    ),
    SampleSpec(
        key="fruiting",
        condition="5. 実がなっている状態",
        output_name="05_tomato_fruiting.jpg",
        commons_title="File:Tomato plant 01.JPG",
        note="Tomato plant with fruit.",
    ),
    SampleSpec(
        key="healthy",
        condition="7. 問題なさそうな状態",
        output_name="07_tomato_healthy.jpg",
        commons_title="File:Tomato plant garden.jpg",
        note="General tomato plant garden image for healthy/normal-looking sample.",
    ),
    SampleSpec(
        key="water_stress_like",
        condition="6. 水不足っぽい状態",
        output_name="06_tomato_water_stress_like_derived.jpg",
        derive_from="whole_plant",
        transform="dry_look",
        note="Derived from the whole-plant sample to simulate a dry-looking demo case. Not a real diagnosis label.",
    ),
    SampleSpec(
        key="blurry",
        condition="8. ぼやけた写真",
        output_name="08_tomato_blurry_derived.jpg",
        derive_from="fruiting",
        transform="blur",
        note="Derived from a licensed tomato plant photo to test blurry-image handling.",
    ),
    SampleSpec(
        key="dark",
        condition="9. 夜・暗い写真",
        output_name="09_tomato_dark_derived.jpg",
        derive_from="healthy",
        transform="dark",
        note="Derived from a licensed tomato plant photo to test low-light handling.",
    ),
    SampleSpec(
        key="bad_angle",
        condition="10. 角度が悪い写真",
        output_name="10_tomato_bad_angle_derived.jpg",
        derive_from="whole_plant",
        transform="bad_angle",
        note="Derived from a licensed tomato plant photo to test poor-angle handling.",
    ),
]


def request_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{url}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_commons_info(title: str) -> dict[str, Any]:
    data = request_json(
        COMMONS_API_URL,
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "imageinfo",
            "titles": title,
            "iiprop": "url|extmetadata",
            "iiurlwidth": "1280",
        },
    )
    pages = data["query"]["pages"]
    if not pages or "missing" in pages[0]:
        raise RuntimeError(f"Commons file not found: {title}")
    imageinfo = pages[0]["imageinfo"][0]
    metadata = imageinfo.get("extmetadata", {})
    return {
        "title": title,
        "description_url": imageinfo["descriptionurl"],
        "download_url": imageinfo.get("thumburl") or imageinfo["url"],
        "source_url": imageinfo["url"],
        "artist": clean_metadata(metadata.get("Artist", {}).get("value", "")),
        "license_short_name": metadata.get("LicenseShortName", {}).get("value", ""),
        "license_url": metadata.get("LicenseUrl", {}).get("value", ""),
        "credit": clean_metadata(metadata.get("Credit", {}).get("value", "")),
    }


def clean_metadata(value: str) -> str:
    value = value.replace("<span class=\"int-own-work\" lang=\"en\">Own work</span>", "Own work")
    value = value.replace("<span class=\"int-own-work\">Own work</span>", "Own work")
    value = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("&amp;", "&").replace("&quot;", '"').replace("&#039;", "'")
    return " ".join(value.split())


def download_file(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                path.write_bytes(response.read())
            return
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code != 429:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"Could not download after retries: {url}") from last_error


def normalize_image(path: Path) -> None:
    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail((1280, 1280))
        image.save(path, quality=88, optimize=True)


def transform_image(source: Path, destination: Path, transform: str) -> None:
    with Image.open(source) as image:
        image = image.convert("RGB")
        if transform == "blur":
            image = image.filter(ImageFilter.GaussianBlur(radius=7))
        elif transform == "dark":
            image = ImageEnhance.Brightness(image).enhance(0.28)
            image = ImageEnhance.Contrast(image).enhance(0.85)
        elif transform == "bad_angle":
            image = image.rotate(-24, expand=True, fillcolor=(28, 34, 28))
            width, height = image.size
            image = image.crop((width * 0.12, height * 0.10, width * 0.88, height * 0.90))
        elif transform == "dry_look":
            image = ImageEnhance.Color(image).enhance(0.55)
            image = ImageEnhance.Contrast(image).enhance(1.25)
            image = ImageEnhance.Brightness(image).enhance(1.08)
        else:
            raise RuntimeError(f"Unknown transform: {transform}")
        image.thumbnail((1280, 1280))
        image.save(destination, quality=88, optimize=True)


def write_attribution(manifest: list[dict[str, Any]]) -> None:
    lines = [
        "# Tomato Sample Image Attribution",
        "",
        "These images are for demo/evaluation use in Gemma Garden Guardian.",
        "Files marked as derived were transformed locally from the listed Wikimedia Commons source.",
        "",
        "| Condition | Local file | Source | Author | License | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for item in manifest:
        source = item.get("source_title", item.get("derived_from", ""))
        source_url = item.get("description_url", "")
        source_link = f"[{source}]({source_url})" if source_url else source
        license_name = item.get("license_short_name", "")
        license_url = item.get("license_url", "")
        license_link = f"[{license_name}]({license_url})" if license_url else license_name
        lines.append(
            f"| {item['condition']} | `{item['file']}` | {source_link} | "
            f"{item.get('artist', '')} | {license_link} | {item.get('note', '')} |"
        )
    ATTRIBUTION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_by_key: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []

    for spec in SAMPLES:
        output_path = OUTPUT_DIR / spec.output_name
        if spec.commons_title:
            info = fetch_commons_info(spec.commons_title)
            download_file(info["download_url"], output_path)
            normalize_image(output_path)
            entry = {
                "key": spec.key,
                "condition": spec.condition,
                "file": str(output_path),
                "source_title": info["title"],
                "description_url": info["description_url"],
                "source_url": info["source_url"],
                "artist": info["artist"],
                "license_short_name": info["license_short_name"],
                "license_url": info["license_url"],
                "note": spec.note,
                "derived": False,
            }
        else:
            if not spec.derive_from or not spec.transform:
                raise RuntimeError(f"Derived sample is missing derive_from/transform: {spec.key}")
            source_entry = manifest_by_key[spec.derive_from]
            transform_image(Path(source_entry["file"]), output_path, spec.transform)
            entry = {
                "key": spec.key,
                "condition": spec.condition,
                "file": str(output_path),
                "derived_from": source_entry["source_title"],
                "description_url": source_entry["description_url"],
                "source_url": source_entry["source_url"],
                "artist": source_entry["artist"],
                "license_short_name": source_entry["license_short_name"],
                "license_url": source_entry["license_url"],
                "transform": spec.transform,
                "note": spec.note,
                "derived": True,
            }

        manifest_by_key[spec.key] = entry
        manifest.append(entry)
        print(f"saved {output_path}")
        time.sleep(1.5)

    manifest.sort(key=lambda item: int(item["condition"].split(".")[0]))
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_attribution(manifest)
    print(f"wrote {MANIFEST_PATH}")
    print(f"wrote {ATTRIBUTION_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
