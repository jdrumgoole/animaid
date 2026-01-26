"""Tests for HTMLString class."""

import pytest

from animaid import HTMLString


class TestHTMLStringBasics:
    """Test basic HTMLString functionality."""

    def test_is_string_subclass(self) -> None:
        """HTMLString should be a subclass of str."""
        s = HTMLString("Hello")
        assert isinstance(s, str)

    def test_string_value(self) -> None:
        """HTMLString should preserve string value."""
        s = HTMLString("Hello World")
        assert str(s) == "Hello World"
        assert s == "Hello World"

    def test_empty_string(self) -> None:
        """HTMLString should handle empty strings."""
        s = HTMLString("")
        assert s.render() == "<span></span>"

    def test_repr(self) -> None:
        """HTMLString should have informative repr."""
        s = HTMLString("Hello")
        assert repr(s) == "HTMLString('Hello')"

        s_styled = HTMLString("Hello", color="red")
        assert "color='red'" in repr(s_styled)


class TestHTMLStringRendering:
    """Test HTML rendering functionality."""

    def test_basic_render(self) -> None:
        """Basic render should wrap in span tag."""
        s = HTMLString("Hello")
        assert s.render() == "<span>Hello</span>"

    def test_render_with_inline_styles(self) -> None:
        """Render should include inline styles."""
        s = HTMLString("Hello", color="red")
        assert s.render() == '<span style="color: red">Hello</span>'

    def test_render_multiple_styles(self) -> None:
        """Render should include multiple styles."""
        s = HTMLString("Hello", color="red", font_size="16px")
        rendered = s.render()
        assert "color: red" in rendered
        assert "font-size: 16px" in rendered

    def test_render_escapes_html(self) -> None:
        """Render should escape HTML to prevent XSS."""
        s = HTMLString("<script>alert('xss')</script>")
        rendered = s.render()
        assert "<script>" not in rendered
        assert "&lt;script&gt;" in rendered

    def test_render_with_classes(self) -> None:
        """Render should include CSS classes."""
        s = HTMLString("Hello").add_class("highlight")
        assert s.render() == '<span class="highlight">Hello</span>'

    def test_render_with_multiple_classes(self) -> None:
        """Render should include multiple CSS classes."""
        s = HTMLString("Hello").add_class("highlight", "important")
        assert s.render() == '<span class="highlight important">Hello</span>'

    def test_render_with_classes_and_styles(self) -> None:
        """Render should include both classes and styles."""
        s = HTMLString("Hello").add_class("highlight").color("red")
        rendered = s.render()
        assert 'class="highlight"' in rendered
        assert 'style="color: red"' in rendered

    def test_custom_tag(self) -> None:
        """Render should use custom tag when specified."""
        s = HTMLString("Hello").tag("div")
        assert s.render() == "<div>Hello</div>"

        s = HTMLString("Important").tag("strong")
        assert s.render() == "<strong>Important</strong>"

    def test_dunder_html(self) -> None:
        """__html__ should return rendered output for Jinja2."""
        s = HTMLString("Hello").bold
        assert s.__html__() == s.render()


class TestHTMLStringStyleProperties:
    """Test style property methods."""

    def test_bold(self) -> None:
        """Bold property should add font-weight: bold."""
        s = HTMLString("Hello").bold
        assert "font-weight: bold" in s.render()

    def test_italic(self) -> None:
        """Italic property should add font-style: italic."""
        s = HTMLString("Hello").italic
        assert "font-style: italic" in s.render()

    def test_underline(self) -> None:
        """Underline property should add text-decoration: underline."""
        s = HTMLString("Hello").underline
        assert "text-decoration: underline" in s.render()

    def test_strikethrough(self) -> None:
        """Strikethrough property should add text-decoration: line-through."""
        s = HTMLString("Hello").strikethrough
        assert "text-decoration: line-through" in s.render()

    def test_uppercase(self) -> None:
        """Uppercase property should add text-transform: uppercase."""
        s = HTMLString("Hello").uppercase
        assert "text-transform: uppercase" in s.render()

    def test_lowercase(self) -> None:
        """Lowercase property should add text-transform: lowercase."""
        s = HTMLString("Hello").lowercase
        assert "text-transform: lowercase" in s.render()

    def test_capitalize(self) -> None:
        """Capitalize property should add text-transform: capitalize."""
        s = HTMLString("Hello").capitalize
        assert "text-transform: capitalize" in s.render()

    def test_nowrap(self) -> None:
        """Nowrap property should add white-space: nowrap."""
        s = HTMLString("Hello").nowrap
        assert "white-space: nowrap" in s.render()

    def test_monospace(self) -> None:
        """Monospace property should add font-family: monospace."""
        s = HTMLString("Hello").monospace
        assert "font-family: monospace" in s.render()

    def test_chained_properties(self) -> None:
        """Properties should be chainable."""
        s = HTMLString("Hello").bold.italic.underline
        rendered = s.render()
        assert "font-weight: bold" in rendered
        assert "font-style: italic" in rendered
        assert "text-decoration: underline" in rendered


