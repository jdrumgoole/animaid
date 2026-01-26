"""Tests for HTMLTuple class."""

from collections import namedtuple

from animaid import HTMLTuple


class TestHTMLTupleBasics:
    """Test basic HTMLTuple functionality."""

    def test_create_html_tuple(self) -> None:
        """Test creating an HTMLTuple."""
        t = HTMLTuple((1, 2, 3))
        assert tuple(t) == (1, 2, 3)

    def test_render_default_parentheses(self) -> None:
        """Test default rendering with parentheses."""
        t = HTMLTuple((1, 2, 3))
        assert t.render() == "<span>(1, 2, 3)</span>"

    def test_empty_tuple(self) -> None:
        """Test empty tuple."""
        t = HTMLTuple(())
        assert t.render() == "<span>()</span>"

    def test_single_item(self) -> None:
        """Test single item tuple."""
        t = HTMLTuple((42,))
        assert t.render() == "<span>(42)</span>"

    def test_string_items(self) -> None:
        """Test tuple with string items."""
        t = HTMLTuple(("a", "b", "c"))
        assert t.render() == "<span>(a, b, c)</span>"

    def test_mixed_items(self) -> None:
        """Test tuple with mixed item types."""
        t = HTMLTuple((1, "two", 3.0))
        assert t.render() == "<span>(1, two, 3.0)</span>"


class TestNamedTuples:
    """Test named tuple support."""

    def test_namedtuple_basic(self) -> None:
        """Test rendering a named tuple."""
        Point = namedtuple("Point", ["x", "y"])
        t = HTMLTuple(Point(10, 20))
        assert tuple(t) == (10, 20)

    def test_namedtuple_labeled(self) -> None:
        """Test labeled rendering of named tuple."""
        Point = namedtuple("Point", ["x", "y"])
        t = HTMLTuple(Point(10, 20)).labeled
        html = t.render()
        assert ">x</dt>" in html
        assert ">10</dd>" in html
        assert ">y</dt>" in html
        assert ">20</dd>" in html

    def test_namedtuple_field_names_preserved(self) -> None:
        """Test that field names are preserved."""
        Person = namedtuple("Person", ["name", "age"])
        t = HTMLTuple(Person("Alice", 30))
        assert t._field_names == ("name", "age")

    def test_regular_tuple_labeled_uses_indices(self) -> None:
        """Test that regular tuples use indices as labels."""
        t = HTMLTuple((1, 2, 3)).labeled
        html = t.render()
        assert ">0</dt>" in html
        assert ">1</dt>" in html
        assert ">2</dt>" in html


class TestTupleFormats:
    """Test different tuple formats."""

    def test_parentheses_format(self) -> None:
        """Test parentheses format."""
        t = HTMLTuple((1, 2, 3)).parentheses
        assert "(1, 2, 3)" in t.render()

    def test_plain_format(self) -> None:
        """Test plain format without parentheses."""
        t = HTMLTuple((1, 2, 3)).plain
        html = t.render()
        assert "(" not in html
        assert "<div" in html

    def test_labeled_format(self) -> None:
        """Test labeled format."""
        t = HTMLTuple((1, 2, 3)).labeled
        html = t.render()
        assert "<dl" in html
        assert "<dt " in html  # dt has style attribute now
        assert "<dd " in html  # dd has style attribute now


class TestTupleDirection:
    """Test tuple layout directions."""

    def test_horizontal(self) -> None:
        """Test horizontal layout (default)."""
        t = HTMLTuple((1, 2, 3)).plain.horizontal
        html = t.render()
        assert "flex-direction: row" in html

    def test_vertical(self) -> None:
        """Test vertical layout."""
        t = HTMLTuple((1, 2, 3)).plain.vertical
        html = t.render()
        assert "flex-direction: column" in html

    def test_horizontal_reverse(self) -> None:
        """Test horizontal reverse layout."""
        t = HTMLTuple((1, 2, 3)).plain.horizontal_reverse
        html = t.render()
        assert "flex-direction: row-reverse" in html

    def test_vertical_reverse(self) -> None:
        """Test vertical reverse layout."""
        t = HTMLTuple((1, 2, 3)).plain.vertical_reverse
        html = t.render()
        assert "flex-direction: column-reverse" in html

    def test_grid(self) -> None:
        """Test grid layout."""
        t = HTMLTuple((1, 2, 3, 4, 5, 6)).plain.grid(3)
        html = t.render()
        assert "display: inline-grid" in html
        assert "grid-template-columns" in html


