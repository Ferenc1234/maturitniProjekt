# KiCad Editing Rules

- Always run `kicad-cli sch erc` after schema edits.
- Always snap components and wires to the 1.27 mm grid.
- Use Python scripts for programmatic changes instead of manual S-expression edits.

## Documentation & BOM Sync Policy

1. Whenever any hardware block, IC, net, or component value is added, removed, or modified in the KiCad schematic/PCB:
   - Automatically update `funkce.md` (move completed roadmap items from Section 2 `[ ]` to `[x]` and document them under Section 1 in Czech, matching the existing technical style and formatting).
   - Automatically update `seznamSoucastek.md` (add/remove/update designators, values, packages, LCSC part numbers, and quantities to match the current KiCad schematic).
2. Always run `F:\kicad\bin\kicad-cli.exe sch erc` and `kicad-cli sch export bom` (or verify component counts via Python) before updating `seznamSoucastek.md` so the BOM never drifts from the schematic.
3. Never commit or push to GitHub without showing a summary of the schematic, `funkce.md`, and `seznamSoucastek.md` changes first.

