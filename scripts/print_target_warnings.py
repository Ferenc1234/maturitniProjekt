import json

with open("BackupProjects_iq.masters.yt_personal_1_20261117-erc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== 6 TARGET WARNINGS DETAILED ===")
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
            print(f"\n--- Violation: {desc} ---")
            print(f"Severity: {v.get('severity')}")
            for item in v.get("items", []):
                print(f"  Item description: {item.get('description')}")
                print(f"  Position: {item.get('pos')}")
                print(f"  UUID: {item.get('uuid')}")
