"""Tests for HTMLFloat class."""

from animaid import HTMLFloat


class TestHTMLFloatBasics:
    """Test basic HTMLFloat functionality."""

    def test_create_html_float(self) -> None:
        """Test creating an HTMLFloat."""
        n = HTMLFloat(3.14159)
        assert float(n) == 3.14159

    def test_render_default(self) -> None:
        """Test default rendering."""
        n = HTMLFloat(3.14159)
        assert n.render() == "<span>3.14159</span>"

    def test_negative_float(self) -> None:
        """Test negative float."""
        n = HTMLFloat(-3.14)
        assert float(n) == -3.14
        assert n.render() == "<span>-3.14</span>"

    def test_zero(self) -> None:
        """Test zero."""
        n = HTMLFloat(0.0)
        assert float(n) == 0.0
        assert n.render() == "<span>0.0</span>"


class TestHTMLFloatFormatting:
    """Test HTMLFloat number formatting."""

    def test_comma_format(self) -> None:
        """Test comma formatting."""
        n = HTMLFloat(1234567.89).comma()
        assert n.render() == "<span>1,234,567.89</span>"

    def test_currency_default(self) -> None:
        """Test default currency formatting."""
        n = HTMLFloat(1000.50).currency()
        assert n.render() == "<span>$1,000.50</span>"

    def test_currency_custom_symbol(self) -> None:
        """Test custom currency symbol."""
        n = HTMLFloat(1000.50).currency("€", 2)
        assert n.render() == "<span>€1,000.50</span>"

    def test_currency_no_decimals(self) -> None:
        """Test currency with no decimals."""
        n = HTMLFloat(1000.50).currency("$", 0)
        assert n.render() == "<span>$1,000</span>"

    def test_percent(self) -> None:
        """Test percent formatting."""
        n = HTMLFloat(0.856).percent()
        assert n.render() == "<span>85.60%</span>"

    def test_percent_no_decimals(self) -> None:
        """Test percent with no decimals."""
        n = HTMLFloat(0.5).percent(0)
        assert n.render() == "<span>50%</span>"

    def test_decimal_places(self) -> None:
        """Test fixed decimal places."""
        n = HTMLFloat(3.14159).decimal(2)
        assert n.render() == "<span>3.14</span>"

    def test_decimal_more_places(self) -> None:
        """Test padding with zeros."""
        n = HTMLFloat(3.1).decimal(4)
        assert n.render() == "<span>3.1000</span>"

    def test_scientific(self) -> None:
        """Test scientific notation."""
        n = HTMLFloat(1234567.89).scientific()
        html = n.render()
        assert 'e+06' in html or 'E+06' in html.upper()

    def test_scientific_custom_precision(self) -> None:
        """Test scientific with custom precision."""
        n = HTMLFloat(1234567.89).scientific(4)
        html = n.render()
        assert 'e+06' in html or 'E+06' in html.upper()

    def test_significant_figures(self) -> None:
        """Test significant figures."""
        n = HTMLFloat(3.14159).significant(3)
        assert n.render() == "<span>3.14</span>"

    def test_significant_small_number(self) -> None:
        """Test significant figures with small number."""
        n = HTMLFloat(0.00123456).significant(2)
        assert "0.0012" in n.render()


class TestHTMLFloatStyles:
    """Test HTMLFloat styling."""

    def test_bold(self) -> None:
        """Test bold style."""
        n = HTMLFloat(3.14).bold
        assert 'font-weight: bold' in n.render()

    def test_italic(self) -> None:
        """Test italic style."""
        n = HTMLFloat(3.14).italic
        assert 'font-style: italic' in n.render()

    def test_underline(self) -> None:
        """Test underline style."""
        n = HTMLFloat(3.14).underline
        assert 'text-decoration: underline' in n.render()

    def test_monospace(self) -> None:
        """Test monospace style."""
        n = HTMLFloat(3.14).monospace
        assert 'font-family: monospace' in n.render()

    def test_color_red(self) -> None:
        """Test red color shortcut."""
        n = HTMLFloat(3.14).red
        assert 'color: red' in n.render()

    def test_color_green(self) -> None:
        """Test green color shortcut."""
        n = HTMLFloat(3.14).green
        assert 'color: green' in n.render()

    def test_color_method(self) -> None:
        """Test color method."""
        n = HTMLFloat(3.14).color("#ff5500")
        assert 'color: #ff5500' in n.render()

    def test_background(self) -> None:
        """Test background color."""
        n = HTMLFloat(3.14).background("yellow")
        assert 'background-color: yellow' in n.render()

    def test_font_size(self) -> None:
        """Test font size."""
        n = HTMLFloat(3.14).font_size("20px")
        assert 'font-size: 20px' in n.render()

    def test_padding(self) -> None:
        """Test padding."""
        n = HTMLFloat(3.14).padding("10px")
        assert 'padding: 10px' in n.render()

    def test_border(self) -> None:
        """Test border."""
        n = HTMLFloat(3.14).border("1px solid black")
        assert 'border: 1px solid black' in n.render()

    def test_border_radius(self) -> None:
        """Test border radius."""
        n = HTMLFloat(3.14).border_radius("5px")
        assert 'border-radius: 5px' in n.render()


