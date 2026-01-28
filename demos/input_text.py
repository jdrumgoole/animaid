#!/usr/bin/env python3
"""Demo: Text Input Showcase

Demonstrates: HTMLTextInput with live typing feedback, character counting, and validation
"""

import time

from animaid import Animate, HTMLString, HTMLTextInput


def main() -> None:
    """Run the text input showcase demo."""
    with Animate(title="Demo: Text Input Showcase") as anim:
        # Title
        title = HTMLString("Text Input Showcase").bold().xl()
        anim.add(title)

        # Section 1: Live Character Counter
        anim.add(HTMLString("Live Character Counter").bold().large())
        anim.add(HTMLString("Type to see the character count update:").muted())

        char_count = HTMLString("Characters: 0").monospace()
        anim.add(char_count, id="char_count")

        def on_text_change(value: str) -> None:
            count = len(value)
            char_count._value = f"Characters: {count}"
            if count > 50:
                char_count._styles = {"color": "red", "font-weight": "bold"}
            elif count > 30:
                char_count._styles = {"color": "orange"}
            else:
                char_count._styles = {"color": "green"}
            anim.refresh("char_count")
            print(f"Text: '{value}' ({count} chars)")

        text_input = HTMLTextInput(
            placeholder="Type something here..."
        ).wide().on_change(on_text_change)
        anim.add(text_input)

        # Section 2: Live Mirror
        anim.add(HTMLString("Live Mirror").bold().large())
        anim.add(HTMLString("What you type appears below in real-time:").muted())

        mirror_display = HTMLString("(Your text will appear here)").italic().muted()
        anim.add(mirror_display, id="mirror")

        def mirror_text(value: str) -> None:
            if value:
                mirror_display._value = value
                mirror_display._styles = {
                    "font-style": "normal",
                    "color": "#2563eb",
                    "font-size": "1.25em",
                }
            else:
                mirror_display._value = "(Your text will appear here)"
                mirror_display._styles = {"font-style": "italic", "color": "#6b7280"}
            anim.refresh("mirror")

        mirror_input = HTMLTextInput(
            placeholder="Type to see live mirroring..."
        ).wide().on_change(mirror_text)
        anim.add(mirror_input)

        # Section 3: Input Sizes
        anim.add(HTMLString("Input Sizes").bold().large())

        small_input = HTMLTextInput(placeholder="Small input").small()
        anim.add(small_input)

        normal_input = HTMLTextInput(placeholder="Normal input")
        anim.add(normal_input)

        large_input = HTMLTextInput(placeholder="Large input").large()
        anim.add(large_input)

        wide_input = HTMLTextInput(placeholder="Wide input (full width)").wide()
        anim.add(wide_input)

        # Section 4: Pre-filled Value
        anim.add(HTMLString("Pre-filled Input").bold().large())

        prefilled = HTMLTextInput(value="This input has a default value")
        anim.add(prefilled)

        value_display = HTMLString(f"Current value: {prefilled.value}").monospace()
        anim.add(value_display, id="prefilled_value")

        def show_prefilled_value(value: str) -> None:
            value_display._value = f"Current value: {value}"
            anim.refresh("prefilled_value")

        prefilled.on_change(show_prefilled_value)

        print("Text Input Showcase Demo")
        print("=" * 40)
        print("Try typing in the various text inputs.")
        print("Watch the live updates and character counting!")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
