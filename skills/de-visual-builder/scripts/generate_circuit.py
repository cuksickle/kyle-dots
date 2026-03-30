#!/usr/bin/env python3
"""
Generate circuit gate symbols and IC diagrams using matplotlib.
"""

import argparse
import sys
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Arc, Polygon, Wedge
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Generate circuit diagrams")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--filename", required=True, help="Output filename")
    parser.add_argument(
        "--type",
        required=True,
        choices=[
            "d_flipflop",
            "jk_flipflop",
            "ic_74ls74",
            "ic_74ls193",
            "gate",
            "seven_segment",
        ],
        help="Diagram type",
    )
    parser.add_argument("--gate", default="and", help="Gate type (for gate type)")
    parser.add_argument(
        "--inputs", type=int, default=2, help="Number of inputs (for gate type)"
    )
    return parser.parse_args()


def draw_and_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw an AND gate symbol."""
    # Gate body (D-shape)
    body_x = x
    body_y = y - height / 2

    # Draw D-shape using bezier curve
    from matplotlib.patches import Path
    from matplotlib.path import Path as MplPath

    # Create D-shape path
    verts = [
        (body_x, body_y),  # Bottom left
        (body_x, body_y + height),  # Top left
        (body_x + width * 0.4, body_y + height),  # Top curve start
        (body_x + width, body_y + height * 0.75),  # Top curve peak
        (body_x + width, body_y + height * 0.25),  # Bottom curve peak
        (body_x + width * 0.4, body_y),  # Bottom curve end
        (body_x, body_y),  # Close
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CLOSEPOLY,
    ]

    path = MplPath(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="white", edgecolor="black", linewidth=2)
    ax.add_patch(patch)

    # Input lines
    spacing = height / (num_inputs + 1)
    for i in range(num_inputs):
        input_y = body_y + spacing * (i + 1)
        ax.plot([x - 0.4, x], [input_y, input_y], "k-", linewidth=1.5)

    # Output line
    ax.plot(
        [body_x + width, body_x + width + 0.4],
        [body_y + height / 2, body_y + height / 2],
        "k-",
        linewidth=1.5,
    )

    return body_x + width + 0.5, body_y + height / 2


def draw_or_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw an OR gate symbol."""
    body_x = x
    body_y = y - height / 2

    # Draw curved D-shape
    from matplotlib.path import Path as MplPath

    verts = [
        (body_x, body_y),
        (body_x, body_y + height),
        (body_x + width * 0.3, body_y + height),
        (body_x + width, body_y + height * 0.8),
        (body_x + width, body_y + height * 0.2),
        (body_x + width * 0.3, body_y),
        (body_x, body_y),
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.LINETO,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.CURVE4,
        MplPath.LINETO,
        MplPath.CLOSEPOLY,
    ]

    path = MplPath(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="white", edgecolor="black", linewidth=2)
    ax.add_patch(patch)

    # Input lines
    spacing = height / (num_inputs + 1)
    for i in range(num_inputs):
        input_y = body_y + spacing * (i + 1)
        ax.plot([x - 0.4, x], [input_y, input_y], "k-", linewidth=1.5)

    # Output line
    ax.plot(
        [body_x + width, body_x + width + 0.4],
        [body_y + height / 2, body_y + height / 2],
        "k-",
        linewidth=1.5,
    )


def draw_not_gate(ax, x, y, width=0.6, height=0.5):
    """Draw a NOT gate (inverter) symbol."""
    body_x = x
    body_y = y - height / 2

    # Triangle
    verts = [
        (body_x, body_y),
        (body_x, body_y + height),
        (body_x + width, body_y + height / 2),
    ]
    codes = [1, 2, 79]  # MOVETO, LINETO, CLOSEPOLY

    from matplotlib.path import Path as MplPath

    path = MplPath(verts, codes)
    patch = mpatches.PathPatch(path, facecolor="white", edgecolor="black", linewidth=2)
    ax.add_patch(patch)

    # Inversion bubble
    bubble = Circle(
        (body_x + width + 0.08, body_y + height / 2),
        0.08,
        facecolor="white",
        edgecolor="black",
        linewidth=1.5,
    )
    ax.add_patch(bubble)

    # Input line
    ax.plot(
        [x - 0.3, x], [body_y + height / 2, body_y + height / 2], "k-", linewidth=1.5
    )

    # Output line
    ax.plot(
        [body_x + width + 0.16, body_x + width + 0.5],
        [body_y + height / 2, body_y + height / 2],
        "k-",
        linewidth=1.5,
    )


