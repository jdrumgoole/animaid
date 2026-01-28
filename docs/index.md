# Animaid

A GUI toolkit for animating Python data structures.

## Overview

Animaid provides tools to visualize and render Python data structures as styled HTML for educational and presentation purposes. It includes three main classes that subclass Python's built-in types:

- **HTMLString** - A `str` subclass for rendering styled text
- **HTMLList** - A `list` subclass for rendering lists with layout options
- **HTMLDict** - A `dict` subclass for rendering key-value pairs
- **Animate** - A Tkinter-like interactive GUI environment using HTML

All classes support a fluent API for chaining style methods and are compatible with Jinja2 templates via the `__html__()` protocol.

The `Animate` class provides a real-time browser-based display where you can add, update, and remove AnimAID objects programmatically with live updates via WebSocket.

## Installation

```bash
pip install animaid
```

Or for development:

```bash
git clone https://github.com/jdrumgoole/animaid.git
cd animaid
uv pip install -e ".[dev,docs]"
```

## Quick Start

### HTMLString

Style text with CSS properties:

```python
from animaid import HTMLString, Color, Size

# Basic styling with strings
s = HTMLString("Hello, World!").bold().color("blue")
print(s.render())
# <span style="font-weight: bold; color: blue">Hello, World!</span>

# Using CSS types for type-safe styling
styled = (
    HTMLString("Important!")
    .bold()
    .italic()
    .color(Color.red)
    .background(Color.hex("#ffff00"))
    .padding(Size.px(10))
)
```

### HTMLList

Render lists with flexible layouts:

```python
from animaid import HTMLList, Size, Color, Border

# Horizontal list with styled items
items = HTMLList(["Apple", "Banana", "Cherry"])
items = items.horizontal().gap(Size.px(10)).item_padding(Size.px(8))
print(items.render())

# Grid layout with CSS types
grid = (
    HTMLList(["A", "B", "C", "D", "E", "F"])
    .grid(3)
    .gap(Size.px(5))
    .item_border(Border().solid().color(Color.gray))
)
```

### HTMLDict

Display key-value pairs in multiple formats:

```python
from animaid import HTMLDict, Color, Size, Border

# Definition list format (default)
d = HTMLDict({"name": "Alice", "role": "Developer"})
d = d.key_bold().key_color(Color.hex("#333")).value_color(Color.hex("#666"))
print(d.render())

# Table format
table = HTMLDict({"x": 1, "y": 2, "z": 3}).as_table()

# Card layout with CSS types
card = (
    HTMLDict({"Name": "Alice", "Email": "alice@example.com"})
    .key_bold()
    .padding(Size.px(12))
    .border(Border().solid().color(Color.hex("#ccc")))
    .border_radius(Size.px(8))
)
```

### Nested Structures

Combine types for complex visualizations:

```python
from animaid import HTMLDict, HTMLList, Size, Border, Color

# Dict of Lists
categories = HTMLDict({
    "Fruits": HTMLList(["Apple", "Banana"]).horizontal().gap(Size.px(8)),
    "Vegetables": HTMLList(["Carrot", "Broccoli"]).horizontal().gap(Size.px(8)),
}).key_bold()

# List of Dicts (cards)
card_border = Border().solid().color(Color.hex("#ddd"))
cards = HTMLList([
    HTMLDict({"Name": "Alice", "Role": "Dev"}).key_bold().padding(Size.px(10)).border(card_border),
    HTMLDict({"Name": "Bob", "Role": "Design"}).key_bold().padding(Size.px(10)).border(card_border),
]).horizontal().gap(Size.px(16))
```

## CSS Types

Animaid provides type-safe CSS value classes that can be used instead of raw strings. These provide better IDE autocomplete, validation, and documentation.

### Size

Create CSS size values with explicit units:

```python
from animaid import Size

Size.px(16)       # "16px"
Size.em(1.5)      # "1.5em"
Size.rem(2)       # "2rem"
Size.percent(50)  # "50%"
Size.vh(100)      # "100vh"
Size.vw(80)       # "80vw"
Size.auto()       # "auto"
```

### Color

Create CSS color values with validation:

```python
from animaid import Color

# Named colors
Color.red         # "red"
Color.blue        # "blue"

# Hex colors
Color.hex("#ff0000")   # "#ff0000"
Color.hex("00f")       # "#00f" (auto-adds #)

# RGB/RGBA
Color.rgb(255, 0, 0)        # "rgb(255, 0, 0)"
Color.rgba(255, 0, 0, 0.5)  # "rgba(255, 0, 0, 0.5)"

# HSL/HSLA
Color.hsl(120, 100, 50)       # "hsl(120, 100%, 50%)"
Color.hsla(120, 100, 50, 0.5) # "hsla(120, 100%, 50%, 0.5)"
```

