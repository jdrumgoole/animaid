"""HTMLTuple - A tuple subclass with HTML rendering capabilities."""

from __future__ import annotations

import html
from enum import Enum
from typing import Any, Self

from animaid.css_types import (
    AlignItems,
    BorderValue,
    ColorValue,
    CSSValue,
    JustifyContent,
    SizeValue,
    SpacingValue,
)
from animaid.html_object import HTMLObject


def _to_css(value: object) -> str:
    """Convert a value to its CSS string representation."""
    if hasattr(value, "to_css"):
        return str(value.to_css())
    return str(value)


def _is_namedtuple(obj: Any) -> bool:
    """Check if an object is a namedtuple instance."""
    return (
        isinstance(obj, tuple)
        and hasattr(obj, "_fields")
        and hasattr(obj, "_asdict")
    )


class TupleDirection(Enum):
    """Direction in which tuple items are rendered."""

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    VERTICAL_REVERSE = "vertical-reverse"
    HORIZONTAL_REVERSE = "horizontal-reverse"
    GRID = "grid"


class TupleFormat(Enum):
    """Format for displaying tuple items."""

    PLAIN = "plain"  # Just items in divs
    PARENTHESES = "parentheses"  # (a, b, c) style
    LABELED = "labeled"  # For named tuples: field: value


