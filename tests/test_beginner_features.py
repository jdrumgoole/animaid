"""Tests for beginner-friendly features in animaid."""

import pytest

from animaid import HTMLString, HTMLList, HTMLDict
from animaid import String, List, Dict  # Beginner aliases
from animaid import Size, Color, Border, Spacing, BorderStyle


class TestStringColorShortcuts:
    """Test HTMLString color shortcut properties."""

    def test_red(self):
        s = HTMLString("Hello").red
        assert 'color: red' in s.render()

    def test_blue(self):
        s = HTMLString("Hello").blue
        assert 'color: blue' in s.render()

    def test_green(self):
        s = HTMLString("Hello").green
        assert 'color: green' in s.render()

    def test_yellow(self):
        s = HTMLString("Hello").yellow
        assert 'color:' in s.render()

    def test_orange(self):
        s = HTMLString("Hello").orange
        assert 'color: orange' in s.render()

    def test_purple(self):
        s = HTMLString("Hello").purple
        assert 'color: purple' in s.render()

    def test_pink(self):
        s = HTMLString("Hello").pink
        assert 'color:' in s.render()

    def test_gray(self):
        s = HTMLString("Hello").gray
        assert 'color: gray' in s.render()

    def test_white(self):
        s = HTMLString("Hello").white
        assert 'color: white' in s.render()

    def test_black(self):
        s = HTMLString("Hello").black
        assert 'color: black' in s.render()

    def test_chaining_colors(self):
        s = HTMLString("Hello").bold.red
        result = s.render()
        assert 'font-weight: bold' in result
        assert 'color: red' in result


class TestStringBackgroundShortcuts:
    """Test HTMLString background color shortcut properties."""

    def test_bg_red(self):
        s = HTMLString("Hello").bg_red
        assert 'background-color:' in s.render()

    def test_bg_blue(self):
        s = HTMLString("Hello").bg_blue
        assert 'background-color:' in s.render()

    def test_bg_green(self):
        s = HTMLString("Hello").bg_green
        assert 'background-color:' in s.render()

    def test_bg_yellow(self):
        s = HTMLString("Hello").bg_yellow
        assert 'background-color:' in s.render()

    def test_bg_orange(self):
        s = HTMLString("Hello").bg_orange
        assert 'background-color:' in s.render()

    def test_bg_purple(self):
        s = HTMLString("Hello").bg_purple
        assert 'background-color:' in s.render()

    def test_bg_pink(self):
        s = HTMLString("Hello").bg_pink
        assert 'background-color:' in s.render()

    def test_bg_gray(self):
        s = HTMLString("Hello").bg_gray
        assert 'background-color:' in s.render()

    def test_bg_white(self):
        s = HTMLString("Hello").bg_white
        assert 'background-color: white' in s.render()

    def test_bg_black(self):
        s = HTMLString("Hello").bg_black
        assert 'background-color: black' in s.render()


class TestStringSizeShortcuts:
    """Test HTMLString size shortcut properties."""

    def test_xs(self):
        s = HTMLString("Hello").xs
        assert 'font-size: 12px' in s.render()

    def test_small(self):
        s = HTMLString("Hello").small
        assert 'font-size: 14px' in s.render()

    def test_medium(self):
        s = HTMLString("Hello").medium
        assert 'font-size: 16px' in s.render()

    def test_large(self):
        s = HTMLString("Hello").large
        assert 'font-size: 20px' in s.render()

    def test_xl(self):
        s = HTMLString("Hello").xl
        assert 'font-size: 24px' in s.render()

    def test_xxl(self):
        s = HTMLString("Hello").xxl
        assert 'font-size: 32px' in s.render()


