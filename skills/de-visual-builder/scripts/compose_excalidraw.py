#!/usr/bin/env python3
"""
Compose multiple PNG images into a single Excalidraw drawing.
"""

import argparse
import base64
import json
import os
import sys
import glob
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Compose PNG images into Excalidraw")
    parser.add_argument("--assets", required=True, help="Asset files (glob pattern)")
    parser.add_argument("--layout", default="lesson_full", help="Layout template name")
    parser.add_argument("--title", default="", help="Title text")
    parser.add_argument("--subtitle", default="", help="Subtitle text")
    parser.add_argument("--output", required=True, help="Output Excalidraw file")
    parser.add_argument("--palette", default="de", help="Color palette name")
    return parser.parse_args()


def load_layout_template(layout_name, templates_dir):
    """Load a layout template from the templates directory."""
    template_path = Path(templates_dir) / f"{layout_name}.json"

    if not template_path.exists():
        # Return default template
        return {
            "sections": [
                {
                    "id": "timing",
                    "type": "image",
                    "x": 50,
                    "y": 100,
                    "width": 400,
                    "height": 250,
                },
                {
                    "id": "circuit",
                    "type": "image",
                    "x": 500,
                    "y": 100,
                    "width": 300,
                    "height": 250,
                },
                {
                    "id": "title",
                    "type": "text",
                    "x": 50,
                    "y": 30,
                    "width": 800,
                    "height": 40,
                },
            ]
        }

    with open(template_path, "r") as f:
        return json.load(f)


def load_color_palette(palette_name, palettes_dir):
    """Load a color palette from the palettes directory."""
    palette_path = Path(palettes_dir) / f"{palette_name}.json"

    if not palette_path.exists():
        # Return default DE palette
        return {
            "primary": "#1a1a2e",
            "secondary": "#16213e",
            "accent": "#0f3460",
            "highlight": "#e94560",
            "background": "#ffffff",
            "text": "#1a1a2e",
            "grid": "#f0f0f0",
        }

    with open(palette_path, "r") as f:
        return json.load(f)


def load_image_as_base64(image_path):
    """Load PNG image and convert to base64 data URL."""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def generate_seed():
    """Generate a random seed for Excalidraw elements."""
    import random

    return random.randint(1, 999999999)


def create_text_element(
    x,
    y,
    width,
    height,
    text,
    font_size=20,
    font_family=1,
    text_align="left",
    vertical_align="top",
    stroke_color="#1a1a2e",
    font_weight="normal",
):
    """Create an Excalidraw text element."""
    return {
        "type": "text",
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "id": f"text_{generate_seed()}",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "boundElements": [],
        "locked": False,
        "linkedNodes": None,
        "text": text,
        "rawText": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": text_align,
        "verticalAlign": vertical_align,
        "baseline": font_size * 0.8,
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25,
        "autoResize": True,
    }


def create_image_element(x, y, width, height, file_id, image_data):
    """Create an Excalidraw image element."""
    return {
        "type": "image",
        "version": 1,
        "versionNonce": generate_seed(),
        "isDeleted": False,
        "id": f"image_{generate_seed()}",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": "transparent",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "boundElements": [],
        "locked": False,
        "linkedNodes": None,
        "fileId": file_id,
        "scale": [1, 1],
        "crop": None,
        "originalURL": None,
        "url": None,
    }


def create_image_file(file_id, mime_type, data_url):
    """Create an Excalidraw file entry."""
    return {
        "id": file_id,
        "mimeType": mime_type,
        "dataURL": data_url,
        "created": 0,
        "lastRetrieved": 0,
    }


def main():
    args = parse_args()

    # Determine base directory
    base_dir = Path(__file__).parent.parent

    # Load layout template
    templates_dir = base_dir / "templates" / "excalidraw_layouts"
    layout = load_layout_template(args.layout, templates_dir)

    # Load color palette
    palettes_dir = base_dir / "templates" / "color_palettes"
    palette = load_color_palette(args.palette, palettes_dir)

    # Find asset files
    asset_files = glob.glob(args.assets)

    if not asset_files:
        print(f"Warning: No asset files found matching: {args.assets}", file=sys.stderr)

    # Map assets to sections by matching filename to section ID
    asset_map = {}
    for asset_path in asset_files:
        filename = Path(asset_path).stem.lower()

        # Try to match to section
        for section in layout.get("sections", []):
            section_id = section.get("id", "").lower()
            if section_id in filename or filename in section_id:
                asset_map[section["id"]] = asset_path
                break

    # Create elements
    elements = []
    files = {}
    y_offset = 0

    # Add title
    if args.title:
        title_element = create_text_element(
            x=50,
            y=30,
            width=600,
            height=50,
            text=args.title,
            font_size=32,
            font_weight="bold",
            stroke_color=palette.get("primary", "#1a1a2e"),
        )
        elements.append(title_element)

    # Add subtitle
    if args.subtitle:
        subtitle_element = create_text_element(
            x=50,
            y=70,
            width=600,
            height=30,
            text=args.subtitle,
            font_size=20,
            stroke_color=palette.get("secondary", "#16213e"),
        )
        elements.append(subtitle_element)

    # Process sections
    for section in layout.get("sections", []):
        section_type = section.get("type", "image")
        section_id = section.get("id", "")

        if section_type == "image":
            if section_id in asset_map:
                asset_path = asset_map[section_id]

                # Load image and create file entry
                file_id = f"file_{section_id}_{generate_seed()}"
                image_data = load_image_as_base64(asset_path)
                files[file_id] = create_image_file(file_id, "image/png", image_data)

                # Get dimensions from section or use defaults
                width = section.get("width", 400)
                height = section.get("height", 300)
                x = section.get("x", 50)
                y = section.get("y", 150) + y_offset

                # Create image element
                image_element = create_image_element(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    file_id=file_id,
                    image_data=image_data,
                )
                elements.append(image_element)

            # Add section label if not title/subtitle
            if section_id and section_id not in ["title", "subtitle"]:
                label_x = section.get("x", 50)
                label_y = section.get("y", 150) - 25 + y_offset
                label_text = section.get("label", section_id.replace("_", " ").title())

                label_element = create_text_element(
                    x=label_x,
                    y=label_y,
                    width=200,
                    height=20,
                    text=label_text,
                    font_size=14,
                    font_weight="bold",
                    stroke_color=palette.get("accent", "#0f3460"),
                )
                elements.append(label_element)

        elif section_type == "text":
            # Add text content
            text_content = section.get("content", "")
            if text_content:
                text_element = create_text_element(
                    x=section.get("x", 50),
                    y=section.get("y", 150),
                    width=section.get("width", 400),
                    height=section.get("height", 100),
                    text=text_content,
                    font_size=section.get("font_size", 14),
                )
                elements.append(text_element)

    # Create Excalidraw document
    excalidraw_doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "viewBackgroundColor": palette.get("background", "#ffffff"),
            "currentItemFontFamily": 1,
            "currentItemBackgroundColor": "transparent",
            "currentItemStrokeColor": palette.get("primary", "#1a1a2e"),
            "currentItemStrokeWidth": 1,
            "currentItemRoughness": 0,
            "currentItemOpacity": 100,
            "currentItemTextAlign": "left",
            "currentItemVerticalAlign": "top",
            "colorPalette": palette,
        },
        "files": files,
    }

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    with open(output_path, "w") as f:
        json.dump(excalidraw_doc, f, indent=2)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
