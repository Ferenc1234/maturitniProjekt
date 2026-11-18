import re

sch_path = r"kicad\maturita.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find symbols in the instance section
# They look like: (symbol (lib_id "...") (at x y rotation) ... (property "Reference" "REF") ...)
matches = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+[\d\.-]+\)[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"', content)

print("Symbols in region (90-120, 40-70):")
for lib_id, x, y, ref in matches:
    if 90 < float(x) < 120 and 40 < float(y) < 70:
        print(f"  {ref} ({lib_id}) at ({x}, {y})")
