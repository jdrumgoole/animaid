#!/usr/bin/env python3
"""Record animated GIFs of AnimAID demos using Playwright and Pillow.

Usage:
    uv run python scripts/record_demo_gif.py input_button
    uv run python scripts/record_demo_gif.py input_button --duration 8 --fps 10
    uv run python scripts/record_demo_gif.py all  # Record all input widget demos
"""

import argparse
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

# Demo configurations: name -> (duration_seconds, actions)
# Actions are tuples of (time_offset, action_type, selector_or_value)
DEMO_CONFIGS = {
    "input_button": {
        "duration": 6,
        "actions": [
            (0.5, "click", "text=Default"),
            (1.0, "click", "text=Primary"),
            (1.5, "click", "text=Success"),
            (2.0, "click", "text=Warning"),
            (2.5, "click", "text=Danger"),
            (3.5, "click", "text=Small"),
            (4.0, "click", "text=Normal"),
            (4.5, "click", "text=Large"),
            (5.5, "click", "text=Reset Counter"),
        ],
    },
    "input_text": {
        "duration": 8,
        "actions": [
            (0.5, "type", ('input[placeholder="Type something here..."]', "Hello World!")),
            (3.0, "clear", 'input[placeholder="Type something here..."]'),
            (3.5, "type", ('input[placeholder="Type to see live mirroring..."]', "AnimAID")),
        ],
    },
    "input_checkbox": {
        "duration": 7,
        "actions": [
            (0.5, "click", "text=Enable Feature"),
            (1.5, "click", "text=I accept the terms"),
            (2.5, "click", "text=Email Notifications"),
            (3.0, "click", "text=Dark Mode"),
            (3.5, "click", "text=Auto-Save"),
            (4.5, "click", "text=Email Notifications"),  # Toggle off
            (5.5, "click", "text=This starts checked"),
        ],
    },
    "input_select": {
        "duration": 8,
        "actions": [
            (1.0, "select", (".anim-select", "Green")),
            (2.0, "select", (".anim-select", "Blue")),
            (3.0, "select", (".anim-select", "Purple")),
            (4.5, "select_nth", (1, "Large")),  # Size selector
            (6.0, "select_nth", (2, "Germany")),  # Country selector
        ],
    },
    "input_slider": {
        "duration": 8,
        "actions": [
            # Slider interactions are complex, we'll just let it run
        ],
    },
    "input_form": {
        "duration": 10,
        "actions": [
            (0.5, "type", ('input[placeholder*="name"]', "Alice Smith")),
            (2.0, "type", ('input[placeholder*="email"]', "alice@example.com")),
            (4.0, "click", "text=I agree"),
            (5.0, "click", "text=Submit"),
        ],
    },
    "input_greeter": {
        "duration": 6,
        "actions": [
            (0.5, "type", (".anim-text-input", "World")),
            (2.0, "click", "text=Greet"),
            (3.5, "clear", ".anim-text-input"),
            (4.0, "type", (".anim-text-input", "AnimAID")),
            (5.0, "click", "text=Greet"),
        ],
    },
    "input_counter": {
        "duration": 6,
        "actions": [
            (0.5, "click", "text=+"),
            (1.0, "click", "text=+"),
            (1.5, "click", "text=+"),
            (2.5, "click", "text=-"),
            (3.5, "click", "text=+5"),
            (4.5, "click", "text=Reset"),
        ],
    },
}

INPUT_WIDGET_DEMOS = [
    "input_button",
    "input_text",
    "input_checkbox",
    "input_select",
    "input_slider",
    "input_greeter",
    "input_counter",
    "input_form",
]


