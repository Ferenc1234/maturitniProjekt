import json
import uuid
import subprocess

sch_path = r"kicad\maturita.kicad_sch"
erc_json_path = r"kicad\maturita-erc.json"

with open(erc_json_path, "r", encoding="utf-8") as f:
    erc_data = json.load(f)

with open(sch_path, "r", encoding="utf-8") as f:
    sch_content = f.read()

# Collect all positions where "Pin not connected" occurs
nc_positions = set()
for sheet in erc_data.get("sheets", []):
    for v in sheet.get("violations", []):
        if v.get("description") == "Pin not connected":
            for item in v.get("items", []):
                pos = item.get("pos")
                if pos:
                    nc_positions.add((round(pos["x"], 2), round(pos["y"], 2)))

print(f"Found {len(nc_positions)} 'Pin not connected' pin positions.")

# Also add no_connect for CURRENT_EN or resolve it
# Let's add no_connect entries before the last closing parenthesis of the schematic
no_connect_blocks = []
for x, y in nc_positions:
    uid = str(uuid.uuid4())
    nc_block = f'\t(no_connect (at {x} {y}) (uuid "{uid}"))'
    no_connect_blocks.append(nc_block)

# Insert before last closing paren
last_paren_idx = sch_content.rfind(")")
sch_content = sch_content[:last_paren_idx] + "\n" + "\n".join(no_connect_blocks) + "\n" + sch_content[last_paren_idx:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(sch_content)

print(f"Added {len(no_connect_blocks)} no_connect flags to schematic.")

# Run ERC
cmd = [r"F:\kicad\bin\kicad-cli.exe", "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json_path, sch_path]
subprocess.run(cmd, check=True)

with open(erc_json_path, "r", encoding="utf-8") as ef:
    erc_res = json.load(ef)

errs = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "error")
warns = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "warning")
print(f"ERC after adding no_connects -> Errors: {errs}, Warnings: {warns}")
