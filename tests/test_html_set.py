"""Tests for HTMLSet class."""

from animaid import HTMLSet


class TestHTMLSetBasics:
    """Test basic HTMLSet functionality."""

    def test_create_html_set(self) -> None:
        """Test creating an HTMLSet."""
        s = HTMLSet({1, 2, 3})
        assert set(s) == {1, 2, 3}

    def test_create_from_list(self) -> None:
        """Test creating HTMLSet from a list."""
        s = HTMLSet([1, 2, 3])
        assert set(s) == {1, 2, 3}

    def test_duplicates_removed(self) -> None:
        """Test that duplicates are removed."""
        s = HTMLSet([1, 1, 2, 2, 3, 3])
        assert len(s) == 3
        assert set(s) == {1, 2, 3}

    def test_render_default_braces(self) -> None:
        """Test default rendering with braces."""
        s = HTMLSet({1, 2, 3}).sorted
        html = s.render()
        assert html.startswith("<span>")
        assert html.endswith("</span>")
        assert "{" in html
        assert "}" in html

    def test_empty_set(self) -> None:
        """Test empty set."""
        s = HTMLSet(set())
        assert s.render() == "<span>{}</span>"

    def test_single_item(self) -> None:
        """Test single item set."""
        s = HTMLSet({42})
        assert s.render() == "<span>{42}</span>"

    def test_string_items(self) -> None:
        """Test set with string items."""
        s = HTMLSet({"a", "b", "c"}).sorted
        html = s.render()
        assert "a" in html
        assert "b" in html
        assert "c" in html


class TestSetFormats:
    """Test different set formats."""

    def test_braces_format(self) -> None:
        """Test braces format."""
        s = HTMLSet({1, 2, 3}).braces.sorted
        html = s.render()
        assert "{" in html
        assert "}" in html

    def test_plain_format(self) -> None:
        """Test plain format without braces."""
        s = HTMLSet({1, 2, 3}).plain
        html = s.render()
        assert "{" not in html
        assert "}" not in html
        assert "<div" in html


class TestSetDirection:
    """Test set layout directions."""

    def test_horizontal(self) -> None:
        """Test horizontal layout (default)."""
        s = HTMLSet({1, 2, 3}).plain.horizontal
        html = s.render()
        assert "flex-direction: row" in html

    def test_vertical(self) -> None:
        """Test vertical layout."""
        s = HTMLSet({1, 2, 3}).plain.vertical
        html = s.render()
        assert "flex-direction: column" in html

    def test_horizontal_reverse(self) -> None:
        """Test horizontal reverse layout."""
        s = HTMLSet({1, 2, 3}).plain.horizontal_reverse
        html = s.render()
        assert "flex-direction: row-reverse" in html

    def test_vertical_reverse(self) -> None:
        """Test vertical reverse layout."""
        s = HTMLSet({1, 2, 3}).plain.vertical_reverse
        html = s.render()
        assert "flex-direction: column-reverse" in html

    def test_grid(self) -> None:
        """Test grid layout."""
        s = HTMLSet({1, 2, 3, 4, 5, 6}).plain.grid(3)
        html = s.render()
        assert "display: inline-grid" in html
        assert "grid-template-columns" in html


class TestSetStyles:
    """Test HTMLSet styling."""

    def test_gap(self) -> None:
        """Test gap styling."""
        s = HTMLSet({1, 2, 3}).plain.gap("10px")
        assert "gap: 10px" in s.render()

    def test_padding(self) -> None:
        """Test padding styling."""
        s = HTMLSet({1, 2, 3}).padding("10px")
        assert "padding: 10px" in s.render()

    def test_margin(self) -> None:
        """Test margin styling."""
        s = HTMLSet({1, 2, 3}).margin("10px")
        assert "margin: 10px" in s.render()

    def test_border(self) -> None:
        """Test border styling."""
        s = HTMLSet({1, 2, 3}).border("1px solid black")
        assert "border: 1px solid black" in s.render()

    def test_border_radius(self) -> None:
        """Test border radius styling."""
        s = HTMLSet({1, 2, 3}).border_radius("5px")
        assert "border-radius: 5px" in s.render()

    def test_background(self) -> None:
        """Test background color."""
        s = HTMLSet({1, 2, 3}).background("yellow")
        assert "background-color: yellow" in s.render()

    def test_color(self) -> None:
        """Test text color."""
        s = HTMLSet({1, 2, 3}).color("red")
        assert "color: red" in s.render()


