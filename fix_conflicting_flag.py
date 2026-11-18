import json
import re

sch_path = r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove PWR_FLAG at (64.77, 95.25)
# Find symbol block for PWR_FLAG at 64.77 95.25
pattern = r'\t\(symbol\s+\(lib_id\s+"PWR_FLAG"\)\s+\(at\s+64\.77\s+95\.25\s+0\).*?\n\t\)'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)
if new_content != content:
    print("Removed conflicting PWR_FLAG at (64.77, 95.25)")
    content = new_content
else:
    print("Could not find exact conflicting PWR_FLAG via regex, searching broadly...")
    # Search for PWR_FLAG near 64.77 95.25
    # Let's find all symbol blocks with lib_id "PWR_FLAG"
    blocks = re.split(r'\n\s*\(symbol\s*\n', content)
    for b in blocks:
        if '"PWR_FLAG"' in b and '64.77' in b and '95.25' in b:
            content = content.replace(b, '')
            print("Removed PWR_FLAG block containing 64.77 95.25")

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated schematic saved.")
