"""Tests for HTMLList class."""

import pytest

from animaid import HTMLList, HTMLString


class TestHTMLListBasics:
    """Test basic HTMLList functionality."""

    def test_is_list_subclass(self) -> None:
        """HTMLList should be a subclass of list."""
        lst = HTMLList(["a", "b", "c"])
        assert isinstance(lst, list)

    def test_list_value(self) -> None:
        """HTMLList should preserve list items."""
        lst = HTMLList(["a", "b", "c"])
        assert list(lst) == ["a", "b", "c"]
        assert len(lst) == 3

    def test_empty_list(self) -> None:
        """HTMLList should handle empty lists."""
        lst = HTMLList()
        assert lst.render() == "<ul></ul>"

    def test_repr(self) -> None:
        """HTMLList should have informative repr."""
        lst = HTMLList(["a", "b"])
        assert repr(lst) == "HTMLList(['a', 'b'])"

    def test_repr_with_direction(self) -> None:
        """HTMLList repr should show direction."""
        lst = HTMLList(["a", "b"]).horizontal
        assert "direction=horizontal" in repr(lst)


class TestHTMLListRendering:
    """Test HTML rendering functionality."""

    def test_basic_render(self) -> None:
        """Basic render should create unordered list."""
        lst = HTMLList(["Apple", "Banana"])
        assert lst.render() == "<ul><li>Apple</li><li>Banana</li></ul>"

    def test_render_escapes_html(self) -> None:
        """Render should escape HTML in items."""
        lst = HTMLList(["<script>alert('xss')</script>"])
        rendered = lst.render()
        assert "<script>" not in rendered
        assert "&lt;script&gt;" in rendered

    def test_render_with_styles(self) -> None:
        """Render should include container styles."""
        lst = HTMLList(["a", "b"]).styled(color="red")
        rendered = lst.render()
        assert "color: red" in rendered

    def test_render_with_classes(self) -> None:
        """Render should include CSS classes."""
        lst = HTMLList(["a", "b"]).add_class("my-list")
        rendered = lst.render()
        assert 'class="my-list"' in rendered

    def test_dunder_html(self) -> None:
        """__html__ should return rendered output for Jinja2."""
        lst = HTMLList(["a", "b"])
        assert lst.__html__() == lst.render()


class TestHTMLListTypes:
    """Test different list types."""

    def test_unordered_list(self) -> None:
        """Unordered list should use <ul> tag."""
        lst = HTMLList(["a", "b"]).unordered
        rendered = lst.render()
        assert rendered.startswith("<ul")
        assert "<li>a</li>" in rendered

    def test_ordered_list(self) -> None:
        """Ordered list should use <ol> tag."""
        lst = HTMLList(["a", "b"]).ordered
        rendered = lst.render()
        assert rendered.startswith("<ol")
        assert "<li>a</li>" in rendered

    def test_plain_list(self) -> None:
        """Plain list should use <div> tags."""
        lst = HTMLList(["a", "b"]).plain
        rendered = lst.render()
        assert rendered.startswith("<div")
        assert "<div>a</div>" in rendered


class TestHTMLListDirection:
    """Test list direction layouts."""

    def test_vertical_default(self) -> None:
        """Default direction should be vertical."""
        lst = HTMLList(["a", "b"])
        # Vertical unordered list doesn't need flexbox
        rendered = lst.render()
        assert "<ul>" in rendered

    def test_horizontal(self) -> None:
        """Horizontal layout should use flexbox row."""
        lst = HTMLList(["a", "b"]).horizontal
        rendered = lst.render()
        assert "display: flex" in rendered
        assert "flex-direction: row" in rendered

    def test_horizontal_reverse(self) -> None:
        """Horizontal reverse should use row-reverse."""
        lst = HTMLList(["a", "b"]).horizontal_reverse
        rendered = lst.render()
        assert "flex-direction: row-reverse" in rendered

    def test_vertical_reverse(self) -> None:
        """Vertical reverse should use column-reverse."""
        lst = HTMLList(["a", "b"]).vertical_reverse
        rendered = lst.render()
        assert "flex-direction: column-reverse" in rendered

    def test_grid_layout(self) -> None:
        """Grid layout should use CSS grid."""
        lst = HTMLList(["a", "b", "c", "d"]).grid(2)
        rendered = lst.render()
        assert "display: grid" in rendered
        assert "grid-template-columns: repeat(2, 1fr)" in rendered

    def test_grid_default_columns(self) -> None:
        """Grid without argument should default to 3 columns."""
        lst = HTMLList(["a", "b"]).grid()
        rendered = lst.render()
        assert "repeat(3, 1fr)" in rendered