class TestSetItemStyles:
    """Test item-level styling."""

    def test_item_padding(self) -> None:
        """Test item padding."""
        s = HTMLSet({1, 2, 3}).plain.item_padding("5px")
        html = s.render()
        assert "padding: 5px" in html

    def test_item_background(self) -> None:
        """Test item background."""
        s = HTMLSet({1, 2, 3}).plain.item_background("#f0f0f0")
        html = s.render()
        assert "background-color: #f0f0f0" in html

    def test_item_border(self) -> None:
        """Test item border."""
        s = HTMLSet({1, 2, 3}).plain.item_border("1px solid gray")
        html = s.render()
        assert "border: 1px solid gray" in html

    def test_item_border_radius(self) -> None:
        """Test item border radius."""
        s = HTMLSet({1, 2, 3}).plain.item_border_radius("4px")
        html = s.render()
        assert "border-radius: 4px" in html


class TestSetPresets:
    """Test style presets."""

    def test_pills_preset(self) -> None:
        """Test pills preset."""
        s = HTMLSet({1, 2, 3}).pills
        html = s.render()
        assert "border-radius: 20px" in html
        assert "background-color: #e0e0e0" in html

    def test_tags_preset(self) -> None:
        """Test tags preset."""
        s = HTMLSet({1, 2, 3}).tags
        html = s.render()
        assert "background-color: #f5f5f5" in html
        assert "border-radius: 4px" in html

    def test_inline_preset(self) -> None:
        """Test inline preset."""
        s = HTMLSet({1, 2, 3}).inline
        html = s.render()
        assert "flex-direction: row" in html


class TestSetAlignment:
    """Test alignment methods."""

    def test_center(self) -> None:
        """Test center alignment."""
        s = HTMLSet({1, 2, 3}).plain.center
        html = s.render()
        assert "align-items: center" in html
        assert "justify-content: center" in html

    def test_align_items(self) -> None:
        """Test align_items method."""
        s = HTMLSet({1, 2, 3}).plain.align_items("flex-start")
        assert "align-items: flex-start" in s.render()

    def test_justify_content(self) -> None:
        """Test justify_content method."""
        s = HTMLSet({1, 2, 3}).plain.justify_content("space-between")
        assert "justify-content: space-between" in s.render()


class TestSetOperations:
    """Test set operations."""

    def test_union(self) -> None:
        """Test union operation preserves settings."""
        s1 = HTMLSet({1, 2}).plain.gap("10px")
        s2 = {3, 4}
        result = s1.union(s2)
        assert set(result) == {1, 2, 3, 4}
        assert isinstance(result, HTMLSet)
        assert "gap: 10px" in result.render()

    def test_union_operator(self) -> None:
        """Test union with | operator."""
        s1 = HTMLSet({1, 2})
        s2 = {3, 4}
        result = s1 | s2
        assert set(result) == {1, 2, 3, 4}
        assert isinstance(result, HTMLSet)

    def test_intersection(self) -> None:
        """Test intersection operation preserves settings."""
        s1 = HTMLSet({1, 2, 3}).plain.gap("10px")
        s2 = {2, 3, 4}
        result = s1.intersection(s2)
        assert set(result) == {2, 3}
        assert isinstance(result, HTMLSet)
        assert "gap: 10px" in result.render()

    def test_intersection_operator(self) -> None:
        """Test intersection with & operator."""
        s1 = HTMLSet({1, 2, 3})
        s2 = {2, 3, 4}
        result = s1 & s2
        assert set(result) == {2, 3}
        assert isinstance(result, HTMLSet)

    def test_difference(self) -> None:
        """Test difference operation preserves settings."""
        s1 = HTMLSet({1, 2, 3}).plain.gap("10px")
        s2 = {2, 3}
        result = s1.difference(s2)
        assert set(result) == {1}
        assert isinstance(result, HTMLSet)
        assert "gap: 10px" in result.render()

    def test_difference_operator(self) -> None:
        """Test difference with - operator."""
        s1 = HTMLSet({1, 2, 3})
        s2 = {2, 3}
        result = s1 - s2
        assert set(result) == {1}
        assert isinstance(result, HTMLSet)

    def test_symmetric_difference(self) -> None:
        """Test symmetric difference operation preserves settings."""
        s1 = HTMLSet({1, 2, 3}).plain.gap("10px")
        s2 = {2, 3, 4}
        result = s1.symmetric_difference(s2)
        assert set(result) == {1, 4}
        assert isinstance(result, HTMLSet)
        assert "gap: 10px" in result.render()

    def test_symmetric_difference_operator(self) -> None:
        """Test symmetric difference with ^ operator."""
        s1 = HTMLSet({1, 2, 3})
        s2 = {2, 3, 4}
        result = s1 ^ s2
        assert set(result) == {1, 4}
        assert isinstance(result, HTMLSet)