class TestTupleStyles:
    """Test HTMLTuple styling."""

    def test_gap(self) -> None:
        """Test gap styling."""
        t = HTMLTuple((1, 2, 3)).plain.gap("10px")
        assert "gap: 10px" in t.render()

    def test_padding(self) -> None:
        """Test padding styling."""
        t = HTMLTuple((1, 2, 3)).padding("10px")
        assert "padding: 10px" in t.render()

    def test_margin(self) -> None:
        """Test margin styling."""
        t = HTMLTuple((1, 2, 3)).margin("10px")
        assert "margin: 10px" in t.render()

    def test_border(self) -> None:
        """Test border styling."""
        t = HTMLTuple((1, 2, 3)).border("1px solid black")
        assert "border: 1px solid black" in t.render()

    def test_border_radius(self) -> None:
        """Test border radius styling."""
        t = HTMLTuple((1, 2, 3)).border_radius("5px")
        assert "border-radius: 5px" in t.render()

    def test_background(self) -> None:
        """Test background color."""
        t = HTMLTuple((1, 2, 3)).background("yellow")
        assert "background-color: yellow" in t.render()

    def test_color(self) -> None:
        """Test text color."""
        t = HTMLTuple((1, 2, 3)).color("red")
        assert "color: red" in t.render()


class TestTupleItemStyles:
    """Test item-level styling."""

    def test_item_padding(self) -> None:
        """Test item padding."""
        t = HTMLTuple((1, 2, 3)).plain.item_padding("5px")
        html = t.render()
        assert "padding: 5px" in html

    def test_item_background(self) -> None:
        """Test item background."""
        t = HTMLTuple((1, 2, 3)).plain.item_background("#f0f0f0")
        html = t.render()
        assert "background-color: #f0f0f0" in html

    def test_item_border(self) -> None:
        """Test item border."""
        t = HTMLTuple((1, 2, 3)).plain.item_border("1px solid gray")
        html = t.render()
        assert "border: 1px solid gray" in html

    def test_item_border_radius(self) -> None:
        """Test item border radius."""
        t = HTMLTuple((1, 2, 3)).plain.item_border_radius("4px")
        html = t.render()
        assert "border-radius: 4px" in html


class TestTuplePresets:
    """Test style presets."""

    def test_pills_preset(self) -> None:
        """Test pills preset."""
        t = HTMLTuple((1, 2, 3)).pills
        html = t.render()
        assert "border-radius: 20px" in html
        assert "background-color: #e0e0e0" in html

    def test_tags_preset(self) -> None:
        """Test tags preset."""
        t = HTMLTuple((1, 2, 3)).tags
        html = t.render()
        assert "background-color: #f5f5f5" in html
        assert "border-radius: 4px" in html

    def test_inline_preset(self) -> None:
        """Test inline preset."""
        t = HTMLTuple((1, 2, 3)).inline
        html = t.render()
        assert "flex-direction: row" in html

    def test_card_preset(self) -> None:
        """Test card preset for named tuples."""
        Point = namedtuple("Point", ["x", "y"])
        t = HTMLTuple(Point(10, 20)).card
        html = t.render()
        assert "border: 1px solid #e0e0e0" in html
        assert "border-radius: 8px" in html
        assert "<dl" in html


