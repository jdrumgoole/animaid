"""Tutorial web app for animaid HTML types."""

import re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from animaid import (
    HTMLDict,
    HTMLFloat,
    HTMLInt,
    HTMLList,
    HTMLSet,
    HTMLString,
    HTMLTuple,
)

# -------------------------------------------------------------------------
# CSS Type Code Generation Helpers
# -------------------------------------------------------------------------

# Named colors that Color class supports
NAMED_COLORS = {
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "pink",
    "cyan",
    "magenta",
    "white",
    "black",
    "gray",
    "grey",
    "transparent",
    "inherit",
    "navy",
    "teal",
    "olive",
    "maroon",
    "aqua",
    "fuchsia",
    "lime",
    "silver",
}

# Semantic colors (map hex values to Color attributes)
SEMANTIC_COLOR_MAP = {
    "#22c55e": "Color.success",
    "#f59e0b": "Color.warning",
    "#ef4444": "Color.error",
    "#3b82f6": "Color.info",
    "#6b7280": "Color.muted",
    "#f5f5f5": "Color.light_gray",
    "#374151": "Color.dark_gray",
}


def size_to_css_type(value: str) -> str:
    """Convert a size string to CSS type code.

    Examples:
        "16px" -> "Size.md()" or "Size.px(16)"
        "1.5em" -> "Size.em(1.5)"
        "50%" -> "Size.half()" or "Size.percent(50)"
        "auto" -> "Size.auto()"
    """
    value = value.strip()
    if not value:
        return f'"{value}"'

    # Handle special keywords
    if value.lower() == "auto":
        return "Size.auto()"
    if value.lower() == "inherit":
        return "Size.inherit()"
    if value.lower() == "none":
        return "Size.none()"

    # Check for preset values first (beginner-friendly)
    size_presets = {
        "0px": "Size.zero()",
        "4px": "Size.xs()",
        "8px": "Size.sm()",
        "16px": "Size.md()",
        "24px": "Size.lg()",
        "32px": "Size.xl()",
        "48px": "Size.xxl()",
        "100%": "Size.full()",
        "50%": "Size.half()",
        "25%": "Size.quarter()",
    }
    if value.lower() in size_presets:
        return size_presets[value.lower()]

    # Try to parse unit-based values
    match = re.match(r"^(-?\d*\.?\d+)(px|em|rem|%|vh|vw|fr|pt|ch)$", value.lower())
    if match:
        num_str, unit = match.groups()
        num = float(num_str) if "." in num_str else int(num_str)
        unit_map = {
            "px": "px",
            "em": "em",
            "rem": "rem",
            "%": "percent",
            "vh": "vh",
            "vw": "vw",
            "fr": "fr",
            "pt": "pt",
            "ch": "ch",
        }
        return f"Size.{unit_map[unit]}({num})"

    # Can't parse, use string
    return f'"{value}"'


# Colors that have direct shortcuts on HTMLString (e.g., .red, .blue)
SHORTCUT_COLORS = {
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "pink",
    "gray",
    "white",
    "black",
}


def color_to_css_type(value: str) -> str:
    """Convert a color string to CSS type code.

    Examples:
        "red" -> "Color.red"
        "#22c55e" -> "Color.success"
        "#ff0000" -> 'Color.hex("#ff0000")'
        "rgb(255, 0, 0)" -> "Color.rgb(255, 0, 0)"
    """
    value = value.strip()
    if not value:
        return f'"{value}"'

    lower = value.lower()

    # Named colors
    if lower in NAMED_COLORS:
        return f"Color.{lower}"

    # Check for semantic colors (by hex value)
    if value.lower() in SEMANTIC_COLOR_MAP:
        return SEMANTIC_COLOR_MAP[value.lower()]

    # Hex colors
    if value.startswith("#"):
        return f'Color.hex("{value}")'

    # RGB/RGBA
    rgb_pattern = (
        r"^rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$"
    )
    rgb_match = re.match(rgb_pattern, lower)
    if rgb_match:
        r, g, b, a = rgb_match.groups()
        if a:
            return f"Color.rgba({r}, {g}, {b}, {a})"
        return f"Color.rgb({r}, {g}, {b})"

    # HSL/HSLA
    hsl_pattern = (
        r"^hsla?\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*(?:,\s*([\d.]+))?\s*\)$"
    )
    hsl_match = re.match(hsl_pattern, lower)
    if hsl_match:
        hue, sat, lum, alpha = hsl_match.groups()
        if alpha:
            return f"Color.hsla({hue}, {sat}, {lum}, {alpha})"
        return f"Color.hsl({hue}, {sat}, {lum})"

    # Can't parse, use string
    return f'"{value}"'


def is_shortcut_color(value: str) -> bool:
    """Check if a color has a direct shortcut method."""
    return value.strip().lower() in SHORTCUT_COLORS


def border_to_css_type(value: str) -> str:
    """Convert a border string to CSS type code.

    Examples:
        "1px solid black" -> "Border.solid(1, Color.black)"
        "2px dashed red" -> "Border.dashed(2, Color.red)"
        "1px solid black" -> "Border.thin()" (for common patterns)
    """
    value = value.strip()
    if not value:
        return f'"{value}"'

    # Parse "Npx style color" format
    styles = "solid|dashed|dotted|double|groove|ridge|inset|outset|none"
    border_pattern = rf"^(\d+)px\s+({styles})\s+(.+)$"
    match = re.match(border_pattern, value, re.I)
    if match:
        width, style, color = match.groups()
        width_int = int(width)
        style_lower = style.lower()
        color_lower = color.strip().lower()

        # Check for common presets first
        if style_lower == "solid" and color_lower == "black":
            if width_int == 1:
                return "Border.thin()"
            elif width_int == 2:
                return "Border.medium()"
            elif width_int == 4:
                return "Border.thick()"

        # Use the cleaner class method syntax
        color_code = color_to_css_type(color)

        # For simple named colors, we can pass them directly
        if color_lower in SHORTCUT_COLORS:
            color_arg = f'"{color_lower}"'
        elif color_code.startswith("Color.") and "(" not in color_code:
            color_arg = color_code
        else:
            color_arg = color_code

        # Use clean class methods: Border.solid(width, color)
        if style_lower in ("solid", "dashed", "dotted", "double"):
            return f"Border.{style_lower}({width_int}, {color_arg})"

        # Fallback for other styles
        return f'Border({width_int}, "{style_lower}", {color_arg})'

    # Can't parse, use string
    return f'"{value}"'


def spacing_to_css_type(value: str) -> str:
    """Convert a spacing/padding string to CSS type code.

    Examples:
        "16px" -> "Spacing.md()" or "Size.px(16)"
        "8px 16px" -> "Spacing.button()"
        "10px 20px" -> "Spacing.symmetric(10, 20)"
    """
    value = value.strip()
    if not value:
        return f'"{value}"'

    parts = value.split()

    # Check for preset patterns first (beginner-friendly)
    spacing_presets = {
        "0px": "Spacing.zero()",
        "4px": "Spacing.xs()",
        "8px": "Spacing.sm()",
        "16px": "Spacing.md()",
        "24px": "Spacing.lg()",
        "32px": "Spacing.xl()",
    }

    # Single value - check presets first
    if len(parts) == 1:
        if parts[0].lower() in spacing_presets:
            return spacing_presets[parts[0].lower()]
        return size_to_css_type(parts[0])

    # Check for common two-value presets
    if len(parts) == 2:
        two_val = f"{parts[0]} {parts[1]}"
        two_val_presets = {
            "8px 16px": "Spacing.button()",
            "8px 12px": "Spacing.input()",
            "4px 8px": "Spacing.compact()",
            "16px 24px": "Spacing.relaxed()",
            "24px 0px": "Spacing.section()",
        }
        if two_val.lower() in two_val_presets:
            return two_val_presets[two_val.lower()]

    # Try to parse numeric values from parts
    nums = []
    for part in parts:
        match = re.match(r"^(-?\d+)px$", part)
        if match:
            nums.append(int(match.group(1)))
        else:
            # Can't parse all parts as simple px values
            return f'"{value}"'

    if len(nums) == 2:
        return f"Spacing.symmetric({nums[0]}, {nums[1]})"
    elif len(nums) == 3:
        return f"Spacing({nums[0]}, {nums[1]}, {nums[2]})"
    elif len(nums) == 4:
        return f"Spacing.edges({nums[0]}, {nums[1]}, {nums[2]}, {nums[3]})"

    return f'"{value}"'


def align_items_to_css_type(value: str) -> str:
    """Convert an align-items string to CSS type code.

    Examples:
        "center" -> "AlignItems.CENTER"
        "flex-start" -> "AlignItems.FLEX_START"
        "stretch" -> "AlignItems.STRETCH"
    """
    value = value.strip().lower()
    if not value:
        return f'"{value}"'

    # Map CSS values to enum names
    mapping = {
        "start": "AlignItems.START",
        "end": "AlignItems.END",
        "center": "AlignItems.CENTER",
        "stretch": "AlignItems.STRETCH",
        "baseline": "AlignItems.BASELINE",
        "flex-start": "AlignItems.FLEX_START",
        "flex-end": "AlignItems.FLEX_END",
    }

    return mapping.get(value, f'"{value}"')


def justify_content_to_css_type(value: str) -> str:
    """Convert a justify-content string to CSS type code.

    Examples:
        "center" -> "JustifyContent.CENTER"
        "space-between" -> "JustifyContent.SPACE_BETWEEN"
        "flex-start" -> "JustifyContent.FLEX_START"
    """
    value = value.strip().lower()
    if not value:
        return f'"{value}"'

    # Map CSS values to enum names
    mapping = {
        "start": "JustifyContent.START",
        "end": "JustifyContent.END",
        "center": "JustifyContent.CENTER",
        "stretch": "JustifyContent.STRETCH",
        "space-between": "JustifyContent.SPACE_BETWEEN",
        "space-around": "JustifyContent.SPACE_AROUND",
        "space-evenly": "JustifyContent.SPACE_EVENLY",
        "flex-start": "JustifyContent.FLEX_START",
        "flex-end": "JustifyContent.FLEX_END",
    }

    return mapping.get(value, f'"{value}"')


