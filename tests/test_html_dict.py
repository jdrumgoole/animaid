"""Tests for HTMLDict class."""

import pytest

from animaid import HTMLDict, HTMLList, HTMLString


class TestHTMLDictBasics:
    """Test basic HTMLDict functionality."""

    def test_is_dict_subclass(self) -> None:
        """HTMLDict should be a subclass of dict."""
        d = HTMLDict({"a": 1, "b": 2})
        assert isinstance(d, dict)

    def test_dict_value(self) -> None:
        """HTMLDict should preserve dict items."""
        d = HTMLDict({"name": "Alice", "age": 30})
        assert dict(d) == {"name": "Alice", "age": 30}
        assert len(d) == 2

    def test_empty_dict(self) -> None:
        """HTMLDict should handle empty dicts."""
        d = HTMLDict()
        assert d.render() == "<dl></dl>"

    def test_repr(self) -> None:
        """HTMLDict should have informative repr."""
        d = HTMLDict({"a": 1})
        assert repr(d) == "HTMLDict({'a': 1})"

    def test_repr_with_format(self) -> None:
        """HTMLDict repr should show format."""
        d = HTMLDict({"a": 1}).as_table
        assert "format=table" in repr(d)


class TestHTMLDictRendering:
    """Test HTML rendering functionality."""

    def test_basic_render(self) -> None:
        """Basic render should create definition list."""
        d = HTMLDict({"name": "Alice"})
        assert d.render() == "<dl><dt>name</dt><dd>Alice</dd></dl>"

    def test_render_multiple_items(self) -> None:
        """Render should handle multiple items."""
        d = HTMLDict({"a": 1, "b": 2})
        rendered = d.render()
        assert "<dt>a</dt><dd>1</dd>" in rendered
        assert "<dt>b</dt><dd>2</dd>" in rendered

    def test_render_escapes_html(self) -> None:
        """Render should escape HTML in keys and values."""
        d = HTMLDict({"<key>": "<value>"})
        rendered = d.render()
        assert "&lt;key&gt;" in rendered
        assert "&lt;value&gt;" in rendered

    def test_render_with_styles(self) -> None:
        """Render should include container styles."""
        d = HTMLDict({"a": 1}).styled(color="red")
        rendered = d.render()
        assert "color: red" in rendered

    def test_render_with_classes(self) -> None:
        """Render should include CSS classes."""
        d = HTMLDict({"a": 1}).add_class("my-dict")
        rendered = d.render()
        assert 'class="my-dict"' in rendered

    def test_dunder_html(self) -> None:
        """__html__ should return rendered output for Jinja2."""
        d = HTMLDict({"a": 1})
        assert d.__html__() == d.render()


class TestHTMLDictFormats:
    """Test different rendering formats."""

    def test_definition_list_format(self) -> None:
        """Definition list format should use dl/dt/dd tags."""
        d = HTMLDict({"key": "value"}).as_definition_list
        rendered = d.render()
        assert rendered.startswith("<dl")
        assert "<dt>key</dt>" in rendered
        assert "<dd>value</dd>" in rendered

    def test_table_format(self) -> None:
        """Table format should use table/tr/td tags."""
        d = HTMLDict({"key": "value"}).as_table
        rendered = d.render()
        assert rendered.startswith("<table")
        assert "<tr>" in rendered
        assert "<td>key</td>" in rendered
        assert "<td>value</td>" in rendered

    def test_divs_format(self) -> None:
        """Divs format should use div tags with flexbox."""
        d = HTMLDict({"key": "value"}).as_divs
        rendered = d.render()
        assert rendered.startswith("<div")
        assert "<div>key</div>" in rendered
        assert "<div>value</div>" in rendered


class TestHTMLDictLayout:
    """Test layout options."""

    def test_vertical_layout(self) -> None:
        """Vertical layout should stack entries."""
        d = HTMLDict({"a": 1, "b": 2}).as_divs.vertical
        rendered = d.render()
        assert "flex-direction: column" in rendered

    def test_horizontal_layout(self) -> None:
        """Horizontal layout should arrange entries side by side."""
        d = HTMLDict({"a": 1, "b": 2}).horizontal
        rendered = d.render()
        assert "display: flex" in rendered
        assert "flex-direction: row" in rendered

    def test_grid_layout(self) -> None:
        """Grid layout should use CSS grid."""
        d = HTMLDict({"a": 1, "b": 2, "c": 3}).grid(2)
        rendered = d.render()
        assert "display: grid" in rendered
        assert "grid-template-columns" in rendered


