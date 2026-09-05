#!/usr/bin/env python3

import argparse
from fontTools.ttLib import TTFont


def new_line_gap(ascent, descent, old_gap, factor):
    # descent is normally negative
    current_height = ascent - descent + old_gap
    target_height = current_height * factor

    # Keep ascent/descent unchanged; put all extra space into lineGap
    return round(target_height - (ascent - descent))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--factor", type=float, default=1.5)
    args = parser.parse_args()

    font = TTFont(args.input)

    # hhea metrics
    hhea = font["hhea"]
    hhea.lineGap = new_line_gap(
        hhea.ascent,
        hhea.descent,
        hhea.lineGap,
        args.factor,
    )

    # OS/2 typographic metrics
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.sTypoLineGap = new_line_gap(
            os2.sTypoAscender,
            os2.sTypoDescender,
            os2.sTypoLineGap,
            args.factor,
        )

    font.save(args.output)


if __name__ == "__main__":
    main()