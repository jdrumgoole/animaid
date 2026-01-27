"""HTMLInt - An int subclass with HTML rendering capabilities."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING, Any, Self

from animaid.css_types import (
    Border,
    BorderValue,
    Color,
    ColorValue,
    CSSValue,
    Display,
    Size,
    SizeValue,
    Spacing,
    SpacingValue,
)
from animaid.html_object import HTMLObject

if TYPE_CHECKING:
    from animaid.html_float import HTMLFloat


def _to_css(value: object) -> str:
    """Convert a value to its CSS string representation."""
    if hasattr(value, "to_css"):
        return str(value.to_css())
    return str(value)


class HTMLInt(HTMLObject, int):
    """An int subclass that renders as styled HTML.

    HTMLInt behaves like a regular Python int but includes methods and
    properties for applying CSS styles, number formatting, and rendering to HTML.

    Examples:
        >>> n = HTMLInt(42)
        >>> n.bold.red.render()
        '<span style="font-weight: bold; color: red">42</span>'

        >>> HTMLInt(1234567).comma().render()
        '<span>1,234,567</span>'

        >>> HTMLInt(1000).currency("$").bold.render()
        '<span style="font-weight: bold">$1,000</span>'

        >>> HTMLInt(1).ordinal().render()
        '<span>1st</span>'
    """

    _styles: dict[str, str]
    _css_classes: list[str]
    _tag: str
    _display_format: str
    _format_options: dict[str, object]

    def __new__(cls, value: int = 0, **styles: str | CSSValue) -> Self:
        """Create a new HTMLInt instance.

        Args:
            value: The integer value.
            **styles: Initial CSS styles (underscores converted to hyphens).

        Returns:
            A new HTMLInt instance.
        """
        instance = super().__new__(cls, value)
        return instance

    def __init__(self, value: int = 0, **styles: str | CSSValue) -> None:
        """Initialize styles for the HTMLInt.

        Args:
            value: The integer value (handled by __new__).
            **styles: CSS property-value pairs.
        """
        self._styles = {}
        self._css_classes = []
        self._tag = "span"
        self._display_format = "default"
        self._format_options = {}

        for key, val in styles.items():
            css_key = key.replace("_", "-")
            self._styles[css_key] = _to_css(val)

    def _copy_with_settings(
        self,
        new_styles: dict[str, str] | None = None,
        new_classes: list[str] | None = None,
        new_tag: str | None = None,
        new_format: str | None = None,
        new_format_options: dict[str, object] | None = None,
    ) -> Self:
        """Create a copy of this HTMLInt with modified settings.

        Args:
            new_styles: Styles to merge with existing styles.
            new_classes: Classes to add to existing classes.
            new_tag: New HTML tag to use.
            new_format: New display format.
            new_format_options: New format options.

        Returns:
            A new HTMLInt with combined settings.
        """
        result = HTMLInt(int(self))
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        result._display_format = self._display_format
        result._format_options = self._format_options.copy()

        if new_styles:
            result._styles.update(new_styles)
        if new_classes:
            result._css_classes.extend(new_classes)
        if new_tag:
            result._tag = new_tag
        if new_format:
            result._display_format = new_format
        if new_format_options:
            result._format_options.update(new_format_options)

        return result  # type: ignore[return-value]

    def styled(self, **styles: str | CSSValue) -> Self:
        """Return a copy with additional inline styles.

        Args:
            **styles: CSS property-value pairs.

        Returns:
            A new HTMLInt with the combined styles.
        """
        css_styles = {k.replace("_", "-"): _to_css(v) for k, v in styles.items()}
        return self._copy_with_settings(new_styles=css_styles)

    def add_class(self, *class_names: str) -> Self:
        """Return a copy with additional CSS classes.

        Args:
            *class_names: CSS class names to add.

        Returns:
            A new HTMLInt with the additional classes.
        """
        return self._copy_with_settings(new_classes=list(class_names))

    def tag(self, tag_name: str) -> Self:
        """Return a copy using a different HTML tag.

        Args:
            tag_name: The HTML tag to use (e.g., "div", "p", "strong").

        Returns:
            A new HTMLInt using the specified tag.
        """
        return self._copy_with_settings(new_tag=tag_name)

    def _format_value(self) -> str:
        """Format the integer value based on display format settings."""
        value = int(self)

        if self._display_format == "comma":
            return f"{value:,}"
        elif self._display_format == "currency":
            symbol = self._format_options.get("symbol", "$")
            return f"{symbol}{value:,}"
        elif self._display_format == "percent":
            return f"{value}%"
        elif self._display_format == "ordinal":
            return self._to_ordinal(value)
        elif self._display_format == "padded":
            width = self._format_options.get("width", 2)
            return f"{value:0{width}d}"
        else:
            return str(value)

    @staticmethod
    def _to_ordinal(n: int) -> str:
        """Convert an integer to its ordinal string (1st, 2nd, 3rd, etc.)."""
        if 11 <= abs(n) % 100 <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs(n) % 10, "th")
        return f"{n}{suffix}"

    def render(self) -> str:
        """Return HTML representation of this integer.

        Returns:
            A string containing valid HTML.
        """
        content = html.escape(self._format_value())
        attrs = self._build_attributes()

        if attrs:
            return f"<{self._tag} {attrs}>{content}</{self._tag}>"
        else:
            return f"<{self._tag}>{content}</{self._tag}>"

    # -------------------------------------------------------------------------
    # Number Formatting Methods
    # -------------------------------------------------------------------------

    def comma(self) -> Self:
        """Return a copy formatted with thousand separators.

        Examples:
            >>> HTMLInt(1234567).comma().render()
            '<span>1,234,567</span>'
        """
        return self._copy_with_settings(new_format="comma")

    def currency(self, symbol: str = "$") -> Self:
        """Return a copy formatted as currency.

        Args:
            symbol: Currency symbol (default "$")

        Examples:
            >>> HTMLInt(1000).currency().render()
            '<span>$1,000</span>'
            >>> HTMLInt(1000).currency("€").render()
            '<span>€1,000</span>'
        """
        return self._copy_with_settings(
            new_format="currency",
            new_format_options={"symbol": symbol}
        )

    def percent(self) -> Self:
        """Return a copy formatted as a percentage.

        Examples:
            >>> HTMLInt(85).percent().render()
            '<span>85%</span>'
        """
        return self._copy_with_settings(new_format="percent")

    def ordinal(self) -> Self:
        """Return a copy formatted as an ordinal (1st, 2nd, 3rd, etc.).

        Examples:
            >>> HTMLInt(1).ordinal().render()
            '<span>1st</span>'
            >>> HTMLInt(22).ordinal().render()
            '<span>22nd</span>'
        """
        return self._copy_with_settings(new_format="ordinal")

    def padded(self, width: int = 2) -> Self:
        """Return a copy zero-padded to the specified width.

        Args:
            width: Minimum width (default 2)

        Examples:
            >>> HTMLInt(7).padded(3).render()
            '<span>007</span>'
        """
        return self._copy_with_settings(
            new_format="padded",
            new_format_options={"width": width}
        )

    # -------------------------------------------------------------------------
    # Style Properties (no-argument styles)
    # -------------------------------------------------------------------------

    @property
    def bold(self) -> Self:
        """Return a copy with bold text."""
        return self.styled(font_weight="bold")

    @property
    def italic(self) -> Self:
        """Return a copy with italic text."""
        return self.styled(font_style="italic")

    @property
    def underline(self) -> Self:
        """Return a copy with underlined text."""
        return self.styled(text_decoration="underline")

    @property
    def strikethrough(self) -> Self:
        """Return a copy with strikethrough text."""
        return self.styled(text_decoration="line-through")

    @property
    def monospace(self) -> Self:
        """Return a copy with monospace font."""
        return self.styled(font_family="monospace")

    # -------------------------------------------------------------------------
    # Color Shortcuts
    # -------------------------------------------------------------------------

    @property
    def red(self) -> Self:
        """Return a copy with red text."""
        return self.color("red")

    @property
    def blue(self) -> Self:
        """Return a copy with blue text."""
        return self.color("blue")

    @property
    def green(self) -> Self:
        """Return a copy with green text."""
        return self.color("green")

    @property
    def yellow(self) -> Self:
        """Return a copy with yellow text."""
        return self.color("#b8860b")

    @property
    def orange(self) -> Self:
        """Return a copy with orange text."""
        return self.color("orange")

    @property
    def purple(self) -> Self:
        """Return a copy with purple text."""
        return self.color("purple")

    @property
    def gray(self) -> Self:
        """Return a copy with gray text."""
        return self.color("gray")

    @property
    def white(self) -> Self:
        """Return a copy with white text."""
        return self.color("white")

    @property
    def black(self) -> Self:
        """Return a copy with black text."""
        return self.color("black")

    # -------------------------------------------------------------------------
    # Size Shortcuts
    # -------------------------------------------------------------------------

    @property
    def xs(self) -> Self:
        """Return a copy with extra-small text (12px)."""
        return self.font_size("12px")

    @property
    def small(self) -> Self:
        """Return a copy with small text (14px)."""
        return self.font_size("14px")

    @property
    def medium(self) -> Self:
        """Return a copy with medium text (16px)."""
        return self.font_size("16px")

    @property
    def large(self) -> Self:
        """Return a copy with large text (20px)."""
        return self.font_size("20px")

    @property
    def xl(self) -> Self:
        """Return a copy with extra-large text (24px)."""
        return self.font_size("24px")

    @property
    def xxl(self) -> Self:
        """Return a copy with 2x extra-large text (32px)."""
        return self.font_size("32px")

    # -------------------------------------------------------------------------
    # Style Presets
    # -------------------------------------------------------------------------

    @property
    def success(self) -> Self:
        """Return a copy styled for success (green)."""
        return self.styled(color="#2e7d32", background_color="#e8f5e9", padding="2px 6px", border_radius="4px")

    @property
    def warning(self) -> Self:
        """Return a copy styled for warning (orange)."""
        return self.styled(color="#e65100", background_color="#fff3e0", padding="2px 6px", border_radius="4px")

    @property
    def error(self) -> Self:
        """Return a copy styled for error (red)."""
        return self.styled(color="#c62828", background_color="#ffebee", padding="2px 6px", border_radius="4px")

    @property
    def info(self) -> Self:
        """Return a copy styled for info (blue)."""
        return self.styled(color="#1565c0", background_color="#e3f2fd", padding="2px 6px", border_radius="4px")

    @property
    def badge(self) -> Self:
        """Return a copy styled as a badge/pill."""
        return self.styled(
            background_color="#e0e0e0",
            padding="4px 10px",
            border_radius="12px",
            font_size="0.85em",
            font_weight="500",
        )

    # -------------------------------------------------------------------------
    # Style Methods (require value arguments)
    # -------------------------------------------------------------------------

    def color(self, value: ColorValue) -> Self:
        """Return a copy with the specified text color."""
        return self.styled(color=_to_css(value))

    def background(self, value: ColorValue) -> Self:
        """Return a copy with the specified background color."""
        return self.styled(background_color=_to_css(value))

    def font_size(self, value: SizeValue) -> Self:
        """Return a copy with the specified font size."""
        return self.styled(font_size=_to_css(value))

    def padding(self, value: SpacingValue) -> Self:
        """Return a copy with the specified padding."""
        return self.styled(padding=_to_css(value))

    def margin(self, value: SpacingValue) -> Self:
        """Return a copy with the specified margin."""
        return self.styled(margin=_to_css(value))

    def border(self, value: BorderValue) -> Self:
        """Return a copy with the specified border."""
        return self.styled(border=_to_css(value))

    def border_radius(self, value: SizeValue) -> Self:
        """Return a copy with the specified border radius."""
        return self.styled(border_radius=_to_css(value))

    # -------------------------------------------------------------------------
    # Arithmetic Operations (return HTMLInt or HTMLFloat)
    # -------------------------------------------------------------------------

    def _preserve_settings(self, result: HTMLInt | HTMLFloat) -> HTMLInt | HTMLFloat:
        """Copy settings to a new HTMLInt or HTMLFloat."""
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        result._display_format = self._display_format
        result._format_options = self._format_options.copy()
        return result

    def __add__(self, other: Any) -> Any:  # type: ignore[override]
        """Add: HTMLInt + number."""
        from animaid.html_float import HTMLFloat
        result: Any
        if isinstance(other, float) and not isinstance(other, int):
            result = HTMLFloat(int(self) + other)
            return self._preserve_settings(result)
        elif isinstance(other, HTMLFloat):
            result = HTMLFloat(int(self) + float(other))
            return self._preserve_settings(result)
        else:
            result = HTMLInt(int.__add__(self, int(other)))
            return self._preserve_settings(result)

    def __radd__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse add: number + HTMLInt."""
        return self.__add__(other)

    def __sub__(self, other: Any) -> Any:  # type: ignore[override]
        """Subtract: HTMLInt - number."""
        from animaid.html_float import HTMLFloat
        result: Any
        if isinstance(other, float) and not isinstance(other, int):
            result = HTMLFloat(int(self) - other)
            return self._preserve_settings(result)
        elif isinstance(other, HTMLFloat):
            result = HTMLFloat(int(self) - float(other))
            return self._preserve_settings(result)
        else:
            result = HTMLInt(int.__sub__(self, int(other)))
            return self._preserve_settings(result)

    def __rsub__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse subtract: number - HTMLInt."""
        from animaid.html_float import HTMLFloat
        result: Any
        if isinstance(other, float):
            result = HTMLFloat(other - int(self))
            return self._preserve_settings(result)
        else:
            result = HTMLInt(other - int(self))
            return self._preserve_settings(result)

    def __mul__(self, other: Any) -> Any:  # type: ignore[override]
        """Multiply: HTMLInt * number."""
        from animaid.html_float import HTMLFloat
        result: Any
        if isinstance(other, float) and not isinstance(other, int):
            result = HTMLFloat(int(self) * other)
            return self._preserve_settings(result)
        elif isinstance(other, HTMLFloat):
            result = HTMLFloat(int(self) * float(other))
            return self._preserve_settings(result)
        else:
            result = HTMLInt(int.__mul__(self, int(other)))
            return self._preserve_settings(result)

    def __rmul__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse multiply: number * HTMLInt."""
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Any:  # type: ignore[override]
        """True divide: HTMLInt / number (always returns HTMLFloat)."""
        from animaid.html_float import HTMLFloat
        result = HTMLFloat(int(self) / other)
        return self._preserve_settings(result)

    def __rtruediv__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse true divide: number / HTMLInt."""
        from animaid.html_float import HTMLFloat
        result = HTMLFloat(other / int(self))
        return self._preserve_settings(result)

    def __floordiv__(self, other: Any) -> Any:  # type: ignore[override]
        """Floor divide: HTMLInt // number."""
        result = HTMLInt(int(self) // int(other))
        return self._preserve_settings(result)

    def __rfloordiv__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse floor divide: number // HTMLInt."""
        result = HTMLInt(int(other) // int(self))
        return self._preserve_settings(result)

    def __mod__(self, other: Any) -> Any:  # type: ignore[override]
        """Modulo: HTMLInt % number."""
        result = HTMLInt(int.__mod__(self, other))
        return self._preserve_settings(result)

    def __rmod__(self, other: Any) -> Any:  # type: ignore[override]
        """Reverse modulo: number % HTMLInt."""
        result = HTMLInt(other % int(self))
        return self._preserve_settings(result)

    def __pow__(self, other: Any) -> Any:  # type: ignore[override]
        """Power: HTMLInt ** number."""
        result = HTMLInt(int.__pow__(self, other))
        return self._preserve_settings(result)

    def __neg__(self) -> Any:
        """Negate: -HTMLInt."""
        result = HTMLInt(-int(self))
        return self._preserve_settings(result)

    def __pos__(self) -> Any:
        """Positive: +HTMLInt."""
        result = HTMLInt(+int(self))
        return self._preserve_settings(result)

    def __abs__(self) -> Any:
        """Absolute value: abs(HTMLInt)."""
        result = HTMLInt(abs(int(self)))
        return self._preserve_settings(result)

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        format_info = ""
        if self._display_format != "default":
            format_info = f", format={self._display_format!r}"
        styles_repr = ", ".join(f"{k}={v!r}" for k, v in self._styles.items())
        if styles_repr:
            return f"HTMLInt({int(self)}{format_info}, {styles_repr})"
        return f"HTMLInt({int(self)}{format_info})"
