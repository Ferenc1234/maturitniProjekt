import re

sch_path = r"kicad\maturita.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    content = f.read()

stubs_uuids = [
    "2459597f-1c79-48bc-8ff5-08b7ef0b0db0",
    "07583c95-0330-4164-9a15-820812fc643d",
    "1d454bc7-0578-441c-9ee4-36e3423c5bfb"
]

for uid in stubs_uuids:
    # Find position of uid and remove enclosing (wire ...) block
    idx = content.find(uid)
    if idx != -1:
        # Find start of (wire
        start = content.rfind("(wire", 0, idx)
        # Find matching closing paren
        if start != -1:
            depth = 0
            end = start
            for i, c in enumerate(content[start:]):
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        end = start + i + 1
                        break
            content = content[:start] + content[end:]
            print(f"Successfully removed wire with UUID {uid}")

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated schematic saved.")
