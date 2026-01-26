"""HTMLString - A str subclass with HTML rendering capabilities."""

from __future__ import annotations

import html
from typing import Self

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


def _to_css(value: object) -> str:
    """Convert a value to its CSS string representation."""
    if hasattr(value, "to_css"):
        return value.to_css()
    return str(value)


class HTMLString(HTMLObject, str):
    """A string subclass that renders as styled HTML.

    HTMLString behaves like a regular Python string but includes
    methods and properties for applying CSS styles and rendering
    to HTML.

    Examples:
        >>> s = HTMLString("Hello World")
        >>> s.bold.color("red").render()
        '<span style="font-weight: bold; color: red">Hello World</span>'

        >>> s = HTMLString("Click me", color="blue", text_decoration="underline")
        >>> s.render()
        '<span style="color: blue; text-decoration: underline">Click me</span>'
    """

    _styles: dict[str, str]
    _css_classes: list[str]
    _tag: str

    def __new__(cls, content: str = "", **styles: str | CSSValue) -> Self:
        """Create a new HTMLString instance.

        Args:
            content: The string content.
            **styles: Initial CSS styles (underscores converted to hyphens).
                      Accepts both strings and CSS type objects (Color, Size, etc.)

        Returns:
            A new HTMLString instance.
        """
        instance = super().__new__(cls, content)
        return instance

    def __init__(self, content: str = "", **styles: str | CSSValue) -> None:
        """Initialize styles for the HTMLString.

        Args:
            content: The string content (handled by __new__).
            **styles: CSS property-value pairs, e.g., font_size="16px" or font_size=Size.px(16)
                      Accepts both strings and CSS type objects (Color, Size, Border, Spacing, etc.)
        """
        self._styles = {}
        self._css_classes = []
        self._tag = "span"

        for key, value in styles.items():
            css_key = key.replace("_", "-")
            self._styles[css_key] = _to_css(value)

    def _copy_with_styles(
        self,
        new_styles: dict[str, str] | None = None,
        new_classes: list[str] | None = None,
        new_tag: str | None = None,
    ) -> Self:
        """Create a copy of this HTMLString with modified styles.

        Args:
            new_styles: Styles to merge with existing styles.
            new_classes: Classes to add to existing classes.
            new_tag: New HTML tag to use.

        Returns:
            A new HTMLString with combined styles/classes.
        """
        result = HTMLString(str(self))
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag

        if new_styles:
            result._styles.update(new_styles)
        if new_classes:
            result._css_classes.extend(new_classes)
        if new_tag:
            result._tag = new_tag

        return result  # type: ignore[return-value]

    def styled(self, **styles: str | CSSValue) -> Self:
        """Return a copy with additional inline styles.

        Style names use Python convention (underscores) and are
        converted to CSS convention (hyphens) automatically.

        Args:
            **styles: CSS property-value pairs. Accepts both strings and CSS type objects.
                      e.g., font_size="16px" or font_size=Size.px(16)

        Returns:
            A new HTMLString with the combined styles.

        Example:
            >>> s = HTMLString("Hello").styled(color="red", font_size="20px")
            >>> s.render()
            '<span style="color: red; font-size: 20px">Hello</span>'

            >>> s = HTMLString("Hello").styled(color=Color.red, font_size=Size.px(20))
            >>> s.render()
            '<span style="color: red; font-size: 20px">Hello</span>'
        """
        css_styles = {k.replace("_", "-"): _to_css(v) for k, v in styles.items()}
        return self._copy_with_styles(new_styles=css_styles)

    def add_class(self, *class_names: str) -> Self:
        """Return a copy with additional CSS classes.

        Args:
            *class_names: CSS class names to add.

        Returns:
            A new HTMLString with the additional classes.

        Example:
            >>> s = HTMLString("Hello").add_class("highlight", "important")
            >>> s.render()
            '<span class="highlight important">Hello</span>'
        """
        return self._copy_with_styles(new_classes=list(class_names))

    def tag(self, tag_name: str) -> Self:
        """Return a copy using a different HTML tag.

        Args:
            tag_name: The HTML tag to use (e.g., "div", "p", "strong").

        Returns:
            A new HTMLString using the specified tag.

        Example:
            >>> s = HTMLString("Hello").tag("strong").render()
            '<strong>Hello</strong>'
        """
        return self._copy_with_styles(new_tag=tag_name)

    def render(self) -> str:
        """Return HTML representation of this string.

        The string content is HTML-escaped to prevent XSS.

        Returns:
            A string containing valid HTML.

        Example:
            >>> HTMLString("<script>alert('xss')</script>").render()
            '<span>&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;</span>'
        """
        escaped_content = html.escape(str(self))
        attrs = self._build_attributes()

        if attrs:
            return f"<{self._tag} {attrs}>{escaped_content}</{self._tag}>"
        else:
            return f"<{self._tag}>{escaped_content}</{self._tag}>"

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
    def uppercase(self) -> Self:
        """Return a copy with uppercase text."""
        return self.styled(text_transform="uppercase")

    @property
    def lowercase(self) -> Self:
        """Return a copy with lowercase text."""
        return self.styled(text_transform="lowercase")

    @property
    def capitalize(self) -> Self:
        """Return a copy with capitalized text."""
        return self.styled(text_transform="capitalize")

    @property
    def nowrap(self) -> Self:
        """Return a copy that prevents text wrapping."""
        return self.styled(white_space="nowrap")

    @property
    def monospace(self) -> Self:
        """Return a copy with monospace font."""
        return self.styled(font_family="monospace")

    # -------------------------------------------------------------------------
    # Color Shortcuts (beginner-friendly)
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
        return self.color("#b8860b")  # Dark golden for readability

    @property
    def orange(self) -> Self:
        """Return a copy with orange text."""
        return self.color("orange")

    @property
    def purple(self) -> Self:
        """Return a copy with purple text."""
        return self.color("purple")

    @property
    def pink(self) -> Self:
        """Return a copy with pink text."""
        return self.color("deeppink")

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
    # Background Color Shortcuts (beginner-friendly)
    # -------------------------------------------------------------------------

    @property
    def bg_red(self) -> Self:
        """Return a copy with red background."""
        return self.background("#ffebee")

    @property
    def bg_blue(self) -> Self:
        """Return a copy with blue background."""
        return self.background("#e3f2fd")

    @property
    def bg_green(self) -> Self:
        """Return a copy with green background."""
        return self.background("#e8f5e9")

    @property
    def bg_yellow(self) -> Self:
        """Return a copy with yellow background."""
        return self.background("#fffde7")

    @property
    def bg_orange(self) -> Self:
        """Return a copy with orange background."""
        return self.background("#fff3e0")

    @property
    def bg_purple(self) -> Self:
        """Return a copy with purple background."""
        return self.background("#f3e5f5")

    @property
    def bg_pink(self) -> Self:
        """Return a copy with pink background."""
        return self.background("#fce4ec")

    @property
    def bg_gray(self) -> Self:
        """Return a copy with gray background."""
        return self.background("#f5f5f5")

    @property
    def bg_white(self) -> Self:
        """Return a copy with white background."""
        return self.background("white")

    @property
    def bg_black(self) -> Self:
        """Return a copy with black background."""
        return self.background("black")

    # -------------------------------------------------------------------------
    # Size Shortcuts (beginner-friendly)
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
    # Common Style Presets (beginner-friendly)
    # -------------------------------------------------------------------------

    @property
    def highlight(self) -> Self:
        """Return a copy styled as highlighted text (yellow background)."""
        return self.styled(background_color="#fff59d", padding="2px 4px")

    @property
    def code(self) -> Self:
        """Return a copy styled as inline code."""
        return self.styled(
            font_family="monospace",
            background_color="#f5f5f5",
            padding="2px 6px",
            border_radius="4px",
            font_size="0.9em",
        )

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
    def muted(self) -> Self:
        """Return a copy styled as muted/secondary text."""
        return self.styled(color="#757575", font_size="0.9em")

    @property
    def link(self) -> Self:
        """Return a copy styled as a link."""
        return self.styled(color="#1976d2", text_decoration="underline")

    # -------------------------------------------------------------------------
    # Style Methods (require value arguments)
    # -------------------------------------------------------------------------

    def color(self, value: ColorValue) -> Self:
        """Return a copy with the specified text color.

        Args:
            value: CSS color value (e.g., "red", "#ff0000", Color.red, Color.hex("#ff0000"))
        """
        return self.styled(color=_to_css(value))

    def background(self, value: ColorValue) -> Self:
        """Return a copy with the specified background color.

        Args:
            value: CSS color value (e.g., "yellow", Color.yellow)
        """
        return self.styled(background_color=_to_css(value))

    def font_size(self, value: SizeValue) -> Self:
        """Return a copy with the specified font size.

        Args:
            value: CSS size value (e.g., "16px", Size.px(16), Size.em(1.2))
        """
        return self.styled(font_size=_to_css(value))

    def font_family(self, value: str) -> Self:
        """Return a copy with the specified font family.

        Args:
            value: CSS font-family value.
        """
        return self.styled(font_family=value)

    def padding(self, value: SpacingValue) -> Self:
        """Return a copy with the specified padding.

        Args:
            value: CSS padding value (e.g., "10px", Size.px(10), Spacing.symmetric(10, 20))
        """
        return self.styled(padding=_to_css(value))

    def margin(self, value: SpacingValue) -> Self:
        """Return a copy with the specified margin.

        Args:
            value: CSS margin value (e.g., "10px", Size.px(10), Spacing.all(10))
        """
        return self.styled(margin=_to_css(value))

    def border(self, value: BorderValue) -> Self:
        """Return a copy with the specified border.

        Args:
            value: CSS border value (e.g., "1px solid black", Border(1, BorderStyle.SOLID, Color.black))
        """
        return self.styled(border=_to_css(value))

    def border_radius(self, value: SizeValue) -> Self:
        """Return a copy with the specified border radius.

        Args:
            value: CSS border-radius value (e.g., "5px", Size.px(5), Size.percent(50))
        """
        return self.styled(border_radius=_to_css(value))

    def opacity(self, value: str | float) -> Self:
        """Return a copy with the specified opacity.

        Args:
            value: CSS opacity value (0.0 to 1.0)
        """
        return self.styled(opacity=str(value))

    def width(self, value: SizeValue) -> Self:
        """Return a copy with the specified width.

        Args:
            value: CSS width value (e.g., "100px", Size.px(100), Size.percent(50))
        """
        return self.styled(width=_to_css(value))

    def height(self, value: SizeValue) -> Self:
        """Return a copy with the specified height.

        Args:
            value: CSS height value (e.g., "50px", Size.px(50), Size.vh(100))
        """
        return self.styled(height=_to_css(value))

    def display(self, value: Display | str) -> Self:
        """Return a copy with the specified display mode.

        Args:
            value: CSS display value (e.g., "block", "flex", Display.FLEX)
        """
        return self.styled(display=_to_css(value))

    # -------------------------------------------------------------------------
    # String operation overrides to preserve HTMLString type
    # -------------------------------------------------------------------------

    def __add__(self, other: str) -> Self:
        """Concatenate strings, preserving styles for this string's content."""
        result = HTMLString(str.__add__(self, other))
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        return result  # type: ignore[return-value]

    def __radd__(self, other: str) -> Self:
        """Handle other + HTMLString."""
        result = HTMLString(str.__add__(other, self))
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        return result  # type: ignore[return-value]

    def __getitem__(self, key: int | slice) -> Self:
        """Slice the string, preserving styles."""
        result = HTMLString(str.__getitem__(self, key))
        result._styles = self._styles.copy()
        result._css_classes = self._css_classes.copy()
        result._tag = self._tag
        return result  # type: ignore[return-value]

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        styles_repr = ", ".join(f"{k}={v!r}" for k, v in self._styles.items())
        if styles_repr:
            return f"HTMLString({str.__repr__(self)}, {styles_repr})"
        return f"HTMLString({str.__repr__(self)})"
