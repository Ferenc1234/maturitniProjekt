import re

sch_path = r"kicad\maturita.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find U8 block
# It's an instance, so look for (symbol (lib_id "ESP32-S3-WROOM-1-N8") ...)
u8_pattern = r'\(symbol\s+\(lib_id\s+"ESP32-S3-WROOM-1-N8"\)[\s\S]*?\(uuid\s+"([^"]+)"\)'
match = re.search(u8_pattern, content)
if match:
    u8_uuid = match.group(1)
    start = match.start()
    # Find the end of this symbol block
    depth = 0
    end = start
    for i, c in enumerate(content[start:]):
        if c == '(': depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                end = start + i + 1
                break
    u8_block = content[start:end]
    
    # Now find all pins and their uuids
    pins = re.findall(r'\(pin\s+"([^"]+)"\s+\(uuid\s+"([^"]+)"\)\)', u8_block)
    
    print(f"U8 (ESP32-S3) Pins and Connections:")
    for pin_num, pin_uuid in pins:
        # Find wires or labels connected to this pin_uuid
        # Pins in the schematic instance are just stubs. The connection is via wires that start/end at the pin's absolute coordinates.
        # However, KiCad 6+ uses the pin uuid in the (symbol ...) block to link to (pin ...) in lib_symbols? No.
        # Actually, let's find the 'at' coordinate of the pin in the block.
        pass

# A better way is to find the absolute position of U8 and then find pins' relative positions in lib_symbols.
# But even easier: Search for labels near U8's pins.

# Let's just list all labels in the schematic and see which ones look like ESP32 pins.
labels = re.findall(r'\(label\s+"([^"]+)"\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)', content)
global_labels = re.findall(r'\(global_label\s+"([^"]+)"\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)', content)
hierarchical_labels = re.findall(r'\(hierarchical_label\s+"([^"]+)"\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)', content)

print("\n--- Labels in Schematic ---")
for l, x, y in sorted(labels + global_labels + hierarchical_labels):
    print(f"Label: {l} at ({x}, {y})")
