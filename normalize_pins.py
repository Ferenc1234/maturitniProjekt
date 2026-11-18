import re
import subprocess
import json

sch_path = r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117.kicad_sch"
erc_json_path = r"kicad\BackupProjects_iq.masters.yt_personal_1_20261117-erc.json"

with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Only modify lib_symbols section
lib_sym_start = content.find("(lib_symbols")
lib_sym_end = content.find("\n\t(symbol\n\t\t(lib_id")
if lib_sym_end == -1:
    lib_sym_end = content.find("\n\t(wire")

lib_sym_text = content[lib_sym_start:lib_sym_end]

# List of symbols to normalize (all resistors + J2)
target_symbols = [
    '0402WGF1002TCE', '0805W8F1002T5E', '0805W8F1002T5E_1', '0805W8F1002T5E_10',
    '0805W8F1002T5E_11', '0805W8F1002T5E_2', '0805W8F1002T5E_3', '0805W8F1002T5E_4',
    '0805W8F1002T5E_5', '0805W8F1002T5E_6', '0805W8F1002T5E_7', '0805W8F1002T5E_8',
    '0805W8F1002T5E_9', '0805W8F3320T5E', '0805W8F3902T5E', '0805W8F4701T5E',
    '0805W8F4701T5E_1', '0805W8F5101T5E', '0805W8F5101T5E_1', '1206W4F3302T5E',
    '1206W4F3302T5E_1', '1206W4F3302T5E_2', '25121WF100KT4E', 'HDR-M-2.54_1x3',
    'RT0805BRD07100KL', 'RT0805BRD07100KL_1', 'RT0805BRD07100KL_2', 'RT0805BRD0710KL',
    'RT0805BRD071KL'
]

modified_lib = lib_sym_text
for sym_name in target_symbols:
    # Find symbol block in lib_sym_text
    sym_start = modified_lib.find(f'(symbol "{sym_name}"')
    if sym_start != -1:
        # Find closing
        sym_end = modified_lib.find('(embedded_fonts no)', sym_start)
        if sym_end != -1:
            sym_block_end = modified_lib.find(')', sym_end) + 2
            sym_block = modified_lib[sym_start:sym_block_end]
            # Replace "(pin input line" with "(pin passive line"
            new_block = sym_block.replace('(pin input line', '(pin passive line')
            modified_lib = modified_lib[:sym_start] + new_block + modified_lib[sym_block_end:]
            print(f"Normalized pins for symbol {sym_name}")

content = content[:lib_sym_start] + modified_lib + content[lib_sym_end:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved schematic with normalized pins.")

# Run ERC
cmd = [r"F:\kicad\bin\kicad-cli.exe", "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json_path, sch_path]
subprocess.run(cmd, check=True)

with open(erc_json_path, "r", encoding="utf-8") as ef:
    erc_res = json.load(ef)

errs = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "error")
warns = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "warning")
print(f"ERC after normalizing pins -> Errors: {errs}, Warnings: {warns}")