def draw_nand_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw a NAND gate symbol."""
    draw_and_gate(ax, x, y, width, height, num_inputs)
    # Add bubble
    bubble = Circle(
        (x + width + 0.08, y), 0.08, facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(bubble)


def draw_xor_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw an XOR gate symbol."""
    # Draw OR shape first
    draw_or_gate(ax, x, y, width, height, num_inputs)
    # Add extra curved line
    from matplotlib.patches import Arc

    extra_arc = Arc(
        (x + 0.1, y),
        width=0.5,
        height=height * 0.9,
        theta1=90,
        theta2=270,
        color="black",
        linewidth=1.5,
    )
    ax.add_patch(extra_arc)


def draw_nor_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw a NOR gate symbol."""
    draw_or_gate(ax, x, y, width, height, num_inputs)
    bubble = Circle(
        (x + width + 0.08, y), 0.08, facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(bubble)


def draw_xnor_gate(ax, x, y, width=1.2, height=0.8, num_inputs=2):
    """Draw an XNOR gate symbol."""
    draw_xor_gate(ax, x, y, width, height, num_inputs)
    bubble = Circle(
        (x + width + 0.08, y), 0.08, facecolor="white", edgecolor="black", linewidth=1.5
    )
    ax.add_patch(bubble)


def draw_d_flipflop(ax, x, y, scale=1.0):
    """Draw a D flip-flop symbol."""
    width, height = 2.5 * scale, 3.0 * scale

    # Main body rectangle
    body = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="white",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(body)

    # Q output (top right)
    ax.plot(
        [x + width, x + width + 0.3],
        [y + height * 0.75, y + height * 0.75],
        "k-",
        linewidth=1.5,
    )
    ax.text(
        x + width + 0.35,
        y + height * 0.75,
        "Q",
        fontsize=11,
        va="center",
        fontfamily="sans-serif",
    )

    # Q' output (bottom right)
    ax.plot(
        [x + width, x + width + 0.3],
        [y + height * 0.25, y + height * 0.25],
        "k-",
        linewidth=1.5,
    )
    # Add bubble for negation
    bubble = Circle(
        (x + width + 0.15, y + height * 0.25),
        0.06,
        facecolor="white",
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(bubble)
    ax.text(
        x + width + 0.35,
        y + height * 0.25,
        "Q'",
        fontsize=11,
        va="center",
        fontfamily="sans-serif",
    )

    # D input (top left)
    ax.plot([x - 0.3, x], [y + height * 0.7, y + height * 0.7], "k-", linewidth=1.5)
    ax.text(
        x - 0.4,
        y + height * 0.7,
        "D",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # CLK input (middle left) - with edge indicator
    ax.plot(
        [x - 0.3, x + 0.2], [y + height * 0.5, y + height * 0.5], "k-", linewidth=1.5
    )
    # Clock edge indicator
    ax.plot(
        [x - 0.1, x - 0.1, x],
        [y + height * 0.45, y + height * 0.5, y + height * 0.5],
        "k-",
        linewidth=1.5,
    )
    ax.text(
        x - 0.4,
        y + height * 0.5,
        "CLK",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # PRE' (bottom left, active low)
    ax.plot([x - 0.3, x], [y + height * 0.3, y + height * 0.3], "k-", linewidth=1.5)
    bubble = Circle(
        (x - 0.22, y + height * 0.3),
        0.05,
        facecolor="black",
        edgecolor="black",
        linewidth=0,
    )
    ax.add_patch(bubble)
    ax.text(
        x - 0.4,
        y + height * 0.3,
        "PRE'",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # CLR' (bottom left, active low)
    ax.plot([x - 0.3, x], [y + height * 0.15, y + height * 0.15], "k-", linewidth=1.5)
    bubble = Circle(
        (x - 0.22, y + height * 0.15),
        0.05,
        facecolor="black",
        edgecolor="black",
        linewidth=0,
    )
    ax.add_patch(bubble)
    ax.text(
        x - 0.4,
        y + height * 0.15,
        "CLR'",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # Title
    ax.text(
        x + width / 2,
        y + height + 0.15,
        "D FF",
        fontsize=12,
        ha="center",
        fontweight="bold",
        fontfamily="sans-serif",
    )


def draw_jk_flipflop(ax, x, y, scale=1.0):
    """Draw a JK flip-flop symbol."""
    width, height = 2.5 * scale, 3.0 * scale

    # Main body rectangle
    body = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="white",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(body)

    # Q output (top right)
    ax.plot(
        [x + width, x + width + 0.3],
        [y + height * 0.8, y + height * 0.8],
        "k-",
        linewidth=1.5,
    )
    ax.text(
        x + width + 0.35,
        y + height * 0.8,
        "Q",
        fontsize=11,
        va="center",
        fontfamily="sans-serif",
    )

    # Q' output (bottom right)
    ax.plot(
        [x + width, x + width + 0.3],
        [y + height * 0.2, y + height * 0.2],
        "k-",
        linewidth=1.5,
    )
    bubble = Circle(
        (x + width + 0.15, y + height * 0.2),
        0.06,
        facecolor="white",
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(bubble)
    ax.text(
        x + width + 0.35,
        y + height * 0.2,
        "Q'",
        fontsize=11,
        va="center",
        fontfamily="sans-serif",
    )

    # J input (top left)
    ax.plot([x - 0.3, x], [y + height * 0.75, y + height * 0.75], "k-", linewidth=1.5)
    ax.text(
        x - 0.4,
        y + height * 0.75,
        "J",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # K input (below J)
    ax.plot([x - 0.3, x], [y + height * 0.6, y + height * 0.6], "k-", linewidth=1.5)
    ax.text(
        x - 0.4,
        y + height * 0.6,
        "K",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # CLK input (middle left)
    ax.plot(
        [x - 0.3, x + 0.2], [y + height * 0.45, y + height * 0.45], "k-", linewidth=1.5
    )
    ax.plot(
        [x - 0.1, x - 0.1, x],
        [y + height * 0.4, y + height * 0.45, y + height * 0.45],
        "k-",
        linewidth=1.5,
    )
    ax.text(
        x - 0.4,
        y + height * 0.45,
        "CLK",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # PRE' (bottom left, active low)
    ax.plot([x - 0.3, x], [y + height * 0.3, y + height * 0.3], "k-", linewidth=1.5)
    bubble = Circle(
        (x - 0.22, y + height * 0.3),
        0.05,
        facecolor="black",
        edgecolor="black",
        linewidth=0,
    )
    ax.add_patch(bubble)
    ax.text(
        x - 0.4,
        y + height * 0.3,
        "PRE'",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # CLR' (bottom left, active low)
    ax.plot([x - 0.3, x], [y + height * 0.15, y + height * 0.15], "k-", linewidth=1.5)
    bubble = Circle(
        (x - 22, y + height * 0.15),
        0.05,
        facecolor="black",
        edgecolor="black",
        linewidth=0,
    )
    ax.add_patch(bubble)
    ax.text(
        x - 0.4,
        y + height * 0.15,
        "CLR'",
        fontsize=11,
        va="center",
        ha="right",
        fontfamily="sans-serif",
    )

    # Title
    ax.text(
        x + width / 2,
        y + height + 0.15,
        "JK FF",
        fontsize=12,
        ha="center",
        fontweight="bold",
        fontfamily="sans-serif",
    )


def draw_ic_74ls74(ax, x, y):
    """Draw 74LS74 IC (dual D flip-flop) - 14-pin DIP."""
    pin_length = 0.25
    body_width, body_height = 2.0, 3.5
    num_pins_per_side = 7

    # IC body
    body = FancyBboxPatch(
        (x, y),
        body_width,
        body_height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#f1f5f9",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(body)

    # Notch indicator (top)
    notch = Wedge(
        (x + body_width / 2, y + body_height),
        0.15,
        0,
        180,
        facecolor="#f1f5f9",
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(notch)

    # Pin numbers and labels (left side: 1-7, right side: 8-14)
    left_pins = [
        (1, "1CLR'"),
        (2, "1D"),
        (3, "1CLK"),
        (4, "1PRE'"),
        (5, "1Q"),
        (6, "1Q'"),
        (7, "GND"),
    ]
    right_pins = [
        (14, "VCC"),
        (13, "2Q'"),
        (12, "2Q"),
        (11, "2PRE'"),
        (10, "2CLK"),
        (9, "2D"),
        (8, "2CLR'"),
    ]

    pin_spacing = body_height / (num_pins_per_side + 1)

    # Draw left side pins
    for pin_num, label in left_pins:
        pin_y = y + body_height - pin_spacing * pin_num
        # Pin line
        ax.plot([x - pin_length, x], [pin_y, pin_y], "k-", linewidth=1.5)
        # Pin number
        ax.text(
            x - pin_length - 0.08,
            pin_y,
            str(pin_num),
            fontsize=8,
            ha="right",
            va="center",
            fontfamily="sans-serif",
        )
        # Label
        ax.text(
            x + body_width / 2,
            pin_y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            fontfamily="sans-serif",
        )

    # Draw right side pins
    for pin_num, label in right_pins:
        pin_y = y + body_height - pin_spacing * pin_num
        # Pin line
        ax.plot(
            [x + body_width, x + body_width + pin_length],
            [pin_y, pin_y],
            "k-",
            linewidth=1.5,
        )
        # Pin number
        ax.text(
            x + body_width + pin_length + 0.08,
            pin_y,
            str(pin_num),
            fontsize=8,
            ha="left",
            va="center",
            fontfamily="sans-serif",
        )
        # Label
        ax.text(
            x + body_width / 2,
            pin_y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            fontfamily="sans-serif",
        )

    # Title
    ax.text(
        x + body_width / 2,
        y + body_height + 0.2,
        "74LS74",
        fontsize=11,
        ha="center",
        fontweight="bold",
        fontfamily="sans-serif",
    )


def draw_ic_74ls193(ax, x, y):
    """Draw 74LS193 IC (4-bit up/down counter) - 16-pin DIP."""
    pin_length = 0.25
    body_width, body_height = 2.2, 4.0
    num_pins_per_side = 8

    # IC body
    body = FancyBboxPatch(
        (x, y),
        body_width,
        body_height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#f1f5f9",
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(body)

    # Notch indicator (top)
    notch = Wedge(
        (x + body_width / 2, y + body_height),
        0.15,
        0,
        180,
        facecolor="#f1f5f9",
        edgecolor="black",
        linewidth=1,
    )
    ax.add_patch(notch)

    # Pin configurations
    left_pins = [
        (1, "B"),
        (2, "QA"),
        (3, "LOAD'"),
        (4, "NC"),
        (5, "C"),
        (6, "QD"),
        (7, "CLR'"),
        (8, "GND"),
    ]
    right_pins = [
        (16, "VCC"),
        (15, "DOWN'"),
        (14, "UP"),
        (13, "QC"),
        (12, "QB"),
        (11, "NC"),
        (10, "A"),
        (9, "BO'"),
    ]

    pin_spacing = body_height / (num_pins_per_side + 1)

    # Draw left side pins
    for pin_num, label in left_pins:
        pin_y = y + body_height - pin_spacing * pin_num
        ax.plot([x - pin_length, x], [pin_y, pin_y], "k-", linewidth=1.5)
        ax.text(
            x - pin_length - 0.08,
            pin_y,
            str(pin_num),
            fontsize=8,
            ha="right",
            va="center",
            fontfamily="sans-serif",
        )
        ax.text(
            x + body_width / 2,
            pin_y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            fontfamily="sans-serif",
        )

    # Draw right side pins
    for pin_num, label in right_pins:
        pin_y = y + body_height - pin_spacing * pin_num
        ax.plot(
            [x + body_width, x + body_width + pin_length],
            [pin_y, pin_y],
            "k-",
            linewidth=1.5,
        )
        ax.text(
            x + body_width + pin_length + 0.08,
            pin_y,
            str(pin_num),
            fontsize=8,
            ha="left",
            va="center",
            fontfamily="sans-serif",
        )
        ax.text(
            x + body_width / 2,
            pin_y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            fontfamily="sans-serif",
        )

    # Title
    ax.text(
        x + body_width / 2,
        y + body_height + 0.2,
        "74LS193",
        fontsize=11,
        ha="center",
        fontweight="bold",
        fontfamily="sans-serif",
    )


def draw_seven_segment(ax, x, y, size=1.0):
    """Draw a 7-segment display with labels."""
    seg_length = 0.8 * size
    seg_width = 0.15 * size
    gap = 0.05 * size

    # Segment positions: a(top), b(top-right), c(bottom-right), d(bottom), e(bottom-left), f(top-left), g(middle)
    segments = {
        "a": (x + seg_length / 2, y + seg_length * 2 + gap * 2),
        "b": (x + seg_length + gap * 2, y + seg_length + gap * 1.5),
        "c": (x + seg_length + gap * 2, y + gap * 0.5),
        "d": (x + seg_length / 2, y),
        "e": (x, y + gap * 0.5),
        "f": (x, y + seg_length + gap * 1.5),
        "g": (x + seg_length / 2, y + seg_length / 2 + gap),
    }

    # Draw each segment as a rounded rectangle
    for name, (sx, sy) in segments.items():
        if name in ["a", "d", "g"]:  # Horizontal segments
            width, height = seg_length, seg_width
        else:  # Vertical segments
            width, height = seg_width, seg_length

        seg = FancyBboxPatch(
            (sx - width / 2, sy - height / 2),
            width,
            height,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor="#fee2e2",
            edgecolor="black",
            linewidth=1,
        )
        ax.add_patch(seg)

        # Label
        if name == "a":
            ax.text(
                sx,
                sy + seg_width + 0.08,
                "a",
                fontsize=9,
                ha="center",
                va="bottom",
                fontfamily="sans-serif",
            )
        elif name == "d":
            ax.text(
                sx,
                sy - seg_width - 0.08,
                "d",
                fontsize=9,
                ha="center",
                va="top",
                fontfamily="sans-serif",
            )
        elif name == "g":
            ax.text(
                sx,
                sy + seg_width + 0.08,
                "g",
                fontsize=9,
                ha="center",
                va="bottom",
                fontfamily="sans-serif",
            )

    # Vertical segment labels
    ax.text(
        x - seg_width - 0.1,
        segments["f"][1],
        "f",
        fontsize=9,
        ha="right",
        va="center",
        fontfamily="sans-serif",
    )
    ax.text(
        x - seg_width - 0.1,
        segments["e"][1],
        "e",
        fontsize=9,
        ha="right",
        va="center",
        fontfamily="sans-serif",
    )
    ax.text(
        x + seg_length + seg_width + 0.1,
        segments["b"][1],
        "b",
        fontsize=9,
        ha="left",
        va="center",
        fontfamily="sans-serif",
    )
    ax.text(
        x + seg_length + seg_width + 0.1,
        segments["c"][1],
        "c",
        fontsize=9,
        ha="left",
        va="center",
        fontfamily="sans-serif",
    )

    # Title
    ax.text(
        x + seg_length / 2,
        y - seg_length * 0.4,
        "7-Segment",
        fontsize=10,
        ha="center",
        fontfamily="sans-serif",
    )


def main():
    args = parse_args()

    # Set up figure based on type
    if args.type == "gate":
        fig_width, fig_height = 6, 5
    elif args.type in ["d_flipflop", "jk_flipflop", "seven_segment"]:
        fig_width, fig_height = 5, 5
    elif args.type in ["ic_74ls74", "ic_74ls193"]:
        fig_width, fig_height = 8, 5
    else:
        fig_width, fig_height = 6, 5

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Remove axes
    ax.set_xlim(0, fig_width)
    ax.set_ylim(0, fig_height)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw based on type
    if args.type == "gate":
        gate_funcs = {
            "and": draw_and_gate,
            "or": draw_or_gate,
            "not": draw_not_gate,
            "nand": draw_nand_gate,
            "nor": draw_nor_gate,
            "xor": draw_xor_gate,
            "xnor": draw_xnor_gate,
        }

        gate_func = gate_funcs.get(args.gate, draw_and_gate)
        gate_func(ax, 1.5, fig_height / 2, num_inputs=args.inputs)

    elif args.type == "d_flipflop":
        draw_d_flipflop(ax, 1.25, 1)

    elif args.type == "jk_flipflop":
        draw_jk_flipflop(ax, 1.25, 1)

    elif args.type == "ic_74ls74":
        draw_ic_74ls74(ax, 1, 0.5)

    elif args.type == "ic_74ls193":
        draw_ic_74ls193(ax, 1, 0.3)

    elif args.type == "seven_segment":
        draw_seven_segment(ax, 1.5, 1.2)

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
