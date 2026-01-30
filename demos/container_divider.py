#!/usr/bin/env python3
"""Demo: Container Divider

Demonstrates: HTMLDivider for visual separation of content.

Shows:
- Horizontal dividers (default)
- Dividers with labels
- Vertical dividers in rows
- Line styles (solid, dashed, dotted)
- Colors and thickness
- Presets (subtle, bold)
"""

import time

from animaid import (
    Animate,
    HTMLButton,
    HTMLCard,
    HTMLColumn,
    HTMLDivider,
    HTMLRow,
    HTMLSpacer,
    HTMLString,
)


def main() -> None:
    print("Starting Container Divider Demo...")
    print("Watch different divider styles appear!")
    print()

    with Animate(title="Demo: HTMLDivider") as anim:
        # Title
        title = HTMLString("HTMLDivider Demo").bold().xxl()
        anim.add(title)
        anim.add(HTMLString("Visual separators for content sections").muted())

        time.sleep(0.5)

        # Section 1: Basic Horizontal Divider
        anim.add(HTMLString("Basic Horizontal Divider").bold().xl().styled(margin_top="20px"))
        anim.add(HTMLString("Content above the divider"))
        anim.add(HTMLDivider())
        anim.add(HTMLString("Content below the divider"))

        time.sleep(0.8)

        # Section 2: Dividers with Labels
        anim.add(HTMLString("Dividers with Labels").bold().xl().styled(margin_top="24px"))

        anim.add(HTMLString("Use labeled dividers to indicate sections"))
        anim.add(HTMLDivider("OR"))
        anim.add(HTMLString("Alternative option below"))

        time.sleep(0.5)

        anim.add(HTMLDivider("SECTION BREAK"))

        time.sleep(0.8)

        # Section 3: Line Styles
        anim.add(HTMLString("Line Styles").bold().xl().styled(margin_top="24px"))

        style_column = HTMLColumn([
            HTMLRow([
                HTMLString("Solid (default)").styled(min_width="120px"),
                HTMLDivider().solid(),
            ]).align("center").gap(16),
            HTMLRow([
                HTMLString("Dashed").styled(min_width="120px"),
                HTMLDivider().dashed(),
            ]).align("center").gap(16),
            HTMLRow([
                HTMLString("Dotted").styled(min_width="120px"),
                HTMLDivider().dotted(),
            ]).align("center").gap(16),
        ]).gap(12).max_width(400)
        anim.add(style_column)

        time.sleep(0.8)

        # Section 4: Colors
        anim.add(HTMLString("Custom Colors").bold().xl().styled(margin_top="24px"))

        color_column = HTMLColumn([
            HTMLDivider().color("#3b82f6"),  # Blue
            HTMLDivider().color("#22c55e"),  # Green
            HTMLDivider().color("#ef4444"),  # Red
            HTMLDivider().color("#8b5cf6"),  # Purple
        ]).gap(8).max_width(400)
        anim.add(color_column)

        time.sleep(0.8)

        # Section 5: Thickness
        anim.add(HTMLString("Thickness Variations").bold().xl().styled(margin_top="24px"))

        thickness_column = HTMLColumn([
            HTMLRow([
                HTMLString("1px").styled(min_width="60px"),
                HTMLDivider().thickness(1),
            ]).align("center").gap(16),
            HTMLRow([
                HTMLString("2px").styled(min_width="60px"),
                HTMLDivider().thickness(2),
            ]).align("center").gap(16),
            HTMLRow([
                HTMLString("4px").styled(min_width="60px"),
                HTMLDivider().thickness(4),
            ]).align("center").gap(16),
        ]).gap(12).max_width(400)
        anim.add(thickness_column)

        time.sleep(0.8)

        # Section 6: Presets
        anim.add(HTMLString("Presets").bold().xl().styled(margin_top="24px"))

        preset_column = HTMLColumn([
            HTMLRow([
                HTMLString("Subtle").styled(min_width="80px"),
                HTMLDivider().subtle(),
            ]).align("center").gap(16),
            HTMLRow([
                HTMLString("Bold").styled(min_width="80px"),
                HTMLDivider().bold(),
            ]).align("center").gap(16),
        ]).gap(12).max_width(400)
        anim.add(preset_column)

        time.sleep(0.8)

        # Section 7: Vertical Dividers
        anim.add(HTMLString("Vertical Dividers (in Rows)").bold().xl().styled(margin_top="24px"))

        toolbar = HTMLRow([
            HTMLButton("File"),
            HTMLButton("Edit"),
            HTMLButton("View"),
            HTMLDivider().vertical(),
            HTMLButton("Cut"),
            HTMLButton("Copy"),
            HTMLButton("Paste"),
            HTMLDivider().vertical(),
            HTMLButton("Help"),
        ]).gap(8).styled(
            padding="8px 12px",
            background_color="#f5f5f5",
            border_radius="8px",
        )
        anim.add(toolbar)

        time.sleep(0.8)

        # Section 8: Real-world Example
        anim.add(HTMLString("Real-World Example: Login Form").bold().xl().styled(margin_top="24px"))

        login_card = HTMLCard(
            title="Sign In",
            children=[
                HTMLColumn([
                    HTMLString("[Email input placeholder]").styled(
                        padding="10px",
                        border="1px solid #ddd",
                        border_radius="4px",
                        background_color="white",
                    ),
                    HTMLString("[Password input placeholder]").styled(
                        padding="10px",
                        border="1px solid #ddd",
                        border_radius="4px",
                        background_color="white",
                    ),
                    HTMLButton("Sign In").primary().styled(width="100%"),
                    HTMLDivider("or continue with"),
                    HTMLRow([
                        HTMLButton("Google").styled(flex="1"),
                        HTMLButton("GitHub").styled(flex="1"),
                    ]).gap(8),
                ]).gap(12),
            ],
        ).shadow().max_width(320)
        anim.add(login_card)

        print()
        print("Divider demo complete!")
        print("The browser shows various HTMLDivider styles and use cases.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
