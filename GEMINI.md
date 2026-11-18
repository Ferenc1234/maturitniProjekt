# KiCad Editing Rules

- Always run `kicad-cli sch erc` after schema edits.
- Always snap components and wires to the 1.27 mm grid.
- Use Python scripts for programmatic changes instead of manual S-expression edits.

## Speed & Memory Rules (Token Efficiency)

1. **Memory-First Rule:** Always read `PROJECT_STATE.md` before touching any KiCad file. NEVER read the entire `.kicad_sch` or `.kicad_pcb` file into context at once—always query or edit specific sections via short Python scripts.
2. **State Sync Rule:** After any schematic, PCB, `funkce.md`, or `seznamSoucastek.md` edit, update `PROJECT_STATE.md` so the pinout table, net list, and free coordinates stay accurate.
3. **Ignore Noise:** Ignore `.bak` files and temporary Python helper scripts when scanning the workspace.

## Documentation & BOM Sync Policy

1. Whenever any hardware block, IC, net, or component value is added, removed, or modified in the KiCad schematic/PCB:
   - Automatically update `funkce.md` (move completed roadmap items from Section 2 `[ ]` to `[x]` and document them under Section 1 in Czech, matching the existing technical style and formatting).
   - Automatically update `seznamSoucastek.md` (add/remove/update designators, values, packages, LCSC part numbers, and quantities to match the current KiCad schematic).
2. Always run `F:\kicad\bin\kicad-cli.exe sch erc` and `kicad-cli sch export bom` (or verify component counts via Python) before updating `seznamSoucastek.md` so the BOM never drifts from the schematic.
3. Never commit or push to GitHub without showing a summary of the schematic, `funkce.md`, and `seznamSoucastek.md` changes first.
