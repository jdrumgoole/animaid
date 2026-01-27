"""HTMLFloat - A float subclass with HTML rendering capabilities."""

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
    from animaid.html_int import HTMLInt


def _to_css(value: object) -> str:
    """Convert a value to its CSS string representation."""
    if hasattr(value, "to_css"):
        return str(value.to_css())
    return str(value)


class HTMLFloat(HTMLObject, float):
    """A float subclass that renders as styled HTML.

    HTMLFloat behaves like a regular Python float but includes methods and
    properties for applying CSS styles, number formatting, and rendering to HTML.

    Examples:
        >>> n = HTMLFloat(3.14159)
        >>> n.bold.red.render()
        '<span style="font-weight: bold; color: red">3.14159</span>'

        >>> HTMLFloat(1234.5678).comma().render()
        '<span>1,234.5678</span>'

        >>> HTMLFloat(0.856).percent().render()
        '<span>85.60%</span>'

        >>> HTMLFloat(3.14159).decimal(2).render()
        '<span>3.14</span>'
    """

    _styles: dict[str, str]
    _css_classes: list[str]
    _tag: str
    _display_format: str
    _format_options: dict[str, object]

    def __new__(cls, value: float = 0.0, **styles: str | CSSValue) -> Self:
        """Create a new HTMLFloat instance.

        Args:
            value: The float value.
            **styles: Initial CSS styles (underscores converted to hyphens).

        Returns:
            A new HTMLFloat instance.
        """
        instance = super().__new__(cls, value)
        return instance

    def __init__(self, value: float = 0.0, **styles: str | CSSValue) -> None:
        """Initialize styles for the HTMLFloat.

        Args:
            value: The float value (handled by __new__).
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
        """Create a copy of this HTMLFloat with modified settings.

        Args:
            new_styles: Styles to merge with existing styles.
            new_classes: Classes to add to existing classes.
            new_tag: New HTML tag to use.
            new_format: New display format.
            new_format_options: New format options.

        Returns:
            A new HTMLFloat with combined settings.
        """
        result = HTMLFloat(float(self))
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
            A new HTMLFloat with the combined styles.
        """
        css_styles = {k.replace("_", "-"): _to_css(v) for k, v in styles.items()}
        return self._copy_with_settings(new_styles=css_styles)

    def add_class(self, *class_names: str) -> Self:
        """Return a copy with additional CSS classes.

        Args:
            *class_names: CSS class names to add.

        Returns:
            A new HTMLFloat with the additional classes.
        """
        return self._copy_with_settings(new_classes=list(class_names))

    def tag(self, tag_name: str) -> Self:
        """Return a copy using a different HTML tag.

        Args:
            tag_name: The HTML tag to use (e.g., "div", "p", "strong").

        Returns:
            A new HTMLFloat using the specified tag.
        """
        return self._copy_with_settings(new_tag=tag_name)

    def _format_value(self) -> str:
        """Format the float value based on display format settings."""
        value = float(self)

        if self._display_format == "comma":
            return f"{value:,}"
        elif self._display_format == "currency":
            symbol = self._format_options.get("symbol", "$")
            decimals = self._format_options.get("decimals", 2)
            return f"{symbol}{value:,.{decimals}f}"
        elif self._display_format == "percent":
            decimals = self._format_options.get("decimals", 2)
            return f"{value * 100:.{decimals}f}%"
        elif self._display_format == "decimal":
            places = self._format_options.get("places", 2)
            return f"{value:.{places}f}"
        elif self._display_format == "scientific":
            precision = self._format_options.get("precision", 2)
            return f"{value:.{precision}e}"
        elif self._display_format == "significant":
            figures = self._format_options.get("figures", 3)
            return f"{value:.{figures}g}"
        else:
            return str(value)

    def render(self) -> str:
        """Return HTML representation of this float.

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
            >>> HTMLFloat(1234567.89).comma().render()
            '<span>1,234,567.89</span>'
        """
        return self._copy_with_settings(new_format="comma")

    def currency(self, symbol: str = "$", decimals: int = 2) -> Self:
        """Return a copy formatted as currency.

        Args:
            symbol: Currency symbol (default "$")
            decimals: Number of decimal places (default 2)

        Examples:
            >>> HTMLFloat(1000.5).currency().render()
            '<span>$1,000.50</span>'
            >>> HTMLFloat(1000.5).currency("€", 0).render()
            '<span>€1,000</span>'
        """
        return self._copy_with_settings(
            new_format="currency",
            new_format_options={"symbol": symbol, "decimals": decimals}
        )

    def percent(self, decimals: int = 2) -> Self:
        """Return a copy formatted as a percentage.

        The value is multiplied by 100 for display.

        Args:
            decimals: Number of decimal places (default 2)

        Examples:
            >>> HTMLFloat(0.856).percent().render()
            '<span>85.60%</span>'
            >>> HTMLFloat(0.5).percent(0).render()
            '<span>50%</span>'
        """
        return self._copy_with_settings(
            new_format="percent",
            new_format_options={"decimals": decimals}
        )

    def decimal(self, places: int = 2) -> Self:
        """Return a copy formatted to a fixed number of decimal places.

        Args:
            places: Number of decimal places (default 2)

        Examples:
            >>> HTMLFloat(3.14159).decimal(2).render()
            '<span>3.14</span>'
            >>> HTMLFloat(3.1).decimal(4).render()
            '<span>3.1000</span>'
        """
        return self._copy_with_settings(
            new_format="decimal",
            new_format_options={"places": places}
        )

    def scientific(self, precision: int = 2) -> Self:
        """Return a copy formatted in scientific notation.

        Args:
            precision: Number of decimal places in mantissa (default 2)

        Examples:
            >>> HTMLFloat(1234567.89).scientific().render()
            '<span>1.23e+06</span>'
        """
        return self._copy_with_settings(
            new_format="scientific",
            new_format_options={"precision": precision}
        )

    def significant(self, figures: int = 3) -> Self:
        """Return a copy formatted to a number of significant figures.

        Args:
            figures: Number of significant figures (default 3)

        Examples:
            >>> HTMLFloat(3.14159).significant(3).render()
            '<span>3.14</span>'
            >>> HTMLFloat(0.00123456).significant(2).render()
            '<span>0.0012</span>'
        """
        return self._copy_with_settings(
            new_format="significant",
            new_format_options={"figures": figures}
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
    # Arithmetic Operations (always return HTMLFloat)
    # -------------------------------------------------------------------------

    def _preserve_settings(self, result: HTMLFloat) -> HTMLFloat:
        """Copy settings to a new HTMLFloat."""
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        result._display_format = self._display_format
        result._format_options = self._format_options.copy()
        return result

    def __add__(self, other: int | float) -> HTMLFloat:
        """Add: HTMLFloat + number."""
        result = HTMLFloat(float(self) + float(other))
        return self._preserve_settings(result)

    def __radd__(self, other: int | float) -> HTMLFloat:
        """Reverse add: number + HTMLFloat."""
        return self.__add__(other)

    def __sub__(self, other: int | float) -> HTMLFloat:
        """Subtract: HTMLFloat - number."""
        result = HTMLFloat(float(self) - float(other))
        return self._preserve_settings(result)

    def __rsub__(self, other: int | float) -> HTMLFloat:
        """Reverse subtract: number - HTMLFloat."""
        result = HTMLFloat(float(other) - float(self))
        return self._preserve_settings(result)

    def __mul__(self, other: int | float) -> HTMLFloat:
        """Multiply: HTMLFloat * number."""
        result = HTMLFloat(float(self) * float(other))
        return self._preserve_settings(result)

    def __rmul__(self, other: int | float) -> HTMLFloat:
        """Reverse multiply: number * HTMLFloat."""
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> HTMLFloat:
        """True divide: HTMLFloat / number."""
        result = HTMLFloat(float(self) / float(other))
        return self._preserve_settings(result)

    def __rtruediv__(self, other: int | float) -> HTMLFloat:
        """Reverse true divide: number / HTMLFloat."""
        result = HTMLFloat(float(other) / float(self))
        return self._preserve_settings(result)

    def __floordiv__(self, other: int | float) -> HTMLFloat:
        """Floor divide: HTMLFloat // number."""
        result = HTMLFloat(float(self) // float(other))
        return self._preserve_settings(result)

    def __rfloordiv__(self, other: int | float) -> HTMLFloat:
        """Reverse floor divide: number // HTMLFloat."""
        result = HTMLFloat(float(other) // float(self))
        return self._preserve_settings(result)

    def __mod__(self, other: int | float) -> HTMLFloat:
        """Modulo: HTMLFloat % number."""
        result = HTMLFloat(float(self) % float(other))
        return self._preserve_settings(result)

    def __rmod__(self, other: int | float) -> HTMLFloat:
        """Reverse modulo: number % HTMLFloat."""
        result = HTMLFloat(float(other) % float(self))
        return self._preserve_settings(result)

    def __pow__(self, other: Any) -> Any:  # type: ignore[override]
        """Power: HTMLFloat ** number."""
        result = HTMLFloat(float(self) ** float(other))
        return self._preserve_settings(result)

    def __neg__(self) -> HTMLFloat:
        """Negate: -HTMLFloat."""
        result = HTMLFloat(-float(self))
        return self._preserve_settings(result)

    def __pos__(self) -> HTMLFloat:
        """Positive: +HTMLFloat."""
        result = HTMLFloat(+float(self))
        return self._preserve_settings(result)

    def __abs__(self) -> HTMLFloat:
        """Absolute value: abs(HTMLFloat)."""
        result = HTMLFloat(abs(float(self)))
        return self._preserve_settings(result)

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        format_info = ""
        if self._display_format != "default":
            format_info = f", format={self._display_format!r}"
        styles_repr = ", ".join(f"{k}={v!r}" for k, v in self._styles.items())
        if styles_repr:
            return f"HTMLFloat({float(self)}{format_info}, {styles_repr})"
        return f"HTMLFloat({float(self)}{format_info})"
