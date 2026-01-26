"""Tests for CSS value types."""

import pytest

from animaid import (
    AlignItems,
    Border,
    BorderStyle,
    Color,
    Display,
    FlexDirection,
    FlexWrap,
    FontStyle,
    FontWeight,
    JustifyContent,
    Overflow,
    Position,
    Size,
    Spacing,
    TextAlign,
    TextDecoration,
    TextTransform,
)


# =============================================================================
# Size Tests
# =============================================================================


class TestSizeBasics:
    """Test basic Size functionality."""

    def test_px_factory(self) -> None:
        """Size.px creates pixel sizes."""
        s = Size.px(10)
        assert s.to_css() == "10px"
        assert s.value == 10
        assert s.unit == "px"

    def test_em_factory(self) -> None:
        """Size.em creates em sizes."""
        s = Size.em(1.5)
        assert s.to_css() == "1.5em"

    def test_rem_factory(self) -> None:
        """Size.rem creates rem sizes."""
        s = Size.rem(2)
        assert s.to_css() == "2rem"

    def test_percent_factory(self) -> None:
        """Size.percent creates percentage sizes."""
        s = Size.percent(50)
        assert s.to_css() == "50%"

    def test_vh_factory(self) -> None:
        """Size.vh creates viewport height sizes."""
        s = Size.vh(100)
        assert s.to_css() == "100vh"

    def test_vw_factory(self) -> None:
        """Size.vw creates viewport width sizes."""
        s = Size.vw(50)
        assert s.to_css() == "50vw"

    def test_fr_factory(self) -> None:
        """Size.fr creates fractional unit sizes."""
        s = Size.fr(1)
        assert s.to_css() == "1fr"

    def test_auto_factory(self) -> None:
        """Size.auto creates auto keyword."""
        s = Size.auto()
        assert s.to_css() == "auto"
        assert s.is_keyword

    def test_none_factory(self) -> None:
        """Size.none creates none keyword."""
        s = Size.none()
        assert s.to_css() == "none"

    def test_inherit_factory(self) -> None:
        """Size.inherit creates inherit keyword."""
        s = Size.inherit()
        assert s.to_css() == "inherit"


class TestSizeParsing:
    """Test Size string parsing."""

    def test_parse_px(self) -> None:
        """Parse pixel string."""
        s = Size("10px")
        assert s.value == 10
        assert s.unit == "px"

    def test_parse_em(self) -> None:
        """Parse em string."""
        s = Size("1.5em")
        assert s.value == 1.5
        assert s.unit == "em"

    def test_parse_percent(self) -> None:
        """Parse percentage string."""
        s = Size("50%")
        assert s.value == 50
        assert s.unit == "%"

    def test_parse_auto(self) -> None:
        """Parse auto keyword."""
        s = Size("auto")
        assert s.is_keyword
        assert s.to_css() == "auto"

    def test_parse_number_without_unit(self) -> None:
        """Parse number without unit defaults to px."""
        s = Size("10")
        assert s.value == 10
        assert s.unit == "px"

    def test_parse_negative(self) -> None:
        """Parse negative values."""
        s = Size("-10px")
        assert s.value == -10
        assert s.unit == "px"

    def test_parse_decimal(self) -> None:
        """Parse decimal values."""
        s = Size("0.5rem")
        assert s.value == 0.5
        assert s.unit == "rem"

    def test_invalid_unit_raises(self) -> None:
        """Invalid unit raises ValueError."""
        with pytest.raises(ValueError, match="Invalid unit"):
            Size("10xyz")

    def test_invalid_string_raises(self) -> None:
        """Invalid string raises ValueError."""
        with pytest.raises(ValueError, match="Cannot parse"):
            Size("abc")


class TestSizeEquality:
    """Test Size equality and hashing."""

    def test_equal_sizes(self) -> None:
        """Equal sizes are equal."""
        assert Size.px(10) == Size.px(10)

    def test_unequal_values(self) -> None:
        """Different values are not equal."""
        assert Size.px(10) != Size.px(20)

    def test_unequal_units(self) -> None:
        """Different units are not equal."""
        assert Size.px(10) != Size.em(10)

    def test_equal_to_string(self) -> None:
        """Size equals equivalent string."""
        assert Size.px(10) == "10px"

    def test_hashable(self) -> None:
        """Sizes can be used in sets."""
        s = {Size.px(10), Size.px(20), Size.px(10)}
        assert len(s) == 2


class TestSizeStringConversion:
    """Test Size string conversion."""

    def test_str(self) -> None:
        """str() returns CSS value."""
        assert str(Size.px(10)) == "10px"

    def test_repr(self) -> None:
        """repr() is informative."""
        assert repr(Size.px(10)) == "Size('10px')"

    def test_integer_values_no_decimal(self) -> None:
        """Integer values don't have .0."""
        assert Size.px(10).to_css() == "10px"
        assert Size.px(10.0).to_css() == "10px"


