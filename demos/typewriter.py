#!/usr/bin/env python3
"""Demo: Typewriter Effect

Demonstrates: Styling changes trigger updates on immutable types, chained methods.

Shows how:
- Building up text character by character
- Applying styles one by one (bold, color, size, background)
- Each style change requires creating a new HTMLString
"""

import time

from animaid import Animate, HTMLString


def main() -> None:
    print("Starting Typewriter Demo...")
    print("Watch the message appear character by character, then get styled!")
    print()

    with Animate(title="Demo: Typewriter Effect") as anim:
        # Title
        title = HTMLString("Typewriter Effect").bold().xxl()
        anim.add(title)

        # The message to type out
        message = "Hello, AnimAID!"

        # Start with empty text
        text = HTMLString("").large()
        text_id = anim.add(text)

        time.sleep(0.5)

        # Type out the message character by character
        print("Typing message:")
        current = ""
        for char in message:
            current += char
            text = HTMLString(current).large()
            anim.update(text_id, text)
            print(f"  '{current}'")
            time.sleep(0.1)

        print()
        time.sleep(0.5)

        # Now apply styles one by one
        print("Applying styles:")

        # 1. Make bold
        print("  + bold")
        text = HTMLString(current).large().bold()
        anim.update(text_id, text)
        time.sleep(0.5)

        # 2. Add color
        print("  + blue color")
        text = HTMLString(current).large().bold().blue()
        anim.update(text_id, text)
        time.sleep(0.5)

        # 3. Make larger
        print("  + extra large size")
        text = HTMLString(current).xxl().bold().blue()
        anim.update(text_id, text)
        time.sleep(0.5)

        # 4. Add background
        print("  + yellow background")
        text = HTMLString(current).xxl().bold().blue().bg_yellow()
        anim.update(text_id, text)
        time.sleep(0.5)

        # 5. Add padding
        print("  + padding")
        text = HTMLString(current).xxl().bold().blue().bg_yellow().padding("10px 20px")
        anim.update(text_id, text)

        print()
        print("Final styled message complete!")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
