# -*- coding: utf-8 -*-
"""Regenerate the public directory without embedding any raw contact list."""

import json
from public_data import DATA_FILE, write_public_database


def main():
    with DATA_FILE.open(encoding="utf-8") as handle:
        source = json.load(handle)
    bundle = write_public_database(source)
    print(f"[OK] Public directory: {bundle['total_units']} units; township-level locations only")


if __name__ == "__main__":
    main()
