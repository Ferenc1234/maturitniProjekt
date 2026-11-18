import re

sch_path = r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split into symbol blocks
symbol_blocks = re.split(r'\n\s*\(symbol\s*\n', content)

print("=== COMPONENTS PLACED AT THE BOTTOM OF SCHEMATIC (y > 200 mm) ===")
for block in symbol_blocks:
    at_match = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)', block)
    ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    val_match = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
    if at_match and ref_match and val_match:
        x = float(at_match.group(1))
        y = float(at_match.group(2))
        ref = ref_match.group(1)
        val = val_match.group(1)
        if y > 200.0 and not ref.startswith("#"):
            print(f"\nDesignator: {ref}, Value: {val}, Position: (x={x}, y={y})")
            # Find pins in this symbol block
            pins = re.findall(r'\(pin\s+"([^"]+)"\s+\(uuid\s+"[^"]+"\)\s*\)', block)
            pin_ats = re.findall(r'\(pin\s+(?:unspecified|input|output|power_in|power_out)\s+line\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)', block)
            # Or search pin coordinates
            for m in re.finditer(r'\(pin\s+([^\)]+)\)', block):
                pin_text = m.group(1)
                at_pin = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)', pin_text)
                num_pin = re.search(r'\(number\s+"([^"]+)"', pin_text)
                if at_pin and num_pin:
                    px = float(at_pin.group(1)) + x
                    py = float(at_pin.group(2)) + y
                    print(f"    Pin {num_pin.group(1)}: relative ({at_pin.group(1)}, {at_pin.group(2)}), absolute ({px:.2f}, {py:.2f})")
