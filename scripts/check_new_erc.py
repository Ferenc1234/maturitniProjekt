import json

with open("maturita-erc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== NEW ERC VIOLATION DESCRIPTIONS ===")
counts = {}
for sheet in data.get("sheets", []):
    for v in sheet.get("violations", []):
        desc = v.get("description", "")
        counts[desc] = counts.get(desc, 0) + 1

for desc, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{count}: {desc}")
