#!/usr/bin/env python3
"""Demo: Container Spacer

Demonstrates: HTMLSpacer for layout spacing control.

Shows:
- Fixed-size spacers (height, width)
- Flexible spacers that expand
- Size presets (xs, sm, md, lg, xl)
- Using spacers to push elements apart
- Spacers in rows and columns
"""

import time

from animaid import (
    App,
    HTMLButton,
    HTMLCard,
    HTMLColumn,
    HTMLRow,
    HTMLSpacer,
    HTMLString,
)


def main() -> None:
    print("Starting Container Spacer Demo...")
    print("Watch different spacer uses appear!")
    print()

    with App(title="Demo: HTMLSpacer") as app:
        # Title
        title = HTMLString("HTMLSpacer Demo").bold().xxl()
        app.add(title)
        app.add(HTMLString("Empty space for precise layout control").muted())

        time.sleep(0.5)

        # Section 1: Fixed Height Spacers
        app.add(HTMLString("Fixed Height Spacers").bold().xl().styled(margin_top="20px"))

        spacer_demo = HTMLCard(
            children=[
                HTMLColumn([
                    HTMLString("Content above").styled(
                        padding="8px",
                        background_color="#e0f2fe",
                        border_radius="4px",
                    ),
                    HTMLSpacer().height(40).styled(background_color="#fef3c7"),  # Yellow to visualize
                    HTMLString("40px spacer above (shown in yellow)").styled(
                        padding="8px",
                        background_color="#e0f2fe",
                        border_radius="4px",
                    ),
                ]),
            ],
        ).outlined()
        app.add(spacer_demo)

        time.sleep(0.8)

        # Section 2: Preset Sizes
        app.add(HTMLString("Size Presets").bold().xl().styled(margin_top="24px"))

        presets_card = HTMLCard(
            children=[
                HTMLColumn([
                    HTMLRow([
                        HTMLString(".xs() = 4px").styled(min_width="120px"),
                        HTMLSpacer().xs().styled(background_color="#fef3c7"),
                        HTMLString("↑").styled(color="#6b7280"),
                    ]).align("center"),
                    HTMLRow([
                        HTMLString(".sm() = 8px").styled(min_width="120px"),
                        HTMLSpacer().sm().styled(background_color="#fef3c7"),
                        HTMLString("↑").styled(color="#6b7280"),
                    ]).align("center"),
                    HTMLRow([
                        HTMLString(".md() = 16px").styled(min_width="120px"),
                        HTMLSpacer().md().styled(background_color="#fef3c7"),
                        HTMLString("↑").styled(color="#6b7280"),
                    ]).align("center"),
                    HTMLRow([
                        HTMLString(".lg() = 24px").styled(min_width="120px"),
                        HTMLSpacer().lg().styled(background_color="#fef3c7"),
                        HTMLString("↑").styled(color="#6b7280"),
                    ]).align("center"),
                    HTMLRow([
                        HTMLString(".xl() = 32px").styled(min_width="120px"),
                        HTMLSpacer().xl().styled(background_color="#fef3c7"),
                        HTMLString("↑").styled(color="#6b7280"),
                    ]).align("center"),
                ]).gap(4),
            ],
        ).outlined().max_width(350)
        app.add(presets_card)

        time.sleep(0.8)

        # Section 3: Flex Spacers (Push Apart)
        app.add(HTMLString("Flex Spacers (Push Apart)").bold().xl().styled(margin_top="24px"))
        app.add(HTMLString("Flex spacers expand to fill available space").muted())

        flex_demo = HTMLCard(
            children=[
                HTMLColumn([
                    HTMLString("Without flex spacer:").bold(),
                    HTMLRow([
                        HTMLButton("Left"),
                        HTMLButton("Right"),
                    ]).gap(8).styled(
                        padding="8px",
                        background_color="#f5f5f5",
                        border_radius="4px",
                    ),
                    HTMLSpacer().md(),
                    HTMLString("With flex spacer:").bold(),
                    HTMLRow([
                        HTMLButton("Left"),
                        HTMLSpacer().flex(),  # Pushes Right to the end
                        HTMLButton("Right"),
                    ]).styled(
                        padding="8px",
                        background_color="#f5f5f5",
                        border_radius="4px",
                    ),
                ]).gap(8),
            ],
        ).outlined()
        app.add(flex_demo)

        time.sleep(0.8)

        # Section 4: Multiple Flex Spacers
        app.add(HTMLString("Multiple Flex Spacers").bold().xl().styled(margin_top="24px"))

        multi_flex = HTMLCard(
            children=[
                HTMLColumn([
                    HTMLString("Two equal flex spacers center the middle button:").muted(),
                    HTMLRow([
                        HTMLSpacer().flex(),
                        HTMLButton("Centered").primary(),
                        HTMLSpacer().flex(),
                    ]).styled(
                        padding="8px",
                        background_color="#f5f5f5",
                        border_radius="4px",
                    ),
                    HTMLSpacer().md(),
                    HTMLString("Different flex values (1:2:1 ratio):").muted(),
                    HTMLRow([
                        HTMLSpacer().flex(1).styled(background_color="#fef3c7"),
                        HTMLString("Content").styled(padding="8px"),
                        HTMLSpacer().flex(2).styled(background_color="#dcfce7"),
                        HTMLString("More space →").styled(padding="8px"),
                        HTMLSpacer().flex(1).styled(background_color="#fef3c7"),
                    ]).styled(
                        padding="4px",
                        background_color="#f5f5f5",
                        border_radius="4px",
                    ),
                ]).gap(8),
            ],
        ).outlined()
        app.add(multi_flex)

        time.sleep(0.8)

        # Section 5: Real-World Header Example
        app.add(HTMLString("Real-World Example: Header Layout").bold().xl().styled(margin_top="24px"))

        header = HTMLRow([
            HTMLString("MyApp").bold().xl(),
            HTMLSpacer().width(32),  # Fixed gap after logo
            HTMLButton("Home"),
            HTMLButton("Products"),
            HTMLButton("About"),
            HTMLSpacer().flex(),  # Push user menu to the right
            HTMLButton("Login"),
            HTMLButton("Sign Up").primary(),
        ]).align("center").gap(8).styled(
            padding="12px 20px",
            background_color="#1f2937",
            border_radius="8px",
        )
        # Style text white
        app.add(header)

        time.sleep(0.8)

        # Section 6: Vertical Spacing in Columns
        app.add(HTMLString("Vertical Spacing in Columns").bold().xl().styled(margin_top="24px"))

        form_card = HTMLCard(
            title="Contact Form",
            children=[
                HTMLColumn([
                    HTMLString("Name").bold(),
                    HTMLString("[Name input]").styled(
                        padding="8px",
                        border="1px solid #ddd",
                        border_radius="4px",
                    ),
                    HTMLSpacer().md(),  # Extra space before next section
                    HTMLString("Email").bold(),
                    HTMLString("[Email input]").styled(
                        padding="8px",
                        border="1px solid #ddd",
                        border_radius="4px",
                    ),
                    HTMLSpacer().lg(),  # More space before button
                    HTMLRow([
                        HTMLSpacer().flex(),
                        HTMLButton("Submit").primary(),
                    ]),
                ]).gap(4),
            ],
        ).shadow().max_width(320)
        app.add(form_card)

        print()
        print("Spacer demo complete!")
        print("The browser shows various HTMLSpacer uses for layout control.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