def get_css_imports(req: Any) -> list[str]:
    """Determine which CSS type imports are needed based on the request."""
    imports = set()

    # Check all string fields that might need CSS types
    items = vars(req).items() if hasattr(req, "__dict__") else []
    for field_name, field_value in items:
        if isinstance(field_value, str) and field_value:
            if any(x in field_name for x in ["color", "background"]):
                imports.add("Color")
            size_fields = ["size", "width", "height", "radius", "gap"]
            if any(x in field_name for x in size_fields):
                imports.add("Size")
            if "border" in field_name and "radius" not in field_name:
                imports.add("Border")
            if any(x in field_name for x in ["padding", "margin"]):
                imports.add("Size")
                imports.add("Spacing")

    return sorted(imports)


def pretty_print_html(html: str, indent: str = "  ") -> str:
    """Format HTML with proper indentation.

    Args:
        html: The HTML string to format.
        indent: The indentation string (default 2 spaces).

    Returns:
        Formatted HTML with newlines and indentation.
    """
    # Tags that should have their content on a new line
    block_tags = {"ul", "ol", "div", "dl", "table", "thead", "tbody", "tr"}

    # Self-closing or inline tags
    inline_tags = {
        "span",
        "strong",
        "em",
        "b",
        "i",
        "a",
        "code",
        "li",
        "dt",
        "dd",
        "td",
        "th",
    }

    result = []
    level = 0
    pos = 0

    # Pattern to match HTML tags
    tag_pattern = re.compile(r"<(/?)(\w+)([^>]*)>")

    while pos < len(html):
        match = tag_pattern.search(html, pos)

        if not match:
            # No more tags, add remaining text
            remaining = html[pos:].strip()
            if remaining:
                result.append(indent * level + remaining)
            break

        # Add text before the tag
        text_before = html[pos : match.start()].strip()
        if text_before:
            result.append(indent * level + text_before)

        is_closing = match.group(1) == "/"
        tag_name = match.group(2).lower()
        full_tag = match.group(0)

        if is_closing:
            # Closing tag
            level = max(0, level - 1)
            if tag_name in block_tags:
                result.append(indent * level + full_tag)
            else:
                # Inline closing tag - append to previous line if possible
                if result and not result[-1].endswith(">"):
                    result[-1] += full_tag
                else:
                    result.append(indent * level + full_tag)
        else:
            # Opening tag
            if tag_name in block_tags:
                result.append(indent * level + full_tag)
                level += 1
            elif tag_name in inline_tags:
                # Check if next content is just text followed by closing tag
                close_pattern = re.compile(rf"([^<]*)</{tag_name}>", re.IGNORECASE)
                close_match = close_pattern.match(html, match.end())
                if close_match:
                    # Inline element with text content - keep on one line
                    content = close_match.group(1)
                    result.append(indent * level + f"{full_tag}{content}</{tag_name}>")
                    pos = close_match.end()
                    continue
                else:
                    result.append(indent * level + full_tag)
                    level += 1
            else:
                result.append(indent * level + full_tag)
                level += 1

        pos = match.end()

    return "\n".join(result)


app = FastAPI(
    title="Animaid Tutorial", description="Interactive tutorial for animaid HTML types"
)

# Setup static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# -------------------------------------------------------------------------
# Pydantic models for API requests
# -------------------------------------------------------------------------


class HTMLStringRequest(BaseModel):
    """Request model for HTMLString rendering."""

    content: str = "Hello, World!"
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    monospace: bool = False
    uppercase: bool = False
    color: str = ""
    background: str = ""
    font_size: str = ""
    padding: str = ""
    border: str = ""
    border_radius: str = ""
    tag: str = "span"


class HTMLIntRequest(BaseModel):
    """Request model for HTMLInt rendering."""

    value: int = 1234567
    format: str = "default"  # default, comma, currency, percent, ordinal, padded
    currency_symbol: str = "$"
    padded_width: int = 6
    bold: bool = False
    italic: bool = False
    underline: bool = False
    monospace: bool = False
    color: str = ""
    background: str = ""
    font_size: str = ""
    padding: str = ""
    border: str = ""
    border_radius: str = ""


class HTMLFloatRequest(BaseModel):
    """Request model for HTMLFloat rendering."""

    value: float = 3.14159
    # Format: default, comma, currency, percent, decimal, scientific, significant
    format: str = "default"
    currency_symbol: str = "$"
    decimals: int = 2
    precision: int = 2
    figures: int = 3
    bold: bool = False
    italic: bool = False
    underline: bool = False
    monospace: bool = False
    color: str = ""
    background: str = ""
    font_size: str = ""
    padding: str = ""
    border: str = ""
    border_radius: str = ""


class HTMLTupleRequest(BaseModel):
    """Request model for HTMLTuple rendering."""

    items: str = "Apple, Banana, Cherry"  # Comma-separated
    namedtuple: bool = False  # Use named tuple with x, y, z fields
    format: str = "parentheses"  # parentheses, plain, labeled
    direction: str = "horizontal"  # horizontal, vertical, grid
    grid_columns: int = 3
    gap: str = ""
    padding: str = ""
    item_padding: str = ""
    border: str = ""
    border_radius: str = ""
    item_border: str = ""
    item_border_radius: str = ""
    background: str = ""
    item_background: str = ""
    color: str = ""


class HTMLSetRequest(BaseModel):
    """Request model for HTMLSet rendering."""

    items: str = "Apple, Banana, Cherry, Apple"  # Comma-separated, duplicates removed
    sorted: bool = False  # Sort items alphabetically
    format: str = "braces"  # braces, plain
    direction: str = "horizontal"  # horizontal, vertical, grid
    grid_columns: int = 3
    gap: str = ""
    padding: str = ""
    item_padding: str = ""
    border: str = ""
    border_radius: str = ""
    item_border: str = ""
    item_border_radius: str = ""
    background: str = ""
    item_background: str = ""
    color: str = ""


class HTMLListRequest(BaseModel):
    """Request model for HTMLList rendering."""

    items: str = "Apple, Banana, Cherry, Date"  # Comma-separated
    direction: str = "vertical"  # vertical, horizontal, grid
    list_type: str = "unordered"  # unordered, ordered, plain
    grid_columns: int = 3
    gap: str = ""
    padding: str = ""
    margin: str = ""
    item_padding: str = ""
    border: str = ""
    border_radius: str = ""
    item_border: str = ""
    item_border_radius: str = ""
    separator: str = ""
    background: str = ""
    item_background: str = ""
    color: str = ""
    align_items: str = ""
    justify_content: str = ""


class HTMLDictRequest(BaseModel):
    """Request model for HTMLDict rendering."""

    # key=value, comma-separated
    items: str = "name=Alice, role=Developer, status=Active"
    format: str = "definition_list"  # definition_list, table, divs
    layout: str = "vertical"  # vertical, horizontal, grid
    grid_columns: int = 2
    key_bold: bool = False
    key_italic: bool = False
    key_color: str = ""
    key_background: str = ""
    key_width: str = ""
    key_padding: str = ""
    value_bold: bool = False
    value_italic: bool = False
    value_color: str = ""
    value_background: str = ""
    value_padding: str = ""
    separator: str = ""
    entry_separator: str = ""
    gap: str = ""
    padding: str = ""
    border: str = ""
    border_radius: str = ""
    background: str = ""
    width: str = ""


class DictOfListsRequest(BaseModel):
    """Request model for Dict of Lists rendering."""

    fruits: str = "Apple, Banana, Cherry"
    vegetables: str = "Carrot, Broccoli, Spinach"
    grains: str = "Rice, Wheat, Oats"
    dict_format: str = "definition_list"
    key_bold: bool = True
    key_color: str = "#2563eb"
    list_direction: str = "horizontal"
    list_gap: str = "8px"
    item_background: str = "#f0f9ff"
    item_padding: str = "4px 8px"
    item_border_radius: str = "4px"


class ListOfDictsRequest(BaseModel):
    """Request model for List of Dicts rendering."""

    record1_name: str = "Alice"
    record1_role: str = "Developer"
    record2_name: str = "Bob"
    record2_role: str = "Designer"
    record3_name: str = "Carol"
    record3_role: str = "Manager"
    list_direction: str = "horizontal"
    list_gap: str = "16px"
    card_format: str = "definition_list"
    card_padding: str = "12px"
    card_border: str = "1px solid #e5e7eb"
    card_border_radius: str = "8px"
    card_background: str = "#ffffff"
    key_bold: bool = True


class InputWidgetRequest(BaseModel):
    """Request model for input widget rendering."""

    widget_type: str = "button"  # button, text, checkbox, slider, select
    # Button settings
    button_label: str = "Click Me"
    button_style: str = "default"  # default, primary, success, danger, warning
    button_size: str = "default"  # default, large, small
    # Text input settings
    text_value: str = ""
    text_placeholder: str = "Enter text..."
    text_size: str = "default"  # default, large, small, wide
    # Checkbox settings
    checkbox_label: str = "Accept terms"
    checkbox_checked: bool = False
    checkbox_size: str = "default"  # default, large, small
    # Slider settings
    slider_min: float = 0
    slider_max: float = 100
    slider_value: float = 50
    slider_step: float = 1
    slider_width: str = "default"  # default, wide, thin, thick
    # Select settings
    select_options: str = "Red\nGreen\nBlue"  # newline-separated
    select_value: str = "Red"
    select_size: str = "default"  # default, large, small, wide
    # Common settings
    show_callback: bool = True


class ContainerRequest(BaseModel):
    """Request model for container widget rendering."""

    container_type: str = "row"  # row, column, card, divider, spacer
    # Row settings
    row_gap: int = 8
    row_justify: str = "start"  # start, center, end, space-between, space-around
    row_align: str = "stretch"  # stretch, start, center, end
    row_wrap: bool = False
    # Column settings
    column_gap: int = 8
    column_align: str = "stretch"  # stretch, start, center, end
    column_max_width: str = ""  # e.g., "300px"
    # Card settings
    card_title: str = "Card Title"
    card_shadow: str = "default"  # none, sm, default, md, lg
    card_radius: str = "default"  # none, sm, default, lg, xl
    card_bordered: bool = False
    card_bg_color: str = ""  # e.g., "#eff6ff"
    # Divider settings
    divider_label: str = ""
    divider_style: str = "solid"  # solid, dashed, dotted
    divider_color: str = ""  # e.g., "#3b82f6"
    divider_thickness: int = 1
    divider_vertical: bool = False
    # Spacer settings
    spacer_mode: str = "height"  # height, width, flex
    spacer_size: int = 16
    spacer_flex_value: int = 1
    # Layout options (for row, column, card)
    layout_full_width: bool = False
    layout_full_height: bool = False
    layout_expand: bool = False


