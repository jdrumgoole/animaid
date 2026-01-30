#!/usr/bin/env python3
"""Demo: Container Card

Demonstrates: HTMLCard for visual grouping with titles, shadows, and borders.

Shows:
- Cards with titles
- Shadow variations (default, elevated, none)
- Border and rounding options
- Card presets (default, elevated, outlined, flat, filled)
- Nested content in cards
"""

import time

from animaid import (
    Animate,
    HTMLCard,
    HTMLColumn,
    HTMLRow,
    HTMLString,
    RadiusSize,
    ShadowSize,
)


def main() -> None:
    print("Starting Container Card Demo...")
    print("Watch different card styles appear!")
    print()

    with Animate(title="Demo: HTMLCard") as anim:
        # Title
        title = HTMLString("HTMLCard Demo").bold().xxl()
        anim.add(title)
        anim.add(HTMLString("Visual grouping with titles, shadows, and borders").muted())

        time.sleep(0.5)

        # Section 1: Basic Cards
        anim.add(HTMLString("Basic Cards").bold().xl().styled(margin_top="20px"))

        row1 = HTMLRow([
            HTMLCard(
                title="Simple Card",
                children=[
                    HTMLString("A card with just a title and content."),
                ],
            ),
            HTMLCard(
                children=[
                    HTMLString("No Title").bold(),
                    HTMLString("Cards can also work without titles."),
                ],
            ),
        ]).gap(16)
        anim.add(row1)

        time.sleep(0.8)

        # Section 2: Shadow Variations
        anim.add(HTMLString("Shadow Variations").bold().xl().styled(margin_top="24px"))

        row2 = HTMLRow([
            HTMLCard(
                title="No Shadow",
                children=[HTMLString("ShadowSize.NONE")],
            ).shadow(ShadowSize.NONE).bordered(),
            HTMLCard(
                title="Small Shadow",
                children=[HTMLString("ShadowSize.SM")],
            ).shadow(ShadowSize.SM),
            HTMLCard(
                title="Default Shadow",
                children=[HTMLString("ShadowSize.DEFAULT")],
            ).shadow(ShadowSize.DEFAULT),
            HTMLCard(
                title="Large Shadow",
                children=[HTMLString("ShadowSize.LG")],
            ).shadow(ShadowSize.LG),
        ]).gap(16)
        anim.add(row2)

        time.sleep(0.8)

        # Section 3: Presets
        anim.add(HTMLString("Card Presets").bold().xl().styled(margin_top="24px"))

        row3 = HTMLRow([
            HTMLCard(
                title="Default",
                children=[HTMLString(".default() preset")],
            ).default(),
            HTMLCard(
                title="Elevated",
                children=[HTMLString(".elevated() preset")],
            ).elevated(),
            HTMLCard(
                title="Outlined",
                children=[HTMLString(".outlined() preset")],
            ).outlined(),
            HTMLCard(
                title="Flat",
                children=[HTMLString(".flat() preset")],
            ).flat().styled(background_color="#f5f5f5"),
        ]).gap(16)
        anim.add(row3)

        time.sleep(0.8)

        # Section 4: Filled Cards
        anim.add(HTMLString("Filled Cards").bold().xl().styled(margin_top="24px"))

        row4 = HTMLRow([
            HTMLCard(
                title="Light Gray",
                children=[HTMLString("Subtle background")],
            ).filled("#f9fafb"),
            HTMLCard(
                title="Blue Tint",
                children=[HTMLString("Info styling")],
            ).filled("#eff6ff"),
            HTMLCard(
                title="Green Tint",
                children=[HTMLString("Success styling")],
            ).filled("#f0fdf4"),
            HTMLCard(
                title="Red Tint",
                children=[HTMLString("Warning styling")],
            ).filled("#fef2f2"),
        ]).gap(16)
        anim.add(row4)

        time.sleep(0.8)

        # Section 5: Nested Content
        anim.add(HTMLString("Cards with Nested Content").bold().xl().styled(margin_top="24px"))

        stats_card = HTMLCard(
            title="User Statistics",
            children=[
                HTMLColumn([
                    HTMLRow([
                        HTMLString("Active Users").styled(color="#6b7280"),
                        HTMLString("1,234").bold(),
                    ]).spaced(),
                    HTMLRow([
                        HTMLString("New Signups").styled(color="#6b7280"),
                        HTMLString("56").bold(),
                    ]).spaced(),
                    HTMLRow([
                        HTMLString("Revenue").styled(color="#6b7280"),
                        HTMLString("$12,345").bold().styled(color="#22c55e"),
                    ]).spaced(),
                ]).gap(8),
            ],
        ).elevated().max_width(300)
        anim.add(stats_card)

        time.sleep(0.8)

        # Section 6: Rounded Corners
        anim.add(HTMLString("Border Radius Options").bold().xl().styled(margin_top="24px"))

        row5 = HTMLRow([
            HTMLCard(
                children=[HTMLString("RadiusSize.NONE")],
            ).rounded(RadiusSize.NONE).bordered(),
            HTMLCard(
                children=[HTMLString("RadiusSize.SM")],
            ).rounded(RadiusSize.SM).bordered(),
            HTMLCard(
                children=[HTMLString("RadiusSize.LG")],
            ).rounded(RadiusSize.LG).bordered(),
            HTMLCard(
                children=[HTMLString("RadiusSize.XL")],
            ).rounded(RadiusSize.XL).bordered(),
        ]).gap(16)
        anim.add(row5)

        print()
        print("Card demo complete!")
        print("The browser shows various HTMLCard styles and configurations.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