class TestHTMLListSpacing:
    """Test spacing methods."""

    def test_gap(self) -> None:
        """Gap should add spacing between items."""
        lst = HTMLList(["a", "b"]).horizontal.gap("20px")
        rendered = lst.render()
        assert "gap: 20px" in rendered

    def test_padding(self) -> None:
        """Padding should add container padding."""
        lst = HTMLList(["a", "b"]).padding("10px")
        rendered = lst.render()
        assert "padding: 10px" in rendered

    def test_margin(self) -> None:
        """Margin should add container margin."""
        lst = HTMLList(["a", "b"]).margin("5px")
        rendered = lst.render()
        assert "margin: 5px" in rendered

    def test_item_padding(self) -> None:
        """Item padding should add padding to each item."""
        lst = HTMLList(["a", "b"]).item_padding("8px")
        rendered = lst.render()
        assert 'style="padding: 8px"' in rendered

    def test_item_margin(self) -> None:
        """Item margin should add margin to each item."""
        lst = HTMLList(["a", "b"]).item_margin("4px")
        rendered = lst.render()
        assert 'style="margin: 4px"' in rendered


class TestHTMLListBorders:
    """Test border methods."""

    def test_container_border(self) -> None:
        """Border should add container border."""
        lst = HTMLList(["a", "b"]).border("1px solid black")
        rendered = lst.render()
        assert "border: 1px solid black" in rendered

    def test_border_radius(self) -> None:
        """Border radius should round container corners."""
        lst = HTMLList(["a", "b"]).border_radius("5px")
        rendered = lst.render()
        assert "border-radius: 5px" in rendered

    def test_item_border(self) -> None:
        """Item border should add border to each item."""
        lst = HTMLList(["a", "b"]).item_border("1px solid gray")
        rendered = lst.render()
        assert 'border: 1px solid gray' in rendered

    def test_item_border_radius(self) -> None:
        """Item border radius should round item corners."""
        lst = HTMLList(["a", "b"]).item_border_radius("3px")
        rendered = lst.render()
        assert 'border-radius: 3px' in rendered

    def test_separator_vertical(self) -> None:
        """Separator should add border-bottom between items vertically."""
        lst = HTMLList(["a", "b", "c"]).plain.separator("1px solid gray")
        rendered = lst.render()
        # First two items should have border-bottom, last should not
        assert "border-bottom: 1px solid gray" in rendered

    def test_separator_horizontal(self) -> None:
        """Separator should add border-right between items horizontally."""
        lst = HTMLList(["a", "b", "c"]).horizontal.separator("1px solid gray")
        rendered = lst.render()
        assert "border-right: 1px solid gray" in rendered


class TestHTMLListColors:
    """Test color methods."""

    def test_background(self) -> None:
        """Background should set container background."""
        lst = HTMLList(["a", "b"]).background("#f0f0f0")
        rendered = lst.render()
        assert "background-color: #f0f0f0" in rendered

    def test_item_background(self) -> None:
        """Item background should set each item's background."""
        lst = HTMLList(["a", "b"]).item_background("yellow")
        rendered = lst.render()
        assert "background-color: yellow" in rendered

    def test_color(self) -> None:
        """Color should set text color."""
        lst = HTMLList(["a", "b"]).color("blue")
        rendered = lst.render()
        assert "color: blue" in rendered


class TestHTMLListAlignment:
    """Test alignment methods."""

    def test_align_items(self) -> None:
        """Align items should set cross-axis alignment."""
        lst = HTMLList(["a", "b"]).horizontal.align_items("center")
        rendered = lst.render()
        assert "align-items: center" in rendered

    def test_justify_content(self) -> None:
        """Justify content should set main-axis alignment."""
        lst = HTMLList(["a", "b"]).horizontal.justify_content("space-between")
        rendered = lst.render()
        assert "justify-content: space-between" in rendered

    def test_center(self) -> None:
        """Center should set both alignments to center."""
        lst = HTMLList(["a", "b"]).horizontal.center
        rendered = lst.render()
        assert "align-items: center" in rendered
        assert "justify-content: center" in rendered


class TestHTMLListSize:
    """Test size methods."""

    def test_width(self) -> None:
        """Width should set container width."""
        lst = HTMLList(["a", "b"]).width("300px")
        rendered = lst.render()
        assert "width: 300px" in rendered

    def test_height(self) -> None:
        """Height should set container height."""
        lst = HTMLList(["a", "b"]).height("200px")
        rendered = lst.render()
        assert "height: 200px" in rendered

    def test_max_width(self) -> None:
        """Max width should constrain container width."""
        lst = HTMLList(["a", "b"]).max_width("500px")
        rendered = lst.render()
        assert "max-width: 500px" in rendered


