#!/usr/bin/env python3
"""
Generate block diagrams showing system architecture.
"""

import argparse
import json
import sys
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Generate block diagrams")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--filename", required=True, help="Output filename")
    parser.add_argument("--spec", required=True, help="JSON specification string")
    return parser.parse_args()


def draw_block(ax, x, y, width, height, label, block_id):
    """Draw a rounded rectangle block."""
    # Main block body
    block = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.05,rounding_size=0.15",
        facecolor="white",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(block)

    # Label
    ax.text(
        x,
        y,
        label,
        fontsize=12,
        ha="center",
        va="center",
        fontfamily="sans-serif",
        fontweight="bold",
        color="#1f2937",
    )

    # Store position for connections
    return {"id": block_id, "x": x, "y": y, "width": width, "height": height}


def draw_arrow(ax, start, end, label="", color="#1f2937"):
    """Draw an arrow between two points."""
    # Calculate direction
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = np.sqrt(dx**2 + dy**2)

    if length == 0:
        return

    # Normalize
    dx, dy = dx / length, dy / length

    # Adjust start and end points (stop at block edges)
    margin = 0.4  # Half block width approx
    actual_start = (start[0] + dx * margin, start[1] + dy * margin)
    actual_end = (end[0] - dx * margin, end[1] - dy * margin)

    # Draw line
    ax.plot(
        [actual_start[0], actual_end[0]],
        [actual_start[1], actual_end[1]],
        color=color,
        linewidth=1.5,
        solid_capstyle="round",
    )

    # Draw arrowhead
    arrow_size = 0.15
    angle = np.arctan2(dy, dx)

    # Arrowhead points
    arrow_tip = actual_end
    arrow_left = (
        arrow_tip[0] - arrow_size * np.cos(angle - np.pi / 6),
        arrow_tip[1] - arrow_size * np.sin(angle - np.pi / 6),
    )
    arrow_right = (
        arrow_tip[0] - arrow_size * np.cos(angle + np.pi / 6),
        arrow_tip[1] - arrow_size * np.sin(angle + np.pi / 6),
    )

    arrow_head = mpatches.Polygon(
        [arrow_tip, arrow_left, arrow_right],
        closed=True,
        facecolor=color,
        edgecolor=color,
        linewidth=1,
    )
    ax.add_patch(arrow_head)

    # Add label on arrow
    if label:
        mid_x = (actual_start[0] + actual_end[0]) / 2
        mid_y = (actual_start[1] + actual_end[1]) / 2

        # Offset label slightly
        offset = 0.2
        label_x = mid_x - dy * offset
        label_y = mid_y + dx * offset

        ax.text(
            label_x,
            label_y,
            label,
            fontsize=9,
            ha="center",
            va="center",
            fontfamily="sans-serif",
            color="#4b5563",
            bbox=dict(
                boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.8
            ),
        )


def auto_layout(blocks, connections):
    """Auto-layout blocks in left-to-right flow."""
    if not blocks:
        return blocks

    # Get blocks without positions
    unpositioned = [b for b in blocks if "x" not in b or "y" not in b]
    positioned = [b for b in blocks if "x" in b and "y" in b]

    if not unpositioned:
        return blocks

    # Simple layout algorithm
    # Determine layout direction based on connections
    max_x = max([b.get("x", 0) for b in positioned]) if positioned else 0

    # Create levels based on connections (BFS)
    levels = {}
    in_degree = {b["id"]: 0 for b in unpositioned}

    # Calculate in-degrees
    for conn in connections:
        if conn.get("from") in in_degree and conn.get("to") in in_degree:
            in_degree[conn.get("to")] = in_degree.get(conn.get("to"), 0) + 1

    # BFS to assign levels
    queue = [b["id"] for b in unpositioned if in_degree[b["id"]] == 0]
    current_level = 0

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            block_id = queue.pop(0)
            if block_id not in levels:
                levels[block_id] = current_level

        # Add neighbors to queue
        for conn in connections:
            if conn.get("from") == block_id and conn.get("to") in in_degree:
                in_degree[conn.get("to")] -= 1
                if in_degree[conn.get("to")] == 0:
                    queue.append(conn.get("to"))

        current_level += 1

    # Assign remaining blocks
    for b in unpositioned:
        if b["id"] not in levels:
            levels[b["id"]] = current_level

    # Assign positions
    blocks_per_level = {}
    for b in unpositioned:
        level = levels.get(b["id"], 0)
        if level not in blocks_per_level:
            blocks_per_level[level] = []
        blocks_per_level[level].append(b)

    # Position blocks
    block_width = 2.0
    block_height = 0.8
    horizontal_spacing = 1.5
    vertical_spacing = 1.2

    # Start position
    start_x = 1.5
    start_y = 3.0

    max_level = max(blocks_per_level.keys()) if blocks_per_level else 0

    for level, level_blocks in blocks_per_level.items():
        x = start_x + level * (block_width + horizontal_spacing)

        # Center vertically
        total_height = len(level_blocks) * vertical_spacing
        y_start = start_y + (max_level - level) * 2 + total_height / 2

        for i, b in enumerate(level_blocks):
            y = y_start - i * vertical_spacing
            b["x"] = x
            b["y"] = y

    return blocks


def main():
    args = parse_args()

    try:
        spec = json.loads(args.spec)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON spec: {e}", file=sys.stderr)
        sys.exit(1)

    blocks = spec.get("blocks", [])
    connections = spec.get("connections", [])

    if not blocks:
        print("Error: No blocks defined in spec", file=sys.stderr)
        sys.exit(1)

    # Auto-layout if needed
    blocks = auto_layout(blocks, connections)

    # Calculate figure dimensions
    max_x = max([b.get("x", 0) for b in blocks]) if blocks else 5
    max_y = max([b.get("y", 0) for b in blocks]) if blocks else 3
    min_x = min([b.get("x", 0) for b in blocks]) if blocks else 0
    min_y = min([b.get("y", 0) for b in blocks]) if blocks else 0

    # Add margins
    margin_x = 2.5
    margin_y = 1.5

    fig_width = (max_x - min_x) + margin_x * 2
    fig_height = (max_y - min_y) + margin_y * 2

    # Minimum figure size
    fig_width = max(fig_width, 6)
    fig_height = max(fig_height, 4)

    # Create figure
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Remove axes
    ax.set_xlim(0, fig_width)
    ax.set_ylim(0, fig_height)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw blocks
    block_width, block_height = 2.0, 0.8

    block_positions = {}
    for block in blocks:
        block_id = block.get("id", "")
        x = block.get("x", 3)
        y = block.get("y", fig_height / 2)
        label = block.get("label", block_id)

        pos = draw_block(ax, x, y, block_width, block_height, label, block_id)
        block_positions[block_id] = (x, y)

    # Draw connections
    for conn in connections:
        from_id = conn.get("from", "")
        to_id = conn.get("to", "")
        label = conn.get("label", "")

        if from_id in block_positions and to_id in block_positions:
            start = block_positions[from_id]
            end = block_positions[to_id]
            draw_arrow(ax, start, end, label)

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
