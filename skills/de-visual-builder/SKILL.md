---
name: de-visual-builder
description: Generate visual assets for lesson markdown files. Reads a lesson, identifies needed diagrams, generates PNGs with specialized tools (matplotlib, schemdraw, Graphviz), and composes them into an Excalidraw drawing. Use when the user wants to create visuals, diagrams, or visual assets for a lesson.
---

# DE Visual Builder

Generate visual assets for lesson markdown files by:
1. Reading the lesson content
2. Planning which visual assets are needed
3. Generating PNGs with specialized Python tools
4. Composing all assets into a single Excalidraw drawing

## Workflow

### Step 1: Read the Lesson
Read the lesson markdown file. Identify sections that would benefit from visuals:
- Timing diagrams (clock signals, flip-flop waveforms)
- Circuit schematics (gate symbols, IC pinouts)
- Breadboard layouts (wiring diagrams)
- Block diagrams (system architecture)
- State diagrams (state machines, flowcharts)
- Comparison diagrams (side-by-side concepts)

### Step 2: Plan Assets
For each visual needed, determine:
- **Type**: timing, circuit, breadboard, block, state, comparison
- **Tool**: which Python script to use
- **Parameters**: what data/values to pass
- **Placement**: where it goes in the final Excalidraw layout

### Step 3: Generate PNGs
Run the appropriate scripts from `scripts/`:

```bash
# Timing diagrams (matplotlib)
python3 SKILL_DIR/scripts/generate_timing.py --output DIR --signals '{"CLK": "clock", "D": [1,0,1,1,0], "Q": [0,1,0,1,1]}'

# Circuit symbols (matplotlib patches)
python3 SKILL_DIR/scripts/generate_circuit.py --output DIR --type d_flipflop

# Breadboard layouts (matplotlib)
python3 SKILL_DIR/scripts/generate_breadboard.py --output DIR --ic 74LS74 --wiring '{"VCC": 14, "GND": 7, "D": 2, "CLK": 3, "Q": 5}'
```

Replace `SKILL_DIR` with the actual skill directory path.

### Step 4: Compose into Excalidraw
Run the composition script to combine all PNGs into one Excalidraw drawing:

```bash
python3 SKILL_DIR/scripts/compose_excalidraw.py \
  --assets DIR/*.png \
  --layout lesson_full \
  --title "Lesson Title" \
  --output lesson.excalidraw
```

### Step 5: Verify
- Check the .excalidraw file is valid JSON
- Confirm all images are embedded
- Suggest opening in Obsidian to verify rendering

## Available Scripts

| Script | Purpose | Input |
|--------|---------|-------|
| `generate_timing.py` | Timing/waveform diagrams | Signal definitions (clock, data, output) |
| `generate_circuit.py` | Circuit gate symbols | Gate type, pin labels |
| `generate_breadboard.py` | Breadboard wiring layouts | IC type, wire connections |
| `generate_block.py` | Block diagrams | Blocks + connections |
| `compose_excalidraw.py` | Compose PNGs into Excalidraw | PNG files + layout template |

## Layout Templates

Located in `templates/excalidraw_layouts/`:
- `lesson_full.json` — Full lesson: symbol + timing + breadboard + practice
- `timing_only.json` — Just timing diagrams
- `circuit_only.json` — Just circuit diagrams
- `comparison.json` — Side-by-side comparison layout

## Color Palettes

Located in `templates/color_palettes/`:
- `de.json` — Digital Electronics colors (signal colors, gate fills)
- `default.json` — Neutral professional palette

## Rules
- Always generate assets in a temporary directory, then compose
- The .excalidraw file goes alongside the lesson markdown
- PNG assets go in an `assets/` subdirectory next to the lesson
- Use `roughness: 0` for clean technical diagrams
- All images embedded as base64 in the Excalidraw JSON
- Target 150 DPI for generated PNGs
