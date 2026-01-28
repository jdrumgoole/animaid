#!/usr/bin/env python3
"""Demo: Countdown Timer

Demonstrates: Real-time updates with anim.update(), color presets, size changes.

A countdown from 10 to 0 with color transitions:
- Green (10-7): Safe zone
- Yellow (6-4): Warning zone
- Red (3-1): Danger zone
- "BLASTOFF!" with success style at the end
"""

import time

from animaid import Animate, HTMLString


def main() -> None:
    print("Starting Countdown Timer Demo...")
    print("Watch the browser for a countdown with color transitions!")
    print()

    with Animate(title="Demo: Countdown Timer") as anim:
        # Create the initial display
        title = HTMLString("Countdown Timer").bold().xxl()
        counter = HTMLString("10").xxl().green()

        anim.add(title)
        counter_id = anim.add(counter)

        time.sleep(1)

        # Countdown from 10 to 1
        for i in range(10, 0, -1):
            # Create new styled string based on count
            if i >= 7:
                # Green zone (safe)
                counter = HTMLString(str(i)).xxl().green()
                print(f"  {i} - Green zone")
            elif i >= 4:
                # Yellow zone (warning)
                counter = HTMLString(str(i)).xxl().yellow()
                print(f"  {i} - Yellow zone")
            else:
                # Red zone (danger)
                counter = HTMLString(str(i)).xxl().red()
                print(f"  {i} - Red zone")

            anim.update(counter_id, counter)
            time.sleep(0.5)

        # Final blastoff message
        print()
        print("  BLASTOFF!")
        blastoff = HTMLString("BLASTOFF!").xxl().success().bold()
        anim.update(counter_id, blastoff)

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
