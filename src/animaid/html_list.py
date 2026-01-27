"""HTMLList - A list subclass with HTML rendering capabilities."""

from __future__ import annotations

import html
import uuid
from enum import Enum
from typing import Any, Self

from animaid.css_types import (
    AlignItems,
    Border,
    BorderValue,
    Color,
    ColorValue,
    CSSValue,
    JustifyContent,
    Size,
    SizeValue,
    Spacing,
    SpacingValue,
)
from animaid.html_object import HTMLObject


def _to_css(value: object) -> str:
    """Convert a value to its CSS string representation."""
    if hasattr(value, "to_css"):
        return str(value.to_css())
    return str(value)


class ListDirection(Enum):
    """Direction in which list items are rendered."""

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    VERTICAL_REVERSE = "vertical-reverse"
    HORIZONTAL_REVERSE = "horizontal-reverse"
    GRID = "grid"


class ListType(Enum):
    """Type of HTML list structure."""

    UNORDERED = "ul"  # <ul><li>...</li></ul>
    ORDERED = "ol"  # <ol><li>...</li></ol>
    PLAIN = "div"  # <div><div>...</div></div> with flexbox


class HTMLList(HTMLObject, list):
    """A list subclass that renders as styled HTML.

    HTMLList behaves like a regular Python list but includes
    methods for applying CSS styles and rendering to HTML.
    Supports vertical, horizontal, and grid layouts.

    Examples:
        >>> items = HTMLList(["Apple", "Banana", "Cherry"])
        >>> items.render()
        '<ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>'

        >>> items.horizontal().gap("10px").render()
        '<div style="display: flex; flex-direction: row; gap: 10px">...</div>'

        >>> HTMLList([1, 2, 3]).ordered().render()
        '<ol><li>1</li><li>2</li><li>3</li></ol>'
    """

    _styles: dict[str, str]
    _item_styles: dict[str, str]
    _css_classes: list[str]
    _item_classes: list[str]
    _direction: ListDirection
    _list_type: ListType
    _grid_columns: int | None
    _separator: str | None
    _obs_id: str

    def __init__(self, items: list[Any] | None = None, **styles: str | CSSValue) -> None:
        """Initialize an HTMLList.

        Args:
            items: Initial list items.
            **styles: CSS styles for the container (underscores to hyphens).
                      Accepts both strings and CSS type objects (Color, Size, etc.)
        """
        super().__init__(items or [])
        self._styles = {}
        self._item_styles = {}
        self._css_classes = []
        self._item_classes = []
        self._direction = ListDirection.VERTICAL
        self._list_type = ListType.UNORDERED
        self._grid_columns = None
        self._separator = None
        self._obs_id = str(uuid.uuid4())

        for key, value in styles.items():
            css_key = key.replace("_", "-")
            self._styles[css_key] = _to_css(value)

    def _notify(self) -> None:
        """Publish change notification via pypubsub."""
        try:
            from pubsub import pub
            pub.sendMessage('animaid.changed', obs_id=self._obs_id)
        except ImportError:
            pass  # pypubsub not installed

    def _copy_with_settings(
        self,
        new_styles: dict[str, str] | None = None,
        new_item_styles: dict[str, str] | None = None,
        new_classes: list[str] | None = None,
        new_item_classes: list[str] | None = None,
        new_direction: ListDirection | None = None,
        new_list_type: ListType | None = None,
        new_grid_columns: int | None = None,
        new_separator: str | None = None,
    ) -> Self:
        """Create a copy with modified settings.

        Args:
            new_styles: Container styles to merge.
            new_item_styles: Item styles to merge.
            new_classes: Classes to add to container.
            new_item_classes: Classes to add to items.
            new_direction: New layout direction.
            new_list_type: New list type.
            new_grid_columns: Grid column count.
            new_separator: Separator style between items.

        Returns:
            A new HTMLList with combined settings.
        """
        result = HTMLList(list(self))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._list_type = self._list_type
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._obs_id = self._obs_id  # Preserve ID so updates still work

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
        if new_list_type is not None:
            result._list_type = new_list_type
        if new_grid_columns is not None:
            result._grid_columns = new_grid_columns
        if new_separator is not None:
            result._separator = new_separator

        return result  # type: ignore[return-value]

    # -------------------------------------------------------------------------
    # HTMLObject interface
    # -------------------------------------------------------------------------

    def styled(self, **styles: str | CSSValue) -> Self:
        """Return a copy with additional container styles.

        Args:
            **styles: CSS property-value pairs for the container.
                      Accepts both strings and CSS type objects (Color, Size, etc.)

        Returns:
            A new HTMLList with combined styles.
        """
        css_styles = {k.replace("_", "-"): _to_css(v) for k, v in styles.items()}
        return self._copy_with_settings(new_styles=css_styles)

    def add_class(self, *class_names: str) -> Self:
        """Return a copy with additional CSS classes on the container.

        Args:
            *class_names: CSS class names to add.

        Returns:
            A new HTMLList with additional classes.
        """
        return self._copy_with_settings(new_classes=list(class_names))

    # -------------------------------------------------------------------------
    # Direction methods
    # -------------------------------------------------------------------------

    @property
    def vertical(self) -> Self:
        """Return a copy with vertical layout (default).

        Items are stacked top to bottom.
        """
        return self._copy_with_settings(new_direction=ListDirection.VERTICAL)

    @property
    def horizontal(self) -> Self:
        """Return a copy with horizontal layout.

        Items are arranged left to right using flexbox.
        """
        return self._copy_with_settings(
            new_direction=ListDirection.HORIZONTAL,
            new_list_type=ListType.PLAIN,
        )

    @property
    def vertical_reverse(self) -> Self:
        """Return a copy with reversed vertical layout.

        Items are stacked bottom to top.
        """
        return self._copy_with_settings(
            new_direction=ListDirection.VERTICAL_REVERSE,
            new_list_type=ListType.PLAIN,
        )

    @property
    def horizontal_reverse(self) -> Self:
        """Return a copy with reversed horizontal layout.

        Items are arranged right to left.
        """
        return self._copy_with_settings(
            new_direction=ListDirection.HORIZONTAL_REVERSE,
            new_list_type=ListType.PLAIN,
        )

    def grid(self, columns: int = 3) -> Self:
        """Return a copy with CSS grid layout.

        Args:
            columns: Number of columns in the grid.

        Returns:
            A new HTMLList with grid layout.
        """
        return self._copy_with_settings(
            new_direction=ListDirection.GRID,
            new_list_type=ListType.PLAIN,
            new_grid_columns=columns,
        )

    # -------------------------------------------------------------------------
    # List type methods
    # -------------------------------------------------------------------------

    @property
    def ordered(self) -> Self:
        """Return a copy as an ordered list (<ol>)."""
        return self._copy_with_settings(new_list_type=ListType.ORDERED)

    @property
    def unordered(self) -> Self:
        """Return a copy as an unordered list (<ul>)."""
        return self._copy_with_settings(new_list_type=ListType.UNORDERED)

    @property
    def plain(self) -> Self:
        """Return a copy as a plain div container (no bullets/numbers)."""
        return self._copy_with_settings(new_list_type=ListType.PLAIN)

    # -------------------------------------------------------------------------
    # Spacing methods
    # -------------------------------------------------------------------------

    def gap(self, value: SizeValue) -> Self:
        """Return a copy with specified gap between items.

        Args:
            value: CSS gap value (e.g., "10px", Size.px(10), Size.rem(1)).
        """
        return self.styled(gap=_to_css(value))

    def padding(self, value: SpacingValue) -> Self:
        """Return a copy with padding inside the container.

        Args:
            value: CSS padding value (e.g., "10px", Size.px(10), Spacing.symmetric(10, 20)).
        """
        return self.styled(padding=_to_css(value))

    def margin(self, value: SpacingValue) -> Self:
        """Return a copy with margin outside the container.

        Args:
            value: CSS margin value (e.g., "10px", Size.px(10), Spacing.all(10)).
        """
        return self.styled(margin=_to_css(value))

    def item_padding(self, value: SpacingValue) -> Self:
        """Return a copy with padding inside each item.

        Args:
            value: CSS padding value for items.
        """
        css_styles = {"padding": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def item_margin(self, value: SpacingValue) -> Self:
        """Return a copy with margin around each item.

        Args:
            value: CSS margin value for items.
        """
        css_styles = {"margin": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    # -------------------------------------------------------------------------
    # Border methods
    # -------------------------------------------------------------------------

    def border(self, value: BorderValue) -> Self:
        """Return a copy with border around the container.

        Args:
            value: CSS border value (e.g., "1px solid black", Border(1, BorderStyle.SOLID, Color.black)).
        """
        return self.styled(border=_to_css(value))

    def border_radius(self, value: SizeValue) -> Self:
        """Return a copy with rounded corners on the container.

        Args:
            value: CSS border-radius value (e.g., "5px", Size.px(5)).
        """
        return self.styled(border_radius=_to_css(value))

    def item_border(self, value: BorderValue) -> Self:
        """Return a copy with border around each item.

        Args:
            value: CSS border value for items.
        """
        css_styles = {"border": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def item_border_radius(self, value: SizeValue) -> Self:
        """Return a copy with rounded corners on each item.

        Args:
            value: CSS border-radius value for items.
        """
        css_styles = {"border-radius": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def separator(self, value: BorderValue) -> Self:
        """Return a copy with separator lines between items.

        Unlike item_border, this only adds borders between items,
        not on the outer edges.

        Args:
            value: CSS border value for separators.
        """
        return self._copy_with_settings(new_separator=_to_css(value))

    # -------------------------------------------------------------------------
    # Background and color methods
    # -------------------------------------------------------------------------

    def background(self, value: ColorValue) -> Self:
        """Return a copy with background color on the container.

        Args:
            value: CSS color value (e.g., "white", Color.white, Color.hex("#fff")).
        """
        return self.styled(background_color=_to_css(value))

    def item_background(self, value: ColorValue) -> Self:
        """Return a copy with background color on each item.

        Args:
            value: CSS color value.
        """
        css_styles = {"background-color": _to_css(value)}
        return self._copy_with_settings(new_item_styles=css_styles)

    def color(self, value: ColorValue) -> Self:
        """Return a copy with text color.

        Args:
            value: CSS color value (e.g., "black", Color.black).
        """
        return self.styled(color=_to_css(value))

    # -------------------------------------------------------------------------
    # Item class methods
    # -------------------------------------------------------------------------

    def add_item_class(self, *class_names: str) -> Self:
        """Return a copy with CSS classes added to each item.

        Args:
            *class_names: CSS class names to add to items.
        """
        return self._copy_with_settings(new_item_classes=list(class_names))

    # -------------------------------------------------------------------------
    # Alignment methods
    # -------------------------------------------------------------------------

    def align_items(self, value: AlignItems | str) -> Self:
        """Return a copy with specified cross-axis alignment.

        Args:
            value: CSS align-items value (e.g., "center", AlignItems.CENTER).
        """
        return self.styled(align_items=_to_css(value))

    def justify_content(self, value: JustifyContent | str) -> Self:
        """Return a copy with specified main-axis alignment.

        Args:
            value: CSS justify-content value (e.g., "space-between", JustifyContent.SPACE_BETWEEN).
        """
        return self.styled(justify_content=_to_css(value))

    @property
    def center(self) -> Self:
        """Return a copy with items centered on both axes."""
        return self.styled(align_items="center", justify_content="center")

    # -------------------------------------------------------------------------
    # Size methods
    # -------------------------------------------------------------------------

    def width(self, value: SizeValue) -> Self:
        """Return a copy with specified width.

        Args:
            value: CSS width value (e.g., "100px", Size.px(100), Size.percent(50)).
        """
        return self.styled(width=_to_css(value))

    def height(self, value: SizeValue) -> Self:
        """Return a copy with specified height.

        Args:
            value: CSS height value (e.g., "200px", Size.px(200), Size.vh(100)).
        """
        return self.styled(height=_to_css(value))

    def max_width(self, value: SizeValue) -> Self:
        """Return a copy with maximum width constraint.

        Args:
            value: CSS max-width value (e.g., "800px", Size.px(800)).
        """
        return self.styled(max_width=_to_css(value))

    # -------------------------------------------------------------------------
    # Style Presets (beginner-friendly)
    # -------------------------------------------------------------------------

    @property
    def cards(self) -> Self:
        """Return a copy styled as a card list with shadows and spacing.

        Creates a visually appealing list where each item looks like a card.
        """
        return (
            self.plain
            .horizontal
            .gap("16px")
            .item_padding("16px")
            .item_border("1px solid #e0e0e0")
            .item_border_radius("8px")
            .item_background("white")
            .styled(flex_wrap="wrap")
        )

    @property
    def pills(self) -> Self:
        """Return a copy styled as pill/badge items.

        Creates a horizontal list of pill-shaped items.
        """
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
        """Return a copy styled as tags/labels.

        Creates a horizontal list of tag-style items with a colored left border.
        """
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
    def menu(self) -> Self:
        """Return a copy styled as a vertical menu.

        Creates a clean vertical menu suitable for navigation.
        """
        return (
            self.plain
            .vertical
            .item_padding("12px 16px")
            .separator("1px solid #e0e0e0")
        )

    @property
    def inline(self) -> Self:
        """Return a copy styled as inline items with commas.

        Creates a simple inline list separated by spacing.
        """
        return self.plain.horizontal.gap("8px").styled(flex_wrap="wrap")

    @property
    def numbered(self) -> Self:
        """Return a copy as a numbered list with nice styling."""
        return (
            self.ordered
            .styled(padding_left="24px")
            .item_padding("4px 0")
        )

    @property
    def bulleted(self) -> Self:
        """Return a copy as a bulleted list with nice styling."""
        return (
            self.unordered
            .styled(padding_left="24px")
            .item_padding("4px 0")
        )

    @property
    def spaced(self) -> Self:
        """Return a copy with generous spacing between items."""
        return self.gap("16px").item_padding("8px")

    @property
    def compact(self) -> Self:
        """Return a copy with minimal spacing."""
        return self.gap("4px").item_padding("2px")

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    def _render_item(self, item: Any) -> str:
        """Render a single item to HTML.

        Args:
            item: The item to render.

        Returns:
            HTML string for the item.
        """
        if isinstance(item, HTMLObject):
            return item.render()
        elif isinstance(item, str):
            return html.escape(item)
        else:
            return html.escape(str(item))

    def _get_container_styles(self) -> dict[str, str]:
        """Build the complete container styles including layout."""
        styles = self._styles.copy()

        # Add layout-specific styles
        if self._list_type == ListType.PLAIN:
            if self._direction == ListDirection.HORIZONTAL:
                styles.setdefault("display", "flex")
                styles.setdefault("flex-direction", "row")
                styles.setdefault("flex-wrap", "wrap")
            elif self._direction == ListDirection.HORIZONTAL_REVERSE:
                styles.setdefault("display", "flex")
                styles.setdefault("flex-direction", "row-reverse")
                styles.setdefault("flex-wrap", "wrap")
            elif self._direction == ListDirection.VERTICAL:
                styles.setdefault("display", "flex")
                styles.setdefault("flex-direction", "column")
            elif self._direction == ListDirection.VERTICAL_REVERSE:
                styles.setdefault("display", "flex")
                styles.setdefault("flex-direction", "column-reverse")
            elif self._direction == ListDirection.GRID:
                styles.setdefault("display", "grid")
                cols = self._grid_columns or 3
                styles.setdefault("grid-template-columns", f"repeat({cols}, 1fr)")

        # Remove list styling for ul/ol if needed
        if self._list_type in (ListType.UNORDERED, ListType.ORDERED):
            if self._direction != ListDirection.VERTICAL:
                styles.setdefault("display", "flex")
                styles.setdefault("list-style", "none")
                styles.setdefault("padding-left", "0")
                if self._direction == ListDirection.HORIZONTAL:
                    styles.setdefault("flex-direction", "row")
                elif self._direction == ListDirection.HORIZONTAL_REVERSE:
                    styles.setdefault("flex-direction", "row-reverse")

        return styles

    def _build_item_style_string(self, index: int, total: int) -> str:
        """Build style string for an item, including separators.

        Args:
            index: Item index (0-based).
            total: Total number of items.

        Returns:
            CSS style attribute value.
        """
        styles = self._item_styles.copy()

        # Add separator styles
        if self._separator:
            is_horizontal = self._direction in (
                ListDirection.HORIZONTAL,
                ListDirection.HORIZONTAL_REVERSE,
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

    def render(self) -> str:
        """Return HTML representation of this list.

        Returns:
            A string containing valid HTML.
        """
        if len(self) == 0:
            # Empty list
            container_tag = self._list_type.value
            attrs = self._build_attributes()
            if attrs:
                return f"<{container_tag} {attrs}></{container_tag}>"
            return f"<{container_tag}></{container_tag}>"

        # Build container styles
        container_styles = self._get_container_styles()
        self._styles = container_styles

        # Determine tags
        container_tag = self._list_type.value
        item_tag = "li" if self._list_type in (ListType.UNORDERED, ListType.ORDERED) else "div"

        # Build container opening tag
        attrs = self._build_attributes()
        if attrs:
            container_open = f"<{container_tag} {attrs}>"
        else:
            container_open = f"<{container_tag}>"

        # Render items
        total = len(self)
        items_html = []
        for i, item in enumerate(self):
            item_content = self._render_item(item)
            item_attrs = self._build_item_attributes(i, total)
            if item_attrs:
                items_html.append(f"<{item_tag} {item_attrs}>{item_content}</{item_tag}>")
            else:
                items_html.append(f"<{item_tag}>{item_content}</{item_tag}>")

        return f"{container_open}{''.join(items_html)}</{container_tag}>"

    # -------------------------------------------------------------------------
    # List operation overrides
    # -------------------------------------------------------------------------

    def __add__(self, other: list[Any]) -> Self:
        """Concatenate lists, preserving settings."""
        result = HTMLList(list.__add__(self, other))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._list_type = self._list_type
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._obs_id = self._obs_id
        return result  # type: ignore[return-value]

    def __getitem__(self, key: Any) -> Any:
        """Get item or slice.

        Single index returns the item itself.
        Slice returns a new HTMLList with settings preserved.
        """
        result = list.__getitem__(self, key)
        if isinstance(key, slice):
            new_list = HTMLList(result)
            new_list._styles = self._styles.copy()
            new_list._item_styles = self._item_styles.copy()
            new_list._css_classes = self._css_classes.copy()
            new_list._item_classes = self._item_classes.copy()
            new_list._direction = self._direction
            new_list._list_type = self._list_type
            new_list._grid_columns = self._grid_columns
            new_list._separator = self._separator
            new_list._obs_id = self._obs_id
            return new_list
        return result

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item, notifying observers."""
        super().__setitem__(key, value)
        self._notify()

    def __delitem__(self, key: Any) -> None:
        """Delete item, notifying observers."""
        super().__delitem__(key)
        self._notify()

    def append(self, item: Any) -> None:
        """Append item, notifying observers."""
        super().append(item)
        self._notify()

    def extend(self, items: Any) -> None:
        """Extend list, notifying observers."""
        super().extend(items)
        self._notify()

    def insert(self, index: Any, item: Any) -> None:
        """Insert item, notifying observers."""
        super().insert(index, item)
        self._notify()

    def remove(self, item: Any) -> None:
        """Remove item, notifying observers."""
        super().remove(item)
        self._notify()

    def pop(self, index: Any = -1) -> Any:
        """Pop item, notifying observers."""
        result = super().pop(index)
        self._notify()
        return result

    def clear(self) -> None:
        """Clear list, notifying observers."""
        super().clear()
        self._notify()

    def sort(self, *, key: Any = None, reverse: bool = False) -> None:
        """Sort list, notifying observers."""
        super().sort(key=key, reverse=reverse)
        self._notify()

    def reverse(self) -> None:
        """Reverse list, notifying observers."""
        super().reverse()
        self._notify()

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        items_repr = list.__repr__(self)
        extras = []
        if self._direction != ListDirection.VERTICAL:
            extras.append(f"direction={self._direction.value}")
        if self._list_type != ListType.UNORDERED:
            extras.append(f"type={self._list_type.value}")
        if self._styles:
            extras.append(f"styles={self._styles}")

        if extras:
            return f"HTMLList({items_repr}, {', '.join(extras)})"
        return f"HTMLList({items_repr})"
