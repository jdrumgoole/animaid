#!/usr/bin/env python3
"""Demo: Button Showcase

Demonstrates: HTMLButton styles, sizes, and click event handling
"""

import time

from animaid import Animate, HTMLButton, HTMLString


def main() -> None:
    """Run the button showcase demo."""
    with Animate(title="Demo: Button Showcase") as anim:
        # Title
        title = HTMLString("Button Showcase").bold().xl()
        anim.add(title)

        # Click counter display
        click_count = 0
        last_clicked = HTMLString("Click any button to see events").muted()
        anim.add(last_clicked, id="status")

        counter_display = HTMLString(f"Total clicks: {click_count}").bold()
        anim.add(counter_display, id="counter")

        # Section: Button Styles
        anim.add(HTMLString("Button Styles").bold().large())

        def make_click_handler(style_name: str):
            def handler() -> None:
                nonlocal click_count
                click_count += 1
                last_clicked._value = f"Clicked: {style_name} button"
                counter_display._value = f"Total clicks: {click_count}"
                anim.refresh("status")
                anim.refresh("counter")
                print(f"[{click_count}] {style_name} button clicked")
            return handler

        # Default button
        default_btn = HTMLButton("Default").on_click(make_click_handler("Default"))
        anim.add(default_btn)

        # Primary button
        primary_btn = HTMLButton("Primary").primary().on_click(
            make_click_handler("Primary")
        )
        anim.add(primary_btn)

        # Success button
        success_btn = HTMLButton("Success").success().on_click(
            make_click_handler("Success")
        )
        anim.add(success_btn)

        # Warning button
        warning_btn = HTMLButton("Warning").warning().on_click(
            make_click_handler("Warning")
        )
        anim.add(warning_btn)

        # Danger button
        danger_btn = HTMLButton("Danger").danger().on_click(
            make_click_handler("Danger")
        )
        anim.add(danger_btn)

        # Section: Button Sizes
        anim.add(HTMLString("Button Sizes").bold().large())

        small_btn = HTMLButton("Small").small().primary().on_click(
            make_click_handler("Small")
        )
        anim.add(small_btn)

        normal_btn = HTMLButton("Normal").primary().on_click(
            make_click_handler("Normal")
        )
        anim.add(normal_btn)

        large_btn = HTMLButton("Large").large().primary().on_click(
            make_click_handler("Large")
        )
        anim.add(large_btn)

        # Section: Action Buttons
        anim.add(HTMLString("Action Buttons").bold().large())

        def reset_counter() -> None:
            nonlocal click_count
            click_count = 0
            last_clicked._value = "Counter reset!"
            counter_display._value = f"Total clicks: {click_count}"
            anim.refresh("status")
            anim.refresh("counter")
            print("Counter reset to 0")

        reset_btn = HTMLButton("Reset Counter").danger().on_click(reset_counter)
        anim.add(reset_btn)

        print("Button Showcase Demo")
        print("=" * 40)
        print("Click the buttons to see different styles and sizes.")
        print("Watch the click counter update in real-time!")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