class TestHTMLListNesting:
    """Test nested list rendering."""

    def test_nested_html_list(self) -> None:
        """Nested HTMLList should render recursively."""
        inner = HTMLList(["x", "y"]).horizontal.gap("5px")
        outer = HTMLList(["a", inner, "b"])
        rendered = outer.render()

        # Should contain outer list structure
        assert "<ul>" in rendered
        assert "<li>a</li>" in rendered
        assert "<li>b</li>" in rendered

        # Should contain inner list with its styles
        assert "display: flex" in rendered
        assert "gap: 5px" in rendered

    def test_nested_html_string(self) -> None:
        """HTMLString items should render with their styles."""
        styled = HTMLString("Important").bold.color("red")
        lst = HTMLList(["Normal", styled, "Also normal"])
        rendered = lst.render()

        assert "<li>Normal</li>" in rendered
        assert "font-weight: bold" in rendered
        assert "color: red" in rendered
        assert "Important" in rendered

    def test_deeply_nested(self) -> None:
        """Deeply nested structures should render correctly."""
        level3 = HTMLList(["deep"]).horizontal
        level2 = HTMLList([level3, "mid"])
        level1 = HTMLList([level2, "top"])
        rendered = level1.render()

        assert "deep" in rendered
        assert "mid" in rendered
        assert "top" in rendered

    def test_mixed_content(self) -> None:
        """Lists with mixed content types should render."""
        lst = HTMLList([
            "plain string",
            HTMLString("styled").italic,
            123,  # number
            HTMLList(["nested"]).horizontal,
        ])
        rendered = lst.render()

        assert "plain string" in rendered
        assert "font-style: italic" in rendered
        assert "123" in rendered
        assert "nested" in rendered


class TestHTMLListImmutability:
    """Test that styling returns new instances."""

    def test_horizontal_returns_new(self) -> None:
        """Horizontal should return new instance."""
        lst1 = HTMLList(["a", "b"])
        lst2 = lst1.horizontal
        assert lst1 is not lst2

    def test_chaining_preserves_original(self) -> None:
        """Chaining should not modify original."""
        lst1 = HTMLList(["a", "b"])
        lst2 = lst1.horizontal.gap("10px").item_padding("5px")

        # Original should be unchanged
        rendered1 = lst1.render()
        assert "display: flex" not in rendered1
        assert "gap" not in rendered1

        # New should have all styles
        rendered2 = lst2.render()
        assert "display: flex" in rendered2
        assert "gap: 10px" in rendered2
        assert "padding: 5px" in rendered2


class TestHTMLListOperations:
    """Test list operations preserve settings."""

    def test_concatenation(self) -> None:
        """Concatenation should preserve settings."""
        lst = HTMLList(["a"]).horizontal.gap("10px")
        result = lst + ["b", "c"]
        assert isinstance(result, HTMLList)
        assert list(result) == ["a", "b", "c"]
        assert "gap: 10px" in result.render()

    def test_slicing(self) -> None:
        """Slicing should return HTMLList with settings."""
        lst = HTMLList(["a", "b", "c", "d"]).horizontal.gap("5px")
        result = lst[1:3]
        assert isinstance(result, HTMLList)
        assert list(result) == ["b", "c"]
        assert "gap: 5px" in result.render()

    def test_indexing_returns_item(self) -> None:
        """Indexing should return the item, not HTMLList."""
        lst = HTMLList(["a", "b", "c"])
        assert lst[0] == "a"
        assert lst[1] == "b"


class TestHTMLListItemClasses:
    """Test item class methods."""

    def test_add_item_class(self) -> None:
        """Add item class should add classes to items."""
        lst = HTMLList(["a", "b"]).add_item_class("item", "card")
        rendered = lst.render()
        assert 'class="item card"' in rendered


class TestHTMLListChaining:
    """Test complex method chaining."""

    def test_full_styling_chain(self) -> None:
        """Complex chaining should work correctly."""
        lst = (
            HTMLList(["A", "B", "C"])
            .horizontal
            .gap("20px")
            .padding("10px")
            .background("#f5f5f5")
            .border("1px solid #ccc")
            .border_radius("8px")
            .item_padding("15px")
            .item_background("white")
            .item_border_radius("4px")
        )
        rendered = lst.render()

        assert "display: flex" in rendered
        assert "gap: 20px" in rendered
        assert "padding: 10px" in rendered
        assert "background-color: #f5f5f5" in rendered
        assert "border: 1px solid #ccc" in rendered
        assert "border-radius: 8px" in rendered
        # Item styles
        assert "padding: 15px" in rendered
        assert "background-color: white" in rendered
