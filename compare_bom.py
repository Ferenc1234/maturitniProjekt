import re
import os

sch_path = r"kicad\maturita.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all symbol references and values from schematic
# Symbols in sch are structured with (symbol ... (property "Reference" "...") (property "Value" "...") ...)
symbols = []
# Find blocks or symbols
# Let's use regex to find symbols and their properties
symbol_blocks = re.split(r'\n\s*\(symbol\s*\n', content)

components = {}
for block in symbol_blocks:
    ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    val_match = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
    foot_match = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', block)
    if ref_match and val_match:
        ref = ref_match.group(1)
        val = val_match.group(1)
        foot = foot_match.group(1) if foot_match else ""
        if not ref.startswith("#"): # ignore power/flags
            components[ref] = {"value": val, "footprint": foot}

print(f"Total schematic components found (excluding power symbols): {len(components)}")
for ref in sorted(components.keys(), key=lambda x: (re.sub(r'\d+', '', x), int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)):
    print(f"  {ref}: Value={components[ref]['value']}, Footprint={components[ref]['footprint']}")