# =============================================================================
# Color Tests
# =============================================================================


class TestColorBasics:
    """Test basic Color functionality."""

    def test_named_color(self) -> None:
        """Named colors work."""
        c = Color("red")
        assert c.to_css() == "red"

    def test_hex_color(self) -> None:
        """Hex colors work."""
        c = Color("#ff0000")
        assert c.to_css() == "#ff0000"

    def test_hex_short(self) -> None:
        """Short hex colors work."""
        c = Color("#f00")
        assert c.to_css() == "#f00"

    def test_hex_with_alpha(self) -> None:
        """Hex with alpha works."""
        c = Color("#ff000080")
        assert c.to_css() == "#ff000080"

    def test_rgb(self) -> None:
        """RGB function works."""
        c = Color("rgb(255, 0, 0)")
        assert c.to_css() == "rgb(255, 0, 0)"

    def test_rgba(self) -> None:
        """RGBA function works."""
        c = Color("rgba(255, 0, 0, 0.5)")
        assert c.to_css() == "rgba(255, 0, 0, 0.5)"


class TestColorFactories:
    """Test Color factory methods."""

    def test_hex_factory(self) -> None:
        """Color.hex creates hex colors."""
        c = Color.hex("#2563eb")
        assert c.to_css() == "#2563eb"

    def test_hex_without_hash(self) -> None:
        """Color.hex adds # if missing."""
        c = Color.hex("2563eb")
        assert c.to_css() == "#2563eb"

    def test_rgb_factory(self) -> None:
        """Color.rgb creates RGB colors."""
        c = Color.rgb(255, 128, 0)
        assert c.to_css() == "rgb(255, 128, 0)"

    def test_rgb_validation(self) -> None:
        """Color.rgb validates range."""
        with pytest.raises(ValueError, match="must be 0-255"):
            Color.rgb(256, 0, 0)

    def test_rgba_factory(self) -> None:
        """Color.rgba creates RGBA colors."""
        c = Color.rgba(255, 128, 0, 0.5)
        assert c.to_css() == "rgba(255, 128, 0, 0.5)"

    def test_rgba_alpha_validation(self) -> None:
        """Color.rgba validates alpha range."""
        with pytest.raises(ValueError, match="alpha must be 0.0-1.0"):
            Color.rgba(255, 0, 0, 1.5)

    def test_hsl_factory(self) -> None:
        """Color.hsl creates HSL colors."""
        c = Color.hsl(0, 100, 50)
        assert c.to_css() == "hsl(0, 100%, 50%)"

    def test_hsla_factory(self) -> None:
        """Color.hsla creates HSLA colors."""
        c = Color.hsla(0, 100, 50, 0.5)
        assert c.to_css() == "hsla(0, 100%, 50%, 0.5)"


class TestColorConstants:
    """Test Color class constants."""

    def test_red(self) -> None:
        """Color.red exists."""
        assert Color.red.to_css() == "red"

    def test_blue(self) -> None:
        """Color.blue exists."""
        assert Color.blue.to_css() == "blue"

    def test_transparent(self) -> None:
        """Color.transparent exists."""
        assert Color.transparent.to_css() == "transparent"


class TestColorValidation:
    """Test Color validation."""

    def test_invalid_color_raises(self) -> None:
        """Invalid color raises ValueError."""
        with pytest.raises(ValueError, match="Invalid color"):
            Color("notacolor")

    def test_invalid_hex_raises(self) -> None:
        """Invalid hex raises ValueError."""
        with pytest.raises(ValueError, match="Invalid hex"):
            Color("#gggggg")


class TestColorEquality:
    """Test Color equality."""

    def test_equal_colors(self) -> None:
        """Equal colors are equal."""
        assert Color("red") == Color("red")

    def test_case_insensitive(self) -> None:
        """Color comparison is case insensitive."""
        assert Color("RED") == Color("red")

    def test_equal_to_string(self) -> None:
        """Color equals equivalent string."""
        assert Color("red") == "red"


# =============================================================================
# Enum Tests
# =============================================================================


class TestFontWeight:
    """Test FontWeight enum."""

    def test_normal(self) -> None:
        """FontWeight.NORMAL works."""
        assert FontWeight.NORMAL.to_css() == "normal"
        assert str(FontWeight.NORMAL) == "normal"

    def test_bold(self) -> None:
        """FontWeight.BOLD works."""
        assert FontWeight.BOLD.to_css() == "bold"

    def test_numeric(self) -> None:
        """Numeric weights work."""
        assert FontWeight.W700.to_css() == "700"


