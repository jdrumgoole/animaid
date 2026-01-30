"""Demo: Window Theme Switching

Demonstrates the window theming capabilities of AnimAID.
Shows how to toggle between light and dark themes dynamically.
"""

import time

from animaid import App, HTMLButton, HTMLString, WindowConfig
from animaid.containers import HTMLCard, HTMLColumn, HTMLRow


def main() -> None:
    """Run the theme switching demo."""
    # Start with dark theme
    with App(title="Theme Demo", theme="dark") as app:
        # Create header
        header = HTMLString("Theme Demo").bold().font_size("24px")
        app.add(header)

        # Create theme toggle button
        toggle_btn = HTMLButton("Switch to Light Theme", variant="primary")
        app.add(toggle_btn)

        # Create sample content to show theme
        content = HTMLColumn([
            HTMLString("This is sample content that demonstrates the theme."),
            HTMLString("The colors will change when you toggle themes.").italic(),
            HTMLCard(
                title="Sample Card",
                children=[
                    HTMLString("Cards also respect the theme settings."),
                    HTMLString("Notice how the background and text colors adapt."),
                ]
            ),
        ]).gap(12).padding(16)
        app.add(content)

        # Theme state
        is_dark = True

        # Wait for events
        print("Theme demo running. Click the button to toggle themes.")
        print("Press Ctrl+C to exit.")

        try:
            while True:
                event = app.wait_for_event(timeout=0.5)
                if event and event.event_type == "click":
                    is_dark = not is_dark
                    if is_dark:
                        app.window.dark()
                        toggle_btn._label = "Switch to Light Theme"
                        app.refresh(toggle_btn._anim_id)
                    else:
                        app.window.light()
                        toggle_btn._label = "Switch to Dark Theme"
                        app.refresh(toggle_btn._anim_id)
        except KeyboardInterrupt:
            print("\nDemo stopped.")


if __name__ == "__main__":
    main()
