import json
import uuid
import subprocess
import os
import re

SCH_FILE = "BackupProjects_iq.masters.yt_personal_1_20261117.kicad_sch"
ERC_JSON = "BackupProjects_iq.masters.yt_personal_1_20261117-erc.json"

with open(ERC_JSON, "r", encoding="utf-8") as f:
    erc_data = json.load(f)

print("="*60)
print("1. DETAILS FOR SPECIFIC WARNINGS/ERRORS")
print("="*60)

targets = [
    "Unconnected wire endpoint",
    "Label connected to only one pin",
    "Both GND and MSR_LO_2 are attached",
    "Both LC_NODE and MEASURE_HIGH are attached"
]

for sheet in erc_data.get("sheets", []):
    for v in sheet.get("violations", []):
        desc = v.get("description", "")
        if any(t in desc for t in targets):
            print(f"\n[Violation] {desc} (Severity: {v.get('severity')})")
            for item in v.get("items", []):
                print(f"  - Item: {item.get('description')}")
                print(f"    Position: {item.get('pos')}")
                print(f"    UUID: {item.get('uuid')}")

print("\n" + "="*60)
print("2. PLACING PWR_FLAG ON 9 UDRIVEN POWER NETS")
print("="*60)

undriven_nets = [
    "+3V3", "VBAT", "TEST_2V5", "+24V", "USB_DN", "GND", "VREF_2V5", "VBUS_5V", "USB_DP"
]

with open(SCH_FILE, "r", encoding="utf-8") as f:
    sch_content = f.read()

# Check if PWR_FLAG is in lib_symbols, if not add it
if '"PWR_FLAG"' not in sch_content:
    with open("pwr_flag_def.txt", "r", encoding="utf-8") as pf:
        pwr_flag_def = pf.read()
    lib_sym_idx = sch_content.find("(lib_symbols")
    if lib_sym_idx != -1:
        insert_pos = sch_content.find("\n", lib_sym_idx) + 1
        sch_content = sch_content[:insert_pos] + "\t" + pwr_flag_def + "\n" + sch_content[insert_pos:]
        print("Added PWR_FLAG definition to lib_symbols.")

# For each undriven net, find where a power symbol of that net is located and place PWR_FLAG at (x, y)
added_count = 0
for net in undriven_nets:
    pattern = rf'\(symbol\s+\(lib_id\s+"{re.escape(net)}"\)\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)'
    match = re.search(pattern, sch_content)
    if match:
        x = float(match.group(1))
        y = float(match.group(2))
        flag_x = round(round(x / 1.27) * 1.27, 2)
        flag_y = round(round(y / 1.27) * 1.27, 2)
        new_uuid = str(uuid.uuid4())
        
        pwr_flag_instance = f'''\t(symbol
		(lib_id "PWR_FLAG")
		(at {flag_x} {flag_y} 0)
		(unit 0)
		(body_style 0)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "{new_uuid}")
		(property "Reference" "#FLG?"
			(at {flag_x} {flag_y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "PWR_FLAG"
			(at {flag_x} {flag_y} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at {flag_x} {flag_y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at {flag_x} {flag_y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at {flag_x} {flag_y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "ki_keywords" "flag power"
			(at {flag_x} {flag_y} 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{str(uuid.uuid4())}")
		)
		(instances
			(project "BackupProjects_iq.masters.yt_personal_1_20261117"
				(path "/0ba0140b-6504-41ba-b53a-eb9f8d614e9e"
					(reference "#FLG?")
					(unit 0)
				)
			)
		)
	)'''
        last_paren_idx = sch_content.rfind(")")
        sch_content = sch_content[:last_paren_idx] + "\n" + pwr_flag_instance + "\n" + sch_content[last_paren_idx:]
        print(f"Placed PWR_FLAG for net '{net}' at ({flag_x}, {flag_y}) with uuid {new_uuid}")
        added_count += 1
    else:
        print(f"Warning: Could not find power symbol for net '{net}'")

with open(SCH_FILE, "w", encoding="utf-8") as f:
    f.write(sch_content)

print(f"Successfully placed {added_count} PWR_FLAG symbols.")

print("\n" + "="*60)
print("3. RUNNING ERC AFTER PWR_FLAG ADDITIONS")
print("="*60)

cmd = [r"F:\kicad\bin\kicad-cli.exe", "sch", "erc", "--severity-all", "--format", "json", "-o", ERC_JSON, SCH_FILE]
subprocess.run(cmd, check=True)

with open(ERC_JSON, "r", encoding="utf-8") as f:
    new_erc = json.load(f)

total_new = sum(len(sheet.get("violations", [])) for sheet in new_erc.get("sheets", []))
error_count = sum(1 for sheet in new_erc.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "error")
warning_count = sum(1 for sheet in new_erc.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "warning")

print(f"Updated ERC Results:")
print(f"  Total Violations: {total_new}")
print(f"  Errors: {error_count}")
print(f"  Warnings: {warning_count}")
