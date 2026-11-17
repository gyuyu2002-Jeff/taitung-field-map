"""Whitelist the fields allowed in the public township-level directory."""

import json
from collections import Counter
from pathlib import Path


PUBLIC_UNIT_FIELDS = ("id", "name", "category", "sub_category", "township")
TOWNSHIP_CENTERS = {
    "臺東市": {"lat": 22.76, "lng": 121.14, "zone": "市區生活圈"},
    "卑南鄉": {"lat": 22.81, "lng": 121.08, "zone": "縱谷南端與近郊"},
    "延平鄉": {"lat": 22.91, "lng": 121.08, "zone": "花東縱谷線"},
    "鹿野鄉": {"lat": 22.91, "lng": 121.14, "zone": "花東縱谷線"},
    "關山鎮": {"lat": 23.05, "lng": 121.16, "zone": "花東縱谷線"},
    "海端鄉": {"lat": 23.10, "lng": 121.14, "zone": "花東縱谷線"},
    "池上鄉": {"lat": 23.12, "lng": 121.22, "zone": "花東縱谷線"},
    "東河鄉": {"lat": 22.97, "lng": 121.30, "zone": "東部海岸線"},
    "成功鎮": {"lat": 23.10, "lng": 121.38, "zone": "東部海岸線"},
    "長濱鄉": {"lat": 23.32, "lng": 121.45, "zone": "東部海岸線"},
    "太麻里鄉": {"lat": 22.62, "lng": 121.01, "zone": "南迴山海線"},
    "金峰鄉": {"lat": 22.60, "lng": 120.97, "zone": "南迴山海線"},
    "大武鄉": {"lat": 22.34, "lng": 120.89, "zone": "南迴山海線"},
    "達仁鄉": {"lat": 22.30, "lng": 120.88, "zone": "南迴山海線"},
    "綠島鄉": {"lat": 22.66, "lng": 121.49, "zone": "離島專區"},
    "蘭嶼鄉": {"lat": 22.06, "lng": 121.55, "zone": "離島專區"},
}
DATA_FILE = Path(__file__).resolve().parent / "data" / "taitung_database.json"


def to_public_bundle(source):
    """Drop all non-public fields, including newly introduced nested metadata."""
    units = []
    seen = set()
    for raw in source["units"]:
        unit = {field: raw[field] for field in PUBLIC_UNIT_FIELDS}
        if not all(isinstance(value, str) for value in unit.values()):
            raise ValueError("Public unit fields must contain text only")
        if unit["id"] in seen:
            raise ValueError("Duplicate public unit ID")
        if unit["township"] not in TOWNSHIP_CENTERS:
            raise ValueError("Unknown township in public directory")
        seen.add(unit["id"])
        units.append(unit)

    counts = Counter(unit["township"] for unit in units)
    wjs_count = sum(unit["category"] == "原住民文化健康站" for unit in units)
    result = {
        "version": str(source.get("version", "")),
        "updated_at": str(source.get("updated_at", "")),
        "public_data_policy": "township-only-v1",
        "data_sources": [
            "臺東縣政府民政處人民團體名冊",
            "臺東縣政府社會處社區發展協會查詢名單",
            "臺東縣政府原住民族行政處文健站核定清冊",
            "原住民族委員會(CIP)文化健康站最新清冊",
        ],
        "township_coords": TOWNSHIP_CENTERS,
        "township_stats": {township: counts[township] for township in TOWNSHIP_CENTERS},
        "total_units": len(units),
        "wjs_units": wjs_count,
        "ass_units": len(units) - wjs_count,
        "units": units,
    }
    if "latest_check_time" in source:
        result["latest_check_time"] = str(source["latest_check_time"])
    return result


def write_public_database(source, path=DATA_FILE):
    bundle = to_public_bundle(source)
    Path(path).write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return bundle
