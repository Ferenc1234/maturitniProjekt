import re
import uuid
import subprocess
import json

sch_path = r"kicad\maturita.kicad_sch"
erc_json_path = r"kicad\maturita-erc.json"

with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

print("Original schematic length:", len(content))

# 1. Remove the 3 dangling vertical wire stubs
# UUIDs: 2459597f-1c79-48bc-8ff5-08b7ef0b0db0, 07583c95-0330-4164-9a15-820812fc643d, 1d454bc7-0578-441c-9ee4-36e3423c5bfb
stubs_uuids = [
    "2459597f-1c79-48bc-8ff5-08b7ef0b0db0",
    "07583c95-0330-4164-9a15-820812fc643d",
    "1d454bc7-0578-441c-9ee4-36e3423c5bfb"
]

for uuid_str in stubs_uuids:
    # Find wire block containing this uuid
    # Wires look like: (wire (pts ...) (stroke ...) (uuid "..."))
    pattern = rf'\t\(wire\s+\(pts\s+\(xy\s+[\d\.-]+\s+[\d\.-]+\)\s+\(xy\s+[\d\.-]+\s+[\d\.-]+\)\)\s+\(stroke\s+\(width\s+[\d\.-]+\)\s+\(type\s+\w+\)\)\s+\(uuid\s+"{uuid_str}"\)\s*\)'
    new_content = re.sub(pattern, '', content)
    if new_content != content:
        print(f"Removed wire stub with UUID {uuid_str}")
        content = new_content
    else:
        # Try a more general regex for wire matching uuid
        pattern_gen = rf'\t\(wire\s+[\s\S]*?\(uuid\s+"{uuid_str}"\)\s*\)'
        new_content = re.sub(pattern_gen, '', content)
        if new_content != content:
            print(f"Removed wire stub (general) with UUID {uuid_str}")
            content = new_content
        else:
            print(f"Warning: Wire stub with UUID {uuid_str} not found via regex.")

# 2. Add no_connect flags for unused/unconnected pins or resolve them.
# Let's add no_connect items for pins that report "Pin not connected" errors where appropriate,
# or add no_connect entries in the schematic.
# A no_connect entry looks like: (no_connect (at x y) (uuid "..."))

# Let's inspect ERC errors to add no_connect for specific unconnected pins if desired,
# or let's write out the modified schematic and run ERC.

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved cleaned schematic.")

# Run ERC
cmd = [r"F:\kicad\bin\kicad-cli.exe", "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json_path, sch_path]
subprocess.run(cmd, check=True)

with open(erc_json_path, "r", encoding="utf-8") as ef:
    erc_res = json.load(ef)

errs = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "error")
warns = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "warning")
print(f"ERC after stub removal -> Errors: {errs}, Warnings: {warns}")
