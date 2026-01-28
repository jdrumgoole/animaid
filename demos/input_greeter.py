#!/usr/bin/env python3
"""Demo: Interactive Greeter

Demonstrates: HTMLTextInput, HTMLButton, on_click callbacks, two-way binding
"""

import time

from animaid import Animate, HTMLButton, HTMLString, HTMLTextInput


def main() -> None:
    """Run the interactive greeter demo."""
    with Animate(title="Demo: Interactive Greeter") as anim:
        # Title
        title = HTMLString("What's your name?").bold().large()
        anim.add(title)

        # Text input for name
        name_input = HTMLTextInput(placeholder="Enter your name...")
        anim.add(name_input, id="name_input")

        # Greeting display
        greeting = HTMLString("").success().xl()
        anim.add(greeting, id="greeting")

        # Greet button with callback
        def greet() -> None:
            name = name_input.value
            if name:
                greeting._value = f"Hello, {name}! 👋"
            else:
                greeting._value = "Please enter your name first!"
            anim.refresh("greeting")

        button = HTMLButton("Greet Me!").primary().on_click(greet)
        anim.add(button)

        print("Interactive Greeter Demo")
        print("=" * 40)
        print("Enter your name in the text field and click the button.")
        print("The greeting will update in real-time!")
        print()

        # Keep running - using event loop style
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
