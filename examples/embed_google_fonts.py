#!/usr/bin/env python3
"""
Example: Embed Google Fonts into an SVG file.

This script demonstrates how to use the svg-matrix Python wrapper to:
1. List fonts used in an SVG
2. Embed external fonts (including Google Fonts) into the SVG
3. Verify the embedding was successful

The resulting SVG will be self-contained and work offline.

Usage:
    python embed_google_fonts.py

Requirements:
    pip install svg-matrix
    # Also requires Bun or Node.js installed
"""

from pathlib import Path

from svg_matrix import run_svgfonts, validate_svg


def main() -> None:
    """Demonstrate font embedding workflow."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    input_svg = script_dir / "google_fonts_sample.svg"
    output_svg = script_dir / "google_fonts_embedded.svg"

    print("=" * 60)
    print("SVG Font Embedding Example")
    print("=" * 60)

    # Step 1: Validate the input SVG
    print("\n1. Validating input SVG...")
    result = validate_svg(str(input_svg))
    if result["valid"]:
        print("   Input SVG is valid")
    else:
        print(f"   Warning: {result.get('issues', [])}")

    # Step 2: List fonts in the SVG
    print("\n2. Listing fonts in SVG...")
    list_result = run_svgfonts(["list", str(input_svg)])
    if list_result["returncode"] == 0:
        print(list_result["stdout"])
    else:
        print(f"   Error: {list_result['stderr']}")

    # Step 3: Embed fonts with subsetting (only includes glyphs used)
    print("\n3. Embedding fonts (with subsetting)...")
    embed_result = run_svgfonts([
        "embed",
        "--woff2",           # Use WOFF2 compression for smaller size
        "--subset",          # Only embed glyphs actually used (default)
        "-o", str(output_svg),
        str(input_svg),
    ])

    if embed_result["returncode"] == 0:
        print("   Fonts embedded successfully!")
        print(embed_result["stdout"])
    else:
        print(f"   Error embedding fonts: {embed_result['stderr']}")
        return

    # Step 4: Verify the output
    print("\n4. Verifying output SVG...")
    result = validate_svg(str(output_svg))
    if result["valid"]:
        print("   Output SVG is valid")
    else:
        print(f"   Warning: {result.get('issues', [])}")

    # Step 5: Compare file sizes
    print("\n5. File size comparison:")
    input_size = input_svg.stat().st_size
    output_size = output_svg.stat().st_size
    print(f"   Input:  {input_size:,} bytes")
    print(f"   Output: {output_size:,} bytes")
    print(f"   Ratio:  {output_size / input_size:.1f}x")

    # Step 6: List fonts in the embedded SVG (should show embedded fonts)
    print("\n6. Fonts in embedded SVG:")
    list_result = run_svgfonts(["list", str(output_svg)])
    if list_result["returncode"] == 0:
        print(list_result["stdout"])

    print("\n" + "=" * 60)
    print(f"Done! Embedded SVG saved to: {output_svg}")
    print("=" * 60)


if __name__ == "__main__":
    main()
