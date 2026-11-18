import json

with open("maturita-erc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== DETAILED TARGET ERC VIOLATIONS ===")
for sheet in data.get("sheets", []):
    for v in sheet.get("violations", []):
        desc = v.get("description", "")
        targets = [
            "Unconnected wire endpoint",
            "Label connected to only one pin",
            "Both GND and MSR_LO_2 are attached",
            "Both LC_NODE and MEASURE_HIGH are attached"
        ]
        if any(t in desc for t in targets):
            print(f"\nDescription: {desc}")
            print(f"Severity: {v.get('severity')}")
            for item in v.get("items", []):
                print(f"  Item: {item}")
