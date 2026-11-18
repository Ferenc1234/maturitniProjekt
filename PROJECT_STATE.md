# Project State: Maturita (High-Precision Component Tester & Curve Tracer)

## 1. File Paths & Core Tooling
- **KiCad CLI Executable**: `F:\kicad\bin\kicad-cli.exe`
- **Project File**: `kicad\maturita.kicad_pro`
- **Schematic File**: `kicad\maturita.kicad_sch`
- **Pre-protection Backup**: `kicad\maturita.kicad_sch.pre_prot`
- **Footprint Library**: `kicad\maturita-import-fps.pretty\`
- **Documentation**: `docs\funkce.md`
- **BOM List**: `docs\seznamSoucastek.md`
- **ERC JSON Report**: `kicad\maturita-erc.json` (Total violations: 278)

## 2. ESP32-S3-WROOM-1 Pin Assignment Table (U1)
| Pin / GPIO | Net / Function | Status |
|---|---|---|
| GPIO0 | BOOT / EN | Assigned |
| GPIO1 | MUX_A0 | Assigned |
| GPIO2 | MUX_A1 | Assigned |
| GPIO3 | MUX_A2 | Assigned |
| GPIO4 | ADC_CS | Assigned |
| GPIO5 | SPI_SCK | Assigned |
| GPIO6 | SPI_MOSI | Assigned |
| GPIO7 | SPI_MISO | Assigned |
| GPIO8 | I2C_SDA | Assigned |
| GPIO9 | I2C_SCL | Assigned |
| GPIO10-14 | General GPIO / Measurement Control | Assigned / Configured |
| GPIO15-21 | Analog / Relay Control | Assigned |
| GPIO38-48 | USB / Native UART / Free GPIO | Free / Available |

*(Note: Exact pin-to-net mapping is dynamically tracked via script queries on `kicad\maturita.kicad_sch`).*

## 3. Power Rails & Key Net Names
- **Power Rails**: `+3V3`, `VBAT`, `VREF_2V5`, `+24V`, `VBUS_5V`, `GND`
- **Analog & Measurement Nets**: `TEST_2V5`, `MSR_LO_2`, `LC_NODE`, `MEASURE_HIGH`, `MEASURE_LOW`, `MUX_OUT`, `ADC_AIN0`, `ADC_AIN1`, `ADC_AIN2`, `ADC_AIN3`
- **Total Unique Labels Found**: 24 labels.

## 4. Sheet Coordinates & Bounding Boxes
- **Schematic Span**: X: [0.0, 364.49], Y: [0.0, 314.96]
- **Functional Block Regions**:
  - Microcontroller (U1): Center-left area
  - 24-bit ADC (U2) & Reference (U3) & Op-Amp (U4): Center-right analog frontend
  - Multiplexers (U6, U7) & Relays: Lower measurement switching matrix
  - 24V Boost (MT3608L) & Current Source: Top/Right high-voltage module
- **Free Whitespace Areas**:
  - Right side (X > 250 mm) and Bottom-right quadrant (X > 200, Y > 150) are clear for adding new blocks (e.g. 3rd terminal gate driver / curve tracer expansion).

## 5. ERC Status & Roadmap Summary
- **Current ERC Violations**: 278 (mostly pin-driven warnings/unconnected pins pending pull-ups/no-connects).
- **Completed Roadmap Items (`funkce.md` Section 1)**:
  - [x] Analog measuring core & TI ADS1220 24-bit ADC
  - [x] Precision reference TI REF5025 (2.5 V) & OPA2333 buffer
  - [x] TMUX1108 analog MUX & Low-side MOSFET 100 ohm range
  - [x] 4-wire Kelvin connection (`MEASURE_HIGH`, `MEASURE_LOW`)
  - [x] 24V Zener test module with MT3608L & LM317L constant current (2.019 mA)
  - [x] LC oscillator circuit with TLV3201
  - [x] TP4056 USB-C charging & AP2112K-3.3 LDO
- **Next Roadmap Items (`funkce.md` Section 2)**:
  - [ ] 100 ohm range MOSFET switch optimization (R_DS(on) reduction)
  - [ ] 3rd terminal gate driver / Curve Tracer expansion (BJT/MOSFET characterization)
  - [ ] Safe pre-scan autodetection & discharge protection circuit
