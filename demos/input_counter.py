#!/usr/bin/env python3
"""Demo: Interactive Counter

Demonstrates: HTMLButton, event polling with wait_for_event(), on_click callbacks
"""

from animaid import Animate, HTMLButton, HTMLString


def main() -> None:
    """Run the interactive counter demo."""
    with Animate(title="Demo: Interactive Counter") as anim:
        count = 0

        # Display
        display = HTMLString(str(count)).xxl().bold()
        anim.add(display, id="display")

        # Increment button
        def increment() -> None:
            nonlocal count
            count += 1
            display._value = str(count)
            anim.refresh("display")
            print(f"Count: {count}")

        inc_button = HTMLButton("+").primary().large().on_click(increment)
        anim.add(inc_button)

        # Decrement button
        def decrement() -> None:
            nonlocal count
            count -= 1
            display._value = str(count)
            anim.refresh("display")
            print(f"Count: {count}")

        dec_button = HTMLButton("-").danger().large().on_click(decrement)
        anim.add(dec_button)

        # Reset button
        def reset() -> None:
            nonlocal count
            count = 0
            display._value = str(count)
            anim.refresh("display")
            print("Count reset to 0")

        reset_button = HTMLButton("Reset").warning().on_click(reset)
        anim.add(reset_button)

        print("Interactive Counter Demo")
        print("=" * 40)
        print("Click + to increment, - to decrement, Reset to reset.")
        print()

        # Event loop
        try:
            while True:
                event = anim.wait_for_event(timeout=0.1)
                if event:
                    # Events are handled by callbacks, but we can also log them
                    pass
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
