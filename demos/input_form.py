#!/usr/bin/env python3
"""Demo: Registration Form

Demonstrates: Multiple input widgets, checkboxes, select, form submission
"""

import time

from animaid import (
    App,
    HTMLButton,
    HTMLCheckbox,
    HTMLSelect,
    HTMLString,
    HTMLTextInput,
)


def main() -> None:
    """Run the registration form demo."""
    with App(title="Demo: Registration Form") as app:
        # Title
        title = HTMLString("User Registration").bold().xl()
        app.add(title)

        # Name input
        app.add(HTMLString("Name:").bold())
        name_input = HTMLTextInput(placeholder="Enter your full name...")
        app.add(name_input)

        # Email input
        app.add(HTMLString("Email:").bold())
        email_input = HTMLTextInput(placeholder="your@email.com")
        app.add(email_input)

        # Country select
        app.add(HTMLString("Country:").bold())
        country_select = HTMLSelect(
            options=["United States", "United Kingdom", "Canada", "Australia", "Other"]
        )
        app.add(country_select)

        # Newsletter checkbox
        newsletter = HTMLCheckbox("Subscribe to newsletter", checked=True)
        app.add(newsletter)

        # Terms checkbox
        terms = HTMLCheckbox("I accept the terms and conditions", checked=False)
        app.add(terms)

        # Result display
        result = HTMLString("")
        app.add(result, id="result")

        # Submit button
        def submit_form() -> None:
            name = name_input.value
            email = email_input.value
            country = country_select.value
            wants_newsletter = newsletter.checked
            accepted_terms = terms.checked

            if not name:
                result._value = "Please enter your name!"
                result._styles = {"color": "red"}
                app.refresh("result")
                return

            if not email or "@" not in email:
                result._value = "Please enter a valid email!"
                result._styles = {"color": "red"}
                app.refresh("result")
                return

            if not accepted_terms:
                result._value = "Please accept the terms and conditions!"
                result._styles = {"color": "red"}
                app.refresh("result")
                return

            # Success!
            newsletter_status = "Yes" if wants_newsletter else "No"
            result._value = (
                f"Registration successful! "
                f"Welcome, {name} from {country}! "
                f"(Newsletter: {newsletter_status})"
            )
            result._styles = {"color": "green", "font-weight": "bold"}
            app.refresh("result")

            print("\nRegistration submitted:")
            print(f"  Name: {name}")
            print(f"  Email: {email}")
            print(f"  Country: {country}")
            print(f"  Newsletter: {wants_newsletter}")

        submit_button = HTMLButton("Register").primary().large().on_click(submit_form)
        app.add(submit_button)

        print("Registration Form Demo")
        print("=" * 40)
        print("Fill out the form and click Register.")
        print()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nDemo closed.")


if __name__ == "__main__":
    main()
