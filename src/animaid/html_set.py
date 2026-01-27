"""HTMLSet - A set subclass with HTML rendering capabilities."""

from __future__ import annotations

import html
import uuid
from enum import Enum
from typing import Any, Iterable, Self

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


class SetDirection(Enum):
    """Direction in which set items are rendered."""

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    VERTICAL_REVERSE = "vertical-reverse"
    HORIZONTAL_REVERSE = "horizontal-reverse"
    GRID = "grid"


class SetFormat(Enum):
    """Format for displaying set items."""

    PLAIN = "plain"  # Just items in divs
    BRACES = "braces"  # {a, b, c} style


class HTMLSet(HTMLObject, set):
    """A set subclass that renders as styled HTML.

    HTMLSet behaves like a regular Python set but includes
    methods for applying CSS styles and rendering to HTML.
    Items are automatically deduplicated (set behavior).
    Mutations trigger notifications for reactive updates.

    Examples:
        >>> s = HTMLSet({1, 2, 3})
        >>> s.render()
        '<span>{1, 2, 3}</span>'

        >>> s.horizontal.pills.render()
        '<div style="display: flex; ...">...</div>'

        >>> HTMLSet([1, 1, 2, 2, 3])  # Duplicates removed
        HTMLSet({1, 2, 3})
    """

    _styles: dict[str, str]
    _item_styles: dict[str, str]
    _css_classes: list[str]
    _item_classes: list[str]
    _direction: SetDirection
    _format: SetFormat
    _grid_columns: int | None
    _separator: str | None
    _sorted: bool
    _obs_id: str

    def __init__(self, items: Iterable[Any] = (), **styles: str | CSSValue) -> None:
        """Initialize an HTMLSet.

        Args:
            items: The set items (any iterable, duplicates removed).
            **styles: CSS styles for the container.
        """
        super().__init__(items)
        self._styles = {}
        self._item_styles = {}
        self._css_classes = []
        self._item_classes = []
        self._direction = SetDirection.HORIZONTAL
        self._format = SetFormat.BRACES
        self._grid_columns = None
        self._separator = None
        self._sorted = False
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
        new_direction: SetDirection | None = None,
        new_format: SetFormat | None = None,
        new_grid_columns: int | None = None,
        new_separator: str | None = None,
        new_sorted: bool | None = None,
    ) -> Self:
        """Create a copy with modified settings."""
        result = HTMLSet(self)
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._sorted = self._sorted
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
        if new_format is not None:
            result._format = new_format
        if new_grid_columns is not None:
            result._grid_columns = new_grid_columns
        if new_separator is not None:
            result._separator = new_separator
        if new_sorted is not None:
            result._sorted = new_sorted

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
        """Return a copy without brace decoration."""
        return self._copy_with_settings(new_format=SetFormat.PLAIN)

    @property
    def braces(self) -> Self:
        """Return a copy with braces around items (default)."""
        return self._copy_with_settings(new_format=SetFormat.BRACES)

    # -------------------------------------------------------------------------
    # Ordering methods
    # -------------------------------------------------------------------------

    @property
    def sorted(self) -> Self:
        """Return a copy that renders items in sorted order."""
        return self._copy_with_settings(new_sorted=True)

    @property
    def unsorted(self) -> Self:
        """Return a copy that renders items in iteration order."""
        return self._copy_with_settings(new_sorted=False)

    # -------------------------------------------------------------------------
    # Direction methods
    # -------------------------------------------------------------------------

    @property
    def vertical(self) -> Self:
        """Return a copy with vertical layout."""
        return self._copy_with_settings(new_direction=SetDirection.VERTICAL)

    @property
    def horizontal(self) -> Self:
        """Return a copy with horizontal layout (default)."""
        return self._copy_with_settings(new_direction=SetDirection.HORIZONTAL)

    @property
    def vertical_reverse(self) -> Self:
        """Return a copy with reversed vertical layout."""
        return self._copy_with_settings(new_direction=SetDirection.VERTICAL_REVERSE)

    @property
    def horizontal_reverse(self) -> Self:
        """Return a copy with reversed horizontal layout."""
        return self._copy_with_settings(new_direction=SetDirection.HORIZONTAL_REVERSE)

    def grid(self, columns: int = 3) -> Self:
        """Return a copy with CSS grid layout."""
        return self._copy_with_settings(
            new_direction=SetDirection.GRID,
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

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    def _get_items(self) -> list[Any]:
        """Get items in render order."""
        items = list(self)
        if self._sorted:
            try:
                items = sorted(items, key=str)
            except TypeError:
                # If items can't be sorted, keep original order
                pass
        return items

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

        if self._format != SetFormat.BRACES:
            # Flexbox/grid layout for non-brace formats
            if self._direction == SetDirection.HORIZONTAL:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "row")
                styles.setdefault("align-items", "center")
            elif self._direction == SetDirection.HORIZONTAL_REVERSE:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "row-reverse")
                styles.setdefault("align-items", "center")
            elif self._direction == SetDirection.VERTICAL:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "column")
            elif self._direction == SetDirection.VERTICAL_REVERSE:
                styles.setdefault("display", "inline-flex")
                styles.setdefault("flex-direction", "column-reverse")
            elif self._direction == SetDirection.GRID:
                styles.setdefault("display", "inline-grid")
                cols = self._grid_columns or 3
                styles.setdefault("grid-template-columns", f"repeat({cols}, 1fr)")

        return styles

    def _build_item_style_string(self, index: int, total: int) -> str:
        """Build style string for an item, including separators."""
        styles = self._item_styles.copy()

        if self._separator:
            is_horizontal = self._direction in (
                SetDirection.HORIZONTAL,
                SetDirection.HORIZONTAL_REVERSE,
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

    def _render_braces(self) -> str:
        """Render with braces style: {a, b, c}."""
        items = self._get_items()

        if len(items) == 0:
            return "<span>{}</span>"

        items_html = []
        for item in items:
            items_html.append(self._render_item(item))

        content = ", ".join(items_html)
        attrs = self._build_attributes()

        if attrs:
            return f"<span {attrs}>{{{content}}}</span>"
        return f"<span>{{{content}}}</span>"

    def _render_plain(self) -> str:
        """Render as plain items in divs."""
        items = self._get_items()

        if len(items) == 0:
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
        total = len(items)
        items_html = []
        for i, item in enumerate(items):
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
        """Return HTML representation of this set.

        Returns:
            A string containing valid HTML.
        """
        if self._format == SetFormat.BRACES:
            return self._render_braces()
        else:  # PLAIN
            return self._render_plain()

    # -------------------------------------------------------------------------
    # Set operation overrides (non-mutating, return new sets)
    # -------------------------------------------------------------------------

    def union(self, *others: Iterable[Any]) -> Self:
        """Return union with other sets, preserving settings."""
        result = HTMLSet(set.union(self, *others))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._sorted = self._sorted
        result._obs_id = self._obs_id
        return result  # type: ignore[return-value]

    def intersection(self, *others: Iterable[Any]) -> Self:
        """Return intersection with other sets, preserving settings."""
        result = HTMLSet(set.intersection(self, *others))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._sorted = self._sorted
        result._obs_id = self._obs_id
        return result  # type: ignore[return-value]

    def difference(self, *others: Iterable[Any]) -> Self:
        """Return difference with other sets, preserving settings."""
        result = HTMLSet(set.difference(self, *others))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._sorted = self._sorted
        result._obs_id = self._obs_id
        return result  # type: ignore[return-value]

    def symmetric_difference(self, other: Iterable[Any]) -> Self:
        """Return symmetric difference with other set, preserving settings."""
        result = HTMLSet(set.symmetric_difference(self, other))
        result._styles = self._styles.copy()
        result._item_styles = self._item_styles.copy()
        result._css_classes = self._css_classes.copy()
        result._item_classes = self._item_classes.copy()
        result._direction = self._direction
        result._format = self._format
        result._grid_columns = self._grid_columns
        result._separator = self._separator
        result._sorted = self._sorted
        result._obs_id = self._obs_id
        return result  # type: ignore[return-value]

    def __or__(self, other: Iterable[Any]) -> Self:
        """Union operator |."""
        return self.union(other)

    def __and__(self, other: Iterable[Any]) -> Self:
        """Intersection operator &."""
        return self.intersection(other)

    def __sub__(self, other: Iterable[Any]) -> Self:
        """Difference operator -."""
        return self.difference(other)

    def __xor__(self, other: Iterable[Any]) -> Self:
        """Symmetric difference operator ^."""
        return self.symmetric_difference(other)

    # -------------------------------------------------------------------------
    # Observable mutating methods
    # -------------------------------------------------------------------------

    def add(self, item: Any) -> None:
        """Add item, notifying observers."""
        super().add(item)
        self._notify()

    def discard(self, item: Any) -> None:
        """Discard item, notifying observers."""
        super().discard(item)
        self._notify()

    def remove(self, item: Any) -> None:
        """Remove item, notifying observers."""
        super().remove(item)
        self._notify()

    def pop(self) -> Any:
        """Pop item, notifying observers."""
        result = super().pop()
        self._notify()
        return result

    def clear(self) -> None:
        """Clear set, notifying observers."""
        super().clear()
        self._notify()

    def update(self, *others: Iterable[Any]) -> None:
        """Update set, notifying observers."""
        super().update(*others)
        self._notify()

    def intersection_update(self, *others: Iterable[Any]) -> None:
        """Intersection update, notifying observers."""
        super().intersection_update(*others)
        self._notify()

    def difference_update(self, *others: Iterable[Any]) -> None:
        """Difference update, notifying observers."""
        super().difference_update(*others)
        self._notify()

    def symmetric_difference_update(self, other: Iterable[Any]) -> None:
        """Symmetric difference update, notifying observers."""
        super().symmetric_difference_update(other)
        self._notify()

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        items_repr = set.__repr__(set(self))
        extras = []
        if self._format != SetFormat.BRACES:
            extras.append(f"format={self._format.value}")
        if self._direction != SetDirection.HORIZONTAL:
            extras.append(f"direction={self._direction.value}")
        if self._sorted:
            extras.append("sorted=True")
        if self._styles:
            extras.append(f"styles={self._styles}")

        if extras:
            return f"HTMLSet({items_repr}, {', '.join(extras)})"
        return f"HTMLSet({items_repr})"