class TestTupleAlignment:
    """Test alignment methods."""

    def test_center(self) -> None:
        """Test center alignment."""
        t = HTMLTuple((1, 2, 3)).plain.center
        html = t.render()
        assert "align-items: center" in html
        assert "justify-content: center" in html

    def test_align_items(self) -> None:
        """Test align_items method."""
        t = HTMLTuple((1, 2, 3)).plain.align_items("flex-start")
        assert "align-items: flex-start" in t.render()

    def test_justify_content(self) -> None:
        """Test justify_content method."""
        t = HTMLTuple((1, 2, 3)).plain.justify_content("space-between")
        assert "justify-content: space-between" in t.render()


class TestTupleOperations:
    """Test tuple operations."""

    def test_concatenation(self) -> None:
        """Test tuple concatenation preserves settings."""
        t1 = HTMLTuple((1, 2)).plain.gap("10px")
        t2 = (3, 4)
        result = t1 + t2
        assert tuple(result) == (1, 2, 3, 4)
        assert isinstance(result, HTMLTuple)
        # Settings should be preserved
        assert "gap: 10px" in result.render()

    def test_slicing(self) -> None:
        """Test tuple slicing preserves settings."""
        t = HTMLTuple((1, 2, 3, 4)).plain.gap("10px")
        result = t[1:3]
        assert tuple(result) == (2, 3)
        assert isinstance(result, HTMLTuple)
        assert "gap: 10px" in result.render()

    def test_indexing_returns_item(self) -> None:
        """Test that indexing returns the item, not HTMLTuple."""
        t = HTMLTuple((1, 2, 3))
        assert t[0] == 1
        assert t[1] == 2
        assert t[2] == 3

    def test_len(self) -> None:
        """Test len function."""
        t = HTMLTuple((1, 2, 3))
        assert len(t) == 3

    def test_iteration(self) -> None:
        """Test iteration."""
        t = HTMLTuple((1, 2, 3))
        items = list(t)
        assert items == [1, 2, 3]


class TestTupleRepr:
    """Test HTMLTuple representation."""

    def test_repr_basic(self) -> None:
        """Test basic repr."""
        t = HTMLTuple((1, 2, 3))
        assert repr(t) == "HTMLTuple((1, 2, 3))"

    def test_repr_with_format(self) -> None:
        """Test repr with format."""
        t = HTMLTuple((1, 2, 3)).plain
        assert "format=plain" in repr(t)

    def test_repr_with_direction(self) -> None:
        """Test repr with direction."""
        t = HTMLTuple((1, 2, 3)).vertical
        assert "direction=vertical" in repr(t)

    def test_repr_with_fields(self) -> None:
        """Test repr with field names."""
        Point = namedtuple("Point", ["x", "y"])
        t = HTMLTuple(Point(10, 20))
        assert "fields=('x', 'y')" in repr(t)


class TestTupleChaining:
    """Test method chaining."""

    def test_multiple_styles(self) -> None:
        """Test chaining multiple style methods."""
        t = (HTMLTuple((1, 2, 3))
             .plain
             .horizontal
             .gap("10px")
             .padding("5px")
             .border("1px solid black"))
        html = t.render()
        assert "gap: 10px" in html
        assert "padding: 5px" in html
        assert "border: 1px solid black" in html

    def test_preset_then_customize(self) -> None:
        """Test using preset then customizing."""
        t = HTMLTuple((1, 2, 3)).pills.gap("20px")
        html = t.render()
        assert "gap: 20px" in html
        assert "border-radius: 20px" in html


class TestHTMLObjectNesting:
    """Test nesting HTML objects in tuples."""

    def test_nested_html_string(self) -> None:
        """Test tuple containing HTMLString."""
        from animaid import HTMLString
        s = HTMLString("hello").bold
        t = HTMLTuple((s, "world"))
        html = t.render()
        assert "font-weight: bold" in html
        assert "hello" in html
        assert "world" in html

    def test_nested_html_int(self) -> None:
        """Test tuple containing HTMLInt."""
        from animaid import HTMLInt
        n = HTMLInt(1000).comma()
        t = HTMLTuple((n, "items"))
        html = t.render()
        assert "1,000" in html
        assert "items" in html