class TestHTMLDictKeyStyles:
    """Test key styling methods."""

    def test_key_bold(self) -> None:
        """Key bold should add font-weight: bold to keys."""
        d = HTMLDict({"key": "value"}).key_bold
        rendered = d.render()
        assert "font-weight: bold" in rendered

    def test_key_italic(self) -> None:
        """Key italic should add font-style: italic to keys."""
        d = HTMLDict({"key": "value"}).key_italic
        rendered = d.render()
        assert "font-style: italic" in rendered

    def test_key_color(self) -> None:
        """Key color should set key text color."""
        d = HTMLDict({"key": "value"}).key_color("blue")
        rendered = d.render()
        assert "color: blue" in rendered

    def test_key_background(self) -> None:
        """Key background should set key background color."""
        d = HTMLDict({"key": "value"}).key_background("yellow")
        rendered = d.render()
        assert "background-color: yellow" in rendered

    def test_key_width(self) -> None:
        """Key width should set fixed key width."""
        d = HTMLDict({"key": "value"}).key_width("100px")
        rendered = d.render()
        assert "width: 100px" in rendered

    def test_key_padding(self) -> None:
        """Key padding should add padding to keys."""
        d = HTMLDict({"key": "value"}).key_padding("10px")
        rendered = d.render()
        assert "padding: 10px" in rendered

    def test_add_key_class(self) -> None:
        """Add key class should add CSS classes to keys."""
        d = HTMLDict({"key": "value"}).add_key_class("key-class")
        rendered = d.render()
        assert 'class="key-class"' in rendered

    def test_hide_keys(self) -> None:
        """Hide keys should render only values."""
        d = HTMLDict({"key": "value"}).hide_keys
        rendered = d.render()
        assert "key" not in rendered or "<dt>" not in rendered


class TestHTMLDictValueStyles:
    """Test value styling methods."""

    def test_value_bold(self) -> None:
        """Value bold should add font-weight: bold to values."""
        d = HTMLDict({"key": "value"}).value_bold
        rendered = d.render()
        # The bold style should be on the dd element
        assert "font-weight: bold" in rendered

    def test_value_italic(self) -> None:
        """Value italic should add font-style: italic to values."""
        d = HTMLDict({"key": "value"}).value_italic
        rendered = d.render()
        assert "font-style: italic" in rendered

    def test_value_color(self) -> None:
        """Value color should set value text color."""
        d = HTMLDict({"key": "value"}).value_color("green")
        rendered = d.render()
        assert "color: green" in rendered

    def test_value_background(self) -> None:
        """Value background should set value background color."""
        d = HTMLDict({"key": "value"}).value_background("lightgray")
        rendered = d.render()
        assert "background-color: lightgray" in rendered

    def test_value_padding(self) -> None:
        """Value padding should add padding to values."""
        d = HTMLDict({"key": "value"}).value_padding("5px")
        rendered = d.render()
        assert "padding: 5px" in rendered

    def test_add_value_class(self) -> None:
        """Add value class should add CSS classes to values."""
        d = HTMLDict({"key": "value"}).add_value_class("value-class")
        rendered = d.render()
        assert 'class="value-class"' in rendered


class TestHTMLDictSeparators:
    """Test separator methods."""

    def test_key_value_separator(self) -> None:
        """Separator should add text between key and value."""
        d = HTMLDict({"name": "Alice"}).separator(": ")
        rendered = d.render()
        assert "name: " in rendered

    def test_entry_separator(self) -> None:
        """Entry separator should add border between entries."""
        d = HTMLDict({"a": 1, "b": 2}).entry_separator("1px solid gray")
        rendered = d.render()
        assert "border-bottom: 1px solid gray" in rendered


