#!/usr/bin/env python3
"""
Generate timing/waveform diagrams for digital electronics education.
"""

import argparse
import json
import sys
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Generate timing/waveform diagrams")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument(
        "--filename", required=True, help="Output filename (without extension)"
    )
    parser.add_argument("--spec", required=True, help="JSON specification string")
    return parser.parse_args()


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple (0-1 range)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def draw_clock(ax, y_pos, num_periods, color, height=0.8):
    """Draw a clock signal with specified number of periods."""
    x_positions = []
    y_positions = []

    # Start at 0
    x_positions.append(0)
    y_positions.append(0)

    for period in range(num_periods):
        # Rising edge
        x_positions.append(period + 0.5)
        y_positions.append(0)
        x_positions.append(period + 0.5)
        y_positions.append(1)

        # Falling edge
        x_positions.append(period + 1)
        y_positions.append(1)
        x_positions.append(period + 1)
        y_positions.append(0)

    # Close the waveform
    x_positions.append(num_periods)
    y_positions.append(0)

    ax.plot(
        x_positions,
        [y_pos + y * height for y in y_positions],
        color=color,
        linewidth=1.5,
        solid_capstyle="round",
    )


def draw_data_signal(ax, y_pos, values, color, height=0.8):
    """Draw a data signal (HIGH/LOW segments)."""
    num_cycles = len(values)

    x_positions = [0]
    y_positions = [y_pos]

    for i, val in enumerate(values):
        # Add transition point
        x_positions.append(i + 1)
        y_positions.append(y_pos + val * height)

    ax.plot(
        x_positions, y_positions, color=color, linewidth=1.5, solid_capstyle="round"
    )

    # Add horizontal baseline
    ax.plot([0, num_cycles], [y_pos, y_pos], color=color, linewidth=0.5, alpha=0.3)


def draw_clock_edges(ax, num_periods, y_min, y_max):
    """Draw vertical dashed lines at clock rising edges."""
    for i in range(num_periods):
        x = i + 0.5
        ax.axvline(
            x=x,
            ymin=0.05,
            ymax=0.95,
            color="#9ca3af",
            linestyle="--",
            linewidth=0.8,
            alpha=0.7,
        )


def draw_edge_markers(ax, num_periods, y_offset):
    """Draw edge markers (t1, t2, etc.) at the bottom."""
    for i in range(num_periods):
        x = i + 0.5
        ax.text(
            x,
            y_offset,
            f"t{i + 1}",
            fontsize=8,
            ha="center",
            va="top",
            color="#6b7280",
            fontfamily="sans-serif",
        )


def main():
    args = parse_args()

    try:
        spec = json.loads(args.spec)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON spec: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract spec parameters
    title = spec.get("title", "Timing Diagram")
    signals = spec.get("signals", [])

    if not signals:
        print("Error: No signals defined in spec", file=sys.stderr)
        sys.exit(1)

    # Determine number of periods from clock signal or data values
    num_periods = 4
    for signal in signals:
        if signal.get("type") == "clock":
            num_periods = signal.get("periods", 4)
            break
        elif signal.get("type") == "data" and "values" in signal:
            num_periods = len(signal.get("values", []))

    # Calculate figure dimensions
    fig_width = max(4, 2 * num_periods)
    fig_height = 1.2 * len(signals) + 1.5

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Remove spines except bottom
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["bottom"].set_color("#d1d5db")

    # Configure axis
    ax.set_xlim(0, num_periods)
    ax.set_ylim(-0.5, len(signals) * 1.2 + 0.5)
    ax.set_yticks([])
    ax.set_xticks([])

    # Add title
    ax.text(
        num_periods / 2,
        len(signals) * 1.2 + 0.3,
        title,
        fontsize=14,
        ha="center",
        va="bottom",
        fontweight="bold",
        fontfamily="sans-serif",
        color="#1f2937",
    )

    # Color mapping
    colors = {
        "clock": hex_to_rgb("#1e1e1e"),  # Black
        "input": hex_to_rgb("#2563eb"),  # Blue
        "output": hex_to_rgb("#dc2626"),  # Red
        "data": hex_to_rgb("#1e1e1e"),  # Default black
    }

    # Draw signals from top to bottom
    y_positions = [(len(signals) - i - 1) * 1.2 for i in range(len(signals))]

    for idx, signal in enumerate(spec.get("signals", [])):
        signal_name = signal.get("name", f"S{idx}")
        signal_type = signal.get("type", "data")
        y_pos = y_positions[idx]

        # Determine color based on type
        if signal_type == "clock":
            color = colors["clock"]
        elif signal_type in ["input", "data"]:
            # Check if it's an input or output based on name
            if signal.get("output", False) or signal_name.startswith("Q"):
                color = colors["output"]
            else:
                color = colors["input"]
        else:
            color = colors.get(signal_type, colors["data"])

        # Draw signal based on type
        if signal_type == "clock":
            periods = signal.get("periods", num_periods)
            draw_clock(ax, y_pos, periods, color)
        elif signal_type == "data":
            values = signal.get("values", [])
            if values:
                draw_data_signal(ax, y_pos, values, color)

        # Add signal label on the left
        ax.text(
            -0.15,
            y_pos + 0.4,
            signal_name,
            fontsize=11,
            ha="right",
            va="center",
            fontfamily="sans-serif",
            fontweight="bold",
            color="#1f2937",
        )

        # Add small dot at signal start
        ax.plot(0, y_pos + 0.4, "o", color=color, markersize=4)

    # Draw clock edges
    draw_clock_edges(ax, num_periods, 0, len(signals) * 1.2)

    # Draw edge markers
    draw_edge_markers(ax, num_periods, -0.3)

    # Adjust layout and save
    plt.tight_layout()

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