class TestStringStylePresets:
    """Test HTMLString style preset properties."""

    def test_highlight(self):
        s = HTMLString("Hello").highlight
        result = s.render()
        assert 'background-color:' in result
        assert 'padding:' in result

    def test_code(self):
        s = HTMLString("x = 1").code
        result = s.render()
        assert 'font-family: monospace' in result
        assert 'background-color:' in result
        assert 'border-radius:' in result

    def test_badge(self):
        s = HTMLString("Tag").badge
        result = s.render()
        assert 'background-color:' in result
        assert 'border-radius:' in result
        assert 'padding:' in result

    def test_success(self):
        s = HTMLString("OK").success
        result = s.render()
        assert 'color:' in result
        assert 'background-color:' in result

    def test_warning(self):
        s = HTMLString("Warning").warning
        result = s.render()
        assert 'color:' in result
        assert 'background-color:' in result

    def test_error(self):
        s = HTMLString("Error").error
        result = s.render()
        assert 'color:' in result
        assert 'background-color:' in result

    def test_info(self):
        s = HTMLString("Info").info
        result = s.render()
        assert 'color:' in result
        assert 'background-color:' in result

    def test_muted(self):
        s = HTMLString("Muted text").muted
        result = s.render()
        assert 'color:' in result
        assert 'font-size:' in result

    def test_link(self):
        s = HTMLString("Click me").link
        result = s.render()
        assert 'color:' in result
        assert 'text-decoration: underline' in result


class TestListPresets:
    """Test HTMLList style preset properties."""

    def test_cards(self):
        lst = HTMLList(["A", "B", "C"]).cards
        result = lst.render()
        assert '<div' in result
        assert 'style=' in result

    def test_pills(self):
        lst = HTMLList(["A", "B", "C"]).pills
        result = lst.render()
        assert '<div' in result
        assert 'border-radius:' in result

    def test_tags(self):
        lst = HTMLList(["A", "B", "C"]).tags
        result = lst.render()
        assert '<div' in result

    def test_menu(self):
        lst = HTMLList(["A", "B", "C"]).menu
        result = lst.render()
        assert '<div' in result

    def test_inline(self):
        lst = HTMLList(["A", "B", "C"]).inline
        result = lst.render()
        assert '<div' in result
        assert 'display: flex' in result

    def test_numbered(self):
        lst = HTMLList(["A", "B", "C"]).numbered
        result = lst.render()
        assert '<ol' in result

    def test_bulleted(self):
        lst = HTMLList(["A", "B", "C"]).bulleted
        result = lst.render()
        assert '<ul' in result

    def test_spaced(self):
        lst = HTMLList(["A", "B", "C"]).spaced
        result = lst.render()
        assert 'gap:' in result

    def test_compact(self):
        lst = HTMLList(["A", "B", "C"]).compact
        result = lst.render()
        assert 'gap:' in result


class TestDictPresets:
    """Test HTMLDict style preset properties."""

    def test_card(self):
        d = HTMLDict({"a": "1", "b": "2"}).card
        result = d.render()
        assert '<div' in result
        assert 'border:' in result
        assert 'border-radius:' in result

    def test_simple(self):
        d = HTMLDict({"a": "1", "b": "2"}).simple
        result = d.render()
        assert 'font-weight: bold' in result

    def test_striped(self):
        d = HTMLDict({"a": "1", "b": "2"}).striped
        result = d.render()
        assert '<table' in result
        assert 'border:' in result

    def test_compact(self):
        d = HTMLDict({"a": "1", "b": "2"}).compact
        result = d.render()
        assert 'gap:' in result or '<dl' in result

    def test_spaced(self):
        d = HTMLDict({"a": "1", "b": "2"}).spaced
        result = d.render()
        assert 'gap:' in result or '<dl' in result

    def test_labeled(self):
        d = HTMLDict({"a": "1", "b": "2"}).labeled
        result = d.render()
        assert '<div' in result

    def test_inline(self):
        d = HTMLDict({"a": "1", "b": "2"}).inline
        result = d.render()
        assert '<div' in result
        assert 'display: flex' in result

    def test_bordered(self):
        d = HTMLDict({"a": "1", "b": "2"}).bordered
        result = d.render()
        assert '<table' in result
        assert 'border:' in result