### Border

Create CSS border values with a fluent API:

```python
from animaid import Border, BorderStyle, Color, Size

# Using constructor
Border(Size.px(1), BorderStyle.SOLID, Color.black)  # "1px solid black"

# Using fluent API
Border().width(2).solid().color("red")    # "2px solid red"
Border().dashed().color(Color.blue)       # "1px dashed blue"

# Factory methods
Border.solid(2, "black")   # "2px solid black"
Border.dashed(1, "gray")   # "1px dashed gray"
```

### Spacing

Create CSS spacing values (padding, margin) for 1-4 edges:

```python
from animaid import Spacing, Size

# Single value (all edges)
Spacing.all(10)              # "10px"

# Two values (vertical, horizontal)
Spacing.symmetric(10, 20)    # "10px 20px"

# Four values (top, right, bottom, left)
Spacing.edges(10, 20, 10, 20)  # "10px 20px 10px 20px"

# Using Size values
Spacing.symmetric(Size.rem(1), Size.rem(2))  # "1rem 2rem"
```

### Enums

CSS enum values for constrained properties:

```python
from animaid import (
    Display, FlexDirection, AlignItems, JustifyContent,
    FontWeight, FontStyle, TextAlign, TextDecoration
)

# Display
Display.FLEX, Display.GRID, Display.BLOCK, Display.INLINE

# Flexbox
FlexDirection.ROW, FlexDirection.COLUMN
AlignItems.CENTER, AlignItems.STRETCH
JustifyContent.SPACE_BETWEEN, JustifyContent.CENTER

# Typography
FontWeight.BOLD, FontWeight.NORMAL
FontStyle.ITALIC, FontStyle.NORMAL
TextAlign.CENTER, TextAlign.LEFT
TextDecoration.UNDERLINE, TextDecoration.LINE_THROUGH
```

### Backward Compatibility

All methods accept both CSS types and raw strings:

```python
from animaid import HTMLString, Color, Size

# Both work identically:
HTMLString("Hello").color("red")        # Using string
HTMLString("Hello").color(Color.red)    # Using CSS type

HTMLString("Hello").font_size("16px")   # Using string
HTMLString("Hello").font_size(Size.px(16))  # Using CSS type
```

## Animate - Interactive Display

The `Animate` class provides a Tkinter-like interactive GUI environment using HTML. The browser becomes the display surface, and AnimAID objects become widgets that can be added, updated, and removed programmatically with real-time visual feedback.

### Basic Usage

```python
from animaid import Animate, HTMLString, HTMLList

# Create and start the server (opens browser automatically)
anim = Animate()
anim.run()

# Add items - browser updates in real-time
anim.add(HTMLString("Hello World!").bold().xl())
anim.add(HTMLString("This updates live").italic().blue())
anim.add(HTMLList(["Apple", "Banana", "Cherry"]).pills())

# Update an existing item
item_id = anim.add(HTMLString("Loading...").muted())
anim.update(item_id, HTMLString("Done!").success())

# Remove items - by ID or by object
anim.remove(item_id)  # By ID
anim.remove(my_item)  # By object reference
anim.clear(my_item)   # Alias for remove
anim.clear_all()      # Clear all items

# Stop the server when done
anim.stop()
```

### Context Manager

Use the context manager for automatic cleanup:

```python
from animaid import Animate, HTMLString

with Animate() as anim:
    anim.add(HTMLString("Temporary display").bold())
    anim.add(HTMLString("Server stops when context exits").muted())
    input("Press Enter to exit...")
# Server stops automatically when context exits
```

### Configuration Options

```python
# Custom port and title
anim = Animate(port=8300, title="My App")

# Disable auto-opening browser
anim = Animate(auto_open=False)
anim.run()
print(f"Open browser at: {anim.url}")
```

### API Methods

| Method | Description |
|--------|-------------|
| `run()` | Start server and open browser |
| `stop()` | Stop the server |
| `add(item, id=None)` | Add item, returns ID |
| `update(id, item)` | Update item by ID |
| `remove(item_or_id)` | Remove item by ID or object |
| `clear(item_or_id)` | Remove item by ID or object (alias for remove) |
| `clear_all()` | Remove all items |
| `get(id)` | Get item by ID |
| `items()` | Get all (id, item) pairs |
| `refresh(id)` | Re-render and broadcast a single item |
| `refresh_all()` | Re-render and broadcast all items |

### Properties

