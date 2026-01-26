"""Tutorial web app for animaid HTML types."""

import re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from animaid import HTMLDict, HTMLFloat, HTMLInt, HTMLList, HTMLSet, HTMLString, HTMLTuple


# -------------------------------------------------------------------------
# CSS Type Code Generation Helpers
# -------------------------------------------------------------------------

# Named colors that Color class supports
NAMED_COLORS = {
    "red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan",
    "magenta", "white", "black", "gray", "grey", "transparent", "inherit",
    "navy", "teal", "olive", "maroon", "aqua", "fuchsia", "lime", "silver",
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
    match = re.match(r'^(-?\d*\.?\d+)(px|em|rem|%|vh|vw|fr|pt|ch)$', value.lower())
    if match:
        num_str, unit = match.groups()
        num = float(num_str) if '.' in num_str else int(num_str)
        unit_map = {
            'px': 'px', 'em': 'em', 'rem': 'rem', '%': 'percent',
            'vh': 'vh', 'vw': 'vw', 'fr': 'fr', 'pt': 'pt', 'ch': 'ch'
        }
        return f"Size.{unit_map[unit]}({num})"

    # Can't parse, use string
    return f'"{value}"'


# Colors that have direct shortcuts on HTMLString (e.g., .red, .blue)
SHORTCUT_COLORS = {"red", "blue", "green", "orange", "purple", "pink", "gray", "white", "black"}


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
    if value.startswith('#'):
        return f'Color.hex("{value}")'

    # RGB/RGBA
    rgb_match = re.match(r'^rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$', lower)
    if rgb_match:
        r, g, b, a = rgb_match.groups()
        if a:
            return f"Color.rgba({r}, {g}, {b}, {a})"
        return f"Color.rgb({r}, {g}, {b})"

    # HSL/HSLA
    hsl_match = re.match(r'^hsla?\s*\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*(?:,\s*([\d.]+))?\s*\)$', lower)
    if hsl_match:
        h, s, l, a = hsl_match.groups()
        if a:
            return f"Color.hsla({h}, {s}, {l}, {a})"
        return f"Color.hsl({h}, {s}, {l})"

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
    match = re.match(r'^(\d+)px\s+(solid|dashed|dotted|double|groove|ridge|inset|outset|none)\s+(.+)$', value, re.I)
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
        match = re.match(r'^(-?\d+)px$', part)
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
    for field_name, field_value in vars(req).items() if hasattr(req, '__dict__') else []:
        if isinstance(field_value, str) and field_value:
            if any(x in field_name for x in ['color', 'background']):
                imports.add('Color')
            if any(x in field_name for x in ['size', 'width', 'height', 'radius', 'gap']):
                imports.add('Size')
            if 'border' in field_name and 'radius' not in field_name:
                imports.add('Border')
            if any(x in field_name for x in ['padding', 'margin']):
                imports.add('Size')
                imports.add('Spacing')

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
    inline_tags = {"span", "strong", "em", "b", "i", "a", "code", "li", "dt", "dd", "td", "th"}

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
        tag_attrs = match.group(3)
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
                close_pattern = re.compile(
                    rf"([^<]*)</{tag_name}>", re.IGNORECASE
                )
                close_match = close_pattern.match(html, match.end())
                if close_match:
                    # Inline element with text content - keep on one line
                    content = close_match.group(1)
                    result.append(
                        indent * level + f"{full_tag}{content}</{tag_name}>"
                    )
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

app = FastAPI(title="Animaid Tutorial", description="Interactive tutorial for animaid HTML types")

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
    format: str = "default"  # default, comma, currency, percent, decimal, scientific, significant
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

    items: str = "name=Alice, role=Developer, status=Active"  # key=value, comma-separated
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
        s = s.bold
    if req.italic:
        s = s.italic
    if req.underline:
        s = s.underline
    if req.strikethrough:
        s = s.strikethrough
    if req.monospace:
        s = s.monospace
    if req.uppercase:
        s = s.uppercase

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
        lst = lst.horizontal
    elif req.direction == "horizontal_reverse":
        lst = lst.horizontal_reverse
    elif req.direction == "vertical_reverse":
        lst = lst.vertical_reverse
    elif req.direction == "grid":
        lst = lst.grid(req.grid_columns)

    # Apply list type
    if req.list_type == "ordered":
        lst = lst.ordered
    elif req.list_type == "plain":
        lst = lst.plain

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
    lines = [f'from animaid import {imports_str}', '', f's = HTMLString("{req.content}")']

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
        chains.append(f'.color({color_to_css_type(req.color)})')
    if req.background:
        chains.append(f'.background({color_to_css_type(req.background)})')
    if req.font_size:
        chains.append(f'.font_size({size_to_css_type(req.font_size)})')
    if req.padding:
        chains.append(f'.padding({spacing_to_css_type(req.padding)})')
    if req.border:
        chains.append(f'.border({border_to_css_type(req.border)})')
    if req.border_radius:
        chains.append(f'.border_radius({size_to_css_type(req.border_radius)})')
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
    lines = ['from animaid import HTMLString', '', f's = HTMLString("{req.content}")']

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
    size_shortcuts = {"12px": ".xs", "14px": ".small", "16px": ".medium", "20px": ".large", "24px": ".xl", "32px": ".xxl"}
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
        n = n.bold
    if req.italic:
        n = n.italic
    if req.underline:
        n = n.underline
    if req.monospace:
        n = n.monospace

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
        n = n.bold
    if req.italic:
        n = n.italic
    if req.underline:
        n = n.underline
    if req.monospace:
        n = n.monospace

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
        t = t.plain
    elif req.format == "labeled":
        t = t.labeled
    # parentheses is the default

    # Apply direction
    if req.direction == "horizontal":
        t = t.horizontal
    elif req.direction == "vertical":
        t = t.vertical
    elif req.direction == "horizontal_reverse":
        t = t.horizontal_reverse
    elif req.direction == "vertical_reverse":
        t = t.vertical_reverse
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
    if req.gap or req.border_radius or req.item_border_radius or req.padding or req.item_padding:
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
        lines = [f"from animaid import {imports_str}", "", f"t = HTMLTuple(({items_str},))"]

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
        lines.append(f"t = t.item_border_radius({size_to_css_type(req.item_border_radius)})")
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
        s = s.sorted

    # Apply format
    if req.format == "plain":
        s = s.plain
    # braces is the default

    # Apply direction
    if req.direction == "horizontal":
        s = s.horizontal
    elif req.direction == "vertical":
        s = s.vertical
    elif req.direction == "horizontal_reverse":
        s = s.horizontal_reverse
    elif req.direction == "vertical_reverse":
        s = s.vertical_reverse
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
    # Use set to remove duplicates for the code generation
    unique_items = sorted(set(items_list), key=items_list.index)  # Preserve order of first occurrence
    items_str = ", ".join(f'"{item}"' for item in unique_items)

    # Build imports (always use CSS types)
    imports = ["HTMLSet"]
    if req.background or req.item_background or req.color:
        imports.append("Color")
    if req.gap or req.border_radius or req.item_border_radius or req.padding or req.item_padding:
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
        lines.append(f"s = s.item_border_radius({size_to_css_type(req.item_border_radius)})")
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
    if req.gap or req.border_radius or req.item_border_radius or req.padding or req.margin or req.item_padding:
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
        lines.append(f'lst = lst.gap({size_to_css_type(req.gap)})')
    if req.padding:
        lines.append(f'lst = lst.padding({spacing_to_css_type(req.padding)})')
    if req.margin:
        lines.append(f'lst = lst.margin({spacing_to_css_type(req.margin)})')
    if req.item_padding:
        lines.append(f'lst = lst.item_padding({spacing_to_css_type(req.item_padding)})')
    if req.border:
        lines.append(f'lst = lst.border({border_to_css_type(req.border)})')
    if req.border_radius:
        lines.append(f'lst = lst.border_radius({size_to_css_type(req.border_radius)})')
    if req.item_border:
        lines.append(f'lst = lst.item_border({border_to_css_type(req.item_border)})')
    if req.item_border_radius:
        lines.append(f'lst = lst.item_border_radius({size_to_css_type(req.item_border_radius)})')
    if req.separator:
        lines.append(f'lst = lst.separator({border_to_css_type(req.separator)})')
    if req.background:
        lines.append(f'lst = lst.background({color_to_css_type(req.background)})')
    if req.item_background:
        lines.append(f'lst = lst.item_background({color_to_css_type(req.item_background)})')
    if req.color:
        lines.append(f'lst = lst.color({color_to_css_type(req.color)})')
    if req.align_items:
        lines.append(f'lst = lst.align_items({align_items_to_css_type(req.align_items)})')
    if req.justify_content:
        lines.append(f'lst = lst.justify_content({justify_content_to_css_type(req.justify_content)})')

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
        d = d.as_table
    elif req.format == "divs":
        d = d.as_divs

    # Apply layout
    if req.layout == "horizontal":
        d = d.horizontal
    elif req.layout == "grid":
        d = d.grid(req.grid_columns)

    # Apply key styles
    if req.key_bold:
        d = d.key_bold
    if req.key_italic:
        d = d.key_italic
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
        d = d.value_bold
    if req.value_italic:
        d = d.value_italic
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
    if req.key_color or req.key_background or req.value_color or req.value_background or req.background:
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
        lines.append(f'd = d.key_color({color_to_css_type(req.key_color)})')
    if req.key_background:
        lines.append(f'd = d.key_background({color_to_css_type(req.key_background)})')
    if req.key_width:
        lines.append(f'd = d.key_width({size_to_css_type(req.key_width)})')
    if req.key_padding:
        lines.append(f'd = d.key_padding({spacing_to_css_type(req.key_padding)})')

    if req.value_bold:
        lines.append("d = d.value_bold")
    if req.value_italic:
        lines.append("d = d.value_italic")
    if req.value_color:
        lines.append(f'd = d.value_color({color_to_css_type(req.value_color)})')
    if req.value_background:
        lines.append(f'd = d.value_background({color_to_css_type(req.value_background)})')
    if req.value_padding:
        lines.append(f'd = d.value_padding({spacing_to_css_type(req.value_padding)})')

    if req.separator:
        lines.append(f'd = d.separator("{req.separator}")')
    if req.entry_separator:
        lines.append(f'd = d.entry_separator({border_to_css_type(req.entry_separator)})')

    if req.gap:
        lines.append(f'd = d.gap({size_to_css_type(req.gap)})')
    if req.padding:
        lines.append(f'd = d.padding({spacing_to_css_type(req.padding)})')
    if req.border:
        lines.append(f'd = d.border({border_to_css_type(req.border)})')
    if req.border_radius:
        lines.append(f'd = d.border_radius({size_to_css_type(req.border_radius)})')
    if req.background:
        lines.append(f'd = d.background({color_to_css_type(req.background)})')
    if req.width:
        lines.append(f'd = d.width({size_to_css_type(req.width)})')

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
        lst = HTMLList(items).plain
        if req.list_direction == "horizontal":
            lst = lst.horizontal
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
        d = d.as_table
    elif req.dict_format == "divs":
        d = d.as_divs

    if req.key_bold:
        d = d.key_bold
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
        list_chains.append(f'    lst = lst.gap({size_to_css_type(req.list_gap)})')
    if req.item_background:
        list_chains.append(f'    lst = lst.item_background({color_to_css_type(req.item_background)})')
    if req.item_padding:
        list_chains.append(f'    lst = lst.item_padding({spacing_to_css_type(req.item_padding)})')
    if req.item_border_radius:
        list_chains.append(f'    lst = lst.item_border_radius({size_to_css_type(req.item_border_radius)})')
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
        lines.append(f'd = d.key_color({color_to_css_type(req.key_color)})')

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
            d = d.as_table
        elif req.card_format == "divs":
            d = d.as_divs
        if req.key_bold:
            d = d.key_bold
        if req.card_padding:
            d = d.padding(req.card_padding)
        if req.card_border:
            d = d.border(req.card_border)
        if req.card_border_radius:
            d = d.border_radius(req.card_border_radius)
        if req.card_background:
            d = d.background(req.card_background)
        cards.append(d)

    lst = HTMLList(cards).plain
    if req.list_direction == "horizontal":
        lst = lst.horizontal
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

    lines.extend([
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
    ])

    if req.card_format == "table":
        lines.append("    d = d.as_table")
    elif req.card_format == "divs":
        lines.append("    d = d.as_divs")

    if req.key_bold:
        lines.append("    d = d.key_bold")
    if req.card_padding:
        lines.append(f'    d = d.padding({spacing_to_css_type(req.card_padding)})')
    if req.card_border:
        lines.append(f'    d = d.border({border_to_css_type(req.card_border)})')
    if req.card_border_radius:
        lines.append(f'    d = d.border_radius({size_to_css_type(req.card_border_radius)})')
    if req.card_background:
        lines.append(f'    d = d.background({color_to_css_type(req.card_background)})')

    lines.append("    cards.append(d)")
    lines.append("")
    lines.append("lst = HTMLList(cards).plain")

    if req.list_direction == "horizontal":
        lines.append("lst = lst.horizontal")
    elif req.list_direction == "grid":
        lines.append("lst = lst.grid(3)")

    if req.list_gap:
        lines.append(f'lst = lst.gap({size_to_css_type(req.list_gap)})')

    lines.append("")
    lines.append("html = lst.render()")

    return {"code": "\n".join(lines)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8200)
