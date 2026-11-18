import re

sch_path = r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

for ref in ['K2', 'K_ISO', 'K_BAT']:
    # Find the block for this reference
    pattern = rf'\(symbol[\s\S]*?\(property\s+"Reference"\s+"{ref}"[\s\S]*?\(at\s+([\d\.-]+)\s+([\d\.-]+)'
    match = re.search(pattern, content)
    if match:
        print(f"{ref} found at ({match.group(1)}, {match.group(2)})")
    else:
        print(f"{ref} NOT found")
