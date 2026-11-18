import re

sch_path = r"kicad\maturita.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Only examine lib_symbols section
lib_sym_start = content.find("(lib_symbols")
lib_sym_end = content.find("\n\t(symbol\n\t\t(lib_id") # start of placed symbols
if lib_sym_end == -1:
    lib_sym_end = content.find("\n\t(wire")

lib_sym_text = content[lib_sym_start:lib_sym_end]

symbols = re.findall(r'\(symbol\s+"([^"]+)"([\s\S]*?embedded_fonts\s+no\s*\)\s*\))', lib_sym_text)
print(f"Total library symbols: {len(symbols)}")

for name, sym_body in symbols:
    if "(pin input line" in sym_body:
        # Check value or reference or keywords
        ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', sym_body)
        ref = ref_match.group(1) if ref_match else ""
        print(f"Symbol '{name}': Ref={ref}, has pin input line")
