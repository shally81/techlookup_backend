import json, re, pathlib, dns.resolver
from typing import Dict, Any

SIG_PATH = pathlib.Path(__file__).parent.parent / "detector" / "sigs" / "apps.json"

with SIG_PATH.open("r", encoding="utf-8") as f:
    SIGNATURES = json.load(f)

for app_data in SIGNATURES.values():
    for method in ("html", "js", "script"):
        if method in app_data:
            app_data[method] = [re.compile(pat, re.I) for pat in app_data[method]]

def detect(html: str, headers: Dict[str, str]) -> Dict[str, Any]:
    detected: Dict[str, Any] = {}
    for app, data in SIGNATURES.items():
        if "html" in data and any(r.search(html) for r in data["html"]):
            detected[app] = data.get("categories", [])
        elif "script" in data and any(r.search(html) for r in data["script"]):
            detected[app] = data.get("categories", [])
    server = headers.get("server", "").lower()
    if server:
        detected["server"] = server
    return detected