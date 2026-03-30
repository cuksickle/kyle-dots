#!/usr/bin/env python3
"""
Generate simplified breadboard wiring diagrams.
"""

import argparse
import json
import sys
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arc
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Generate breadboard wiring diagrams")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--filename", required=True, help="Output filename")
    parser.add_argument("--ic", required=True, help="IC type (e.g., 74LS74)")
    parser.add_argument("--wiring", required=True, help="JSON wiring specification")
    parser.add_argument(
        "--components", default="[]", help="JSON array of component types"
    )
    return parser.parse_args()


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def draw_breadboard_outline(ax, x, y, width, height):
    """Draw the breadboard body."""
    body = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="#f5f0e6",
        edgecolor="#8b7355",
        linewidth=2,
    )
    ax.add_patch(body)


def draw_power_rails(ax, x, y, width, rail_height):
    """Draw power rails (+5V and GND)."""
    # +5V rail (red)
    vcc_rail = FancyBboxPatch(
        (x, y + height - rail_height),
        width,
        rail_height,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        facecolor="#dc2626",
        edgecolor="#991b1b",
        linewidth=1,
    )
    ax.add_patch(vcc_rail)
    ax.text(
        x + width / 2,
        y + height - rail_height / 2,
        "+5V",
        fontsize=10,
        ha="center",
        va="center",
        color="white",
        fontweight="bold",
    )

    # GND rail (blue)
    gnd_rail = FancyBboxPatch(
        (x, y),
        width,
        rail_height,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        facecolor="#2563eb",
        edgecolor="#1e40af",
        linewidth=1,
    )
    ax.add_patch(gnd_rail)
    ax.text(
        x + width / 2,
        y + rail_height / 2,
        "GND",
        fontsize=10,
        ha="center",
        va="center",
        color="white",
        fontweight="bold",
    )


def draw_breadboard_holes(ax, x, y, num_rows, num_cols, spacing):
    """Draw the grid of breadboard holes."""
    for row in range(num_rows):
        for col in range(num_cols):
            hole_x = x + col * spacing
            hole_y = y + row * spacing
            # Alternate colors for better visual
            color = "#e5e5e5" if (row + col) % 2 == 0 else "#d4d4d4"
            hole = Circle(
                (hole_x, hole_y),
                0.06,
                facecolor=color,
                edgecolor="#a3a3a3",
                linewidth=0.5,
            )
            ax.add_patch(hole)


def draw_ic(ax, x, y, ic_name, pin_count=14):
    """Draw IC in center of breadboard."""
    body_width = 0.8
    body_height = pin_count * 0.18

    # IC body
    body = FancyBboxPatch(
        (x - body_width / 2, y),
        body_width,
        body_height,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        facecolor="#6b7280",
        edgecolor="#374151",
        linewidth=2,
    )
    ax.add_patch(body)

    # Notch
    notch = Arc(
        (x, y + body_height),
        0.15,
        0.3,
        theta1=0,
        theta2=180,
        color="#374151",
        linewidth=1,
    )
    ax.add_patch(notch)

    # Label
    ax.text(
        x,
        y + body_height / 2,
        ic_name,
        fontsize=9,
        ha="center",
        va="center",
        color="white",
        fontweight="bold",
        rotation=90,
    )

    return x, y, body_width, body_height