# -------------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main tutorial page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/render/string", response_class=HTMLResponse)
async def render_string(req: HTMLStringRequest) -> str:
    """Render an HTMLString with the given properties."""
    s = HTMLString(req.content)

    # Apply boolean properties
    if req.bold:
        s = s.bold()
    if req.italic:
        s = s.italic()
    if req.underline:
        s = s.underline()
    if req.strikethrough:
        s = s.strikethrough()
    if req.monospace:
        s = s.monospace()
    if req.uppercase:
        s = s.uppercase()

    # Apply value properties
    if req.color:
        s = s.color(req.color)
    if req.background:
        s = s.background(req.background)
    if req.font_size:
        s = s.font_size(req.font_size)
    if req.padding:
        s = s.padding(req.padding)
    if req.border:
        s = s.border(req.border)
    if req.border_radius:
        s = s.border_radius(req.border_radius)
    if req.tag and req.tag != "span":
        s = s.tag(req.tag)

    return s.render()


@app.post("/api/render/list", response_class=HTMLResponse)
async def render_list(req: HTMLListRequest) -> str:
    """Render an HTMLList with the given properties."""
    # Parse comma-separated items
    items = [item.strip() for item in req.items.split(",") if item.strip()]
    lst = HTMLList(items)

    # Apply direction
    if req.direction == "horizontal":
        lst = lst.horizontal()
    elif req.direction == "horizontal_reverse":
        lst = lst.horizontal_reverse()
    elif req.direction == "vertical_reverse":
        lst = lst.vertical_reverse()
    elif req.direction == "grid":
        lst = lst.grid(req.grid_columns)

    # Apply list type
    if req.list_type == "ordered":
        lst = lst.ordered()
    elif req.list_type == "plain":
        lst = lst.plain()

    # Apply spacing
    if req.gap:
        lst = lst.gap(req.gap)
    if req.padding:
        lst = lst.padding(req.padding)
    if req.margin:
        lst = lst.margin(req.margin)
    if req.item_padding:
        lst = lst.item_padding(req.item_padding)

    # Apply borders
    if req.border:
        lst = lst.border(req.border)
    if req.border_radius:
        lst = lst.border_radius(req.border_radius)
    if req.item_border:
        lst = lst.item_border(req.item_border)
    if req.item_border_radius:
        lst = lst.item_border_radius(req.item_border_radius)
    if req.separator:
        lst = lst.separator(req.separator)

    # Apply colors
    if req.background:
        lst = lst.background(req.background)
    if req.item_background:
        lst = lst.item_background(req.item_background)
    if req.color:
        lst = lst.color(req.color)

    # Apply alignment
    if req.align_items:
        lst = lst.align_items(req.align_items)
    if req.justify_content:
        lst = lst.justify_content(req.justify_content)

    return lst.render()


@app.get("/api/code/string")
async def get_string_code(req: HTMLStringRequest = None) -> dict[str, str]:
    """Generate Python code for the current HTMLString configuration."""
    if req is None:
        req = HTMLStringRequest()

    # Build imports (always use CSS types)
    imports = ["HTMLString"]
    if req.color or req.background:
        imports.append("Color")
    if req.font_size or req.border_radius or req.padding:
        imports.append("Size")
        # Check if padding needs Spacing (multiple values)
        if req.padding and len(req.padding.split()) > 1:
            imports.append("Spacing")
    if req.border:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    imports = sorted(set(imports), key=lambda x: (x != "HTMLString", x))
    imports_str = ", ".join(imports)
    lines = [
        f"from animaid import {imports_str}",
        "",
        f's = HTMLString("{req.content}")',
    ]

    # Add chained methods
    chains = []
    if req.bold:
        chains.append(".bold")
    if req.italic:
        chains.append(".italic")
    if req.underline:
        chains.append(".underline")
    if req.strikethrough:
        chains.append(".strikethrough")
    if req.monospace:
        chains.append(".monospace")
    if req.uppercase:
        chains.append(".uppercase")
    if req.color:
        chains.append(f".color({color_to_css_type(req.color)})")
    if req.background:
        chains.append(f".background({color_to_css_type(req.background)})")
    if req.font_size:
        chains.append(f".font_size({size_to_css_type(req.font_size)})")
    if req.padding:
        chains.append(f".padding({spacing_to_css_type(req.padding)})")
    if req.border:
        chains.append(f".border({border_to_css_type(req.border)})")
    if req.border_radius:
        chains.append(f".border_radius({size_to_css_type(req.border_radius)})")
    if req.tag and req.tag != "span":
        chains.append(f'.tag("{req.tag}")')

    if chains:
        lines[-1] = f's = HTMLString("{req.content}")'
        for chain in chains:
            lines.append(f"s = s{chain}")

    lines.append("")
    lines.append("html = s.render()")

    return {"code": "\n".join(lines)}