class TestFontStyle:
    """Test FontStyle enum."""

    def test_italic(self) -> None:
        """FontStyle.ITALIC works."""
        assert FontStyle.ITALIC.to_css() == "italic"


class TestTextTransform:
    """Test TextTransform enum."""

    def test_uppercase(self) -> None:
        """TextTransform.UPPERCASE works."""
        assert TextTransform.UPPERCASE.to_css() == "uppercase"


class TestTextDecoration:
    """Test TextDecoration enum."""

    def test_underline(self) -> None:
        """TextDecoration.UNDERLINE works."""
        assert TextDecoration.UNDERLINE.to_css() == "underline"

    def test_line_through(self) -> None:
        """TextDecoration.LINE_THROUGH works."""
        assert TextDecoration.LINE_THROUGH.to_css() == "line-through"


class TestDisplay:
    """Test Display enum."""

    def test_flex(self) -> None:
        """Display.FLEX works."""
        assert Display.FLEX.to_css() == "flex"

    def test_grid(self) -> None:
        """Display.GRID works."""
        assert Display.GRID.to_css() == "grid"


class TestFlexDirection:
    """Test FlexDirection enum."""

    def test_row(self) -> None:
        """FlexDirection.ROW works."""
        assert FlexDirection.ROW.to_css() == "row"

    def test_column(self) -> None:
        """FlexDirection.COLUMN works."""
        assert FlexDirection.COLUMN.to_css() == "column"


class TestAlignItems:
    """Test AlignItems enum."""

    def test_center(self) -> None:
        """AlignItems.CENTER works."""
        assert AlignItems.CENTER.to_css() == "center"


class TestJustifyContent:
    """Test JustifyContent enum."""

    def test_space_between(self) -> None:
        """JustifyContent.SPACE_BETWEEN works."""
        assert JustifyContent.SPACE_BETWEEN.to_css() == "space-between"


class TestBorderStyle:
    """Test BorderStyle enum."""

    def test_solid(self) -> None:
        """BorderStyle.SOLID works."""
        assert BorderStyle.SOLID.to_css() == "solid"

    def test_dashed(self) -> None:
        """BorderStyle.DASHED works."""
        assert BorderStyle.DASHED.to_css() == "dashed"


# =============================================================================
# Border Tests
# =============================================================================


class TestBorderBasics:
    """Test basic Border functionality."""

    def test_default_border(self) -> None:
        """Default border is 1px solid black."""
        b = Border()
        assert b.to_css() == "1px solid black"

    def test_with_size(self) -> None:
        """Border with Size."""
        b = Border(Size.px(2))
        assert b.to_css() == "2px solid black"

    def test_with_all_params(self) -> None:
        """Border with all parameters."""
        b = Border(Size.px(2), BorderStyle.DASHED, Color.red)
        assert b.to_css() == "2px dashed red"

    def test_with_strings(self) -> None:
        """Border with string parameters."""
        b = Border("2px", "dashed", "red")
        assert b.to_css() == "2px dashed red"

    def test_with_number(self) -> None:
        """Border with number (pixels)."""
        b = Border(2)
        assert b.to_css() == "2px solid black"


class TestBorderFluent:
    """Test Border fluent methods."""

    def test_width(self) -> None:
        """width() returns new Border."""
        b = Border().width(Size.px(3))
        assert b.to_css() == "3px solid black"

    def test_color(self) -> None:
        """color() returns new Border."""
        b = Border().color(Color.blue)
        assert b.to_css() == "1px solid blue"

    def test_as_solid(self) -> None:
        """as_solid() sets style."""
        b = Border().as_solid()
        assert "solid" in b.to_css()

    def test_as_dashed(self) -> None:
        """as_dashed() sets style."""
        b = Border().as_dashed()
        assert "dashed" in b.to_css()

    def test_as_dotted(self) -> None:
        """as_dotted() sets style."""
        b = Border().as_dotted()
        assert "dotted" in b.to_css()

    def test_chaining(self) -> None:
        """Methods can be chained."""
        b = Border().width(2).as_dashed().color("red")
        assert b.to_css() == "2px dashed red"


class TestBorderFactories:
    """Test Border factory methods."""

    def test_solid(self) -> None:
        """Border.solid() factory."""
        b = Border.solid(2, "red")
        assert b.to_css() == "2px solid red"

    def test_dashed(self) -> None:
        """Border.dashed() factory."""
        b = Border.dashed(2, "blue")
        assert b.to_css() == "2px dashed blue"


class TestBorderImmutability:
    """Test Border immutability."""

    def test_width_returns_new(self) -> None:
        """width() returns new instance."""
        b1 = Border()
        b2 = b1.width(2)
        assert b1 is not b2
        assert b1.to_css() == "1px solid black"
        assert b2.to_css() == "2px solid black"


