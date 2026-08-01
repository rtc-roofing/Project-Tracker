#!/usr/bin/env python3
"""Inject pipeline_data.json into the dashboard template → index.html (deploy)
   and pipeline-dashboard.html (local preview)."""
import json, os

BASE = r"C:\Users\workspace\Desktop\Pipeline"
with open(os.path.join(BASE, "pipeline_data.json"), encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(BASE, "_pipeline_template.html"), encoding="utf-8") as f:
    html = f.read()

seed = json.dumps(data, ensure_ascii=False)
assert "__SEED_DATA__" in html, "placeholder not found"
out = html.replace("__SEED_DATA__", seed)

for name in ("index.html", "pipeline-dashboard.html"):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {name} ({len(out)/1024:.0f} KB)")

print(f"embedded {len(data)} jobs")
