"""
Animaid - Create beautiful HTML from Python data structures.

Quick Start:
    >>> from animaid import HTMLString, HTMLList, HTMLDict

    # Styled text - chain methods for easy styling
    >>> HTMLString("Hello").bold().red().render()
    '<span style="font-weight: bold; color: red">Hello</span>'

    # Styled lists - use presets for common patterns
    >>> HTMLList(["Apple", "Banana", "Cherry"]).pills().render()

    # Styled dicts - display key-value data beautifully
    >>> HTMLDict({"name": "Alice", "age": 30}).card().render()

Beginner Tips:
    - Use method shortcuts: .bold(), .red(), .large() instead of .styled(...)
    - Use presets: .cards(), .pills(), .badge(), .highlight() for common styles
    - Chain methods: HTMLString("Hi").bold().red().large()
    - Methods modify in-place and return self for chaining
"""

from animaid.css_types import (
    # Layout enums
    AlignItems,
    # Border
    Border,
    BorderStyle,
    # Type aliases
    BorderValue,
    # Primitives
    Color,
    ColorValue,
    # Base class
    CSSValue,
    Display,
    FlexDirection,
    FlexWrap,
    # Text enums
    FontStyle,
    FontWeight,
    JustifyContent,
    Overflow,
    Position,
    Size,
    SizeValue,
    # Spacing
    Spacing,
    SpacingValue,
    TextAlign,
    TextDecoration,
    TextTransform,
)
from animaid.html_dict import HTMLDict
from animaid.html_float import HTMLFloat
from animaid.html_int import HTMLInt
from animaid.html_list import HTMLList
from animaid.html_object import HTMLObject
from animaid.html_set import HTMLSet
from animaid.html_string import HTMLString
from animaid.html_tuple import HTMLTuple

# Conditional import for Animate (requires tutorial dependencies)
try:
    from animaid.animate import Animate
except ImportError:
    Animate = None  # type: ignore[misc, assignment]

__version__ = "0.4.0"

# Beginner-friendly aliases (shorter names)
String = HTMLString
List = HTMLList
Dict = HTMLDict
Int = HTMLInt
Float = HTMLFloat
Tuple = HTMLTuple
Set = HTMLSet

# Short h_ prefixed aliases
h_string = HTMLString
h_list = HTMLList
h_dict = HTMLDict
h_int = HTMLInt
h_float = HTMLFloat
h_tuple = HTMLTuple
h_set = HTMLSet

__all__ = [
    "__version__",
    # Animation
    "Animate",
    # HTML types (full names)
    "HTMLDict",
    "HTMLFloat",
    "HTMLInt",
    "HTMLList",
    "HTMLObject",
    "HTMLSet",
    "HTMLString",
    "HTMLTuple",
    # HTML types (short aliases)
    "String",
    "List",
    "Dict",
    "Int",
    "Float",
    "Tuple",
    "Set",
    # HTML types (h_ prefixed aliases)
    "h_string",
    "h_list",
    "h_dict",
    "h_int",
    "h_float",
    "h_tuple",
    "h_set",
    # CSS value types
    "CSSValue",
    "Color",
    "Size",
    # Text enums
    "FontStyle",
    "FontWeight",
    "TextAlign",
    "TextDecoration",
    "TextTransform",
    # Layout enums
    "AlignItems",
    "Display",
    "FlexDirection",
    "FlexWrap",
    "JustifyContent",
    "Overflow",
    "Position",
    # Border
    "Border",
    "BorderStyle",
    # Spacing
    "Spacing",
    # Type aliases
    "BorderValue",
    "ColorValue",
    "SizeValue",
    "SpacingValue",
]
