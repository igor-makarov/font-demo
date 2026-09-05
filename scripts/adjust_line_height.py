#!/usr/bin/env python3

"""Create a copy of a font with proportionally larger line spacing.

A font's recommended line height is the distance from its ascender to its
(usually negative) descender, plus a line gap:

    line height = ascender - descender + line gap

This script keeps the ascender and descender unchanged and adjusts only the
line gap. It updates both sets of vertical metrics that applications commonly
read from OpenType fonts.
"""

import argparse

from fontTools.ttLib import TTFont


DEFAULT_SCALE_FACTOR = 1.5


def scaled_line_gap(
    ascender: int,
    descender: int,
    line_gap: int,
    scale_factor: float,
) -> int:
    """Calculate the line gap needed to scale the total line height."""
    text_height = ascender - descender
    current_line_height = text_height + line_gap
    target_line_height = current_line_height * scale_factor

    return round(target_line_height - text_height)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_font", help="font file to read")
    parser.add_argument("output_font", help="adjusted font file to create")
    parser.add_argument(
        "--factor",
        dest="scale_factor",
        type=float,
        default=DEFAULT_SCALE_FACTOR,
        help=f"line-height multiplier (default: {DEFAULT_SCALE_FACTOR})",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    font = TTFont(arguments.input_font)

    # The hhea table contains the horizontal layout metrics used by many
    # applications, despite its name.
    horizontal_metrics = font["hhea"]
    horizontal_metrics.lineGap = scaled_line_gap(
        horizontal_metrics.ascent,
        horizontal_metrics.descent,
        horizontal_metrics.lineGap,
        arguments.scale_factor,
    )

    # The OS/2 table has a second set of typographic vertical metrics. It is
    # optional, so update it only when the input font provides it.
    if "OS/2" in font:
        typographic_metrics = font["OS/2"]
        typographic_metrics.sTypoLineGap = scaled_line_gap(
            typographic_metrics.sTypoAscender,
            typographic_metrics.sTypoDescender,
            typographic_metrics.sTypoLineGap,
            arguments.scale_factor,
        )

    font.save(arguments.output_font)


if __name__ == "__main__":
    main()