class TestHTMLFloatPresets:
    """Test HTMLFloat style presets."""

    def test_success_preset(self) -> None:
        """Test success preset."""
        n = HTMLFloat(3.14).success
        html = n.render()
        assert 'color: #2e7d32' in html
        assert 'background-color: #e8f5e9' in html

    def test_warning_preset(self) -> None:
        """Test warning preset."""
        n = HTMLFloat(3.14).warning
        html = n.render()
        assert 'color: #e65100' in html
        assert 'background-color: #fff3e0' in html

    def test_error_preset(self) -> None:
        """Test error preset."""
        n = HTMLFloat(3.14).error
        html = n.render()
        assert 'color: #c62828' in html
        assert 'background-color: #ffebee' in html

    def test_badge_preset(self) -> None:
        """Test badge preset."""
        n = HTMLFloat(3.14).badge
        html = n.render()
        assert 'background-color: #e0e0e0' in html
        assert 'border-radius: 12px' in html


class TestHTMLFloatArithmetic:
    """Test HTMLFloat arithmetic operations."""

    def test_add_int(self) -> None:
        """Test HTMLFloat + int returns HTMLFloat."""
        n = HTMLFloat(10.5)
        result = n + 5
        assert isinstance(result, HTMLFloat)
        assert float(result) == 15.5

    def test_add_float(self) -> None:
        """Test HTMLFloat + float returns HTMLFloat."""
        n = HTMLFloat(10.5)
        result = n + 2.5
        assert isinstance(result, HTMLFloat)
        assert float(result) == 13.0

    def test_add_html_float(self) -> None:
        """Test HTMLFloat + HTMLFloat returns HTMLFloat."""
        n = HTMLFloat(10.5)
        f = HTMLFloat(2.5)
        result = n + f
        assert isinstance(result, HTMLFloat)
        assert float(result) == 13.0

    def test_radd(self) -> None:
        """Test float + HTMLFloat returns HTMLFloat."""
        n = HTMLFloat(10.5)
        result = 5 + n
        assert isinstance(result, HTMLFloat)
        assert float(result) == 15.5

    def test_subtract(self) -> None:
        """Test subtraction."""
        n = HTMLFloat(10.5)
        result = n - 3.0
        assert isinstance(result, HTMLFloat)
        assert float(result) == 7.5

    def test_multiply(self) -> None:
        """Test multiplication."""
        n = HTMLFloat(10.5)
        result = n * 2
        assert isinstance(result, HTMLFloat)
        assert float(result) == 21.0

    def test_truediv(self) -> None:
        """Test true division."""
        n = HTMLFloat(10.5)
        result = n / 2
        assert isinstance(result, HTMLFloat)
        assert float(result) == 5.25

    def test_floordiv(self) -> None:
        """Test floor division."""
        n = HTMLFloat(10.5)
        result = n // 3
        assert isinstance(result, HTMLFloat)
        assert float(result) == 3.0

    def test_mod(self) -> None:
        """Test modulo."""
        n = HTMLFloat(10.5)
        result = n % 3
        assert isinstance(result, HTMLFloat)
        assert float(result) == 1.5

    def test_pow(self) -> None:
        """Test power."""
        n = HTMLFloat(2.0)
        result = n ** 3
        assert isinstance(result, HTMLFloat)
        assert float(result) == 8.0

    def test_neg(self) -> None:
        """Test negation."""
        n = HTMLFloat(10.5)
        result = -n
        assert isinstance(result, HTMLFloat)
        assert float(result) == -10.5

    def test_abs(self) -> None:
        """Test absolute value."""
        n = HTMLFloat(-10.5)
        result = abs(n)
        assert isinstance(result, HTMLFloat)
        assert float(result) == 10.5


class TestHTMLFloatStylePreservation:
    """Test that styles are preserved across operations."""

    def test_styles_preserved_after_add(self) -> None:
        """Test styles are preserved after addition."""
        n = HTMLFloat(10.5).bold.red
        result = n + 5.0
        html = result.render()
        assert 'font-weight: bold' in html
        assert 'color: red' in html
        assert '15.5' in html

    def test_format_preserved_after_add(self) -> None:
        """Test formatting is preserved after addition."""
        n = HTMLFloat(1000.50).currency()
        result = n + 234.50
        assert '$1,235.00' in result.render()

    def test_styles_preserved_after_multiply(self) -> None:
        """Test styles are preserved after multiplication."""
        n = HTMLFloat(10.5).success
        result = n * 2
        html = result.render()
        assert 'color: #2e7d32' in html
        assert '21' in html


class TestHTMLFloatChaining:
    """Test method chaining."""

    def test_format_and_style_chain(self) -> None:
        """Test chaining format and style methods."""
        n = HTMLFloat(0.856).percent().bold.blue.large
        html = n.render()
        assert '85.60%' in html
        assert 'font-weight: bold' in html
        assert 'color: blue' in html
        assert 'font-size: 20px' in html

    def test_multiple_styles(self) -> None:
        """Test chaining multiple styles."""
        n = HTMLFloat(3.14).bold.italic.underline.monospace
        html = n.render()
        assert 'font-weight: bold' in html
        assert 'font-style: italic' in html
        assert 'text-decoration: underline' in html
        assert 'font-family: monospace' in html

    def test_currency_with_styles(self) -> None:
        """Test currency formatting with styles."""
        n = HTMLFloat(1234.56).currency("$", 2).success.xl
        html = n.render()
        assert '$1,234.56' in html
        assert 'color: #2e7d32' in html
        assert 'font-size: 24px' in html


class TestHTMLFloatRepr:
    """Test HTMLFloat representation."""

    def test_repr_basic(self) -> None:
        """Test basic repr."""
        n = HTMLFloat(3.14)
        assert repr(n) == "HTMLFloat(3.14)"

    def test_repr_with_format(self) -> None:
        """Test repr with format."""
        n = HTMLFloat(3.14).decimal(2)
        assert "format='decimal'" in repr(n)

    def test_repr_with_styles(self) -> None:
        """Test repr with styles."""
        n = HTMLFloat(3.14).bold
        assert "font-weight='bold'" in repr(n)
