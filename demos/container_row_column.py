#!/usr/bin/env python3
"""Demo: Container Row & Column

Demonstrates: HTMLRow and HTMLColumn for flexbox layouts.

Shows:
- Horizontal rows with gap and alignment
- Vertical columns with gap and alignment
- Row presets (buttons, toolbar, centered, spaced)
- Column presets (stack, form, centered)
- Nested layouts
- Wrapping behavior
"""

import time

from animaid import (
    AlignItems,
    App,
    HTMLButton,
    HTMLCard,
    HTMLColumn,
    HTMLRow,
    HTMLString,
    JustifyContent,
)


def main() -> None:
    print("Starting Container Row & Column Demo...")
    print("Watch flexbox layouts appear!")
    print()

    with App(title="Demo: HTMLRow & HTMLColumn") as app:
        # Title
        title = HTMLString("HTMLRow & HTMLColumn Demo").bold().xxl()
        app.add(title)
        app.add(HTMLString("Flexbox layouts for horizontal and vertical arrangement").muted())

        time.sleep(0.5)

        # Section 1: Basic Row
        app.add(HTMLString("Basic HTMLRow").bold().xl().styled(margin_top="20px"))

        basic_row = HTMLRow([
            HTMLString("Item 1").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
            HTMLString("Item 2").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            HTMLString("Item 3").styled(padding="8px", background_color="#fef3c7", border_radius="4px"),
        ]).gap(12).styled(
            padding="12px",
            background_color="#f5f5f5",
            border_radius="8px",
        )
        app.add(basic_row)

        time.sleep(0.8)

        # Section 2: Basic Column
        app.add(HTMLString("Basic HTMLColumn").bold().xl().styled(margin_top="24px"))

        basic_column = HTMLColumn([
            HTMLString("Item 1").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
            HTMLString("Item 2").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            HTMLString("Item 3").styled(padding="8px", background_color="#fef3c7", border_radius="4px"),
        ]).gap(12).styled(
            padding="12px",
            background_color="#f5f5f5",
            border_radius="8px",
            max_width="200px",
        )
        app.add(basic_column)

        time.sleep(0.8)

        # Section 3: Row Alignment
        app.add(HTMLString("Row Alignment Options").bold().xl().styled(margin_top="24px"))

        alignment_demo = HTMLColumn([
            HTMLString("justify: start (default)").muted(),
            HTMLRow([
                HTMLButton("A"), HTMLButton("B"), HTMLButton("C"),
            ]).justify(JustifyContent.START).styled(
                padding="8px", background_color="#f5f5f5", border_radius="4px",
            ),
            HTMLString("justify: center").muted(),
            HTMLRow([
                HTMLButton("A"), HTMLButton("B"), HTMLButton("C"),
            ]).justify(JustifyContent.CENTER).styled(
                padding="8px", background_color="#f5f5f5", border_radius="4px",
            ),
            HTMLString("justify: end").muted(),
            HTMLRow([
                HTMLButton("A"), HTMLButton("B"), HTMLButton("C"),
            ]).justify(JustifyContent.END).styled(
                padding="8px", background_color="#f5f5f5", border_radius="4px",
            ),
            HTMLString("justify: space-between").muted(),
            HTMLRow([
                HTMLButton("A"), HTMLButton("B"), HTMLButton("C"),
            ]).justify(JustifyContent.SPACE_BETWEEN).styled(
                padding="8px", background_color="#f5f5f5", border_radius="4px",
            ),
        ]).gap(8).max_width(400)
        app.add(alignment_demo)

        time.sleep(0.8)

        # Section 4: Vertical Alignment
        app.add(HTMLString("Vertical Alignment (align)").bold().xl().styled(margin_top="24px"))

        valign_demo = HTMLRow([
            HTMLColumn([
                HTMLString("start").muted(),
                HTMLRow([
                    HTMLString("Tall").styled(padding="20px 8px", background_color="#e0f2fe"),
                    HTMLString("Short").styled(padding="8px", background_color="#dcfce7"),
                ]).align(AlignItems.START).gap(4).styled(
                    padding="4px", background_color="#f5f5f5", height="80px",
                ),
            ]).gap(4),
            HTMLColumn([
                HTMLString("center").muted(),
                HTMLRow([
                    HTMLString("Tall").styled(padding="20px 8px", background_color="#e0f2fe"),
                    HTMLString("Short").styled(padding="8px", background_color="#dcfce7"),
                ]).align(AlignItems.CENTER).gap(4).styled(
                    padding="4px", background_color="#f5f5f5", height="80px",
                ),
            ]).gap(4),
            HTMLColumn([
                HTMLString("end").muted(),
                HTMLRow([
                    HTMLString("Tall").styled(padding="20px 8px", background_color="#e0f2fe"),
                    HTMLString("Short").styled(padding="8px", background_color="#dcfce7"),
                ]).align(AlignItems.END).gap(4).styled(
                    padding="4px", background_color="#f5f5f5", height="80px",
                ),
            ]).gap(4),
            HTMLColumn([
                HTMLString("stretch").muted(),
                HTMLRow([
                    HTMLString("Same").styled(padding="8px", background_color="#e0f2fe"),
                    HTMLString("Height").styled(padding="8px", background_color="#dcfce7"),
                ]).align(AlignItems.STRETCH).gap(4).styled(
                    padding="4px", background_color="#f5f5f5", height="80px",
                ),
            ]).gap(4),
        ]).gap(16)
        app.add(valign_demo)

        time.sleep(0.8)

        # Section 5: Row Presets
        app.add(HTMLString("Row Presets").bold().xl().styled(margin_top="24px"))

        presets_card = HTMLCard(
            children=[
                HTMLColumn([
                    HTMLString(".buttons() - Right-aligned button row").muted(),
                    HTMLRow([
                        HTMLButton("Cancel"),
                        HTMLButton("Save").primary(),
                    ]).buttons(),

                    HTMLString(".toolbar() - Compact toolbar").muted(),
                    HTMLRow([
                        HTMLButton("New"),
                        HTMLButton("Open"),
                        HTMLButton("Save"),
                    ]).toolbar().styled(background_color="#e5e7eb", border_radius="4px"),

                    HTMLString(".centered() - Center all items").muted(),
                    HTMLRow([
                        HTMLButton("Centered Button"),
                    ]).centered().styled(background_color="#f5f5f5", padding="16px"),

                    HTMLString(".spaced() - Space between items").muted(),
                    HTMLRow([
                        HTMLString("Left"),
                        HTMLString("Center"),
                        HTMLString("Right"),
                    ]).spaced().styled(background_color="#f5f5f5", padding="8px"),
                ]).gap(16),
            ],
        ).outlined()
        app.add(presets_card)

        time.sleep(0.8)

        # Section 6: Column Presets
        app.add(HTMLString("Column Presets").bold().xl().styled(margin_top="24px"))

        col_presets = HTMLRow([
            HTMLCard(
                title=".stack()",
                children=[
                    HTMLColumn([
                        HTMLString("Item 1"),
                        HTMLString("Item 2"),
                        HTMLString("Item 3"),
                    ]).stack(),
                ],
            ).outlined(),
            HTMLCard(
                title=".form()",
                children=[
                    HTMLColumn([
                        HTMLString("Label 1"),
                        HTMLString("[Input 1]").styled(
                            padding="6px", border="1px solid #ddd", border_radius="4px",
                        ),
                        HTMLString("Label 2"),
                        HTMLString("[Input 2]").styled(
                            padding="6px", border="1px solid #ddd", border_radius="4px",
                        ),
                    ]).form(),
                ],
            ).outlined(),
            HTMLCard(
                title=".centered()",
                children=[
                    HTMLColumn([
                        HTMLString("Centered"),
                        HTMLString("Content"),
                    ]).centered().height(100),
                ],
            ).outlined(),
        ]).gap(16)
        app.add(col_presets)

        time.sleep(0.8)

        # Section 7: Nested Layouts
        app.add(HTMLString("Nested Layouts").bold().xl().styled(margin_top="24px"))

        nested = HTMLCard(
            title="Dashboard Layout",
            children=[
                HTMLColumn([
                    # Header row
                    HTMLRow([
                        HTMLString("Dashboard").bold().xl(),
                        HTMLString("Welcome back!").muted(),
                    ]).spaced().styled(padding_bottom="12px", border_bottom="1px solid #e5e7eb"),

                    # Content area: sidebar + main
                    HTMLRow([
                        # Sidebar
                        HTMLColumn([
                            HTMLString("Navigation").bold(),
                            HTMLString("Home"),
                            HTMLString("Profile"),
                            HTMLString("Settings"),
                        ]).gap(4).styled(
                            padding="12px",
                            background_color="#f9fafb",
                            border_radius="4px",
                            min_width="120px",
                        ),

                        # Main content
                        HTMLColumn([
                            HTMLString("Main Content").bold(),
                            HTMLString("This is the main content area with nested row/column layouts."),
                            HTMLRow([
                                HTMLCard(children=[HTMLString("Card 1")]).filled("#eff6ff"),
                                HTMLCard(children=[HTMLString("Card 2")]).filled("#f0fdf4"),
                            ]).gap(8),
                        ]).gap(8).styled(flex="1"),
                    ]).gap(16),

                    # Footer
                    HTMLRow([
                        HTMLString("Footer content").muted(),
                    ]).styled(padding_top="12px", border_top="1px solid #e5e7eb"),
                ]).gap(16),
            ],
        ).shadow()
        app.add(nested)

        print()
        print("Row & Column demo complete!")
        print("The browser shows various flexbox layout patterns.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
