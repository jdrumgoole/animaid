# Animaid

A GUI toolkit for animating Python data structures.

## Overview

Animaid provides tools to visualize and render Python data structures as styled HTML for educational and presentation purposes. It includes three main classes that subclass Python's built-in types:

- **HTMLString** - A `str` subclass for rendering styled text
- **HTMLList** - A `list` subclass for rendering lists with layout options
- **HTMLDict** - A `dict` subclass for rendering key-value pairs

All classes support a fluent API for chaining style methods and are compatible with Jinja2 templates via the `__html__()` protocol.

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
s = HTMLString("Hello, World!").bold.color("blue")
print(s.render())
# <span style="font-weight: bold; color: blue">Hello, World!</span>

# Using CSS types for type-safe styling
styled = (
    HTMLString("Important!")
    .bold
    .italic
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
items = items.horizontal.gap(Size.px(10)).item_padding(Size.px(8))
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
d = d.key_bold.key_color(Color.hex("#333")).value_color(Color.hex("#666"))
print(d.render())

# Table format
table = HTMLDict({"x": 1, "y": 2, "z": 3}).as_table

# Card layout with CSS types
card = (
    HTMLDict({"Name": "Alice", "Email": "alice@example.com"})
    .key_bold
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
    "Fruits": HTMLList(["Apple", "Banana"]).horizontal.gap(Size.px(8)),
    "Vegetables": HTMLList(["Carrot", "Broccoli"]).horizontal.gap(Size.px(8)),
}).key_bold

# List of Dicts (cards)
card_border = Border().solid().color(Color.hex("#ddd"))
cards = HTMLList([
    HTMLDict({"Name": "Alice", "Role": "Dev"}).key_bold.padding(Size.px(10)).border(card_border),
    HTMLDict({"Name": "Bob", "Role": "Design"}).key_bold.padding(Size.px(10)).border(card_border),
]).horizontal.gap(Size.px(16))
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