class HTMLTuple(HTMLObject, tuple):
    """A tuple subclass that renders as styled HTML.

    HTMLTuple behaves like a regular Python tuple but includes
    methods for applying CSS styles and rendering to HTML.
    Supports named tuples with field name display.

    Examples:
        >>> t = HTMLTuple((1, 2, 3))
        >>> t.render()
        '<div>(1, 2, 3)</div>'

        >>> t.horizontal.pills.render()
        '<div style="display: flex; ...">...</div>'

        >>> from collections import namedtuple
        >>> Point = namedtuple('Point', ['x', 'y'])
        >>> HTMLTuple(Point(10, 20)).labeled.render()
        '<dl><dt>x</dt><dd>10</dd><dt>y</dt><dd>20</dd></dl>'
    """

    _styles: dict[str, str]
    _item_styles: dict[str, str]
    _css_classes: list[str]
    _item_classes: list[str]
    _direction: TupleDirection
    _format: TupleFormat
    _grid_columns: int | None
    _separator: str | None
    _show_parens: bool
    _field_names: tuple[str, ...] | None

    def __new__(cls, items: tuple[Any, ...] = (), **styles: str | CSSValue) -> Self:
        """Create a new HTMLTuple instance.

        Args:
            items: The tuple items.
            **styles: Initial CSS styles.

        Returns:
            A new HTMLTuple instance.
        """
        # Handle namedtuple - extract values
        if _is_namedtuple(items):
            instance = super().__new__(cls, items)
        else:
            instance = super().__new__(cls, items)
        return instance

    def __init__(self, items: tuple[Any, ...] = (), **styles: str | CSSValue) -> None:
        """Initialize an HTMLTuple.

        Args:
            items: The tuple items.
            **styles: CSS styles for the container.
        """
        # Note: tuple is immutable, so we can't call super().__init__
        self._styles = {}
        self._item_styles = {}
        self._css_classes = []
        self._item_classes = []
        self._direction = TupleDirection.HORIZONTAL
        self._format = TupleFormat.PARENTHESES
        self._grid_columns = None
        self._separator = None
        self._show_parens = True

        # Check for named tuple and store field names
        if _is_namedtuple(items):
            self._field_names = items._fields  # type: ignore[attr-defined]
        else:
            self._field_names = None

        for key, value in styles.items():
            css_key = key.replace("_", "-")
            self._styles[css_key] = _to_css(value)

    def _copy_with_settings(
        self,
        new_styles: dict[str, str] | None = None,
        new_item_styles: dict[str, str] | None = None,
        new_classes: list[str] | None = None,
        new_item_classes: list[str] | None = None,
        new_direction: TupleDirection | None = None,
        new_format: TupleFormat | None = None,
        new_grid_columns: int | None = None,
        new_separator: str | None = None,
        new_show_parens: bool | None = None,
    ) -> Self:
        """Create a copy with modified settings."""
        result = HTMLTuple(tuple(self))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._show_parens = self._show_parens
        result._field_names = self._field_names

        if new_styles:
            result._styles.update(new_styles)
        if new_item_styles:
            result._item_styles.update(new_item_styles)
        if new_classes:
            result._css_classes.extend(new_classes)
        if new_item_classes:
            result._item_classes.extend(new_item_classes)
        if new_direction is not None:
            result._direction = new_direction
        if new_format is not None:
            result._format = new_format
        if new_grid_columns is not None:
            result._grid_columns = new_grid_columns
        if new_separator is not None:
            result._separator = new_separator
        if new_show_parens is not None:
            result._show_parens = new_show_parens

        return result  # type: ignore[return-value]

    # -------------------------------------------------------------------------
    # HTMLObject interface
    # -------------------------------------------------------------------------

    def styled(self, **styles: str | CSSValue) -> Self:
        """Return a copy with additional container styles."""
        css_styles = {k.replace("_", "-"): _to_css(v) for k, v in styles.items()}
        return self._copy_with_settings(new_styles=css_styles)

    def add_class(self, *class_names: str) -> Self:
        """Return a copy with additional CSS classes on the container."""
        return self._copy_with_settings(new_classes=list(class_names))

    # -------------------------------------------------------------------------
    # Format methods
    # -------------------------------------------------------------------------

    @property
    def plain(self) -> Self:
        """Return a copy without parentheses decoration."""
        return self._copy_with_settings(new_format=TupleFormat.PLAIN, new_show_parens=False)

    @property
    def parentheses(self) -> Self:
        """Return a copy with parentheses around items (default)."""
        return self._copy_with_settings(new_format=TupleFormat.PARENTHESES, new_show_parens=True)

    @property
    def labeled(self) -> Self:
        """Return a copy showing field names (for named tuples).

        For regular tuples, shows index numbers as labels.
        """
        return self._copy_with_settings(new_format=TupleFormat.LABELED, new_show_parens=False)

    # -------------------------------------------------------------------------
    # Direction methods
    # -------------------------------------------------------------------------

    @property
    def vertical(self) -> Self:
        """Return a copy with vertical layout."""
        return self._copy_with_settings(new_direction=TupleDirection.VERTICAL)

    @property
    def horizontal(self) -> Self:
        """Return a copy with horizontal layout (default)."""
        return self._copy_with_settings(new_direction=TupleDirection.HORIZONTAL)

    @property
    def vertical_reverse(self) -> Self:
        """Return a copy with reversed vertical layout."""
        return self._copy_with_settings(new_direction=TupleDirection.VERTICAL_REVERSE)

    @property
    def horizontal_reverse(self) -> Self:
        """Return a copy with reversed horizontal layout."""
        return self._copy_with_settings(new_direction=TupleDirection.HORIZONTAL_REVERSE)

    def grid(self, columns: int = 3) -> Self:
        """Return a copy with CSS grid layout."""
        return self._copy_with_settings(
            new_direction=TupleDirection.GRID,
            new_grid_columns=columns,
        )

    # -------------------------------------------------------------------------
    # Spacing methods
    # -------------------------------------------------------------------------

    def gap(self, value: SizeValue) -> Self:
        """Return a copy with specified gap between items."""
        return self.styled(gap=_to_css(value))

    def padding(self, value: SpacingValue) -> Self:
        """Return a copy with padding inside the container."""
        return self.styled(padding=_to_css(value))

    def margin(self, value: SpacingValue) -> Self:
        """Return a copy with margin outside the container."""
        return self.styled(margin=_to_css(value))

    def item_padding(self, value: SpacingValue) -> Self:
        """Return a copy with padding inside each item."""
        css_styles = {"padding": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def item_margin(self, value: SpacingValue) -> Self:
        """Return a copy with margin around each item."""
        css_styles = {"margin": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    # -------------------------------------------------------------------------
    # Border methods
    # -------------------------------------------------------------------------

    def border(self, value: BorderValue) -> Self:
        """Return a copy with border around the container."""
        return self.styled(border=_to_css(value))

    def border_radius(self, value: SizeValue) -> Self:
        """Return a copy with rounded corners on the container."""
        return self.styled(border_radius=_to_css(value))

    def item_border(self, value: BorderValue) -> Self:
        """Return a copy with border around each item."""
        css_styles = {"border": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def item_border_radius(self, value: SizeValue) -> Self:
        """Return a copy with rounded corners on each item."""
        css_styles = {"border-radius": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def separator(self, value: BorderValue) -> Self:
        """Return a copy with separator lines between items."""
        return self._copy_with_settings(new_separator=_to_css(value))

    # -------------------------------------------------------------------------
    # Background and color methods
    # -------------------------------------------------------------------------

    def background(self, value: ColorValue) -> Self:
        """Return a copy with background color on the container."""
        return self.styled(background_color=_to_css(value))

    def item_background(self, value: ColorValue) -> Self:
        """Return a copy with background color on each item."""
        css_styles = {"background-color": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def color(self, value: ColorValue) -> Self:
        """Return a copy with text color."""
        return self.styled(color=_to_css(value))

    # -------------------------------------------------------------------------
    # Item class methods
    # -------------------------------------------------------------------------

    def add_item_class(self, *class_names: str) -> Self:
        """Return a copy with CSS classes added to each item."""
        return self._copy_with_settings(new_item_classes=list(class_names))

    # -------------------------------------------------------------------------
    # Alignment methods
    # -------------------------------------------------------------------------

    def align_items(self, value: AlignItems | str) -> Self:
        """Return a copy with specified cross-axis alignment."""
        return self.styled(align_items=_to_css(value))

    def justify_content(self, value: JustifyContent | str) -> Self:
        """Return a copy with specified main-axis alignment."""
        return self.styled(justify_content=_to_css(value))

    @property
    def center(self) -> Self:
        """Return a copy with items centered on both axes."""
        return self.styled(align_items="center", justify_content="center")

    # -------------------------------------------------------------------------
    # Size methods
    # -------------------------------------------------------------------------

    def width(self, value: SizeValue) -> Self:
        """Return a copy with specified width."""
        return self.styled(width=_to_css(value))

    def height(self, value: SizeValue) -> Self:
        """Return a copy with specified height."""
        return self.styled(height=_to_css(value))

    # -------------------------------------------------------------------------
    # Style Presets
    # -------------------------------------------------------------------------

    @property
    def pills(self) -> Self:
        """Return a copy styled as pill/badge items."""
        return (
            self.plain
            .horizontal
            .gap("8px")
            .item_padding("6px 14px")
            .item_border_radius("20px")
            .item_background("#e0e0e0")
            .styled(flex_wrap="wrap")
        )

    @property
    def tags(self) -> Self:
        """Return a copy styled as tags/labels."""
        return (
            self.plain
            .horizontal
            .gap("8px")
            .item_padding("4px 10px")
            .item_background("#f5f5f5")
            .item_border_radius("4px")
            .styled(flex_wrap="wrap")
        )

    @property
    def inline(self) -> Self:
        """Return a copy styled as inline items."""
        return self.plain.horizontal.gap("8px").styled(flex_wrap="wrap")

    @property
    def spaced(self) -> Self:
        """Return a copy with generous spacing between items."""
        return self.gap("16px").item_padding("8px")

    @property
    def compact(self) -> Self:
        """Return a copy with minimal spacing."""
        return self.gap("4px").item_padding("2px")

    @property
    def card(self) -> Self:
        """Return a copy styled as a card for named tuple display."""
        return (
            self.labeled
            .padding("16px")
            .border("1px solid #e0e0e0")
            .border_radius("8px")
            .background("white")
        )

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    def _render_item(self, item: Any) -> str:
        """Render a single item to HTML."""
        if isinstance(item, HTMLObject):
            return item.render()
        elif isinstance(item, str):
            return html.escape(item)
        else:
            return html.escape(str(item))

    def _get_container_styles(self) -> dict[str, str]:
        """Build the complete container styles including layout."""
        styles = self._styles.copy()

        if self._format != TupleFormat.LABELED:
            # Flexbox/grid layout for non-labeled formats
            if self._direction == TupleDirection.HORIZONTAL:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "row")
                styles.setdefault("align-items", "center")
            elif self._direction == TupleDirection.HORIZONTAL_REVERSE:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "row-reverse")
                styles.setdefault("align-items", "center")
            elif self._direction == TupleDirection.VERTICAL:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "column")
            elif self._direction == TupleDirection.VERTICAL_REVERSE:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "column-reverse")
            elif self._direction == TupleDirection.GRID:
                styles.setdefault("display", "inline-grid")
                cols = self._grid_columns or 3
                styles.setdefault("grid-template-columns", f"repeat({cols}, 1fr)")

        return styles

    def _build_item_style_string(self, index: int, total: int) -> str:
        """Build style string for an item, including separators."""
        styles = self._item_styles.copy()

        if self._separator:
            is_horizontal = self._direction in (
                TupleDirection.HORIZONTAL,
                TupleDirection.HORIZONTAL_REVERSE,
            )
            is_last = index == total - 1

            if not is_last:
                if is_horizontal:
                    styles["border-right"] = self._separator
                else:
                    styles["border-bottom"] = self._separator

        if not styles:
            return ""
        return "; ".join(f"{k}: {v}" for k, v in styles.items())

    def _build_item_attributes(self, index: int, total: int) -> str:
        """Build complete attribute string for an item."""
        parts = []

        if self._item_classes:
            class_str = " ".join(self._item_classes)
            parts.append(f'class="{class_str}"')

        style_str = self._build_item_style_string(index, total)
        if style_str:
            parts.append(f'style="{style_str}"')

        return " ".join(parts)

    def _get_labeled_container_styles(self) -> dict[str, str]:
        """Build container styles for labeled format."""
        styles = self._styles.copy()

        if self._direction == TupleDirection.HORIZONTAL:
            # Horizontal: use CSS grid with 2 columns per pair
            styles.setdefault("display", "inline-grid")
            styles.setdefault("grid-template-columns", "auto auto")
            styles.setdefault("column-gap", styles.pop("gap", "8px"))
            styles.setdefault("row-gap", "4px")
            styles.setdefault("align-items", "center")
        elif self._direction == TupleDirection.VERTICAL:
            # Vertical: single column layout
            styles.setdefault("display", "block")
        elif self._direction == TupleDirection.GRID:
            # Grid: multiple pairs per row
            cols = self._grid_columns or 3
            styles.setdefault("display", "inline-grid")
            styles.setdefault("grid-template-columns", f"repeat({cols}, auto auto)")
            styles.setdefault("gap", "8px")
            styles.setdefault("align-items", "center")

        return styles

    def _render_labeled(self) -> str:
        """Render as labeled format (like a definition list)."""
        if len(self) == 0:
            attrs = self._build_attributes()
            if attrs:
                return f"<dl {attrs}></dl>"
            return "<dl></dl>"

        # Get field names
        if self._field_names:
            labels = self._field_names
        else:
            labels = tuple(str(i) for i in range(len(self)))

        # Build container styles for dl
        container_styles = self._get_labeled_container_styles()
        self._styles = container_styles

        # Build content with styled dt/dd
        items_html = []
        dt_style = "margin: 0; font-weight: bold;"
        dd_style = "margin: 0; margin-left: 0;"

        for label, value in zip(labels, self):
            key_html = html.escape(str(label))
            value_html = self._render_item(value)
            items_html.append(f'<dt style="{dt_style}">{key_html}</dt><dd style="{dd_style}">{value_html}</dd>')

        attrs = self._build_attributes()
        if attrs:
            return f"<dl {attrs}>{''.join(items_html)}</dl>"
        return f"<dl>{''.join(items_html)}</dl>"

    def _render_parentheses(self) -> str:
        """Render with parentheses style: (a, b, c)."""
        if len(self) == 0:
            return "<span>()</span>"

        items_html = []
        for item in self:
            items_html.append(self._render_item(item))

        content = ", ".join(items_html)
        attrs = self._build_attributes()

        if attrs:
            return f"<span {attrs}>({content})</span>"
        return f"<span>({content})</span>"

    def _render_plain(self) -> str:
        """Render as plain items in divs."""
        if len(self) == 0:
            attrs = self._build_attributes()
            if attrs:
                return f"<div {attrs}></div>"
            return "<div></div>"

        # Build container styles
        container_styles = self._get_container_styles()
        self._styles = container_styles

        # Build container opening tag
        attrs = self._build_attributes()
        if attrs:
            container_open = f"<div {attrs}>"
        else:
            container_open = "<div>"

        # Render items with commas between them
        total = len(self)
        items_html = []
        for i, item in enumerate(self):
            item_content = self._render_item(item)
            item_attrs = self._build_item_attributes(i, total)
            if item_attrs:
                items_html.append(f"<span {item_attrs}>{item_content}</span>")
            else:
                items_html.append(f"<span>{item_content}</span>")
            # Add comma separator after each item except the last
            if i < total - 1:
                items_html.append("<span>, </span>")

        return f"{container_open}{''.join(items_html)}</div>"

    def render(self) -> str:
        """Return HTML representation of this tuple.

        Returns:
            A string containing valid HTML.
        """
        if self._format == TupleFormat.LABELED:
            return self._render_labeled()
        elif self._format == TupleFormat.PARENTHESES:
            return self._render_parentheses()
        else:  # PLAIN
            return self._render_plain()

    # -------------------------------------------------------------------------
    # Tuple operation overrides
    # -------------------------------------------------------------------------

    def __add__(self, other: tuple[Any, ...]) -> Self:
        """Concatenate tuples, preserving settings."""
        result = HTMLTuple(tuple.__add__(self, other))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._show_parens = self._show_parens
        result._field_names = None  # Concatenation loses field names
        return result  # type: ignore[return-value]

    def __getitem__(self, key: Any) -> Any:  # type: ignore[override]
        """Get item or slice.

        Single index returns the item itself.
        Slice returns a new HTMLTuple with settings preserved.
        """
        result = tuple.__getitem__(self, key)
        if isinstance(key, slice):
            new_tuple = HTMLTuple(result)
            new_tuple._styles = self._styles.copy()
            new_tuple._item_styles = self._item_styles.copy()
            new_tuple._css_classes = self._css_classes.copy()
            new_tuple._item_classes = self._item_classes.copy()
            new_tuple._direction = self._direction
            new_tuple._format = self._format
            new_tuple._grid_columns = self._grid_columns
            new_tuple._separator = self._separator
            new_tuple._show_parens = self._show_parens
            # Slicing loses field name association
            new_tuple._field_names = None
            return new_tuple
        return result

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        items_repr = tuple.__repr__(self)
        extras = []
        if self._field_names:
            extras.append(f"fields={self._field_names}")
        if self._format != TupleFormat.PARENTHESES:
            extras.append(f"format={self._format.value}")
        if self._direction != TupleDirection.HORIZONTAL:
            extras.append(f"direction={self._direction.value}")
        if self._styles:
            extras.append(f"styles={self._styles}")

        if extras:
            return f"HTMLTuple({items_repr}, {', '.join(extras)})"
        return f"HTMLTuple({items_repr})"