@app.post("/api/code/string")
async def post_string_code(req: HTMLStringRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLString configuration (POST)."""
    return await get_string_code(req)


def generate_simple_string_code(req: HTMLStringRequest) -> dict[str, str]:
    """Generate beginner-friendly Python code using shortcuts.

    Uses simple shortcuts like .red, .large instead of .color(Color.red).
    """
    lines = ["from animaid import HTMLString", "", f's = HTMLString("{req.content}")']

    chains = []
    # Boolean properties
    if req.bold:
        chains.append(".bold")
    if req.italic:
        chains.append(".italic")
    if req.underline:
        chains.append(".underline")
    if req.strikethrough:
        chains.append(".strikethrough")
    if req.monospace:
        chains.append(".monospace")
    if req.uppercase:
        chains.append(".uppercase")

    # Color shortcuts
    if req.color and is_shortcut_color(req.color):
        chains.append(f".{req.color.lower()}")
    elif req.color:
        chains.append(f'.color("{req.color}")')

    # Background shortcuts
    if req.background and is_shortcut_color(req.background):
        chains.append(f".bg_{req.background.lower()}")
    elif req.background:
        chains.append(f'.background("{req.background}")')

    # Size shortcuts
    size_shortcuts = {
        "12px": ".xs",
        "14px": ".small",
        "16px": ".medium",
        "20px": ".large",
        "24px": ".xl",
        "32px": ".xxl",
    }
    if req.font_size in size_shortcuts:
        chains.append(size_shortcuts[req.font_size])
    elif req.font_size:
        chains.append(f'.font_size("{req.font_size}")')

    # Other properties (use simple strings)
    if req.padding:
        chains.append(f'.padding("{req.padding}")')
    if req.border:
        chains.append(f'.border("{req.border}")')
    if req.border_radius:
        chains.append(f'.border_radius("{req.border_radius}")')
    if req.tag and req.tag != "span":
        chains.append(f'.tag("{req.tag}")')

    if chains:
        # Show chained on single line if short enough
        chain_str = "".join(chains)
        if len(chain_str) < 60:
            lines[-1] = f's = HTMLString("{req.content}"){chain_str}'
        else:
            for chain in chains:
                lines.append(f"s = s{chain}")

    lines.append("")
    lines.append("html = s.render()")

    return {"code": "\n".join(lines)}


@app.post("/api/code/string/simple")
async def get_simple_string_code(req: HTMLStringRequest) -> dict[str, str]:
    """Generate beginner-friendly Python code using shortcuts (POST)."""
    return generate_simple_string_code(req)


@app.post("/api/html/string")
async def get_string_html(req: HTMLStringRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLString configuration."""
    html = await render_string(req)
    return {"html": pretty_print_html(html)}


# -------------------------------------------------------------------------
# HTMLInt Routes
# -------------------------------------------------------------------------


@app.post("/api/render/int", response_class=HTMLResponse)
async def render_int(req: HTMLIntRequest) -> str:
    """Render an HTMLInt with the given properties."""
    n = HTMLInt(req.value)

    # Apply formatting
    if req.format == "comma":
        n = n.comma()
    elif req.format == "currency":
        n = n.currency(req.currency_symbol)
    elif req.format == "percent":
        n = n.percent()
    elif req.format == "ordinal":
        n = n.ordinal()
    elif req.format == "padded":
        n = n.padded(req.padded_width)

    # Apply boolean properties
    if req.bold:
        n = n.bold()
    if req.italic:
        n = n.italic()
    if req.underline:
        n = n.underline()
    if req.monospace:
        n = n.monospace()

    # Apply value properties
    if req.color:
        n = n.color(req.color)
    if req.background:
        n = n.background(req.background)
    if req.font_size:
        n = n.font_size(req.font_size)
    if req.padding:
        n = n.padding(req.padding)
    if req.border:
        n = n.border(req.border)
    if req.border_radius:
        n = n.border_radius(req.border_radius)

    return n.render()


@app.post("/api/html/int")
async def get_int_html(req: HTMLIntRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLInt configuration."""
    html = await render_int(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/int")
async def get_int_code(req: HTMLIntRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLInt configuration."""
    # Build imports
    imports = ["HTMLInt"]
    if req.color or req.background:
        imports.append("Color")
    if req.font_size or req.border_radius or req.padding:
        imports.append("Size")
        if req.padding and len(req.padding.split()) > 1:
            imports.append("Spacing")
    if req.border:
        imports.append("Border")
        imports.append("Color")
    imports = sorted(set(imports), key=lambda x: (x != "HTMLInt", x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}", "", f"n = HTMLInt({req.value})"]

    # Add formatting methods
    if req.format == "comma":
        lines.append("n = n.comma()")
    elif req.format == "currency":
        lines.append(f'n = n.currency("{req.currency_symbol}")')
    elif req.format == "percent":
        lines.append("n = n.percent()")
    elif req.format == "ordinal":
        lines.append("n = n.ordinal()")
    elif req.format == "padded":
        lines.append(f"n = n.padded({req.padded_width})")

    # Add style chains
    if req.bold:
        lines.append("n = n.bold")
    if req.italic:
        lines.append("n = n.italic")
    if req.underline:
        lines.append("n = n.underline")
    if req.monospace:
        lines.append("n = n.monospace")
    if req.color:
        lines.append(f"n = n.color({color_to_css_type(req.color)})")
    if req.background:
        lines.append(f"n = n.background({color_to_css_type(req.background)})")
    if req.font_size:
        lines.append(f"n = n.font_size({size_to_css_type(req.font_size)})")
    if req.padding:
        lines.append(f"n = n.padding({spacing_to_css_type(req.padding)})")
    if req.border:
        lines.append(f"n = n.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"n = n.border_radius({size_to_css_type(req.border_radius)})")

    lines.append("")
    lines.append("html = n.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# HTMLFloat Routes
# -------------------------------------------------------------------------


@app.post("/api/render/float", response_class=HTMLResponse)
async def render_float(req: HTMLFloatRequest) -> str:
    """Render an HTMLFloat with the given properties."""
    n = HTMLFloat(req.value)

    # Apply formatting
    if req.format == "comma":
        n = n.comma()
    elif req.format == "currency":
        n = n.currency(req.currency_symbol, req.decimals)
    elif req.format == "percent":
        n = n.percent(req.decimals)
    elif req.format == "decimal":
        n = n.decimal(req.decimals)
    elif req.format == "scientific":
        n = n.scientific(req.precision)
    elif req.format == "significant":
        n = n.significant(req.figures)

    # Apply boolean properties
    if req.bold:
        n = n.bold()
    if req.italic:
        n = n.italic()
    if req.underline:
        n = n.underline()
    if req.monospace:
        n = n.monospace()

    # Apply value properties
    if req.color:
        n = n.color(req.color)
    if req.background:
        n = n.background(req.background)
    if req.font_size:
        n = n.font_size(req.font_size)
    if req.padding:
        n = n.padding(req.padding)
    if req.border:
        n = n.border(req.border)
    if req.border_radius:
        n = n.border_radius(req.border_radius)

    return n.render()


@app.post("/api/html/float")
async def get_float_html(req: HTMLFloatRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLFloat configuration."""
    html = await render_float(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/float")
async def get_float_code(req: HTMLFloatRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLFloat configuration."""
    # Build imports
    imports = ["HTMLFloat"]
    if req.color or req.background:
        imports.append("Color")
    if req.font_size or req.border_radius or req.padding:
        imports.append("Size")
        if req.padding and len(req.padding.split()) > 1:
            imports.append("Spacing")
    if req.border:
        imports.append("Border")
        imports.append("Color")
    imports = sorted(set(imports), key=lambda x: (x != "HTMLFloat", x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}", "", f"n = HTMLFloat({req.value})"]

    # Add formatting methods
    if req.format == "comma":
        lines.append("n = n.comma()")
    elif req.format == "currency":
        lines.append(f'n = n.currency("{req.currency_symbol}", {req.decimals})')
    elif req.format == "percent":
        lines.append(f"n = n.percent({req.decimals})")
    elif req.format == "decimal":
        lines.append(f"n = n.decimal({req.decimals})")
    elif req.format == "scientific":
        lines.append(f"n = n.scientific({req.precision})")
    elif req.format == "significant":
        lines.append(f"n = n.significant({req.figures})")

    # Add style chains
    if req.bold:
        lines.append("n = n.bold")
    if req.italic:
        lines.append("n = n.italic")
    if req.underline:
        lines.append("n = n.underline")
    if req.monospace:
        lines.append("n = n.monospace")
    if req.color:
        lines.append(f"n = n.color({color_to_css_type(req.color)})")
    if req.background:
        lines.append(f"n = n.background({color_to_css_type(req.background)})")
    if req.font_size:
        lines.append(f"n = n.font_size({size_to_css_type(req.font_size)})")
    if req.padding:
        lines.append(f"n = n.padding({spacing_to_css_type(req.padding)})")
    if req.border:
        lines.append(f"n = n.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"n = n.border_radius({size_to_css_type(req.border_radius)})")

    lines.append("")
    lines.append("html = n.render()")

    return {"code": "\n".join(lines)}


# =============================================================================
# HTMLTuple endpoints
# =============================================================================


def build_tuple(req: HTMLTupleRequest) -> HTMLTuple:
    """Build an HTMLTuple from a request."""
    from collections import namedtuple

    items_list = [item.strip() for item in req.items.split(",") if item.strip()]

    # Create tuple - optionally as a named tuple
    if req.namedtuple and items_list:
        # Generate field names (a, b, c, ...)
        field_names = [chr(ord("a") + i) for i in range(len(items_list))]
        NamedTuple = namedtuple("Point", field_names)
        t = HTMLTuple(NamedTuple(*items_list))
    else:
        t = HTMLTuple(tuple(items_list))

    # Apply format
    if req.format == "plain":
        t = t.plain()
    elif req.format == "labeled":
        t = t.labeled()
    # parentheses is the default

    # Apply direction
    if req.direction == "horizontal":
        t = t.horizontal()
    elif req.direction == "vertical":
        t = t.vertical()
    elif req.direction == "horizontal_reverse":
        t = t.horizontal_reverse()
    elif req.direction == "vertical_reverse":
        t = t.vertical_reverse()
    elif req.direction == "grid":
        t = t.grid(req.grid_columns)

    # Apply styles
    if req.gap:
        t = t.gap(req.gap)
    if req.padding:
        t = t.padding(req.padding)
    if req.item_padding:
        t = t.item_padding(req.item_padding)
    if req.border:
        t = t.border(req.border)
    if req.border_radius:
        t = t.border_radius(req.border_radius)
    if req.item_border:
        t = t.item_border(req.item_border)
    if req.item_border_radius:
        t = t.item_border_radius(req.item_border_radius)
    if req.background:
        t = t.background(req.background)
    if req.item_background:
        t = t.item_background(req.item_background)
    if req.color:
        t = t.color(req.color)

    return t


@app.post("/api/render/tuple", response_class=HTMLResponse)
async def render_tuple(req: HTMLTupleRequest) -> str:
    """Render an HTMLTuple with the given configuration."""
    t = build_tuple(req)
    return t.render()


@app.post("/api/html/tuple")
async def get_tuple_html(req: HTMLTupleRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLTuple configuration."""
    t = build_tuple(req)
    return {"html": pretty_print_html(t.render())}


@app.post("/api/code/tuple")
async def get_tuple_code(req: HTMLTupleRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLTuple configuration."""
    items_list = [item.strip() for item in req.items.split(",") if item.strip()]
    items_str = ", ".join(f'"{item}"' for item in items_list)

    # Build imports (always use CSS types)
    imports = ["HTMLTuple"]
    if req.background or req.item_background or req.color:
        imports.append("Color")
    size_check = (
        req.gap
        or req.border_radius
        or req.item_border_radius
        or req.padding
        or req.item_padding
    )
    if size_check:
        imports.append("Size")
        # Check if any spacing values need Spacing (multiple values)
        for spacing_val in [req.padding, req.item_padding]:
            if spacing_val and len(spacing_val.split()) > 1:
                imports.append("Spacing")
                break
    if req.border or req.item_border:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    imports = sorted(set(imports), key=lambda x: (x != "HTMLTuple", x))
    imports_str = ", ".join(imports)

    if req.namedtuple:
        field_names = [chr(ord("a") + i) for i in range(len(items_list))]
        fields_str = ", ".join(f'"{f}"' for f in field_names)
        lines = [
            "from collections import namedtuple",
            f"from animaid import {imports_str}",
            "",
            f'Point = namedtuple("Point", [{fields_str}])',
            f"t = HTMLTuple(Point({items_str}))",
        ]
    else:
        lines = [
            f"from animaid import {imports_str}",
            "",
            f"t = HTMLTuple(({items_str},))",
        ]

    # Add chained methods
    if req.format == "plain":
        lines.append("t = t.plain")
    elif req.format == "labeled":
        lines.append("t = t.labeled")

    if req.direction == "horizontal":
        lines.append("t = t.horizontal")
    elif req.direction == "vertical":
        lines.append("t = t.vertical")
    elif req.direction == "horizontal_reverse":
        lines.append("t = t.horizontal_reverse")
    elif req.direction == "vertical_reverse":
        lines.append("t = t.vertical_reverse")
    elif req.direction == "grid":
        lines.append(f"t = t.grid({req.grid_columns})")

    if req.gap:
        lines.append(f"t = t.gap({size_to_css_type(req.gap)})")
    if req.padding:
        lines.append(f"t = t.padding({spacing_to_css_type(req.padding)})")
    if req.item_padding:
        lines.append(f"t = t.item_padding({spacing_to_css_type(req.item_padding)})")
    if req.border:
        lines.append(f"t = t.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"t = t.border_radius({size_to_css_type(req.border_radius)})")
    if req.item_border:
        lines.append(f"t = t.item_border({border_to_css_type(req.item_border)})")
    if req.item_border_radius:
        radius = size_to_css_type(req.item_border_radius)
        lines.append(f"t = t.item_border_radius({radius})")
    if req.background:
        lines.append(f"t = t.background({color_to_css_type(req.background)})")
    if req.item_background:
        lines.append(f"t = t.item_background({color_to_css_type(req.item_background)})")
    if req.color:
        lines.append(f"t = t.color({color_to_css_type(req.color)})")

    lines.append("")
    lines.append("html = t.render()")

    return {"code": "\n".join(lines)}


# =============================================================================
# HTMLSet endpoints
# =============================================================================


def build_set(req: HTMLSetRequest) -> HTMLSet:
    """Build an HTMLSet from a request."""
    items_list = [item.strip() for item in req.items.split(",") if item.strip()]

    # Create set (duplicates automatically removed)
    s = HTMLSet(items_list)

    # Apply sorted
    if req.sorted:
        s = s.sorted()

    # Apply format
    if req.format == "plain":
        s = s.plain()
    # braces is the default

    # Apply direction
    if req.direction == "horizontal":
        s = s.horizontal()
    elif req.direction == "vertical":
        s = s.vertical()
    elif req.direction == "horizontal_reverse":
        s = s.horizontal_reverse()
    elif req.direction == "vertical_reverse":
        s = s.vertical_reverse()
    elif req.direction == "grid":
        s = s.grid(req.grid_columns)

    # Apply styles
    if req.gap:
        s = s.gap(req.gap)
    if req.padding:
        s = s.padding(req.padding)
    if req.item_padding:
        s = s.item_padding(req.item_padding)
    if req.border:
        s = s.border(req.border)
    if req.border_radius:
        s = s.border_radius(req.border_radius)
    if req.item_border:
        s = s.item_border(req.item_border)
    if req.item_border_radius:
        s = s.item_border_radius(req.item_border_radius)
    if req.background:
        s = s.background(req.background)
    if req.item_background:
        s = s.item_background(req.item_background)
    if req.color:
        s = s.color(req.color)

    return s


@app.post("/api/render/set", response_class=HTMLResponse)
async def render_set(req: HTMLSetRequest) -> str:
    """Render an HTMLSet with the given configuration."""
    s = build_set(req)
    return s.render()


@app.post("/api/html/set")
async def get_set_html(req: HTMLSetRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLSet configuration."""
    s = build_set(req)
    return {"html": pretty_print_html(s.render())}


@app.post("/api/code/set")
async def get_set_code(req: HTMLSetRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLSet configuration."""
    items_list = [item.strip() for item in req.items.split(",") if item.strip()]
    # Use set to remove duplicates for code generation (preserve first occurrence order)
    unique_items = sorted(set(items_list), key=items_list.index)
    items_str = ", ".join(f'"{item}"' for item in unique_items)

    # Build imports (always use CSS types)
    imports = ["HTMLSet"]
    if req.background or req.item_background or req.color:
        imports.append("Color")
    size_check = (
        req.gap
        or req.border_radius
        or req.item_border_radius
        or req.padding
        or req.item_padding
    )
    if size_check:
        imports.append("Size")
        # Check if any spacing values need Spacing (multiple values)
        for spacing_val in [req.padding, req.item_padding]:
            if spacing_val and len(spacing_val.split()) > 1:
                imports.append("Spacing")
                break
    if req.border or req.item_border:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    imports = sorted(set(imports), key=lambda x: (x != "HTMLSet", x))
    imports_str = ", ".join(imports)

    lines = [f"from animaid import {imports_str}", "", f"s = HTMLSet({{{items_str}}})"]

    # Add chained methods
    if req.sorted:
        lines.append("s = s.sorted")

    if req.format == "plain":
        lines.append("s = s.plain")

    if req.direction == "horizontal":
        lines.append("s = s.horizontal")
    elif req.direction == "vertical":
        lines.append("s = s.vertical")
    elif req.direction == "horizontal_reverse":
        lines.append("s = s.horizontal_reverse")
    elif req.direction == "vertical_reverse":
        lines.append("s = s.vertical_reverse")
    elif req.direction == "grid":
        lines.append(f"s = s.grid({req.grid_columns})")

    if req.gap:
        lines.append(f"s = s.gap({size_to_css_type(req.gap)})")
    if req.padding:
        lines.append(f"s = s.padding({spacing_to_css_type(req.padding)})")
    if req.item_padding:
        lines.append(f"s = s.item_padding({spacing_to_css_type(req.item_padding)})")
    if req.border:
        lines.append(f"s = s.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"s = s.border_radius({size_to_css_type(req.border_radius)})")
    if req.item_border:
        lines.append(f"s = s.item_border({border_to_css_type(req.item_border)})")
    if req.item_border_radius:
        radius = size_to_css_type(req.item_border_radius)
        lines.append(f"s = s.item_border_radius({radius})")
    if req.background:
        lines.append(f"s = s.background({color_to_css_type(req.background)})")
    if req.item_background:
        lines.append(f"s = s.item_background({color_to_css_type(req.item_background)})")
    if req.color:
        lines.append(f"s = s.color({color_to_css_type(req.color)})")

    lines.append("")
    lines.append("html = s.render()")

    return {"code": "\n".join(lines)}


@app.post("/api/html/list")
async def get_list_html(req: HTMLListRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLList configuration."""
    html = await render_list(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/list")
async def get_list_code(req: HTMLListRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLList configuration."""
    items_list = [item.strip() for item in req.items.split(",") if item.strip()]
    items_str = ", ".join(f'"{item}"' for item in items_list)

    # Build imports (always use CSS types)
    imports = ["HTMLList"]
    if req.background or req.item_background or req.color:
        imports.append("Color")
    size_check = (
        req.gap
        or req.border_radius
        or req.item_border_radius
        or req.padding
        or req.margin
        or req.item_padding
    )
    if size_check:
        imports.append("Size")
        # Check if any spacing values need Spacing (multiple values)
        for spacing_val in [req.padding, req.margin, req.item_padding]:
            if spacing_val and len(spacing_val.split()) > 1:
                imports.append("Spacing")
                break
    if req.border or req.item_border or req.separator:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    if req.align_items:
        imports.append("AlignItems")
    if req.justify_content:
        imports.append("JustifyContent")
    imports = sorted(set(imports), key=lambda x: (x != "HTMLList", x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}", "", f"lst = HTMLList([{items_str}])"]

    # Add chained methods
    if req.direction == "horizontal":
        lines.append("lst = lst.horizontal")
    elif req.direction == "horizontal_reverse":
        lines.append("lst = lst.horizontal_reverse")
    elif req.direction == "vertical_reverse":
        lines.append("lst = lst.vertical_reverse")
    elif req.direction == "grid":
        lines.append(f"lst = lst.grid({req.grid_columns})")

    if req.list_type == "ordered":
        lines.append("lst = lst.ordered")
    elif req.list_type == "plain":
        lines.append("lst = lst.plain")

    if req.gap:
        lines.append(f"lst = lst.gap({size_to_css_type(req.gap)})")
    if req.padding:
        lines.append(f"lst = lst.padding({spacing_to_css_type(req.padding)})")
    if req.margin:
        lines.append(f"lst = lst.margin({spacing_to_css_type(req.margin)})")
    if req.item_padding:
        lines.append(f"lst = lst.item_padding({spacing_to_css_type(req.item_padding)})")
    if req.border:
        lines.append(f"lst = lst.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"lst = lst.border_radius({size_to_css_type(req.border_radius)})")
    if req.item_border:
        lines.append(f"lst = lst.item_border({border_to_css_type(req.item_border)})")
    if req.item_border_radius:
        radius = size_to_css_type(req.item_border_radius)
        lines.append(f"lst = lst.item_border_radius({radius})")
    if req.separator:
        lines.append(f"lst = lst.separator({border_to_css_type(req.separator)})")
    if req.background:
        lines.append(f"lst = lst.background({color_to_css_type(req.background)})")
    if req.item_background:
        bg = color_to_css_type(req.item_background)
        lines.append(f"lst = lst.item_background({bg})")
    if req.color:
        lines.append(f"lst = lst.color({color_to_css_type(req.color)})")
    if req.align_items:
        align = align_items_to_css_type(req.align_items)
        lines.append(f"lst = lst.align_items({align})")
    if req.justify_content:
        justify = justify_content_to_css_type(req.justify_content)
        lines.append(f"lst = lst.justify_content({justify})")

    lines.append("")
    lines.append("html = lst.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# HTMLDict Routes
# -------------------------------------------------------------------------


def parse_dict_items(items_str: str) -> dict[str, str]:
    """Parse key=value, comma-separated string into a dict."""
    result = {}
    for item in items_str.split(","):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            result[key.strip()] = value.strip()
    return result


@app.post("/api/render/dict", response_class=HTMLResponse)
async def render_dict(req: HTMLDictRequest) -> str:
    """Render an HTMLDict with the given properties."""
    data = parse_dict_items(req.items)
    d = HTMLDict(data)

    # Apply format
    if req.format == "table":
        d = d.as_table()
    elif req.format == "divs":
        d = d.as_divs()

    # Apply layout
    if req.layout == "horizontal":
        d = d.horizontal()
    elif req.layout == "grid":
        d = d.grid(req.grid_columns)

    # Apply key styles
    if req.key_bold:
        d = d.key_bold()
    if req.key_italic:
        d = d.key_italic()
    if req.key_color:
        d = d.key_color(req.key_color)
    if req.key_background:
        d = d.key_background(req.key_background)
    if req.key_width:
        d = d.key_width(req.key_width)
    if req.key_padding:
        d = d.key_padding(req.key_padding)

    # Apply value styles
    if req.value_bold:
        d = d.value_bold()
    if req.value_italic:
        d = d.value_italic()
    if req.value_color:
        d = d.value_color(req.value_color)
    if req.value_background:
        d = d.value_background(req.value_background)
    if req.value_padding:
        d = d.value_padding(req.value_padding)

    # Apply separators
    if req.separator:
        d = d.separator(req.separator)
    if req.entry_separator:
        d = d.entry_separator(req.entry_separator)

    # Apply container styles
    if req.gap:
        d = d.gap(req.gap)
    if req.padding:
        d = d.padding(req.padding)
    if req.border:
        d = d.border(req.border)
    if req.border_radius:
        d = d.border_radius(req.border_radius)
    if req.background:
        d = d.background(req.background)
    if req.width:
        d = d.width(req.width)

    return d.render()


@app.post("/api/html/dict")
async def get_dict_html(req: HTMLDictRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the current HTMLDict configuration."""
    html = await render_dict(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/dict")
async def get_dict_code(req: HTMLDictRequest) -> dict[str, str]:
    """Generate Python code for the current HTMLDict configuration."""
    data = parse_dict_items(req.items)
    items_str = ", ".join(f'"{k}": "{v}"' for k, v in data.items())

    # Build imports - always use CSS types
    imports = ["HTMLDict"]
    color_fields = (
        req.key_color
        or req.key_background
        or req.value_color
        or req.value_background
        or req.background
    )
    if color_fields:
        imports.append("Color")
    if req.key_width or req.gap or req.border_radius or req.width:
        imports.append("Size")
    if req.key_padding or req.value_padding or req.padding:
        imports.append("Size")
        # Check if any padding values need Spacing (multiple values)
        for pad_val in [req.key_padding, req.value_padding, req.padding]:
            if pad_val and len(pad_val.split()) > 1:
                imports.append("Spacing")
                break
    if req.border or req.entry_separator:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    imports = sorted(set(imports), key=lambda x: (x != "HTMLDict", x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}", "", f"d = HTMLDict({{{items_str}}})"]

    # Add chained methods
    if req.format == "table":
        lines.append("d = d.as_table")
    elif req.format == "divs":
        lines.append("d = d.as_divs")

    if req.layout == "horizontal":
        lines.append("d = d.horizontal")
    elif req.layout == "grid":
        lines.append(f"d = d.grid({req.grid_columns})")

    if req.key_bold:
        lines.append("d = d.key_bold")
    if req.key_italic:
        lines.append("d = d.key_italic")
    if req.key_color:
        lines.append(f"d = d.key_color({color_to_css_type(req.key_color)})")
    if req.key_background:
        lines.append(f"d = d.key_background({color_to_css_type(req.key_background)})")
    if req.key_width:
        lines.append(f"d = d.key_width({size_to_css_type(req.key_width)})")
    if req.key_padding:
        lines.append(f"d = d.key_padding({spacing_to_css_type(req.key_padding)})")

    if req.value_bold:
        lines.append("d = d.value_bold")
    if req.value_italic:
        lines.append("d = d.value_italic")
    if req.value_color:
        lines.append(f"d = d.value_color({color_to_css_type(req.value_color)})")
    if req.value_background:
        bg = color_to_css_type(req.value_background)
        lines.append(f"d = d.value_background({bg})")
    if req.value_padding:
        lines.append(f"d = d.value_padding({spacing_to_css_type(req.value_padding)})")

    if req.separator:
        lines.append(f'd = d.separator("{req.separator}")')
    if req.entry_separator:
        sep = border_to_css_type(req.entry_separator)
        lines.append(f"d = d.entry_separator({sep})")

    if req.gap:
        lines.append(f"d = d.gap({size_to_css_type(req.gap)})")
    if req.padding:
        lines.append(f"d = d.padding({spacing_to_css_type(req.padding)})")
    if req.border:
        lines.append(f"d = d.border({border_to_css_type(req.border)})")
    if req.border_radius:
        lines.append(f"d = d.border_radius({size_to_css_type(req.border_radius)})")
    if req.background:
        lines.append(f"d = d.background({color_to_css_type(req.background)})")
    if req.width:
        lines.append(f"d = d.width({size_to_css_type(req.width)})")

    lines.append("")
    lines.append("html = d.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# Dict of Lists Routes
# -------------------------------------------------------------------------


def build_dict_of_lists(req: DictOfListsRequest) -> HTMLDict:
    """Build an HTMLDict with HTMLList values."""

    def make_list(items_str: str) -> HTMLList:
        items = [item.strip() for item in items_str.split(",") if item.strip()]
        lst = HTMLList(items).plain()
        if req.list_direction == "horizontal":
            lst = lst.horizontal()
        if req.list_gap:
            lst = lst.gap(req.list_gap)
        if req.item_background:
            lst = lst.item_background(req.item_background)
        if req.item_padding:
            lst = lst.item_padding(req.item_padding)
        if req.item_border_radius:
            lst = lst.item_border_radius(req.item_border_radius)
        return lst

    d = HTMLDict(
        {
            "Fruits": make_list(req.fruits),
            "Vegetables": make_list(req.vegetables),
            "Grains": make_list(req.grains),
        }
    )

    if req.dict_format == "table":
        d = d.as_table()
    elif req.dict_format == "divs":
        d = d.as_divs()

    if req.key_bold:
        d = d.key_bold()
    if req.key_color:
        d = d.key_color(req.key_color)

    return d


@app.post("/api/render/dict-of-lists", response_class=HTMLResponse)
async def render_dict_of_lists(req: DictOfListsRequest) -> str:
    """Render a Dict of Lists."""
    return build_dict_of_lists(req).render()


@app.post("/api/html/dict-of-lists")
async def get_dict_of_lists_html(req: DictOfListsRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the Dict of Lists."""
    html = build_dict_of_lists(req).render()
    return {"html": pretty_print_html(html)}


@app.post("/api/code/dict-of-lists")
async def get_dict_of_lists_code(req: DictOfListsRequest) -> dict[str, str]:
    """Generate Python code for the Dict of Lists."""
    fruits = [item.strip() for item in req.fruits.split(",") if item.strip()]
    vegetables = [item.strip() for item in req.vegetables.split(",") if item.strip()]
    grains = [item.strip() for item in req.grains.split(",") if item.strip()]

    def list_str(items: list[str]) -> str:
        return ", ".join(f'"{item}"' for item in items)

    # Build imports - always use CSS types
    imports = ["HTMLDict", "HTMLList"]
    if req.key_color or req.item_background:
        imports.append("Color")
    if req.list_gap or req.item_border_radius:
        imports.append("Size")
    if req.item_padding:
        imports.append("Size")
        # Check if item_padding needs Spacing (multiple values)
        if len(req.item_padding.split()) > 1:
            imports.append("Spacing")
    imports = sorted(set(imports), key=lambda x: (x not in ["HTMLDict", "HTMLList"], x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}", "", "def make_list(items):"]

    list_chains = ["    lst = HTMLList(items).plain"]
    if req.list_direction == "horizontal":
        list_chains.append("    lst = lst.horizontal")
    if req.list_gap:
        gap = size_to_css_type(req.list_gap)
        list_chains.append(f"    lst = lst.gap({gap})")
    if req.item_background:
        bg = color_to_css_type(req.item_background)
        list_chains.append(f"    lst = lst.item_background({bg})")
    if req.item_padding:
        pad = spacing_to_css_type(req.item_padding)
        list_chains.append(f"    lst = lst.item_padding({pad})")
    if req.item_border_radius:
        radius = size_to_css_type(req.item_border_radius)
        list_chains.append(f"    lst = lst.item_border_radius({radius})")
    list_chains.append("    return lst")
    lines.extend(list_chains)

    lines.append("")
    lines.append("d = HTMLDict({")
    lines.append(f'    "Fruits": make_list([{list_str(fruits)}]),')
    lines.append(f'    "Vegetables": make_list([{list_str(vegetables)}]),')
    lines.append(f'    "Grains": make_list([{list_str(grains)}]),')
    lines.append("})")

    if req.dict_format == "table":
        lines.append("d = d.as_table")
    elif req.dict_format == "divs":
        lines.append("d = d.as_divs")

    if req.key_bold:
        lines.append("d = d.key_bold")
    if req.key_color:
        lines.append(f"d = d.key_color({color_to_css_type(req.key_color)})")

    lines.append("")
    lines.append("html = d.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# List of Dicts Routes
# -------------------------------------------------------------------------


def build_list_of_dicts(req: ListOfDictsRequest) -> HTMLList:
    """Build an HTMLList with HTMLDict items."""
    records = [
        {"Name": req.record1_name, "Role": req.record1_role},
        {"Name": req.record2_name, "Role": req.record2_role},
        {"Name": req.record3_name, "Role": req.record3_role},
    ]

    cards = []
    for record in records:
        d = HTMLDict(record)
        if req.card_format == "table":
            d = d.as_table()
        elif req.card_format == "divs":
            d = d.as_divs()
        if req.key_bold:
            d = d.key_bold()
        if req.card_padding:
            d = d.padding(req.card_padding)
        if req.card_border:
            d = d.border(req.card_border)
        if req.card_border_radius:
            d = d.border_radius(req.card_border_radius)
        if req.card_background:
            d = d.background(req.card_background)
        cards.append(d)

    lst = HTMLList(cards).plain()
    if req.list_direction == "horizontal":
        lst = lst.horizontal()
    elif req.list_direction == "grid":
        lst = lst.grid(3)
    if req.list_gap:
        lst = lst.gap(req.list_gap)

    return lst


@app.post("/api/render/list-of-dicts", response_class=HTMLResponse)
async def render_list_of_dicts(req: ListOfDictsRequest) -> str:
    """Render a List of Dicts."""
    return build_list_of_dicts(req).render()


@app.post("/api/html/list-of-dicts")
async def get_list_of_dicts_html(req: ListOfDictsRequest) -> dict[str, str]:
    """Get pretty-printed HTML for the List of Dicts."""
    html = build_list_of_dicts(req).render()
    return {"html": pretty_print_html(html)}


@app.post("/api/code/list-of-dicts")
async def get_list_of_dicts_code(req: ListOfDictsRequest) -> dict[str, str]:
    """Generate Python code for the List of Dicts."""
    # Build imports - always use CSS types
    imports = ["HTMLDict", "HTMLList"]
    if req.card_background:
        imports.append("Color")
    if req.card_border_radius or req.list_gap:
        imports.append("Size")
    if req.card_padding:
        imports.append("Size")
        # Check if card_padding needs Spacing (multiple values)
        if len(req.card_padding.split()) > 1:
            imports.append("Spacing")
    if req.card_border:
        imports.append("Border")
        imports.append("Color")  # Border often includes color
    imports = sorted(set(imports), key=lambda x: (x not in ["HTMLDict", "HTMLList"], x))
    imports_str = ", ".join(imports)
    lines = [f"from animaid import {imports_str}"]

    lines.extend(
        [
            "",
            "records = [",
            f'    {{"Name": "{req.record1_name}", "Role": "{req.record1_role}"}},',
            f'    {{"Name": "{req.record2_name}", "Role": "{req.record2_role}"}},',
            f'    {{"Name": "{req.record3_name}", "Role": "{req.record3_role}"}},',
            "]",
            "",
            "cards = []",
            "for record in records:",
            "    d = HTMLDict(record)",
        ]
    )

    if req.card_format == "table":
        lines.append("    d = d.as_table")
    elif req.card_format == "divs":
        lines.append("    d = d.as_divs")

    if req.key_bold:
        lines.append("    d = d.key_bold")
    if req.card_padding:
        lines.append(f"    d = d.padding({spacing_to_css_type(req.card_padding)})")
    if req.card_border:
        lines.append(f"    d = d.border({border_to_css_type(req.card_border)})")
    if req.card_border_radius:
        radius = size_to_css_type(req.card_border_radius)
        lines.append(f"    d = d.border_radius({radius})")
    if req.card_background:
        lines.append(f"    d = d.background({color_to_css_type(req.card_background)})")

    lines.append("    cards.append(d)")
    lines.append("")
    lines.append("lst = HTMLList(cards).plain")

    if req.list_direction == "horizontal":
        lines.append("lst = lst.horizontal")
    elif req.list_direction == "grid":
        lines.append("lst = lst.grid(3)")

    if req.list_gap:
        lines.append(f"lst = lst.gap({size_to_css_type(req.list_gap)})")

    lines.append("")
    lines.append("html = lst.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# Input Widget Routes
# -------------------------------------------------------------------------


@app.post("/api/render/input", response_class=HTMLResponse)
async def render_input(req: InputWidgetRequest) -> str:
    """Render an input widget with the given properties."""
    from animaid import HTMLButton, HTMLCheckbox, HTMLSelect, HTMLSlider, HTMLTextInput

    if req.widget_type == "button":
        widget = HTMLButton(req.button_label)
        if req.button_style == "primary":
            widget = widget.primary()
        elif req.button_style == "success":
            widget = widget.success()
        elif req.button_style == "danger":
            widget = widget.danger()
        elif req.button_style == "warning":
            widget = widget.warning()
        if req.button_size == "large":
            widget = widget.large()
        elif req.button_size == "small":
            widget = widget.small()
        return widget.render()

    elif req.widget_type == "text":
        widget = HTMLTextInput(value=req.text_value, placeholder=req.text_placeholder)
        if req.text_size == "large":
            widget = widget.large()
        elif req.text_size == "small":
            widget = widget.small()
        elif req.text_size == "wide":
            widget = widget.wide()
        return widget.render()

    elif req.widget_type == "checkbox":
        widget = HTMLCheckbox(req.checkbox_label, checked=req.checkbox_checked)
        if req.checkbox_size == "large":
            widget = widget.large()
        elif req.checkbox_size == "small":
            widget = widget.small()
        return widget.render()

    elif req.widget_type == "slider":
        widget = HTMLSlider(
            min=req.slider_min,
            max=req.slider_max,
            value=req.slider_value,
            step=req.slider_step,
        )
        if req.slider_width == "wide":
            widget = widget.wide()
        elif req.slider_width == "thin":
            widget = widget.thin()
        elif req.slider_width == "thick":
            widget = widget.thick()
        return widget.render()

    elif req.widget_type == "select":
        options = [opt.strip() for opt in req.select_options.split("\n") if opt.strip()]
        widget = HTMLSelect(options=options, value=req.select_value)
        if req.select_size == "large":
            widget = widget.large()
        elif req.select_size == "small":
            widget = widget.small()
        elif req.select_size == "wide":
            widget = widget.wide()
        return widget.render()

    return "<p>Unknown widget type</p>"


@app.post("/api/html/input")
async def get_input_html(req: InputWidgetRequest) -> dict[str, str]:
    """Get the pretty-printed HTML for an input widget."""
    html = await render_input(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/input")
async def get_input_code(req: InputWidgetRequest) -> dict[str, str]:
    """Generate Python code for the current input widget configuration."""
    lines: list[str] = []

    if req.widget_type == "button":
        lines.append("from animaid import HTMLButton")
        lines.append("")
        lines.append(f'button = HTMLButton("{req.button_label}")')

        if req.button_style != "default":
            lines.append(f"button = button.{req.button_style}()")
        if req.button_size != "default":
            lines.append(f"button = button.{req.button_size}()")

        if req.show_callback:
            lines.append("")
            lines.append("# With App for interactivity:")
            lines.append("# def on_click():")
            lines.append('#     print("Button clicked!")')
            lines.append("# button = button.on_click(on_click)")

        lines.append("")
        lines.append("html = button.render()")

    elif req.widget_type == "text":
        lines.append("from animaid import HTMLTextInput")
        lines.append("")
        if req.text_value:
            lines.append(
                f'text_input = HTMLTextInput(value="{req.text_value}", '
                f'placeholder="{req.text_placeholder}")'
            )
        else:
            lines.append(
                f'text_input = HTMLTextInput(placeholder="{req.text_placeholder}")'
            )

        if req.text_size != "default":
            lines.append(f"text_input = text_input.{req.text_size}()")

        if req.show_callback:
            lines.append("")
            lines.append("# With App for interactivity:")
            lines.append("# def on_change(value):")
            lines.append('#     print(f"Value changed to: {value}")')
            lines.append("# text_input = text_input.on_change(on_change)")
            lines.append("")
            lines.append("# Read the current value:")
            lines.append("# current_value = text_input.value")

        lines.append("")
        lines.append("html = text_input.render()")

    elif req.widget_type == "checkbox":
        lines.append("from animaid import HTMLCheckbox")
        lines.append("")
        checked_str = "True" if req.checkbox_checked else "False"
        lines.append(
            f'checkbox = HTMLCheckbox("{req.checkbox_label}", checked={checked_str})'
        )

        if req.checkbox_size != "default":
            lines.append(f"checkbox = checkbox.{req.checkbox_size}()")

        if req.show_callback:
            lines.append("")
            lines.append("# With App for interactivity:")
            lines.append("# def on_change(checked):")
            lines.append('#     print(f"Checkbox is now: {checked}")')
            lines.append("# checkbox = checkbox.on_change(on_change)")
            lines.append("")
            lines.append("# Read the current state:")
            lines.append("# is_checked = checkbox.checked")

        lines.append("")
        lines.append("html = checkbox.render()")

    elif req.widget_type == "slider":
        lines.append("from animaid import HTMLSlider")
        lines.append("")
        lines.append(
            f"slider = HTMLSlider(min={req.slider_min}, max={req.slider_max}, "
            f"value={req.slider_value}, step={req.slider_step})"
        )

        if req.slider_width != "default":
            lines.append(f"slider = slider.{req.slider_width}()")

        if req.show_callback:
            lines.append("")
            lines.append("# With App for interactivity:")
            lines.append("# def on_change(value):")
            lines.append('#     print(f"Slider value: {value}")')
            lines.append("# slider = slider.on_change(on_change)")
            lines.append("")
            lines.append("# Read the current value:")
            lines.append("# current_value = slider.value")

        lines.append("")
        lines.append("html = slider.render()")

    elif req.widget_type == "select":
        lines.append("from animaid import HTMLSelect")
        lines.append("")
        options = [
            opt.strip() for opt in req.select_options.split("\n") if opt.strip()
        ]
        options_str = ", ".join(f'"{opt}"' for opt in options)
        lines.append(
            f'select = HTMLSelect(options=[{options_str}], '
            f'value="{req.select_value}")'
        )

        if req.select_size != "default":
            lines.append(f"select = select.{req.select_size}()")

        if req.show_callback:
            lines.append("")
            lines.append("# With App for interactivity:")
            lines.append("# def on_change(value):")
            lines.append('#     print(f"Selected: {value}")')
            lines.append("# select = select.on_change(on_change)")
            lines.append("")
            lines.append("# Read the current value:")
            lines.append("# current_value = select.value")

        lines.append("")
        lines.append("html = select.render()")

    return {"code": "\n".join(lines)}


# -------------------------------------------------------------------------
# Container Widget Endpoints
# -------------------------------------------------------------------------


@app.post("/api/render/container", response_class=HTMLResponse)
async def render_container(req: ContainerRequest) -> str:
    """Render a container widget with the given properties."""
    from animaid import (
        HTMLCard,
        HTMLColumn,
        HTMLDivider,
        HTMLRow,
        HTMLSpacer,
        HTMLString,
        RadiusSize,
        ShadowSize,
    )

    if req.container_type == "row":
        row = HTMLRow([
            HTMLString("Item 1").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
            HTMLString("Item 2").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            HTMLString("Item 3").styled(padding="8px", background_color="#fef3c7", border_radius="4px"),
        ]).gap(req.row_gap)
        if req.row_justify != "start":
            row = row.justify(req.row_justify)
        if req.row_align != "stretch":
            row = row.align(req.row_align)
        if req.row_wrap:
            row = row.wrap()
        # Layout options
        if req.layout_full_width:
            row = row.full_width()
        if req.layout_full_height:
            row = row.full_height()
        if req.layout_expand:
            row = row.expand()
        return row.render()

    elif req.container_type == "column":
        column = HTMLColumn([
            HTMLString("Item 1").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
            HTMLString("Item 2").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            HTMLString("Item 3").styled(padding="8px", background_color="#fef3c7", border_radius="4px"),
        ]).gap(req.column_gap)
        if req.column_align != "stretch":
            column = column.align(req.column_align)
        if req.column_max_width:
            column = column.max_width(req.column_max_width)
        # Layout options
        if req.layout_full_width:
            column = column.full_width()
        if req.layout_full_height:
            column = column.full_height()
        if req.layout_expand:
            column = column.expand()
        return column.render()

    elif req.container_type == "card":
        title = req.card_title if req.card_title else None
        card = HTMLCard(
            title=title,
            children=[
                HTMLColumn([
                    HTMLRow([
                        HTMLString("Status:").bold(),
                        HTMLString("Active").styled(color="#22c55e"),
                    ]).gap(8),
                    HTMLRow([
                        HTMLString("Members:").bold(),
                        HTMLString("42"),
                    ]).gap(8),
                ]).gap(4),
            ],
        )
        shadow_map = {
            "none": ShadowSize.NONE,
            "sm": ShadowSize.SM,
            "default": ShadowSize.DEFAULT,
            "md": ShadowSize.MD,
            "lg": ShadowSize.LG,
        }
        card = card.shadow(shadow_map.get(req.card_shadow, ShadowSize.DEFAULT))
        radius_map = {
            "none": RadiusSize.NONE,
            "sm": RadiusSize.SM,
            "default": RadiusSize.DEFAULT,
            "lg": RadiusSize.LG,
            "xl": RadiusSize.XL,
        }
        card = card.rounded(radius_map.get(req.card_radius, RadiusSize.DEFAULT))
        if req.card_bordered:
            card = card.bordered()
        if req.card_bg_color:
            card = card.filled(req.card_bg_color)
        # Layout options
        if req.layout_full_width:
            card = card.full_width()
        if req.layout_full_height:
            card = card.full_height()
        if req.layout_expand:
            card = card.expand()
        return card.render()

    elif req.container_type == "divider":
        divider = HTMLDivider(req.divider_label if req.divider_label else None)
        if req.divider_style == "dashed":
            divider = divider.dashed()
        elif req.divider_style == "dotted":
            divider = divider.dotted()
        if req.divider_color:
            divider = divider.color(req.divider_color)
        if req.divider_thickness != 1:
            divider = divider.thickness(req.divider_thickness)
        if req.divider_vertical:
            divider = divider.vertical()
            # Show vertical divider in a row context
            container = HTMLRow([
                HTMLString("Left Section").styled(padding="12px", background_color="#e0f2fe", border_radius="4px"),
                divider,
                HTMLString("Right Section").styled(padding="12px", background_color="#dcfce7", border_radius="4px"),
            ]).gap(12).align("stretch").styled(min_height="60px")
            return container.render()
        else:
            # Show horizontal divider between content
            container = HTMLColumn([
                HTMLString("Content Above").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
                divider,
                HTMLString("Content Below").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            ]).gap(0).styled(max_width="400px")
            return container.render()

    elif req.container_type == "spacer":
        spacer = HTMLSpacer()
        if req.spacer_mode == "height":
            spacer = spacer.height(req.spacer_size)
            # Show vertical spacer between content
            spacer = spacer.styled(background_color="#fef3c7")
            container = HTMLColumn([
                HTMLString("Content Above").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
                spacer,
                HTMLString(f"↑ {req.spacer_size}px spacer (yellow) ↑").muted().styled(text_align="center"),
                HTMLString("Content Below").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            ]).gap(4).styled(max_width="300px")
            return container.render()
        elif req.spacer_mode == "width":
            spacer = spacer.width(req.spacer_size)
            spacer = spacer.styled(background_color="#fef3c7", min_height="40px")
            container = HTMLRow([
                HTMLString("Left").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
                spacer,
                HTMLString("Right").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            ]).gap(0).align("center")
            return container.render()
        else:  # flex
            spacer = spacer.flex(req.spacer_flex_value)
            spacer = spacer.styled(background_color="#fef3c7", min_height="30px")
            container = HTMLRow([
                HTMLString("Left").styled(padding="8px", background_color="#e0f2fe", border_radius="4px"),
                spacer,
                HTMLString("Right (pushed by flex spacer)").styled(padding="8px", background_color="#dcfce7", border_radius="4px"),
            ]).gap(4).align("center").styled(width="100%")
            return container.render()

    return "<p>Unknown container type</p>"


@app.post("/api/html/container")
async def get_container_html(req: ContainerRequest) -> dict[str, str]:
    """Get the pretty-printed HTML for a container widget."""
    html = await render_container(req)
    return {"html": pretty_print_html(html)}


@app.post("/api/code/container")
async def get_container_code(req: ContainerRequest) -> dict[str, str]:
    """Generate Python code for the current container configuration."""
    lines: list[str] = []

    if req.container_type == "row":
        lines.append("from animaid import HTMLRow, HTMLString")
        lines.append("")
        lines.append("row = HTMLRow([")
        lines.append('    HTMLString("Item 1"),')
        lines.append('    HTMLString("Item 2"),')
        lines.append('    HTMLString("Item 3"),')
        lines.append(f"]).gap({req.row_gap})")
        if req.row_justify != "start":
            lines.append(f'row = row.justify("{req.row_justify}")')
        if req.row_align != "stretch":
            lines.append(f'row = row.align("{req.row_align}")')
        if req.row_wrap:
            lines.append("row = row.wrap()")
        # Layout options
        if req.layout_full_width:
            lines.append("row = row.full_width()")
        if req.layout_full_height:
            lines.append("row = row.full_height()")
        if req.layout_expand:
            lines.append("row = row.expand()")
        lines.append("")
        lines.append("html = row.render()")

    elif req.container_type == "column":
        lines.append("from animaid import HTMLColumn, HTMLString")
        lines.append("")
        lines.append("column = HTMLColumn([")
        lines.append('    HTMLString("Item 1"),')
        lines.append('    HTMLString("Item 2"),')
        lines.append('    HTMLString("Item 3"),')
        lines.append(f"]).gap({req.column_gap})")
        if req.column_align != "stretch":
            lines.append(f'column = column.align("{req.column_align}")')
        if req.column_max_width:
            lines.append(f'column = column.max_width("{req.column_max_width}")')
        # Layout options
        if req.layout_full_width:
            lines.append("column = column.full_width()")
        if req.layout_full_height:
            lines.append("column = column.full_height()")
        if req.layout_expand:
            lines.append("column = column.expand()")
        lines.append("")
        lines.append("html = column.render()")

    elif req.container_type == "card":
        imports = ["HTMLCard", "HTMLColumn", "HTMLRow", "HTMLString"]
        shadow_import = ""
        radius_import = ""
        if req.card_shadow != "default":
            imports.append("ShadowSize")
            shadow_import = f"ShadowSize.{req.card_shadow.upper()}"
        if req.card_radius != "default":
            imports.append("RadiusSize")
            radius_import = f"RadiusSize.{req.card_radius.upper()}"

        lines.append(f"from animaid import {', '.join(imports)}")
        lines.append("")
        if req.card_title:
            lines.append("card = HTMLCard(")
            lines.append(f'    title="{req.card_title}",')
            lines.append("    children=[")
        else:
            lines.append("card = HTMLCard(")
            lines.append("    children=[")
        lines.append("        HTMLColumn([")
        lines.append("            HTMLRow([")
        lines.append('                HTMLString("Status:").bold(),')
        lines.append('                HTMLString("Active").styled(color="#22c55e"),')
        lines.append("            ]).gap(8),")
        lines.append("            HTMLRow([")
        lines.append('                HTMLString("Members:").bold(),')
        lines.append('                HTMLString("42"),')
        lines.append("            ]).gap(8),")
        lines.append("        ]).gap(4),")
        lines.append("    ],")
        lines.append(")")

        if req.card_shadow != "default":
            lines.append(f"card = card.shadow({shadow_import})")
        if req.card_radius != "default":
            lines.append(f"card = card.rounded({radius_import})")
        if req.card_bordered:
            lines.append("card = card.bordered()")
        if req.card_bg_color:
            lines.append(f'card = card.filled("{req.card_bg_color}")')
        # Layout options
        if req.layout_full_width:
            lines.append("card = card.full_width()")
        if req.layout_full_height:
            lines.append("card = card.full_height()")
        if req.layout_expand:
            lines.append("card = card.expand()")

        lines.append("")
        lines.append("html = card.render()")

    elif req.container_type == "divider":
        if req.divider_vertical:
            lines.append("from animaid import HTMLDivider, HTMLRow, HTMLString")
        else:
            lines.append("from animaid import HTMLDivider, HTMLColumn, HTMLString")
        lines.append("")
        lines.append("# Create the divider")
        if req.divider_label:
            lines.append(f'divider = HTMLDivider("{req.divider_label}")')
        else:
            lines.append("divider = HTMLDivider()")
        if req.divider_style == "dashed":
            lines.append("divider = divider.dashed()")
        elif req.divider_style == "dotted":
            lines.append("divider = divider.dotted()")
        if req.divider_color:
            lines.append(f'divider = divider.color("{req.divider_color}")')
        if req.divider_thickness != 1:
            lines.append(f"divider = divider.thickness({req.divider_thickness})")
        if req.divider_vertical:
            lines.append("divider = divider.vertical()")
            lines.append("")
            lines.append("# Use in a row to separate content horizontally")
            lines.append("layout = HTMLRow([")
            lines.append('    HTMLString("Left Section"),')
            lines.append("    divider,")
            lines.append('    HTMLString("Right Section"),')
            lines.append("]).gap(12)")
        else:
            lines.append("")
            lines.append("# Use in a column to separate content vertically")
            lines.append("layout = HTMLColumn([")
            lines.append('    HTMLString("Content Above"),')
            lines.append("    divider,")
            lines.append('    HTMLString("Content Below"),')
            lines.append("])")
        lines.append("")
        lines.append("html = layout.render()")

    elif req.container_type == "spacer":
        if req.spacer_mode == "width" or req.spacer_mode == "flex":
            lines.append("from animaid import HTMLRow, HTMLSpacer, HTMLString")
        else:
            lines.append("from animaid import HTMLColumn, HTMLSpacer, HTMLString")
        lines.append("")
        lines.append("# Create the spacer")
        lines.append("spacer = HTMLSpacer()")
        if req.spacer_mode == "height":
            lines.append(f"spacer = spacer.height({req.spacer_size})")
            lines.append("")
            lines.append("# Use in a column for vertical spacing")
            lines.append("layout = HTMLColumn([")
            lines.append('    HTMLString("Content Above"),')
            lines.append("    spacer,")
            lines.append('    HTMLString("Content Below"),')
            lines.append("])")
        elif req.spacer_mode == "width":
            lines.append(f"spacer = spacer.width({req.spacer_size})")
            lines.append("")
            lines.append("# Use in a row for horizontal spacing")
            lines.append("layout = HTMLRow([")
            lines.append('    HTMLString("Left"),')
            lines.append("    spacer,")
            lines.append('    HTMLString("Right"),')
            lines.append("])")
        else:  # flex
            lines.append(f"spacer = spacer.flex({req.spacer_flex_value})")
            lines.append("")
            lines.append("# Flex spacer pushes content apart")
            lines.append("layout = HTMLRow([")
            lines.append('    HTMLString("Left"),')
            lines.append("    spacer,  # Expands to fill space")
            lines.append('    HTMLString("Right"),')
            lines.append("])")
        lines.append("")
        lines.append("html = layout.render()")

    return {"code": "\n".join(lines)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8200)
