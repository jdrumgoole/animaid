"""Tests for HTMLInt class."""

from animaid import HTMLInt, HTMLFloat


class TestHTMLIntBasics:
    """Test basic HTMLInt functionality."""

    def test_create_html_int(self) -> None:
        """Test creating an HTMLInt."""
        n = HTMLInt(42)
        assert int(n) == 42

    def test_render_default(self) -> None:
        """Test default rendering."""
        n = HTMLInt(42)
        assert n.render() == "<span>42</span>"

    def test_negative_int(self) -> None:
        """Test negative integer."""
        n = HTMLInt(-42)
        assert int(n) == -42
        assert n.render() == "<span>-42</span>"

    def test_zero(self) -> None:
        """Test zero."""
        n = HTMLInt(0)
        assert int(n) == 0
        assert n.render() == "<span>0</span>"


class TestHTMLIntFormatting:
    """Test HTMLInt number formatting."""

    def test_comma_format(self) -> None:
        """Test comma formatting."""
        n = HTMLInt(1234567).comma()
        assert n.render() == "<span>1,234,567</span>"

    def test_currency_default(self) -> None:
        """Test default currency formatting."""
        n = HTMLInt(1000).currency()
        assert n.render() == "<span>$1,000</span>"

    def test_currency_custom_symbol(self) -> None:
        """Test custom currency symbol."""
        n = HTMLInt(1000).currency("€")
        assert n.render() == "<span>€1,000</span>"

    def test_percent(self) -> None:
        """Test percent formatting."""
        n = HTMLInt(85).percent()
        assert n.render() == "<span>85%</span>"

    def test_ordinal_first(self) -> None:
        """Test ordinal - 1st."""
        n = HTMLInt(1).ordinal()
        assert n.render() == "<span>1st</span>"

    def test_ordinal_second(self) -> None:
        """Test ordinal - 2nd."""
        n = HTMLInt(2).ordinal()
        assert n.render() == "<span>2nd</span>"

    def test_ordinal_third(self) -> None:
        """Test ordinal - 3rd."""
        n = HTMLInt(3).ordinal()
        assert n.render() == "<span>3rd</span>"

    def test_ordinal_fourth(self) -> None:
        """Test ordinal - 4th."""
        n = HTMLInt(4).ordinal()
        assert n.render() == "<span>4th</span>"

    def test_ordinal_eleventh(self) -> None:
        """Test ordinal - 11th (special case)."""
        n = HTMLInt(11).ordinal()
        assert n.render() == "<span>11th</span>"

    def test_ordinal_twelfth(self) -> None:
        """Test ordinal - 12th (special case)."""
        n = HTMLInt(12).ordinal()
        assert n.render() == "<span>12th</span>"

    def test_ordinal_thirteenth(self) -> None:
        """Test ordinal - 13th (special case)."""
        n = HTMLInt(13).ordinal()
        assert n.render() == "<span>13th</span>"

    def test_ordinal_twenty_first(self) -> None:
        """Test ordinal - 21st."""
        n = HTMLInt(21).ordinal()
        assert n.render() == "<span>21st</span>"

    def test_ordinal_twenty_second(self) -> None:
        """Test ordinal - 22nd."""
        n = HTMLInt(22).ordinal()
        assert n.render() == "<span>22nd</span>"

    def test_padded(self) -> None:
        """Test zero-padding."""
        n = HTMLInt(7).padded(3)
        assert n.render() == "<span>007</span>"

    def test_padded_default_width(self) -> None:
        """Test default padding width."""
        n = HTMLInt(7).padded()
        assert n.render() == "<span>07</span>"


class TestHTMLIntStyles:
    """Test HTMLInt styling."""

    def test_bold(self) -> None:
        """Test bold style."""
        n = HTMLInt(42).bold
        assert 'font-weight: bold' in n.render()

    def test_italic(self) -> None:
        """Test italic style."""
        n = HTMLInt(42).italic
        assert 'font-style: italic' in n.render()

    def test_underline(self) -> None:
        """Test underline style."""
        n = HTMLInt(42).underline
        assert 'text-decoration: underline' in n.render()

    def test_monospace(self) -> None:
        """Test monospace style."""
        n = HTMLInt(42).monospace
        assert 'font-family: monospace' in n.render()

    def test_color_red(self) -> None:
        """Test red color shortcut."""
        n = HTMLInt(42).red
        assert 'color: red' in n.render()

    def test_color_blue(self) -> None:
        """Test blue color shortcut."""
        n = HTMLInt(42).blue
        assert 'color: blue' in n.render()

    def test_color_method(self) -> None:
        """Test color method."""
        n = HTMLInt(42).color("#ff5500")
        assert 'color: #ff5500' in n.render()

    def test_background(self) -> None:
        """Test background color."""
        n = HTMLInt(42).background("yellow")
        assert 'background-color: yellow' in n.render()

    def test_font_size(self) -> None:
        """Test font size."""
        n = HTMLInt(42).font_size("20px")
        assert 'font-size: 20px' in n.render()

    def test_padding(self) -> None:
        """Test padding."""
        n = HTMLInt(42).padding("10px")
        assert 'padding: 10px' in n.render()

    def test_border(self) -> None:
        """Test border."""
        n = HTMLInt(42).border("1px solid black")
        assert 'border: 1px solid black' in n.render()

    def test_border_radius(self) -> None:
        """Test border radius."""
        n = HTMLInt(42).border_radius("5px")
        assert 'border-radius: 5px' in n.render()