# =============================================================================
# Spacing Tests
# =============================================================================


class TestSpacingBasics:
    """Test basic Spacing functionality."""

    def test_single_value(self) -> None:
        """Single value applies to all sides."""
        s = Spacing(Size.px(10))
        assert s.to_css() == "10px"

    def test_two_values(self) -> None:
        """Two values: vertical horizontal."""
        s = Spacing(Size.px(10), Size.px(20))
        assert s.to_css() == "10px 20px"

    def test_three_values(self) -> None:
        """Three values: top horizontal bottom."""
        s = Spacing(Size.px(10), Size.px(20), Size.px(30))
        assert s.to_css() == "10px 20px 30px"

    def test_four_values(self) -> None:
        """Four values: top right bottom left."""
        s = Spacing(Size.px(1), Size.px(2), Size.px(3), Size.px(4))
        assert s.to_css() == "1px 2px 3px 4px"

    def test_with_numbers(self) -> None:
        """Numbers are converted to pixels."""
        s = Spacing(10, 20)
        assert s.to_css() == "10px 20px"

    def test_with_strings(self) -> None:
        """Strings are parsed."""
        s = Spacing("10px", "1em")
        assert s.to_css() == "10px 1em"


class TestSpacingFactories:
    """Test Spacing factory methods."""

    def test_all(self) -> None:
        """Spacing.all() creates uniform spacing."""
        s = Spacing.all(10)
        assert s.to_css() == "10px"

    def test_symmetric(self) -> None:
        """Spacing.symmetric() creates vertical/horizontal."""
        s = Spacing.symmetric(10, 20)
        assert s.to_css() == "10px 20px"

    def test_edges(self) -> None:
        """Spacing.edges() creates all four sides."""
        s = Spacing.edges(1, 2, 3, 4)
        assert s.to_css() == "1px 2px 3px 4px"

    def test_horizontal(self) -> None:
        """Spacing.horizontal() creates left/right only."""
        s = Spacing.horizontal(10)
        assert s.to_css() == "0px 10px"

    def test_vertical(self) -> None:
        """Spacing.vertical() creates top/bottom only."""
        s = Spacing.vertical(10)
        assert s.to_css() == "10px 0px"


class TestSpacingProperties:
    """Test Spacing edge properties."""

    def test_single_value_edges(self) -> None:
        """Single value returns same for all edges."""
        s = Spacing.all(10)
        assert s.top == Size.px(10)
        assert s.right == Size.px(10)
        assert s.bottom == Size.px(10)
        assert s.left == Size.px(10)

    def test_two_value_edges(self) -> None:
        """Two values return correct edges."""
        s = Spacing.symmetric(10, 20)
        assert s.top == Size.px(10)
        assert s.right == Size.px(20)
        assert s.bottom == Size.px(10)
        assert s.left == Size.px(20)

    def test_four_value_edges(self) -> None:
        """Four values return correct edges."""
        s = Spacing.edges(1, 2, 3, 4)
        assert s.top == Size.px(1)
        assert s.right == Size.px(2)
        assert s.bottom == Size.px(3)
        assert s.left == Size.px(4)


class TestSpacingEquality:
    """Test Spacing equality."""

    def test_equal(self) -> None:
        """Equal spacings are equal."""
        assert Spacing.all(10) == Spacing.all(10)

    def test_equal_to_string(self) -> None:
        """Spacing equals equivalent string."""
        assert Spacing.all(10) == "10px"


# =============================================================================
# Integration Tests
# =============================================================================


class TestCSSValueProtocol:
    """Test that all types follow the CSSValue protocol."""

    def test_size_is_css_value(self) -> None:
        """Size implements CSSValue."""
        s = Size.px(10)
        assert hasattr(s, "to_css")
        assert str(s) == s.to_css()

    def test_color_is_css_value(self) -> None:
        """Color implements CSSValue."""
        c = Color.red
        assert hasattr(c, "to_css")
        assert str(c) == c.to_css()

    def test_border_is_css_value(self) -> None:
        """Border implements CSSValue."""
        b = Border()
        assert hasattr(b, "to_css")
        assert str(b) == b.to_css()

    def test_spacing_is_css_value(self) -> None:
        """Spacing implements CSSValue."""
        s = Spacing.all(10)
        assert hasattr(s, "to_css")
        assert str(s) == s.to_css()

    def test_enums_have_to_css(self) -> None:
        """Enums have to_css method."""
        assert FontWeight.BOLD.to_css() == "bold"
        assert BorderStyle.SOLID.to_css() == "solid"
        assert Display.FLEX.to_css() == "flex"
