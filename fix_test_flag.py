import json
import uuid
import subprocess
import re

sch_path = r"kicad\maturita.kicad_sch"
erc_json_path = r"kicad\maturita-erc.json"

with open(sch_path, "r", encoding="utf-8") as f:
    sch_content = f.read()

# Add PWR_FLAG for TEST_2V5 at (64.77, 92.71)
flag_x = 64.77
flag_y = 92.71
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
			(project "maturita"
				(path "/0ba0140b-6504-41ba-b53a-eb9f8d614e9e"
					(reference "#FLG?")
					(unit 0)
				)
			)
		)
	)'''

last_paren_idx = sch_content.rfind(")")
sch_content = sch_content[:last_paren_idx] + "\n" + pwr_flag_instance + "\n" + sch_content[last_paren_idx:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(sch_content)

print("Added non-conflicting PWR_FLAG for TEST_2V5.")

# Run ERC
cmd = [r"F:\kicad\bin\kicad-cli.exe", "sch", "erc", "--severity-all", "--format", "json", "-o", erc_json_path, sch_path]
subprocess.run(cmd, check=True)

with open(erc_json_path, "r", encoding="utf-8") as ef:
    erc_res = json.load(ef)

errs = sum(1 for sheet in erc_res.get("sheets", []) for v in sheet.get("violations", []) if v.get("severity") == "error")
print(f"Errors after adding TEST_2V5 flag: {errs}")
