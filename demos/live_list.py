#!/usr/bin/env python3
"""Demo: Live List (Shopping Cart)

Demonstrates: Reactive mutable updates with HTMLList.

Shows how HTMLList automatically updates the browser when you:
- append() items
- pop() items
- Use styling methods like .pills()

No manual refresh needed - mutations trigger automatic updates!
"""

import time

from animaid import Animate, HTMLList, HTMLString


def main() -> None:
    print("Starting Live List Demo (Shopping Cart)...")
    print("Watch items appear and disappear in real-time!")
    print()

    with Animate(title="Demo: Shopping Cart") as anim:
        # Create title and empty cart
        title = HTMLString("Shopping Cart").bold().xxl()
        cart = HTMLList([]).pills()

        anim.add(title)
        anim.add(cart)

        time.sleep(1)

        # Add items one by one
        items_to_add = [
            "Apples",
            "Bananas",
            "Milk",
            "Bread",
            "Cheese",
            "Eggs",
        ]

        print("Adding items to cart:")
        for item in items_to_add:
            print(f"  + {item}")
            cart.append(item)  # Triggers automatic browser update!
            time.sleep(0.4)

        print()
        time.sleep(0.5)

        # Remove some items
        print("Removing items from cart:")
        for _ in range(2):
            removed = cart.pop()  # Triggers automatic browser update!
            print(f"  - {removed}")
            time.sleep(0.4)

        print()
        print(f"Final cart: {list(cart)}")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