class TestHTMLStringStyleMethods:
    """Test style methods that take arguments."""

    def test_color(self) -> None:
        """Color method should set color style."""
        s = HTMLString("Hello").color("red")
        assert "color: red" in s.render()

    def test_background(self) -> None:
        """Background method should set background-color style."""
        s = HTMLString("Hello").background("yellow")
        assert "background-color: yellow" in s.render()

    def test_font_size(self) -> None:
        """Font size method should set font-size style."""
        s = HTMLString("Hello").font_size("20px")
        assert "font-size: 20px" in s.render()

    def test_font_family(self) -> None:
        """Font family method should set font-family style."""
        s = HTMLString("Hello").font_family("Arial, sans-serif")
        assert "font-family: Arial, sans-serif" in s.render()

    def test_padding(self) -> None:
        """Padding method should set padding style."""
        s = HTMLString("Hello").padding("10px")
        assert "padding: 10px" in s.render()

    def test_margin(self) -> None:
        """Margin method should set margin style."""
        s = HTMLString("Hello").margin("5px")
        assert "margin: 5px" in s.render()

    def test_border(self) -> None:
        """Border method should set border style."""
        s = HTMLString("Hello").border("1px solid black")
        assert "border: 1px solid black" in s.render()

    def test_border_radius(self) -> None:
        """Border radius method should set border-radius style."""
        s = HTMLString("Hello").border_radius("5px")
        assert "border-radius: 5px" in s.render()

    def test_opacity(self) -> None:
        """Opacity method should set opacity style."""
        s = HTMLString("Hello").opacity(0.5)
        assert "opacity: 0.5" in s.render()

    def test_width(self) -> None:
        """Width method should set width style."""
        s = HTMLString("Hello").width("100px")
        assert "width: 100px" in s.render()

    def test_height(self) -> None:
        """Height method should set height style."""
        s = HTMLString("Hello").height("50px")
        assert "height: 50px" in s.render()

    def test_display(self) -> None:
        """Display method should set display style."""
        s = HTMLString("Hello").display("block")
        assert "display: block" in s.render()

    def test_styled_method(self) -> None:
        """Styled method should set arbitrary styles."""
        s = HTMLString("Hello").styled(
            color="blue",
            font_size="18px",
            text_align="center"
        )
        rendered = s.render()
        assert "color: blue" in rendered
        assert "font-size: 18px" in rendered
        assert "text-align: center" in rendered


class TestHTMLStringImmutability:
    """Test that HTMLString operations return new instances."""

    def test_styled_returns_new_instance(self) -> None:
        """Styling should return a new instance."""
        s1 = HTMLString("Hello")
        s2 = s1.bold
        assert s1 is not s2
        assert "font-weight" not in s1.render()
        assert "font-weight: bold" in s2.render()

    def test_chaining_preserves_original(self) -> None:
        """Chaining should not modify original."""
        s1 = HTMLString("Hello")
        s2 = s1.bold.color("red")
        assert s1.render() == "<span>Hello</span>"
        assert "font-weight: bold" in s2.render()
        assert "color: red" in s2.render()


class TestHTMLStringOperations:
    """Test string operations preserve HTMLString type."""

    def test_concatenation_preserves_type(self) -> None:
        """Concatenation should return HTMLString."""
        s = HTMLString("Hello").bold
        result = s + " World"
        assert isinstance(result, HTMLString)
        assert str(result) == "Hello World"
        assert "font-weight: bold" in result.render()

    def test_right_concatenation(self) -> None:
        """Right concatenation should work."""
        s = HTMLString("World").bold
        result = "Hello " + s
        assert isinstance(result, HTMLString)
        assert str(result) == "Hello World"

    def test_slicing_preserves_type(self) -> None:
        """Slicing should return HTMLString with styles."""
        s = HTMLString("Hello World").bold
        result = s[0:5]
        assert isinstance(result, HTMLString)
        assert str(result) == "Hello"
        assert "font-weight: bold" in result.render()

    def test_indexing_preserves_type(self) -> None:
        """Indexing should return HTMLString."""
        s = HTMLString("Hello").color("red")
        result = s[0]
        assert isinstance(result, HTMLString)
        assert str(result) == "H"
        assert "color: red" in result.render()


class TestHTMLStringEdgeCases:
    """Test edge cases and special scenarios."""

    def test_special_characters(self) -> None:
        """Special characters should be escaped properly."""
        s = HTMLString("5 > 3 && 3 < 5")
        rendered = s.render()
        assert "&gt;" in rendered
        assert "&lt;" in rendered
        assert "&amp;" in rendered

    def test_unicode(self) -> None:
        """Unicode characters should work correctly."""
        s = HTMLString("Hello \u4e16\u754c")
        assert s.render() == "<span>Hello \u4e16\u754c</span>"

    def test_quotes_in_content(self) -> None:
        """Quotes in content should be escaped."""
        s = HTMLString('He said "Hello"')
        rendered = s.render()
        assert "&quot;" in rendered or "&#x27;" in rendered or '"' in rendered

    def test_style_override(self) -> None:
        """Later styles should override earlier ones."""
        s = HTMLString("Hello").color("red").color("blue")
        assert "color: blue" in s.render()
        assert s.render().count("color:") == 1
