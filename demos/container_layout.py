#!/usr/bin/env python3
"""Demo: Container Layout

Demonstrates container widgets for organizing layouts:
- HTMLRow and HTMLColumn for flexbox layouts
- HTMLCard for visual grouping with titles and shadows
- HTMLDivider for separating content
- HTMLSpacer for flexible spacing
"""

import time

from animaid import (
    AlignItems,
    Animate,
    HTMLButton,
    HTMLCard,
    HTMLColumn,
    HTMLDivider,
    HTMLRow,
    HTMLSpacer,
    HTMLString,
    JustifyContent,
)


def main() -> None:
    with Animate(title="Container Layout Demo") as anim:
        # Title
        title = HTMLString("Container Layout Demo").bold().styled(font_size="24px")
        anim.add(title)

        # Horizontal row of buttons
        anim.add(HTMLString("Button Row:").styled(margin_top="20px"))
        button_row = HTMLRow([
            HTMLButton("Save").primary(),
            HTMLButton("Cancel"),
            HTMLButton("Delete").danger(),
        ]).gap(10).align(AlignItems.CENTER)
        anim.add(button_row)

        time.sleep(1)

        # Spaced row (items pushed apart)
        anim.add(HTMLString("Spaced Row:").styled(margin_top="20px"))
        spaced_row = HTMLRow([
            HTMLString("Left").bold(),
            HTMLString("Center"),
            HTMLString("Right").bold(),
        ]).spaced().styled(
            padding="10px",
            background_color="#f0f0f0",
            border_radius="8px",
        )
        anim.add(spaced_row)

        time.sleep(1)

        # Vertical column
        anim.add(HTMLString("Vertical Column:").styled(margin_top="20px"))
        column = HTMLColumn([
            HTMLString("Title").bold().styled(font_size="18px"),
            HTMLString("Subtitle").styled(color="gray"),
            HTMLString("This is the main content of the column."),
        ]).gap(8).styled(
            padding="16px",
            background_color="#e8f4fc",
            border_radius="8px",
        )
        anim.add(column)

        time.sleep(1)

        # Nested layout: Row containing Columns
        anim.add(HTMLString("Nested Layout (Row with Columns):").styled(margin_top="20px"))

        left_column = HTMLColumn([
            HTMLString("Left Panel").bold(),
            HTMLString("Item 1"),
            HTMLString("Item 2"),
            HTMLString("Item 3"),
        ]).gap(4).styled(
            padding="12px",
            background_color="#fff3e0",
            border_radius="8px",
            min_width="150px",
        )

        right_column = HTMLColumn([
            HTMLString("Right Panel").bold(),
            HTMLString("Description goes here."),
            HTMLString("More content below."),
        ]).gap(4).styled(
            padding="12px",
            background_color="#e8f5e9",
            border_radius="8px",
            min_width="150px",
        )

        nested_row = HTMLRow([left_column, right_column]).gap(16)
        anim.add(nested_row)

        time.sleep(1)

        # Divider example
        anim.add(HTMLDivider("Container Widgets"))

        time.sleep(1)

        # Card examples
        anim.add(HTMLString("HTMLCard Examples:").styled(margin_top="10px"))
        card_row = HTMLRow([
            HTMLCard(
                title="Default Card",
                children=[HTMLString("With title and default styling.")],
            ).default(),
            HTMLCard(
                title="Elevated Card",
                children=[HTMLString("Prominent shadow for emphasis.")],
            ).elevated(),
            HTMLCard(
                title="Outlined Card",
                children=[HTMLString("Border only, no shadow.")],
            ).outlined(),
        ]).gap(16)
        anim.add(card_row)

        time.sleep(1)

        # Spacer example
        anim.add(HTMLString("HTMLSpacer Example (flex spacer):").styled(margin_top="20px"))
        spacer_row = HTMLRow([
            HTMLButton("Left"),
            HTMLSpacer().flex(),  # Takes remaining space
            HTMLButton("Right").primary(),
        ]).styled(
            padding="10px",
            background_color="#f0f0f0",
            border_radius="8px",
        )
        anim.add(spacer_row)

        time.sleep(1)

        # Toolbar with divider
        anim.add(HTMLString("Toolbar with Vertical Divider:").styled(margin_top="20px"))
        toolbar = HTMLRow([
            HTMLButton("New").primary(),
            HTMLButton("Open"),
            HTMLButton("Save"),
            HTMLDivider().vertical(),
            HTMLButton("Cut"),
            HTMLButton("Copy"),
            HTMLButton("Paste"),
            HTMLSpacer().flex(),
            HTMLButton("Help"),
        ]).toolbar().styled(
            background_color="#333",
            border_radius="4px",
        )
        anim.add(toolbar)

        time.sleep(1)

        # Form in a card
        anim.add(HTMLString("Form Layout in Card:").styled(margin_top="20px"))
        form = HTMLCard(
            title="Create Account",
            children=[
                HTMLColumn([
                    HTMLString("Username").bold(),
                    HTMLString("[text input]").styled(
                        padding="8px",
                        border="1px solid #ccc",
                        border_radius="4px",
                        background_color="white",
                    ),
                    HTMLSpacer().sm(),
                    HTMLString("Password").bold(),
                    HTMLString("[password input]").styled(
                        padding="8px",
                        border="1px solid #ccc",
                        border_radius="4px",
                        background_color="white",
                    ),
                    HTMLSpacer().md(),
                    HTMLRow([
                        HTMLButton("Cancel"),
                        HTMLSpacer().flex(),
                        HTMLButton("Submit").primary(),
                    ]),
                ]).form(),
            ],
        ).shadow().max_width(300)
        anim.add(form)

        print("\nContainer layout demo complete!")
        print("The browser shows various container layouts.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
