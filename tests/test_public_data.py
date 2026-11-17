import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from public_data import PUBLIC_UNIT_FIELDS, TOWNSHIP_CENTERS, to_public_bundle


ROOT = Path(__file__).resolve().parents[1]


def private_fixture():
    return {
        "version": "test",
        "updated_at": "2026-11-17",
        "total_units": 1,
        "wjs_units": 0,
        "ass_units": 1,
        "private_metadata": "PRIVATE_CANARY",
        "units": [{
            "id": "TEST-001", "name": "測試團體", "category": "社會團體與人民團體",
            "sub_category": "測試分類", "township": "臺東市",
            "leader": "PRIVATE_CANARY", "phone": "PRIVATE_CANARY",
            "address": "PRIVATE_CANARY", "street": "PRIVATE_CANARY",
            "lat": 22.123456, "lng": 121.654321,
            "future_private_field": {"notes": "PRIVATE_CANARY"},
        }],
    }


def embedded_bundle(html):
    match = re.search(r"const TAITUNG_DB = (.*?);\s*\n", html)
    if not match:
        raise AssertionError("Public database missing from HTML")
    return json.loads(match[1])


class PublicDataTests(unittest.TestCase):
    def test_whitelist_discards_contacts_coordinates_and_unknown_fields(self):
        public = to_public_bundle(private_fixture())
        self.assertEqual(set(public["units"][0]), set(PUBLIC_UNIT_FIELDS))
        self.assertNotIn("PRIVATE_CANARY", json.dumps(public))
        self.assertEqual(public["total_units"], 1)
        self.assertEqual(public["township_stats"]["臺東市"], 1)

    def test_snapshot_and_embedded_data_share_the_public_schema(self):
        data = json.loads((ROOT / "data/taitung_database.json").read_text(encoding="utf-8"))
        self.assertEqual(data, to_public_bundle(data))
        self.assertEqual(embedded_bundle((ROOT / "index.html").read_text(encoding="utf-8")), data)
        self.assertEqual(data["total_units"], 701)
        self.assertEqual((data["wjs_units"], data["ass_units"]), (114, 587))
        self.assertEqual(len({unit["id"] for unit in data["units"]}), 701)

    def test_map_contains_only_shared_township_centers(self):
        data = to_public_bundle(private_fixture())
        self.assertEqual(data["township_coords"], TOWNSHIP_CENTERS)
        self.assertEqual(len(TOWNSHIP_CENTERS), 16)
        for center in data["township_coords"].values():
            self.assertEqual(center["lat"], round(center["lat"], 2))
            self.assertEqual(center["lng"], round(center["lng"], 2))

    def test_generator_sanitizes_input_before_saving(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            for filename in ("public_data.py", "generate_taitung_database.py"):
                shutil.copyfile(ROOT / filename, root / filename)
            output = root / "data/taitung_database.json"
            output.write_text(json.dumps(private_fixture()), encoding="utf-8")
            subprocess.run([sys.executable, str(root / "generate_taitung_database.py")], check=True, capture_output=True)
            self.assertNotIn("PRIVATE_CANARY", output.read_text(encoding="utf-8"))

    def test_builder_sanitizes_even_if_input_contains_private_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            for filename in ("public_data.py", "build_taitung_html.py"):
                shutil.copyfile(ROOT / filename, root / filename)
            fixture = private_fixture()
            fixture["units"][0]["name"] = "</script><script>UNTRUSTED_MARKUP</script>"
            (root / "data/taitung_database.json").write_text(json.dumps(fixture), encoding="utf-8")
            subprocess.run([sys.executable, str(root / "build_taitung_html.py")], check=True, capture_output=True)
            html = (root / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("PRIVATE_CANARY", html)
            self.assertNotIn(fixture["units"][0]["name"], html)
            self.assertEqual(embedded_bundle(html)["units"][0]["name"], fixture["units"][0]["name"])
            self.assertEqual(set(embedded_bundle(html)["units"][0]), set(PUBLIC_UNIT_FIELDS))

    def test_scheduled_sync_drops_private_fields(self):
        spec = importlib.util.spec_from_file_location("taitung_sync", ROOT / "scripts/update_taitung_data.py")
        sync = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sync)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "database.json"
            output.write_text(json.dumps(private_fixture()), encoding="utf-8")
            with patch.object(sync, "DATA_FILE", str(output)), patch.object(sync, "OPEN_DATA_ENDPOINTS", []):
                self.assertTrue(sync.check_government_updates())
            self.assertNotIn("PRIVATE_CANARY", output.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
