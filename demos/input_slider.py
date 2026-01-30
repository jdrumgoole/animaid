#!/usr/bin/env python3
"""Demo: Color Mixer with Sliders

Demonstrates: HTMLSlider, on_change callbacks, real-time updates
"""

import time

from animaid import App, HTMLSlider, HTMLString


def main() -> None:
    """Run the color mixer demo with sliders."""
    with App(title="Demo: RGB Color Mixer") as app:
        # Title
        title = HTMLString("RGB Color Mixer").bold().xl()
        app.add(title)

        # Color preview box
        color_preview = HTMLString("Color Preview").styled(
            background_color="rgb(128, 128, 128)",
            padding="40px",
            text_align="center",
            border_radius="8px",
            color="white",
            font_weight="bold",
        )
        app.add(color_preview, id="preview")

        # RGB values
        r_value, g_value, b_value = 128, 128, 128

        def update_color() -> None:
            color = f"rgb({r_value}, {g_value}, {b_value})"
            # Determine text color based on brightness
            brightness = (r_value * 299 + g_value * 587 + b_value * 114) / 1000
            text_color = "black" if brightness > 128 else "white"

            color_preview._value = f"RGB({r_value}, {g_value}, {b_value})"
            color_preview._styles["background-color"] = color
            color_preview._styles["color"] = text_color
            app.refresh("preview")

        # Red slider
        app.add(HTMLString("Red:").bold().red())

        def on_red_change(value: float) -> None:
            nonlocal r_value
            r_value = int(value)
            update_color()

        red_slider = HTMLSlider(min=0, max=255, value=128).wide().on_change(
            on_red_change
        )
        app.add(red_slider)

        # Green slider
        app.add(HTMLString("Green:").bold().green())

        def on_green_change(value: float) -> None:
            nonlocal g_value
            g_value = int(value)
            update_color()

        green_slider = HTMLSlider(min=0, max=255, value=128).wide().on_change(
            on_green_change
        )
        app.add(green_slider)

        # Blue slider
        app.add(HTMLString("Blue:").bold().blue())

        def on_blue_change(value: float) -> None:
            nonlocal b_value
            b_value = int(value)
            update_color()

        blue_slider = HTMLSlider(min=0, max=255, value=128).wide().on_change(
            on_blue_change
        )
        app.add(blue_slider)

        print("RGB Color Mixer Demo")
        print("=" * 40)
        print("Move the sliders to mix colors!")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