| Property | Description |
|----------|-------------|
| `url` | Server URL (e.g., `http://127.0.0.1:8200`) |
| `is_running` | Whether server is running |
| `title` | Display title |
| `port` | Server port |

### Installation

The `Animate` class requires the tutorial dependencies:

```bash
pip install animaid[tutorial]
# or with uv
uv pip install animaid[tutorial]
```

### Reactive Updates

Mutable HTML objects (`HTMLList`, `HTMLDict`, `HTMLSet`) automatically notify the Animate display when their contents change. This means you can mutate these objects directly and the browser will update in real-time without calling `update()`.

```python
from animaid import Animate, HTMLList, HTMLDict, HTMLSet

anim = Animate()
anim.run()

# Add a mutable list
scores = HTMLList([10, 20, 30]).pills()
anim.add(scores)

# Mutate the list - browser updates automatically!
scores.append(40)      # Browser shows [10, 20, 30, 40]
scores[0] = 100        # Browser shows [100, 20, 30, 40]
scores.pop()           # Browser shows [100, 20, 30]

# Same for dicts
data = HTMLDict({"score": 0, "level": 1}).card()
anim.add(data)
data["score"] = 500    # Browser updates automatically

# And sets
tags = HTMLSet({"python", "html"}).pills()
anim.add(tags)
tags.add("css")        # Browser updates automatically
```

**Styling updates work on all types:** All HTML types (`HTMLString`, `HTMLInt`, `HTMLFloat`, `HTMLTuple`, `HTMLList`, `HTMLDict`, `HTMLSet`) automatically notify Animate when their styles change:

```python
from animaid import Animate, HTMLString, HTMLInt

anim = Animate()
anim.run()

# Style changes trigger automatic updates
message = HTMLString("Hello")
anim.add(message)
message.bold()        # Browser updates automatically
message.red()         # Browser updates automatically

number = HTMLInt(42)
anim.add(number)
number.badge()        # Browser updates automatically
```

**Immutable types need update() for data changes:** Since `HTMLString`, `HTMLInt`, `HTMLFloat`, and `HTMLTuple` inherit from Python's immutable types, you cannot change their underlying data. To display different content, use the `update()` method:

```python
from animaid import Animate, HTMLString

anim = Animate()
anim.run()

message = HTMLString("Loading...").muted()
item_id = anim.add(message)

# Must use update() to change the content (not just style)
anim.update(item_id, HTMLString("Complete!").success())
```

**Manual refresh:** If you modify an object through a method that bypasses the notification system, use `refresh()` or `refresh_all()`:

```python
# Force re-render of a specific item
anim.refresh(item_id)

# Force re-render of all items
anim.refresh_all()
```

## Demo Programs

AnimAID includes several demo programs that showcase its interactive capabilities. Run them to see real-time updates in action!

### Running Demos

List all available demos:
```bash
uv run invoke demo-list
```

Run a specific demo:
```bash
uv run invoke demo countdown_timer
```

Or run directly with Python:
```bash
uv run python demos/countdown_timer.py
```

### Available Demos

| Demo | Description |
|------|-------------|
| `countdown_timer` | Real-time countdown with color transitions (green → yellow → red) |
| `live_list` | Reactive shopping cart showing `.append()` and `.pop()` |
| `score_tracker` | Game score tracking with automatic dict updates |
| `sorting_visualizer` | Bubble sort algorithm with step-by-step visualization |
| `dashboard` | Multi-type dashboard with HTMLString, HTMLDict, HTMLList, HTMLSet |
| `typewriter` | Typewriter effect with progressive styling |
| `todo_app` | Interactive todo list with CRUD operations |
| `data_pipeline` | ETL pipeline progress tracking |

Each demo opens a browser window and shows real-time updates as Python code executes.

### Demo Gallery

**Countdown Timer** - Color transitions from green to yellow to red

![Countdown Timer Demo](images/demos/countdown_timer.gif)

**Sorting Visualizer** - Bubble sort with step-by-step animation

![Sorting Visualizer Demo](images/demos/sorting_visualizer.gif)

**Dashboard** - Multiple HTML types updating together

![Dashboard Demo](images/demos/dashboard.gif)

**Todo App** - Interactive task management

![Todo App Demo](images/demos/todo_app.gif)

## Tutorial

Run the interactive tutorial to explore all features:

```bash
uv run invoke tutorial
```

This opens a web app at http://127.0.0.1:8200 with tabs for each type, allowing you to experiment with different properties and see the generated Python code and HTML.

## Contents

```{toctree}
:maxdepth: 2
:caption: Contents

api
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