def capture_screenshots(
    url: str,
    duration: float,
    fps: int,
    output_dir: Path,
    actions: list,
    width: int = 800,
    height: int = 600,
) -> list[Path]:
    """Capture screenshots from the browser at regular intervals."""
    screenshots = []
    interval = 1.0 / fps
    action_idx = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})

        # Navigate to demo
        page.goto(url)
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)  # Let the page settle

        start_time = time.time()
        frame = 0

        while time.time() - start_time < duration:
            current_time = time.time() - start_time

            # Execute any actions due at this time
            while action_idx < len(actions) and actions[action_idx][0] <= current_time:
                action = actions[action_idx]
                action_type = action[1]

                try:
                    if action_type == "click":
                        selector = action[2]
                        page.click(selector, timeout=1000)
                    elif action_type == "type":
                        selector, text = action[2]
                        page.fill(selector, text, timeout=1000)
                    elif action_type == "clear":
                        selector = action[2]
                        page.fill(selector, "", timeout=1000)
                    elif action_type == "select":
                        selector, value = action[2]
                        page.select_option(selector, label=value, timeout=1000)
                    elif action_type == "select_nth":
                        nth, value = action[2]
                        selects = page.query_selector_all(".anim-select")
                        if nth < len(selects):
                            selects[nth].select_option(label=value)
                except Exception as e:
                    print(f"Action failed: {action} - {e}")

                action_idx += 1
                time.sleep(0.1)  # Small delay after action

            # Capture screenshot
            screenshot_path = output_dir / f"frame_{frame:04d}.png"
            page.screenshot(path=str(screenshot_path))
            screenshots.append(screenshot_path)
            frame += 1

            # Wait for next frame
            elapsed = time.time() - start_time
            next_frame_time = (frame) * interval
            if next_frame_time > elapsed:
                time.sleep(next_frame_time - elapsed)

        browser.close()

    return screenshots


def create_gif(screenshots: list[Path], output_path: Path, fps: int) -> None:
    """Create an animated GIF from screenshots using Pillow."""
    if not screenshots:
        print("No screenshots to process")
        return

    images = []
    for path in screenshots:
        img = Image.open(path)
        # Convert to palette mode for smaller GIF size
        img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        images.append(img)

    # Save as animated GIF
    duration_ms = int(1000 / fps)
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,  # Loop forever
        optimize=True,
    )

    print(f"Created GIF: {output_path} ({len(images)} frames)")


def record_demo(
    demo_name: str,
    output_dir: Path,
    duration: float | None = None,
    fps: int = 10,
    port: int = 8250,
) -> Path | None:
    """Record a demo and create an animated GIF."""
    config = DEMO_CONFIGS.get(demo_name, {"duration": 6, "actions": []})
    if duration is None:
        duration = config["duration"]
    actions = config.get("actions", [])

    print(f"Recording demo: {demo_name} ({duration}s at {fps} fps)")

    # Start the demo in a subprocess
    demo_script = Path("demos") / f"{demo_name}.py"
    if not demo_script.exists():
        print(f"Demo script not found: {demo_script}")
        return None

    # Create a wrapper script that sets the port
    wrapper_code = f'''
import sys
sys.path.insert(0, "src")
import animaid.animate as animate_mod

# Patch Animate to use custom port
_orig_init = animate_mod.Animate.__init__
def _patched_init(self, port={port}, **kwargs):
    return _orig_init(self, port=port, **kwargs)
animate_mod.Animate.__init__ = _patched_init

# Now run the demo
exec(open("{demo_script}").read())
'''

    demo_process = subprocess.Popen(
        [sys.executable, "-c", wrapper_code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path.cwd()),
    )

    try:
        # Wait for server to start
        time.sleep(2.0)

        url = f"http://127.0.0.1:{port}"

        # Create temp directory for screenshots
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Capture screenshots
            screenshots = capture_screenshots(
                url=url,
                duration=duration,
                fps=fps,
                output_dir=temp_path,
                actions=actions,
            )

            # Create GIF
            output_path = output_dir / f"{demo_name}.gif"
            create_gif(screenshots, output_path, fps)

            return output_path

    finally:
        # Stop the demo
        demo_process.terminate()
        try:
            demo_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            demo_process.kill()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Record AnimAID demo as animated GIF")
    parser.add_argument(
        "demo",
        help="Demo name to record (e.g., input_button) or 'all' for all input demos",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Recording duration in seconds (default: demo-specific)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=10,
        help="Frames per second (default: 10)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/images/demos"),
        help="Output directory for GIFs",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8250,
        help="Port for demo server (default: 8250)",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.demo == "all":
        # Record all input widget demos
        for demo_name in INPUT_WIDGET_DEMOS:
            try:
                record_demo(
                    demo_name,
                    args.output_dir,
                    args.duration,
                    args.fps,
                    args.port,
                )
            except Exception as e:
                print(f"Error recording {demo_name}: {e}")
            # Small delay between demos
            time.sleep(1)
    else:
        record_demo(
            args.demo,
            args.output_dir,
            args.duration,
            args.fps,
            args.port,
        )


if __name__ == "__main__":
    main()
