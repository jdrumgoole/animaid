# Input Widgets

AnimAID provides interactive input widgets that work with the `App` class for building interactive browser-based applications.

## Installation

Input widgets require the tutorial dependencies:

```bash
pip install animaid[tutorial]
```

## Available Widgets

### HTMLButton

A clickable button with style presets.

```python
from animaid import App, HTMLButton

with App() as app:
    def on_click():
        print("Button clicked!")

    button = HTMLButton("Click Me").primary().on_click(on_click)
    app.add(button)
```

**Style Presets:**
- `.primary()` - Blue button
- `.success()` - Green button
- `.danger()` - Red button
- `.warning()` - Orange button

**Size Presets:**
- `.large()` - Larger text and padding
- `.small()` - Smaller text and padding

### HTMLTextInput

A text input field with two-way binding.

```python
from animaid import App, HTMLTextInput

with App() as app:
    def on_change(value: str):
        print(f"Input changed to: {value}")

    text_input = HTMLTextInput(
        placeholder="Enter text..."
    ).wide().on_change(on_change)
    app.add(text_input)

    # Read the current value
    print(text_input.value)
```

**Properties:**
- `value` - Current text value (read/write)
- `placeholder` - Placeholder text

**Methods:**
- `.on_change(callback)` - Register change handler
- `.on_submit(callback)` - Register submit handler (Enter key)
- `.wide()` - Full width
- `.large()` / `.small()` - Size presets

### HTMLCheckbox

A checkbox with a label and two-way binding.

```python
from animaid import App, HTMLCheckbox

with App() as app:
    def on_change(checked: bool):
        print(f"Checkbox is now: {'checked' if checked else 'unchecked'}")

    checkbox = HTMLCheckbox("Enable feature").on_change(on_change)
    app.add(checkbox)

    # Read the current state
    print(checkbox.checked)
```

**Properties:**
- `checked` - Current checked state (read/write)
- `value` - Alias for `checked`
- `label` - The checkbox label text

**Methods:**
- `.on_change(callback)` - Register change handler
- `.large()` / `.small()` - Size presets

### HTMLSlider

A range slider with two-way binding.

```python
from animaid import App, HTMLSlider

with App() as app:
    def on_change(value: float):
        print(f"Slider value: {value}")

    slider = HTMLSlider(
        min=0,
        max=100,
        value=50,
        step=1
    ).wide().on_change(on_change)
    app.add(slider)

    # Read the current value
    print(slider.value)
```

**Properties:**
- `value` - Current numeric value (read/write)
- `min` - Minimum value
- `max` - Maximum value
- `step` - Step increment

**Methods:**
- `.on_change(callback)` - Register change handler
- `.wide()` - Full width
- `.thin()` / `.thick()` - Track thickness

### HTMLSelect

A dropdown select menu with two-way binding.

```python
from animaid import App, HTMLSelect

with App() as app:
    def on_change(value: str):
        print(f"Selected: {value}")

    select = HTMLSelect(
        options=["Red", "Green", "Blue"],
        value="Green"
    ).wide().on_change(on_change)
    app.add(select)

    # Read the current value
    print(select.value)
```

**Properties:**
- `value` - Currently selected option (read/write)
- `options` - List of option strings

**Methods:**
- `.on_change(callback)` - Register change handler
- `.wide()` - Full width
- `.large()` / `.small()` - Size presets

## Two-Way Binding

All input widgets support two-way binding with the `App` class:

1. **User → Python**: When the user interacts with a widget in the browser, the widget's value/state is automatically updated and any registered callbacks are called.

2. **Python → Browser**: You can read the current value at any time using the widget's properties (`value`, `checked`).

```python
from animaid import App, HTMLTextInput, HTMLButton

with App() as app:
    text_input = HTMLTextInput(placeholder="Enter your name")
    app.add(text_input)

    def greet():
        name = text_input.value  # Read current value
        print(f"Hello, {name}!")

    button = HTMLButton("Greet").primary().on_click(greet)
    app.add(button)
```

## Event Handlers

### on_change

Called when the widget's value changes.

```python
def on_change(value):
    # value type depends on widget:
    # - HTMLTextInput: str
    # - HTMLCheckbox: bool
    # - HTMLSlider: float
    # - HTMLSelect: str
    print(f"New value: {value}")

widget.on_change(on_change)
```

### on_click (HTMLButton only)

Called when the button is clicked.

```python
def on_click():
    print("Button clicked!")

button.on_click(on_click)
```

### on_submit (HTMLTextInput only)

Called when Enter is pressed in the text input.

```python
def on_submit(value: str):
    print(f"Submitted: {value}")

text_input.on_submit(on_submit)
```

## Styling

All widgets support the `.styled()` method for custom CSS:

```python
button = HTMLButton("Custom").styled(
    background_color="#6366f1",
    border_radius="20px",
    font_weight="bold"
)
```

And the `.add_class()` method for CSS classes:

```python
button = HTMLButton("Styled").add_class("my-custom-class")
```

## Complete Example

```python
from animaid import App, HTMLString, HTMLButton, HTMLTextInput, HTMLCheckbox

with App(title="User Form") as app:
    app.add(HTMLString("User Registration").bold().xl())

    name_input = HTMLTextInput(placeholder="Enter your name").wide()
    app.add(name_input)

    agree_checkbox = HTMLCheckbox("I agree to the terms")
    app.add(agree_checkbox)

    status = HTMLString("").muted()
    app.add(status, id="status")

    def submit():
        if not name_input.value:
            status._value = "Please enter your name"
            status._styles = {"color": "red"}
        elif not agree_checkbox.checked:
            status._value = "Please agree to the terms"
            status._styles = {"color": "red"}
        else:
            status._value = f"Welcome, {name_input.value}!"
            status._styles = {"color": "green"}
        app.refresh("status")

    submit_btn = HTMLButton("Submit").primary().on_click(submit)
    app.add(submit_btn)

    input("Press Enter to exit...")
```