def draw_led(ax, x, y, direction="up"):
    """Draw an LED symbol."""
    # LED body (triangle + rectangle)
    if direction == "up":
        # Triangle pointing up
        triangle = Polygon(
            [(x, y), (x - 0.15, y - 0.2), (x + 0.15, y - 0.2)],
            closed=True,
            facecolor="#fee2e2",
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(triangle)
        # Cathode line
        ax.plot([x - 0.12, x - 0.12], [y - 0.2, y - 0.25], "k-", linewidth=1.5)
        ax.plot([x + 0.12, x + 0.12], [y - 0.2, y - 0.25], "k-", linewidth=1.5)
        # LED label
        ax.text(x, y + 0.1, "LED", fontsize=8, ha="center", va="bottom")
    else:
        triangle = Polygon(
            [(x, y), (x - 0.15, y + 0.2), (x + 0.15, y + 0.2)],
            closed=True,
            facecolor="#fee2e2",
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(triangle)
        ax.text(x, y - 0.1, "LED", fontsize=8, ha="center", va="top")


def draw_resistor(ax, x, y, orientation="vertical"):
    """Draw a resistor symbol (zigzag)."""
    if orientation == "vertical":
        # Zigzag pattern
        x_center = x
        segments = [
            (0, 0),
            (0.05, 0.03),
            (-0.05, 0.06),
            (0.05, 0.09),
            (-0.05, 0.12),
            (0.05, 0.15),
            (-0.05, 0.18),
            (0.05, 0.21),
            (0, 0.24),
        ]
        points = [(x_center + dx, y + dy) for dx, dy in segments]
        ax.plot(*zip(*points), "k-", linewidth=1.5)
        ax.text(x, y + 0.35, "330Ω", fontsize=8, ha="center", va="bottom")
    else:
        # Horizontal resistor
        segments = [
            (0, 0),
            (0.05, 0.03),
            (-0.05, 0.06),
            (0.05, 0.09),
            (-0.05, 0.12),
            (0.05, 0.15),
            (-0.05, 0.18),
            (0.05, 0.21),
            (0, 0.24),
        ]
        points = [(x + dx, y + dy) for dx, dy in segments]
        ax.plot(*zip(*points), "k-", linewidth=1.5)


def draw_switch(ax, x, y, switch_type="spdt"):
    """Draw a switch symbol."""
    if switch_type == "spdt":
        # SPDT switch
        ax.plot([x - 0.2, x], [y, y], "k-", linewidth=1.5)  # Common
        ax.plot([x, x + 0.15], [y, y + 0.1], "k-", linewidth=1.5)  # NO
        ax.plot([x, x + 0.15], [y, y - 0.1], "k-", linewidth=1.5)  # NC
        # Pivot point
        circle = Circle((x, y), 0.03, facecolor="black")
        ax.add_patch(circle)
        ax.text(x, y + 0.2, "SW", fontsize=8, ha="center", va="bottom")
    else:
        # Simple pushbutton
        rect = FancyBboxPatch(
            (x - 0.1, y - 0.05),
            0.2,
            0.1,
            boxstyle="round,pad=0.01",
            facecolor="#f5f5f5",
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x, y + 0.1, "BTN", fontsize=8, ha="center", va="bottom")


def draw_button(ax, x, y):
    """Draw a pushbutton symbol."""
    # Two contacts
    contact1 = Circle(
        (x - 0.08, y + 0.05), 0.03, facecolor="#d4d4d4", edgecolor="black", linewidth=1
    )
    contact2 = Circle(
        (x + 0.08, y + 0.05), 0.03, facecolor="#d4d4d4", edgecolor="black", linewidth=1
    )
    ax.add_patch(contact1)
    ax.add_patch(contact2)
    # Contact lines
    ax.plot([x - 0.08, x - 0.08], [y + 0.05, y + 0.15], "k-", linewidth=1)
    ax.plot([x + 0.08, x + 0.08], [y + 0.05, y + 0.15], "k-", linewidth=1)
    # Button
    rect = FancyBboxPatch(
        (x - 0.12, y - 0.08),
        0.24,
        0.1,
        boxstyle="round,pad=0.01",
        facecolor="#ef4444",
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(rect)
    ax.text(x, y - 0.15, "BTN", fontsize=8, ha="center", va="top")


def draw_wire(ax, start, end, color, linewidth=2):
    """Draw a wire between two points."""
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        color=color,
        linewidth=linewidth,
        solid_capstyle="round",
    )


def draw_wire_legend(ax, x, y, colors):
    """Draw wire color legend."""
    labels = ["Signal", "VCC", "GND", "Data", "Clock"]
    for i, (color, label) in enumerate(zip(colors[: len(labels)], labels)):
        y_pos = y - i * 0.25
        line = FancyBboxPatch(
            (x, y_pos - 0.05),
            0.3,
            0.1,
            boxstyle="round,pad=0.01",
            facecolor=color,
            edgecolor="black",
            linewidth=1,
        )
        ax.add_patch(line)
        ax.text(x + 0.4, y_pos, label, fontsize=8, va="center", fontfamily="sans-serif")


def main():
    args = parse_args()

    # Parse wiring and components
    try:
        wiring = json.loads(args.wiring)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid wiring JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        components = json.loads(args.components)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid components JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Figure setup
    fig_width, fig_height = 10, 6
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Set limits
    ax.set_xlim(0, fig_width)
    ax.set_ylim(0, fig_height)
    ax.set_aspect("equal")
    ax.axis("off")

    # Breadboard dimensions
    bb_x, bb_y = 1.5, 1.0
    bb_width, bb_height = 7, 4
    rail_height = 0.3

    # Draw breadboard
    draw_breadboard_outline(ax, bb_x, bb_y, bb_width, bb_height)

    # Draw power rails
    draw_power_rails(ax, bb_x, bb_y, bb_width, rail_height)

    # Draw hole grid (simplified)
    num_rows = 10
    num_cols = 50
    spacing = (bb_width - 1) / num_cols
    hole_start_x = bb_x + 0.5
    hole_start_y = bb_y + rail_height + 0.3

    # Left side holes (a-e)
    draw_breadboard_holes(ax, hole_start_x, hole_start_y, num_rows, 5, spacing)
    # Right side holes (f-j)
    draw_breadboard_holes(
        ax, hole_start_x + 6 * spacing, hole_start_y, num_rows, 5, spacing
    )

    # Draw IC in center
    ic_center_x = bb_x + bb_width / 2
    ic_start_y = bb_y + rail_height + 0.5
    pin_count = 14 if "74" in args.ic else 16
    draw_ic(ax, ic_center_x, ic_start_y, args.ic, pin_count)

    # Wire colors (cycle through)
    wire_colors = ["#dc2626", "#1e1e1e", "#2563eb", "#16a34a", "#ca8a04", "#9333ea"]

    # Draw wiring connections
    wire_idx = 0
    pin_positions = {}

    # Calculate pin positions
    for pin_num in range(1, pin_count + 1):
        if pin_num <= pin_count // 2:
            # Left side
            row = (pin_count // 2) - pin_num + 1
            pin_positions[pin_num] = (ic_center_x - 0.6, ic_start_y + row * 0.18 + 0.05)
        else:
            # Right side
            row = pin_num - (pin_count // 2) - 1
            pin_positions[pin_num] = (ic_center_x + 0.6, ic_start_y + row * 0.18 + 0.05)

    # Draw wires based on wiring spec
    for signal_name, pin_num in wiring.items():
        if pin_num in pin_positions:
            start = pin_positions[pin_num]
            color = wire_colors[wire_idx % len(wire_colors)]
            wire_idx += 1

            # Determine endpoint based on signal type
            if "VCC" in signal_name.upper() or "5V" in signal_name.upper():
                # Connect to +5V rail
                end = (
                    bb_x + bb_width / 2 + (1 if pin_num > pin_count // 2 else -1),
                    bb_y + bb_height - rail_height + 0.15,
                )
            elif "GND" in signal_name.upper():
                # Connect to GND rail
                end = (
                    bb_x + bb_width / 2 + (1 if pin_num > pin_count // 2 else -1),
                    bb_y + rail_height - 0.15,
                )
            elif "Q" in signal_name.upper() or "CLK" in signal_name.upper():
                # Output signals go to right side
                end = (bb_x + bb_width - 0.5, start[1])
            else:
                # Input signals go to left side
                end = (bb_x + 0.5, start[1])

            draw_wire(ax, start, end, color)

            # Add label at component end
            ax.text(
                end[0],
                end[1],
                signal_name,
                fontsize=7,
                va="center",
                ha="left" if end[0] > bb_x + bb_width / 2 else "right",
            )

    # Draw components
    comp_x = bb_x + bb_width + 0.8
    for i, comp in enumerate(components):
        comp_y = bb_y + bb_height - 1 - i * 1.2
        if "LED" in comp.upper():
            draw_led(ax, comp_x + 0.5, comp_y + 0.5)
        elif "RESISTOR" in comp.upper() or "Ω" in comp:
            draw_resistor(ax, comp_x, comp_y + 0.5)
        elif "SWITCH" in comp.upper():
            draw_switch(ax, comp_x, comp_y + 0.5, "spdt")
        elif "BUTTON" in comp.upper() or "BTN" in comp.upper():
            draw_button(ax, comp_x + 0.5, comp_y)

    # Draw legend
    draw_wire_legend(ax, 0.3, 2.5, wire_colors[:5])

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    output_path = os.path.join(args.output, f"{args.filename}.png")
    plt.savefig(
        output_path, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none"
    )
    plt.close()

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
