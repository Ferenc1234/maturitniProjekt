# KiCad MCP-First Engineering Rules

1. **MCP-First Hardware Edits:**
   - Always use the `kicad` MCP server tools to inspect pins, move/place components, wire nets, and run ERC/DRC.
   - Never edit `.kicad_sch` or `.kicad_pcb` via raw text manipulation or custom S-expression Python scripts.

2. **Context & Memory:**
   - Always check `@./PROJECT_STATE.md` first for assigned/free ESP32-S3 GPIOs, net names, and sheet coordinates.
   - Update `PROJECT_STATE.md` after every hardware or schematic change to keep the pinout table and coordinates accurate.

3. **Documentation & BOM Sync:**
   - Whenever any hardware block, IC, net, or component value is added, removed, or modified:
     - Automatically update `docs/funkce.md` (Czech technical style, moving completed roadmap items from `[ ]` to `[x]`).
     - Automatically update `docs/seznamSoucastek.md` (BOM) to match current schematic components and quantities.

4. **Safety & Git Workflow:**
   - Never overwrite open KiCad GUI files without warning.
   - Summarize schematic, `funkce.md`, and `seznamSoucastek.md` changes before committing to Git.
