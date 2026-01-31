#!/usr/bin/env python3
"""
Example: Embed Google Fonts into an SVG file.

WHAT THIS SCRIPT DOES:
======================
This script demonstrates how to make an SVG file self-contained by embedding
external fonts directly into the SVG. This is essential for:

- Offline viewing: The SVG works without internet access
- Reliable rendering: Fonts display correctly on any system
- Portability: Share SVGs without worrying about font availability
- Email/PDF export: Embedded fonts render correctly in all contexts

HOW IT WORKS:
=============
1. The input SVG references Google Fonts via CSS @import rules
2. The svgfonts tool downloads the fonts from Google's servers
3. Fonts are converted to WOFF2 format (best compression)
4. Only the glyphs actually used in the SVG are included (subsetting)
5. The fonts are embedded as base64 data URIs in the SVG's <style> block

SUPPORTED FONT SOURCES:
=======================
- Google Fonts (fonts.googleapis.com)
- Adobe Fonts (use.typekit.net)
- Local system fonts
- Any HTTP/HTTPS font URL

Usage:
    # From the examples directory:
    python embed_google_fonts.py

    # Or from anywhere:
    python /path/to/examples/embed_google_fonts.py

Requirements:
    pip install svg-matrix    # or: uv add svg-matrix
    # Also requires Bun (recommended) or Node.js installed
"""

from pathlib import Path

# Import the svg-matrix Python wrapper functions
from svg_matrix import run_svgfonts, validate_svg


def main() -> None:
    """
    Demonstrate the complete font embedding workflow.

    This function shows the typical steps for embedding fonts:
    1. Validate the input SVG to ensure it's well-formed
    2. List fonts referenced in the SVG (for inspection)
    3. Embed the fonts with optimal settings
    4. Verify the output is valid
    5. Compare file sizes to see the trade-off
    6. Confirm the fonts are now embedded
    """
    # =========================================================================
    # SETUP: Define input and output paths
    # =========================================================================
    # Get the directory where this script is located
    script_dir = Path(__file__).parent

    # Input: SVG with Google Fonts loaded via @import
    input_svg = script_dir / "google_fonts_sample.svg"

    # Output: Self-contained SVG with embedded fonts
    output_svg = script_dir / "google_fonts_embedded.svg"

    print("=" * 60)
    print("SVG Font Embedding Example")
    print("=" * 60)

    # =========================================================================
    # STEP 1: Validate the input SVG
    # =========================================================================
    # Always validate before processing to catch malformed SVGs early.
    # The validate_svg() function checks for:
    # - Well-formed XML structure
    # - Valid SVG namespace
    # - Common SVG issues (missing viewBox, invalid attributes, etc.)
    print("\n1. Validating input SVG...")
    result = validate_svg(str(input_svg))
    if result["valid"]:
        print("   ✓ Input SVG is valid")
    else:
        # Print any issues found (doesn't stop processing)
        print(f"   ⚠ Warning: {result.get('issues', [])}")

    # =========================================================================
    # STEP 2: List fonts in the SVG
    # =========================================================================
    # The 'list' command shows all fonts referenced in the SVG.
    # This helps you understand what fonts will be downloaded.
    # Note: Fonts loaded via @import may not appear until embedding.
    print("\n2. Listing fonts in SVG...")
    list_result = run_svgfonts(["list", str(input_svg)])
    if list_result["returncode"] == 0:
        print(list_result["stdout"])
    else:
        print(f"   Error: {list_result['stderr']}")

    # =========================================================================
    # STEP 3: Embed fonts with optimal settings
    # =========================================================================
    # The 'embed' command downloads external fonts and embeds them.
    #
    # Key options:
    #   --woff2    Convert to WOFF2 format (~30% smaller than WOFF)
    #   --subset   Only include glyphs used in the SVG (much smaller)
    #   --full     Include ALL glyphs (larger, but supports dynamic text)
    #   --source   Prefer a specific source: google, local, fontget
    #   -o FILE    Write to output file (default: overwrite input)
    #
    # The tool automatically:
    #   - Detects @import and @font-face rules
    #   - Downloads fonts from Google Fonts, Adobe Fonts, etc.
    #   - Converts to optimal web format
    #   - Subsets to only include needed characters
    #   - Embeds as base64 data URIs
    print("\n3. Embedding fonts (with subsetting)...")
    embed_result = run_svgfonts(
        [
            "embed",
            "--woff2",  # WOFF2 format = best compression ratio
            "--subset",  # Only glyphs used = smallest file size
            "-o",
            str(output_svg),  # Write to new file (preserve original)
            str(input_svg),  # Input file to process
        ]
    )

    if embed_result["returncode"] == 0:
        print("   ✓ Fonts embedded successfully!")
        print(embed_result["stdout"])
    else:
        print(f"   ✗ Error embedding fonts: {embed_result['stderr']}")
        return

    # =========================================================================
    # STEP 4: Verify the output SVG is valid
    # =========================================================================
    # After processing, validate again to ensure nothing broke.
    print("\n4. Verifying output SVG...")
    result = validate_svg(str(output_svg))
    if result["valid"]:
        print("   ✓ Output SVG is valid")
    else:
        print(f"   ⚠ Warning: {result.get('issues', [])}")

    # =========================================================================
    # STEP 5: Compare file sizes
    # =========================================================================
    # Embedding fonts increases file size significantly.
    # This is the trade-off for portability.
    #
    # Typical size increase:
    #   - Small icon with 1 font: 2-10x larger
    #   - Document with 3 fonts: 100-500x larger
    #   - Subsetting reduces this significantly
    print("\n5. File size comparison:")
    input_size = input_svg.stat().st_size
    output_size = output_svg.stat().st_size
    print(f"   Input:  {input_size:>10,} bytes (references external fonts)")
    print(f"   Output: {output_size:>10,} bytes (fonts embedded)")
    print(f"   Ratio:  {output_size / input_size:>10.1f}x")

    # =========================================================================
    # STEP 6: Confirm fonts are embedded
    # =========================================================================
    # List fonts again - now they should show as "embedded" type
    # instead of external references.
    print("\n6. Fonts in embedded SVG:")
    list_result = run_svgfonts(["list", str(output_svg)])
    if list_result["returncode"] == 0:
        print(list_result["stdout"])

    # =========================================================================
    # DONE
    # =========================================================================
    print("\n" + "=" * 60)
    print("✓ Done! Embedded SVG saved to:")
    print(f"  {output_svg}")
    print("=" * 60)
    print("\nThe output SVG is now self-contained and works offline.")
    print("You can open it in any browser or vector editor.")


if __name__ == "__main__":
    main()
