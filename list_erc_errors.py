import json

with open(r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117-erc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== CURRENT ERC ERRORS ===")
for sheet in data.get("sheets", []):
    for v in sheet.get("violations", []):
        if v.get("severity") == "error":
            print(f"Desc: {v.get('description')}")
            for item in v.get("items", []):
                print(f"  Item: {item.get('description')} at {item.get('pos')}")