class TestSetMembership:
    """Test set membership operations."""

    def test_contains(self) -> None:
        """Test in operator."""
        s = HTMLSet({1, 2, 3})
        assert 1 in s
        assert 4 not in s

    def test_len(self) -> None:
        """Test len function."""
        s = HTMLSet({1, 2, 3})
        assert len(s) == 3

    def test_iteration(self) -> None:
        """Test iteration."""
        s = HTMLSet({1, 2, 3})
        items = set(s)
        assert items == {1, 2, 3}

    def test_issubset(self) -> None:
        """Test issubset method."""
        s1 = HTMLSet({1, 2})
        s2 = HTMLSet({1, 2, 3})
        assert s1.issubset(s2)
        assert not s2.issubset(s1)

    def test_issuperset(self) -> None:
        """Test issuperset method."""
        s1 = HTMLSet({1, 2, 3})
        s2 = HTMLSet({1, 2})
        assert s1.issuperset(s2)
        assert not s2.issuperset(s1)


class TestSetOrdering:
    """Test set ordering options."""

    def test_sorted_property(self) -> None:
        """Test sorted property."""
        s = HTMLSet({3, 1, 2}).sorted
        html = s.render()
        # Items should be in sorted order in the output
        idx_1 = html.find("1")
        idx_2 = html.find("2")
        idx_3 = html.find("3")
        assert idx_1 < idx_2 < idx_3

    def test_unsorted_property(self) -> None:
        """Test unsorted property."""
        s = HTMLSet({1, 2, 3}).sorted.unsorted
        assert s._sorted is False


class TestSetRepr:
    """Test HTMLSet representation."""

    def test_repr_basic(self) -> None:
        """Test basic repr."""
        s = HTMLSet({1, 2, 3})
        r = repr(s)
        assert "HTMLSet" in r
        assert "1" in r
        assert "2" in r
        assert "3" in r

    def test_repr_with_format(self) -> None:
        """Test repr with format."""
        s = HTMLSet({1, 2, 3}).plain
        assert "format=plain" in repr(s)

    def test_repr_with_direction(self) -> None:
        """Test repr with direction."""
        s = HTMLSet({1, 2, 3}).vertical
        assert "direction=vertical" in repr(s)

    def test_repr_with_sorted(self) -> None:
        """Test repr with sorted."""
        s = HTMLSet({1, 2, 3}).sorted
        assert "sorted=True" in repr(s)


class TestSetChaining:
    """Test method chaining."""

    def test_multiple_styles(self) -> None:
        """Test chaining multiple style methods."""
        s = (HTMLSet({1, 2, 3})
             .plain
             .horizontal
             .gap("10px")
             .padding("5px")
             .border("1px solid black"))
        html = s.render()
        assert "gap: 10px" in html
        assert "padding: 5px" in html
        assert "border: 1px solid black" in html

    def test_preset_then_customize(self) -> None:
        """Test using preset then customizing."""
        s = HTMLSet({1, 2, 3}).pills.gap("20px")
        html = s.render()
        assert "gap: 20px" in html
        assert "border-radius: 20px" in html


class TestHTMLObjectNesting:
    """Test nesting HTML objects in sets."""

    def test_nested_html_string(self) -> None:
        """Test set containing HTMLString."""
        from animaid import HTMLString
        s1 = HTMLString("hello").bold
        s2 = HTMLString("world").italic
        # Note: HTMLString must be hashable for this to work
        # Sets require hashable items
        s = HTMLSet({s1, s2})
        html = s.render()
        assert "hello" in html
        assert "world" in html

    def test_nested_html_int(self) -> None:
        """Test set containing HTMLInt."""
        from animaid import HTMLInt
        n1 = HTMLInt(1000).comma()
        n2 = HTMLInt(2000).comma()
        s = HTMLSet({n1, n2})
        html = s.render()
        assert "1,000" in html
        assert "2,000" in html