class TestHTMLIntPresets:
    """Test HTMLInt style presets."""

    def test_success_preset(self) -> None:
        """Test success preset."""
        n = HTMLInt(42).success
        html = n.render()
        assert 'color: #2e7d32' in html
        assert 'background-color: #e8f5e9' in html

    def test_warning_preset(self) -> None:
        """Test warning preset."""
        n = HTMLInt(42).warning
        html = n.render()
        assert 'color: #e65100' in html
        assert 'background-color: #fff3e0' in html

    def test_error_preset(self) -> None:
        """Test error preset."""
        n = HTMLInt(42).error
        html = n.render()
        assert 'color: #c62828' in html
        assert 'background-color: #ffebee' in html

    def test_badge_preset(self) -> None:
        """Test badge preset."""
        n = HTMLInt(42).badge
        html = n.render()
        assert 'background-color: #e0e0e0' in html
        assert 'border-radius: 12px' in html


class TestHTMLIntArithmetic:
    """Test HTMLInt arithmetic operations."""

    def test_add_int(self) -> None:
        """Test HTMLInt + int returns HTMLInt."""
        n = HTMLInt(10)
        result = n + 5
        assert isinstance(result, HTMLInt)
        assert int(result) == 15

    def test_add_float(self) -> None:
        """Test HTMLInt + float returns HTMLFloat."""
        n = HTMLInt(10)
        result = n + 2.5
        assert isinstance(result, HTMLFloat)
        assert float(result) == 12.5

    def test_add_html_float(self) -> None:
        """Test HTMLInt + HTMLFloat returns HTMLFloat."""
        n = HTMLInt(10)
        f = HTMLFloat(2.5)
        result = n + f
        assert isinstance(result, HTMLFloat)
        assert float(result) == 12.5

    def test_radd(self) -> None:
        """Test int + HTMLInt returns HTMLInt."""
        n = HTMLInt(10)
        result = 5 + n
        assert isinstance(result, HTMLInt)
        assert int(result) == 15

    def test_subtract(self) -> None:
        """Test subtraction."""
        n = HTMLInt(10)
        result = n - 3
        assert isinstance(result, HTMLInt)
        assert int(result) == 7

    def test_multiply(self) -> None:
        """Test multiplication."""
        n = HTMLInt(10)
        result = n * 3
        assert isinstance(result, HTMLInt)
        assert int(result) == 30

    def test_truediv(self) -> None:
        """Test true division always returns HTMLFloat."""
        n = HTMLInt(10)
        result = n / 4
        assert isinstance(result, HTMLFloat)
        assert float(result) == 2.5

    def test_floordiv(self) -> None:
        """Test floor division returns HTMLInt."""
        n = HTMLInt(10)
        result = n // 3
        assert isinstance(result, HTMLInt)
        assert int(result) == 3

    def test_mod(self) -> None:
        """Test modulo."""
        n = HTMLInt(10)
        result = n % 3
        assert isinstance(result, HTMLInt)
        assert int(result) == 1

    def test_pow(self) -> None:
        """Test power."""
        n = HTMLInt(2)
        result = n ** 3
        assert isinstance(result, HTMLInt)
        assert int(result) == 8

    def test_neg(self) -> None:
        """Test negation."""
        n = HTMLInt(10)
        result = -n
        assert isinstance(result, HTMLInt)
        assert int(result) == -10

    def test_abs(self) -> None:
        """Test absolute value."""
        n = HTMLInt(-10)
        result = abs(n)
        assert isinstance(result, HTMLInt)
        assert int(result) == 10


class TestHTMLIntStylePreservation:
    """Test that styles are preserved across operations."""

    def test_styles_preserved_after_add(self) -> None:
        """Test styles are preserved after addition."""
        n = HTMLInt(10).bold.red
        result = n + 5
        html = result.render()
        assert 'font-weight: bold' in html
        assert 'color: red' in html
        assert '>15<' in html

    def test_format_preserved_after_add(self) -> None:
        """Test formatting is preserved after addition."""
        n = HTMLInt(1000000).comma()
        result = n + 234567
        assert '1,234,567' in result.render()

    def test_styles_preserved_after_multiply(self) -> None:
        """Test styles are preserved after multiplication."""
        n = HTMLInt(10).success
        result = n * 5
        html = result.render()
        assert 'color: #2e7d32' in html
        assert '>50<' in html


class TestHTMLIntChaining:
    """Test method chaining."""

    def test_format_and_style_chain(self) -> None:
        """Test chaining format and style methods."""
        n = HTMLInt(1234567).comma().bold.blue.large
        html = n.render()
        assert '1,234,567' in html
        assert 'font-weight: bold' in html
        assert 'color: blue' in html
        assert 'font-size: 20px' in html

    def test_multiple_styles(self) -> None:
        """Test chaining multiple styles."""
        n = HTMLInt(42).bold.italic.underline.monospace
        html = n.render()
        assert 'font-weight: bold' in html
        assert 'font-style: italic' in html
        assert 'text-decoration: underline' in html
        assert 'font-family: monospace' in html

    def test_currency_with_styles(self) -> None:
        """Test currency formatting with styles."""
        n = HTMLInt(1000).currency("$").success.xl
        html = n.render()
        assert '$1,000' in html
        assert 'color: #2e7d32' in html
        assert 'font-size: 24px' in html


class TestHTMLIntRepr:
    """Test HTMLInt representation."""

    def test_repr_basic(self) -> None:
        """Test basic repr."""
        n = HTMLInt(42)
        assert repr(n) == "HTMLInt(42)"

    def test_repr_with_format(self) -> None:
        """Test repr with format."""
        n = HTMLInt(42).comma()
        assert "format='comma'" in repr(n)

    def test_repr_with_styles(self) -> None:
        """Test repr with styles."""
        n = HTMLInt(42).bold
        assert "font-weight='bold'" in repr(n)