class TestHTMLDictContainerStyles:
    """Test container styling methods."""

    def test_gap(self) -> None:
        """Gap should add spacing between entries."""
        d = HTMLDict({"a": 1}).as_divs.gap("10px")
        rendered = d.render()
        assert "gap: 10px" in rendered

    def test_padding(self) -> None:
        """Padding should add container padding."""
        d = HTMLDict({"a": 1}).padding("15px")
        rendered = d.render()
        assert "padding: 15px" in rendered

    def test_margin(self) -> None:
        """Margin should add container margin."""
        d = HTMLDict({"a": 1}).margin("5px")
        rendered = d.render()
        assert "margin: 5px" in rendered

    def test_border(self) -> None:
        """Border should add container border."""
        d = HTMLDict({"a": 1}).border("1px solid black")
        rendered = d.render()
        assert "border: 1px solid black" in rendered

    def test_border_radius(self) -> None:
        """Border radius should round container corners."""
        d = HTMLDict({"a": 1}).border_radius("5px")
        rendered = d.render()
        assert "border-radius: 5px" in rendered

    def test_background(self) -> None:
        """Background should set container background."""
        d = HTMLDict({"a": 1}).background("#f0f0f0")
        rendered = d.render()
        assert "background-color: #f0f0f0" in rendered

    def test_color(self) -> None:
        """Color should set text color."""
        d = HTMLDict({"a": 1}).color("navy")
        rendered = d.render()
        assert "color: navy" in rendered

    def test_width(self) -> None:
        """Width should set container width."""
        d = HTMLDict({"a": 1}).width("300px")
        rendered = d.render()
        assert "width: 300px" in rendered

    def test_max_width(self) -> None:
        """Max width should constrain container."""
        d = HTMLDict({"a": 1}).max_width("500px")
        rendered = d.render()
        assert "max-width: 500px" in rendered


class TestHTMLDictNesting:
    """Test nested rendering."""

    def test_nested_html_string(self) -> None:
        """HTMLString values should render with their styles."""
        styled = HTMLString("Important").bold.color("red")
        d = HTMLDict({"status": styled})
        rendered = d.render()
        assert "font-weight: bold" in rendered
        assert "color: red" in rendered
        assert "Important" in rendered

    def test_nested_html_list(self) -> None:
        """HTMLList values should render recursively."""
        items = HTMLList(["a", "b", "c"]).horizontal.gap("5px")
        d = HTMLDict({"items": items})
        rendered = d.render()
        assert "display: flex" in rendered
        assert "gap: 5px" in rendered

    def test_nested_html_dict(self) -> None:
        """HTMLDict values should render recursively."""
        inner = HTMLDict({"x": 1, "y": 2}).as_table
        d = HTMLDict({"nested": inner})
        rendered = d.render()
        assert "<table>" in rendered

    def test_mixed_nested(self) -> None:
        """Mixed nested types should render correctly."""
        d = HTMLDict({
            "name": HTMLString("Alice").bold,
            "hobbies": HTMLList(["reading", "coding"]),
            "scores": HTMLDict({"math": 95, "science": 88}),
        })
        rendered = d.render()
        assert "Alice" in rendered
        assert "reading" in rendered
        assert "math" in rendered


class TestHTMLDictImmutability:
    """Test that styling returns new instances."""

    def test_key_bold_returns_new(self) -> None:
        """Key bold should return new instance."""
        d1 = HTMLDict({"a": 1})
        d2 = d1.key_bold
        assert d1 is not d2

    def test_chaining_preserves_original(self) -> None:
        """Chaining should not modify original."""
        d1 = HTMLDict({"a": 1})
        d2 = d1.key_bold.key_color("blue").value_italic

        # Original unchanged
        rendered1 = d1.render()
        assert "font-weight: bold" not in rendered1

        # New has all styles
        rendered2 = d2.render()
        assert "font-weight: bold" in rendered2
        assert "color: blue" in rendered2


class TestHTMLDictOperations:
    """Test dict operations preserve settings."""

    def test_merge_operator(self) -> None:
        """Merge operator should preserve settings."""
        d = HTMLDict({"a": 1}).key_bold
        result = d | {"b": 2}
        assert isinstance(result, HTMLDict)
        assert dict(result) == {"a": 1, "b": 2}
        assert "font-weight: bold" in result.render()


class TestHTMLDictChaining:
    """Test complex method chaining."""

    def test_full_styling_chain(self) -> None:
        """Complex chaining should work correctly."""
        d = (
            HTMLDict({"name": "Alice", "role": "Developer"})
            .as_table
            .key_bold
            .key_color("#333")
            .key_padding("10px")
            .value_color("#666")
            .value_padding("10px")
            .separator(": ")
            .border("1px solid #ccc")
            .padding("15px")
        )
        rendered = d.render()

        assert "<table" in rendered
        assert "font-weight: bold" in rendered
        assert "color: #333" in rendered
        assert "padding: 15px" in rendered
        assert "border: 1px solid #ccc" in rendered
