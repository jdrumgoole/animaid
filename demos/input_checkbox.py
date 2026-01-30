#!/usr/bin/env python3
"""Demo: Checkbox Showcase

Demonstrates: HTMLCheckbox with toggle handling, state display, and multi-checkbox patterns
"""

import time

from animaid import App, HTMLCheckbox, HTMLString


def main() -> None:
    """Run the checkbox showcase demo."""
    with App(title="Demo: Checkbox Showcase") as app:
        # Title
        title = HTMLString("Checkbox Showcase").bold().xl()
        app.add(title)

        # Section 1: Single Toggle with Status
        app.add(HTMLString("Single Toggle").bold().large())
        app.add(HTMLString("Toggle to see the status update:").muted())

        toggle_status = HTMLString("Status: OFF").monospace()
        app.add(toggle_status, id="toggle_status")

        def on_toggle(checked: bool) -> None:
            if checked:
                toggle_status._value = "Status: ON"
                toggle_status._styles = {"color": "#10b981", "font-weight": "bold"}
            else:
                toggle_status._value = "Status: OFF"
                toggle_status._styles = {"color": "#6b7280"}
            app.refresh("toggle_status")
            print(f"Toggle is now: {'ON' if checked else 'OFF'}")

        toggle_checkbox = HTMLCheckbox("Enable Feature").on_change(on_toggle)
        app.add(toggle_checkbox)

        # Section 2: Terms Agreement
        app.add(HTMLString("Terms Agreement").bold().large())

        agreement_msg = HTMLString("Please accept the terms to continue").muted()
        app.add(agreement_msg, id="agreement_msg")

        def on_terms_change(checked: bool) -> None:
            if checked:
                agreement_msg._value = "Thank you for accepting!"
                agreement_msg._styles = {"color": "#10b981", "font-weight": "bold"}
            else:
                agreement_msg._value = "Please accept the terms to continue"
                agreement_msg._styles = {"color": "#6b7280", "font-style": "italic"}
            app.refresh("agreement_msg")
            print(f"Terms {'accepted' if checked else 'not accepted'}")

        terms_checkbox = HTMLCheckbox("I accept the terms and conditions").on_change(
            on_terms_change
        )
        app.add(terms_checkbox)

        # Section 3: Multiple Checkboxes (Preferences)
        app.add(HTMLString("Preferences Panel").bold().large())
        app.add(HTMLString("Select your preferences:").muted())

        preferences = {
            "notifications": False,
            "dark_mode": False,
            "auto_save": False,
            "sounds": False,
        }

        pref_display = HTMLString("Selected: None").monospace()
        app.add(pref_display, id="pref_display")

        def update_preferences_display() -> None:
            selected = [k for k, v in preferences.items() if v]
            if selected:
                pref_display._value = f"Selected: {', '.join(selected)}"
                pref_display._styles = {"color": "#2563eb"}
            else:
                pref_display._value = "Selected: None"
                pref_display._styles = {"color": "#6b7280"}
            app.refresh("pref_display")

        def make_pref_handler(pref_name: str):
            def handler(checked: bool) -> None:
                preferences[pref_name] = checked
                update_preferences_display()
                print(f"{pref_name}: {'enabled' if checked else 'disabled'}")

            return handler

        notifications_cb = HTMLCheckbox("Email Notifications").on_change(
            make_pref_handler("notifications")
        )
        app.add(notifications_cb)

        dark_mode_cb = HTMLCheckbox("Dark Mode").on_change(
            make_pref_handler("dark_mode")
        )
        app.add(dark_mode_cb)

        auto_save_cb = HTMLCheckbox("Auto-Save").on_change(
            make_pref_handler("auto_save")
        )
        app.add(auto_save_cb)

        sounds_cb = HTMLCheckbox("Sound Effects").on_change(make_pref_handler("sounds"))
        app.add(sounds_cb)

        # Section 4: Checkbox Sizes
        app.add(HTMLString("Checkbox Sizes").bold().large())

        def log_size_check(size: str):
            def handler(checked: bool) -> None:
                print(f"{size} checkbox: {'checked' if checked else 'unchecked'}")

            return handler

        small_cb = HTMLCheckbox("Small checkbox").small().on_change(
            log_size_check("Small")
        )
        app.add(small_cb)

        normal_cb = HTMLCheckbox("Normal checkbox").on_change(log_size_check("Normal"))
        app.add(normal_cb)

        large_cb = HTMLCheckbox("Large checkbox").large().on_change(
            log_size_check("Large")
        )
        app.add(large_cb)

        # Section 5: Pre-checked Checkbox
        app.add(HTMLString("Pre-checked Checkbox").bold().large())

        prechecked = HTMLCheckbox("This starts checked", checked=True)
        app.add(prechecked)

        checked_status = HTMLString(f"Initial state: {prechecked.checked}").monospace()
        app.add(checked_status, id="prechecked_status")

        def show_prechecked_state(checked: bool) -> None:
            checked_status._value = f"Current state: {checked}"
            app.refresh("prechecked_status")

        prechecked.on_change(show_prechecked_state)

        print("Checkbox Showcase Demo")
        print("=" * 40)
        print("Try toggling the various checkboxes.")
        print("Watch the live updates and preferences panel!")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