class TestBeginnerAliases:
    """Test beginner-friendly type aliases."""

    def test_string_alias(self):
        assert String is HTMLString
        s = String("Hello")
        assert isinstance(s, HTMLString)

    def test_list_alias(self):
        assert List is HTMLList
        lst = List(["A", "B"])
        assert isinstance(lst, HTMLList)

    def test_dict_alias(self):
        assert Dict is HTMLDict
        d = Dict({"a": "1"})
        assert isinstance(d, HTMLDict)

    def test_alias_methods_work(self):
        # String with shortcuts
        s = String("Hello").bold.red
        assert 'font-weight: bold' in s.render()
        assert 'color: red' in s.render()

        # List with presets
        lst = List(["A", "B"]).pills
        assert '<div' in lst.render()

        # Dict with presets
        d = Dict({"a": "1"}).card
        assert 'border:' in d.render()


class TestChainingShortcuts:
    """Test chaining multiple shortcuts together."""

    def test_color_and_size(self):
        s = HTMLString("Hello").red.large
        result = s.render()
        assert 'color: red' in result
        assert 'font-size: 20px' in result

    def test_background_and_bold(self):
        s = HTMLString("Hello").bg_yellow.bold
        result = s.render()
        assert 'background-color:' in result
        assert 'font-weight: bold' in result

    def test_preset_with_color(self):
        s = HTMLString("Code").code.blue
        result = s.render()
        assert 'font-family: monospace' in result
        assert 'color: blue' in result

    def test_multiple_list_methods(self):
        lst = HTMLList(["A", "B"]).pills.gap("20px")
        result = lst.render()
        assert 'gap:' in result

    def test_multiple_dict_methods(self):
        d = HTMLDict({"a": "1"}).card.separator(" -> ")
        result = d.render()
        assert '-&gt;' in result or '->' in result


# =============================================================================
# CSS Class Method Tests
# =============================================================================


class TestSizePresets:
    """Test Size class preset methods."""

    def test_zero(self):
        assert Size.zero().to_css() == "0px"

    def test_xs(self):
        assert Size.xs().to_css() == "4px"

    def test_sm(self):
        assert Size.sm().to_css() == "8px"

    def test_md(self):
        assert Size.md().to_css() == "16px"

    def test_lg(self):
        assert Size.lg().to_css() == "24px"

    def test_xl(self):
        assert Size.xl().to_css() == "32px"

    def test_xxl(self):
        assert Size.xxl().to_css() == "48px"

    def test_full(self):
        assert Size.full().to_css() == "100%"

    def test_half(self):
        assert Size.half().to_css() == "50%"

    def test_third(self):
        assert "33" in Size.third().to_css()
        assert "%" in Size.third().to_css()

    def test_quarter(self):
        assert Size.quarter().to_css() == "25%"


class TestColorSemanticColors:
    """Test Color class semantic color attributes."""

    def test_success(self):
        assert Color.success.to_css() == "#22c55e"

    def test_warning(self):
        assert Color.warning.to_css() == "#f59e0b"

    def test_error(self):
        assert Color.error.to_css() == "#ef4444"

    def test_info(self):
        assert Color.info.to_css() == "#3b82f6"

    def test_muted(self):
        assert Color.muted.to_css() == "#6b7280"

    def test_light_gray(self):
        assert Color.light_gray.to_css() == "#f5f5f5"

    def test_dark_gray(self):
        assert Color.dark_gray.to_css() == "#374151"


