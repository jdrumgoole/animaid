#!/usr/bin/env python3
"""Demo: Sorting Visualizer

Demonstrates: Algorithm visualization, educational use case.

Visualizes bubble sort step-by-step:
- Shows array as HTMLList with numbers
- Highlights comparisons
- Shows swaps visually
"""

import time

from animaid import Animate, HTMLList, HTMLString


def create_styled_list(
    arr: list[int],
    highlight_i: int | None = None,
    highlight_j: int | None = None,
    swapped: bool = False,
) -> HTMLList:
    """Create a styled list with optional highlighting."""
    items = []
    for idx, num in enumerate(arr):
        item = HTMLString(str(num)).padding("12px 16px").monospace()

        if idx == highlight_i or idx == highlight_j:
            if swapped:
                # Green for successful swap
                item = item.success()
            else:
                # Yellow for comparison
                item = item.warning()
        else:
            item = item.bg_gray()

        items.append(item)

    return HTMLList(items).horizontal().gap("8px")


def main() -> None:
    print("Starting Sorting Visualizer Demo...")
    print("Watch bubble sort in action!")
    print()

    with Animate(title="Demo: Bubble Sort Visualizer") as anim:
        # Title
        title = HTMLString("Bubble Sort Visualizer").bold().xxl()
        anim.add(title)

        # Status
        status = HTMLString("Starting sort...").muted()
        status_id = anim.add(status)

        # Initial array
        arr = [64, 34, 25, 12, 22, 11, 90]
        print(f"Initial array: {arr}")
        print()

        # Create initial display
        array_list = create_styled_list(arr)
        array_id = anim.add(array_list)

        time.sleep(1)

        # Bubble sort with visualization
        n = len(arr)
        comparisons = 0
        swaps = 0

        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1

                # Highlight comparison
                status = HTMLString(f"Comparing {arr[j]} and {arr[j + 1]}...").info()
                anim.update(status_id, status)
                array_list = create_styled_list(arr, j, j + 1)
                anim.update(array_id, array_list)
                time.sleep(0.3)

                if arr[j] > arr[j + 1]:
                    # Swap
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

                    # Show swap
                    status = HTMLString(f"Swapped! {arr[j]} <-> {arr[j + 1]}").success()
                    anim.update(status_id, status)
                    array_list = create_styled_list(arr, j, j + 1, swapped=True)
                    anim.update(array_id, array_list)
                    print(f"  Swap: {arr[j]} <-> {arr[j + 1]} -> {arr}")
                    time.sleep(0.3)

        # Final sorted display
        status = (
            HTMLString(f"Sorted! ({comparisons} comparisons, {swaps} swaps)")
            .success()
            .bold()
        )
        anim.update(status_id, status)

        # Create final display with all green
        final_items = []
        for num in arr:
            item = HTMLString(str(num)).padding("12px 16px").monospace().success()
            final_items.append(item)

        array_list = HTMLList(final_items).horizontal().gap("8px")
        anim.update(array_id, array_list)

        print()
        print(f"Final sorted array: {arr}")
        print(f"Total comparisons: {comparisons}")
        print(f"Total swaps: {swaps}")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
