#!/usr/bin/env python3
"""Demo: Select Dropdown Showcase

Demonstrates: HTMLSelect with selection handling, dynamic updates, and styling options
"""

import time

from animaid import App, HTMLSelect, HTMLString


def main() -> None:
    """Run the select dropdown showcase demo."""
    with App(title="Demo: Select Dropdown Showcase") as app:
        # Title
        title = HTMLString("Select Dropdown Showcase").bold().xl()
        app.add(title)

        # Section 1: Basic Selection with Display
        app.add(HTMLString("Basic Selection").bold().large())
        app.add(HTMLString("Choose a color to see it displayed:").muted())

        color_display = HTMLString("Selected: Red").monospace()
        app.add(color_display, id="color_display")

        color_preview = HTMLString("Sample Text")
        app.add(color_preview, id="color_preview")

        def on_color_change(value: str) -> None:
            color_display._value = f"Selected: {value}"
            color_map = {
                "Red": "#ef4444",
                "Green": "#22c55e",
                "Blue": "#3b82f6",
                "Purple": "#a855f7",
                "Orange": "#f97316",
            }
            color = color_map.get(value, "#1e293b")
            color_preview._styles = {"color": color, "font-weight": "bold"}
            app.refresh("color_display")
            app.refresh("color_preview")
            print(f"Color selected: {value}")

        color_select = HTMLSelect(
            options=["Red", "Green", "Blue", "Purple", "Orange"]
        ).on_change(on_color_change)
        app.add(color_select)

        # Initialize preview color
        color_preview._styles = {"color": "#ef4444", "font-weight": "bold"}

        # Section 2: Size Selector
        app.add(HTMLString("Size Selector").bold().large())

        size_display = HTMLString("Font size: 16px").monospace()
        app.add(size_display, id="size_display")

        size_sample = HTMLString("This text changes size")
        app.add(size_sample, id="size_sample")

        def on_size_change(value: str) -> None:
            size_map = {
                "Small": "12px",
                "Medium": "16px",
                "Large": "20px",
                "Extra Large": "28px",
            }
            px_size = size_map.get(value, "16px")
            size_display._value = f"Font size: {px_size}"
            size_sample._styles = {"font-size": px_size}
            app.refresh("size_display")
            app.refresh("size_sample")
            print(f"Size selected: {value} ({px_size})")

        size_select = HTMLSelect(
            options=["Small", "Medium", "Large", "Extra Large"], value="Medium"
        ).on_change(on_size_change)
        app.add(size_select)

        # Section 3: Country Selector with Flag
        app.add(HTMLString("Country Selector").bold().large())

        country_info = HTMLString("USA - United States of America").monospace()
        app.add(country_info, id="country_info")

        country_data = {
            "USA": {"name": "United States of America", "capital": "Washington, D.C."},
            "UK": {"name": "United Kingdom", "capital": "London"},
            "France": {"name": "France", "capital": "Paris"},
            "Germany": {"name": "Germany", "capital": "Berlin"},
            "Japan": {"name": "Japan", "capital": "Tokyo"},
            "Australia": {"name": "Australia", "capital": "Canberra"},
        }

        def on_country_change(value: str) -> None:
            info = country_data.get(value, {})
            country_info._value = (
                f"{value} - {info.get('name', '')}\nCapital: {info.get('capital', '')}"
            )
            app.refresh("country_info")
            print(f"Country selected: {value}")

        country_select = HTMLSelect(
            options=["USA", "UK", "France", "Germany", "Japan", "Australia"]
        ).wide().on_change(on_country_change)
        app.add(country_select)

        # Section 4: Select Sizes
        app.add(HTMLString("Select Sizes").bold().large())

        small_select = HTMLSelect(options=["Small Option 1", "Small Option 2"]).small()
        app.add(small_select)

        normal_select = HTMLSelect(options=["Normal Option 1", "Normal Option 2"])
        app.add(normal_select)

        large_select = HTMLSelect(options=["Large Option 1", "Large Option 2"]).large()
        app.add(large_select)

        wide_select = HTMLSelect(
            options=["Wide Option (Full Width)"]
        ).wide()
        app.add(wide_select)

        # Section 5: Pre-selected Value
        app.add(HTMLString("Pre-selected Value").bold().large())

        preselected = HTMLSelect(
            options=["First", "Second", "Third", "Fourth"], value="Third"
        )
        app.add(preselected)

        value_display = HTMLString(f"Current value: {preselected.value}").monospace()
        app.add(value_display, id="preselected_value")

        def show_preselected_value(value: str) -> None:
            value_display._value = f"Current value: {value}"
            app.refresh("preselected_value")

        preselected.on_change(show_preselected_value)

        print("Select Dropdown Showcase Demo")
        print("=" * 40)
        print("Try selecting different options from the dropdowns.")
        print("Watch the live updates and styling changes!")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