class TestBorderClassMethods:
    """Test Border class factory methods."""

    def test_solid_default(self):
        b = Border.solid()
        assert "1px" in b.to_css()
        assert "solid" in b.to_css()
        assert "black" in b.to_css()

    def test_solid_with_width(self):
        b = Border.solid(2)
        assert "2px" in b.to_css()
        assert "solid" in b.to_css()

    def test_solid_with_width_and_color(self):
        b = Border.solid(2, "red")
        assert "2px" in b.to_css()
        assert "solid" in b.to_css()
        assert "red" in b.to_css()

    def test_dashed_default(self):
        b = Border.dashed()
        assert "1px" in b.to_css()
        assert "dashed" in b.to_css()

    def test_dashed_with_args(self):
        b = Border.dashed(3, "blue")
        assert "3px" in b.to_css()
        assert "dashed" in b.to_css()
        assert "blue" in b.to_css()

    def test_dotted_default(self):
        b = Border.dotted()
        assert "1px" in b.to_css()
        assert "dotted" in b.to_css()

    def test_double_default(self):
        b = Border.double()
        assert "3px" in b.to_css()  # Default is 3px for double
        assert "double" in b.to_css()

    def test_none(self):
        b = Border.none()
        assert "none" in b.to_css()

    def test_thin(self):
        b = Border.thin()
        assert "1px" in b.to_css()
        assert "solid" in b.to_css()

    def test_thin_with_color(self):
        b = Border.thin("red")
        assert "1px" in b.to_css()
        assert "red" in b.to_css()

    def test_medium(self):
        b = Border.medium()
        assert "2px" in b.to_css()
        assert "solid" in b.to_css()

    def test_thick(self):
        b = Border.thick()
        assert "4px" in b.to_css()
        assert "solid" in b.to_css()

    def test_thick_with_color(self):
        b = Border.thick("navy")
        assert "4px" in b.to_css()
        assert "navy" in b.to_css()


class TestBorderInstanceMethods:
    """Test Border instance methods (renamed to as_*)."""

    def test_as_solid(self):
        b = Border(2, BorderStyle.DASHED, "red").as_solid()
        assert "solid" in b.to_css()

    def test_as_dashed(self):
        b = Border.solid(2, "blue").as_dashed()
        assert "dashed" in b.to_css()

    def test_as_dotted(self):
        b = Border.solid().as_dotted()
        assert "dotted" in b.to_css()

    def test_as_double(self):
        b = Border.solid(3).as_double()
        assert "double" in b.to_css()


class TestSpacingPresets:
    """Test Spacing class preset methods."""

    def test_zero(self):
        assert Spacing.zero().to_css() == "0px"

    def test_xs(self):
        assert Spacing.xs().to_css() == "4px"

    def test_sm(self):
        assert Spacing.sm().to_css() == "8px"

    def test_md(self):
        assert Spacing.md().to_css() == "16px"

    def test_lg(self):
        assert Spacing.lg().to_css() == "24px"

    def test_xl(self):
        assert Spacing.xl().to_css() == "32px"

    def test_button(self):
        s = Spacing.button()
        assert "8px" in s.to_css()
        assert "16px" in s.to_css()

    def test_card(self):
        assert Spacing.card().to_css() == "16px"

    def test_input(self):
        s = Spacing.input()
        assert "8px" in s.to_css()
        assert "12px" in s.to_css()

    def test_section(self):
        s = Spacing.section()
        assert "24px" in s.to_css()
        assert "0px" in s.to_css()

    def test_compact(self):
        s = Spacing.compact()
        assert "4px" in s.to_css()
        assert "8px" in s.to_css()

    def test_relaxed(self):
        s = Spacing.relaxed()
        assert "16px" in s.to_css()
        assert "24px" in s.to_css()


class TestCSSClassesWithHTMLTypes:
    """Test using CSS class methods with HTML types."""

    def test_string_with_size_preset(self):
        s = HTMLString("Hello").padding(Size.md())
        assert "padding: 16px" in s.render()

    def test_string_with_color_semantic(self):
        s = HTMLString("Error!").color(Color.error)
        assert "#ef4444" in s.render()

    def test_string_with_border_factory(self):
        s = HTMLString("Box").border(Border.solid(2, "blue"))
        assert "2px solid blue" in s.render()

    def test_string_with_spacing_preset(self):
        s = HTMLString("Button").padding(Spacing.button())
        assert "8px 16px" in s.render()

    def test_list_with_border_thin(self):
        lst = HTMLList(["A", "B"]).item_border(Border.thin())
        result = lst.render()
        assert "1px solid black" in result

    def test_dict_with_multiple_presets(self):
        d = HTMLDict({"a": "1"}).padding(Spacing.card()).border(Border.solid())
        result = d.render()
        assert "16px" in result
        assert "solid" in result
