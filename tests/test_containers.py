"""Tests for container widgets (HTMLContainer, HTMLRow, HTMLColumn, HTMLCard, HTMLDivider, HTMLSpacer)."""

import pytest

from animaid import (
    AlignItems,
    DividerStyle,
    FlexWrap,
    HTMLCard,
    HTMLColumn,
    HTMLContainer,
    HTMLDivider,
    HTMLRow,
    HTMLSpacer,
    HTMLString,
    JustifyContent,
    RadiusSize,
    ShadowSize,
    Size,
)


# =============================================================================
# HTMLContainer Base Tests
# =============================================================================


class TestHTMLContainerBasics:
    """Test basic HTMLContainer functionality."""

    def test_empty_container(self) -> None:
        """Empty container renders correctly."""
        container = HTMLContainer()
        html = container.render()
        assert html == "<div></div>"

    def test_container_with_children(self) -> None:
        """Container with children renders them."""
        container = HTMLContainer([
            HTMLString("Hello"),
            HTMLString("World"),
        ])
        html = container.render()
        assert "<span" in html
        assert "Hello" in html
        assert "World" in html

    def test_container_with_plain_strings(self) -> None:
        """Container escapes plain strings."""
        container = HTMLContainer(["Hello", "<script>bad</script>"])
        html = container.render()
        assert "Hello" in html
        assert "&lt;script&gt;" in html  # Escaped

    def test_len(self) -> None:
        """Container reports correct length."""
        container = HTMLContainer([1, 2, 3])
        assert len(container) == 3

    def test_iter(self) -> None:
        """Container is iterable."""
        items = [HTMLString("A"), HTMLString("B")]
        container = HTMLContainer(items)
        result = list(container)
        assert len(result) == 2

    def test_getitem(self) -> None:
        """Container supports indexing."""
        items = [HTMLString("A"), HTMLString("B")]
        container = HTMLContainer(items)
        assert container[0].render() == items[0].render()


class TestHTMLContainerChildManagement:
    """Test child management methods."""

    def test_append(self) -> None:
        """append() adds a child."""
        container = HTMLContainer()
        container.append(HTMLString("New"))
        assert len(container) == 1

    def test_append_returns_self(self) -> None:
        """append() returns self for chaining."""
        container = HTMLContainer()
        result = container.append(HTMLString("A"))
        assert result is container

    def test_extend(self) -> None:
        """extend() adds multiple children."""
        container = HTMLContainer()
        container.extend([HTMLString("A"), HTMLString("B")])
        assert len(container) == 2

    def test_insert(self) -> None:
        """insert() adds at specific position."""
        container = HTMLContainer([HTMLString("A"), HTMLString("C")])
        container.insert(1, HTMLString("B"))
        assert len(container) == 3

    def test_remove(self) -> None:
        """remove() removes a child."""
        item = HTMLString("Remove me")
        container = HTMLContainer([item])
        container.remove(item)
        assert len(container) == 0

    def test_pop(self) -> None:
        """pop() removes and returns last child."""
        item = HTMLString("Last")
        container = HTMLContainer([HTMLString("First"), item])
        popped = container.pop()
        assert len(container) == 1
        assert popped is item

    def test_pop_with_index(self) -> None:
        """pop(index) removes at specific position."""
        container = HTMLContainer([HTMLString("A"), HTMLString("B"), HTMLString("C")])
        popped = container.pop(1)
        assert len(container) == 2

    def test_clear(self) -> None:
        """clear() removes all children."""
        container = HTMLContainer([HTMLString("A"), HTMLString("B")])
        container.clear()
        assert len(container) == 0

    def test_children_property(self) -> None:
        """children property returns a copy."""
        item = HTMLString("A")
        container = HTMLContainer([item])
        children = container.children
        children.append(HTMLString("B"))  # Modify the copy
        assert len(container) == 1  # Original unchanged


class TestHTMLContainerStyling:
    """Test container styling methods."""

    def test_styled(self) -> None:
        """styled() applies CSS styles."""
        container = HTMLContainer().styled(background_color="red")
        html = container.render()
        assert 'style="background-color: red"' in html

    def test_styled_converts_underscores(self) -> None:
        """styled() converts underscores to hyphens."""
        container = HTMLContainer().styled(font_size="16px")
        html = container.render()
        assert "font-size: 16px" in html

    def test_add_class(self) -> None:
        """add_class() adds CSS classes."""
        container = HTMLContainer().add_class("my-class")
        html = container.render()
        assert 'class="my-class"' in html

    def test_add_multiple_classes(self) -> None:
        """add_class() can add multiple classes."""
        container = HTMLContainer().add_class("class1", "class2")
        html = container.render()
        assert "class1" in html
        assert "class2" in html

    def test_remove_class(self) -> None:
        """remove_class() removes CSS classes."""
        container = HTMLContainer().add_class("keep", "remove")
        container.remove_class("remove")
        html = container.render()
        assert "keep" in html
        assert "remove" not in html

    def test_gap(self) -> None:
        """gap() sets gap style."""
        container = HTMLContainer().gap(10)
        html = container.render()
        assert "gap: 10px" in html

    def test_gap_with_size(self) -> None:
        """gap() accepts Size object."""
        container = HTMLContainer().gap(Size.rem(1))
        html = container.render()
        assert "gap: 1rem" in html

    def test_padding(self) -> None:
        """padding() sets padding style."""
        container = HTMLContainer().padding(20)
        html = container.render()
        assert "padding: 20px" in html

    def test_margin(self) -> None:
        """margin() sets margin style."""
        container = HTMLContainer().margin("10px 20px")
        html = container.render()
        assert "margin: 10px 20px" in html

    def test_width_height(self) -> None:
        """width() and height() set dimensions."""
        container = HTMLContainer().width(100).height(200)
        html = container.render()
        assert "width: 100px" in html
        assert "height: 200px" in html


class TestHTMLContainerFullWindowLayout:
    """Test full-window layout convenience methods."""

    def test_full_width(self) -> None:
        """full_width() sets width to 100%."""
        container = HTMLContainer().full_width()
        html = container.render()
        assert "width: 100%" in html

    def test_full_height(self) -> None:
        """full_height() sets min-height to 100vh."""
        container = HTMLContainer().full_height()
        html = container.render()
        assert "min-height: 100vh" in html

    def test_full_screen(self) -> None:
        """full_screen() sets both width and min-height."""
        container = HTMLContainer().full_screen()
        html = container.render()
        assert "width: 100%" in html
        assert "min-height: 100vh" in html

    def test_expand(self) -> None:
        """expand() sets flex: 1."""
        container = HTMLContainer().expand()
        html = container.render()
        assert "flex: 1" in html

    def test_full_width_on_row(self) -> None:
        """full_width() works on HTMLRow."""
        row = HTMLRow([HTMLString("Test")]).full_width()
        html = row.render()
        assert "width: 100%" in html

    def test_full_height_on_column(self) -> None:
        """full_height() works on HTMLColumn."""
        column = HTMLColumn([HTMLString("Test")]).full_height()
        html = column.render()
        assert "min-height: 100vh" in html

    def test_expand_on_column(self) -> None:
        """expand() works on HTMLColumn for flex layouts."""
        column = HTMLColumn([HTMLString("Content")]).expand()
        html = column.render()
        assert "flex: 1" in html


# =============================================================================
# HTMLRow Tests
# =============================================================================


class TestHTMLRowBasics:
    """Test basic HTMLRow functionality."""

    def test_default_styles(self) -> None:
        """HTMLRow has flex row styles by default."""
        row = HTMLRow()
        html = row.render()
        assert "display: flex" in html
        assert "flex-direction: row" in html

    def test_with_children(self) -> None:
        """HTMLRow renders children."""
        row = HTMLRow([HTMLString("A"), HTMLString("B")])
        html = row.render()
        assert "A" in html
        assert "B" in html


class TestHTMLRowAlignment:
    """Test HTMLRow alignment methods."""

    def test_align_with_enum(self) -> None:
        """align() accepts AlignItems enum."""
        row = HTMLRow().align(AlignItems.CENTER)
        html = row.render()
        assert "align-items: center" in html

    def test_align_with_string(self) -> None:
        """align() accepts string value."""
        row = HTMLRow().align("center")
        html = row.render()
        assert "align-items: center" in html

    def test_justify_with_enum(self) -> None:
        """justify() accepts JustifyContent enum."""
        row = HTMLRow().justify(JustifyContent.SPACE_BETWEEN)
        html = row.render()
        assert "justify-content: space-between" in html

    def test_justify_with_string(self) -> None:
        """justify() accepts string value."""
        row = HTMLRow().justify("space-between")
        html = row.render()
        assert "justify-content: space-between" in html


class TestHTMLRowWrapping:
    """Test HTMLRow wrapping methods."""

    def test_wrap_default(self) -> None:
        """wrap() enables wrapping."""
        row = HTMLRow().wrap()
        html = row.render()
        assert "flex-wrap: wrap" in html

    def test_wrap_with_enum(self) -> None:
        """wrap() accepts FlexWrap enum."""
        row = HTMLRow().wrap(FlexWrap.WRAP_REVERSE)
        html = row.render()
        assert "flex-wrap: wrap-reverse" in html

    def test_nowrap(self) -> None:
        """nowrap() disables wrapping."""
        row = HTMLRow().nowrap()
        html = row.render()
        assert "flex-wrap: nowrap" in html


class TestHTMLRowDirection:
    """Test HTMLRow direction methods."""

    def test_reverse(self) -> None:
        """reverse() reverses row direction."""
        row = HTMLRow().reverse()
        html = row.render()
        assert "flex-direction: row-reverse" in html


class TestHTMLRowPresets:
    """Test HTMLRow preset methods."""

    def test_buttons_preset(self) -> None:
        """buttons() applies button row styling."""
        row = HTMLRow().buttons()
        html = row.render()
        assert "gap: 8px" in html
        assert "justify-content: flex-end" in html

    def test_toolbar_preset(self) -> None:
        """toolbar() applies toolbar styling."""
        row = HTMLRow().toolbar()
        html = row.render()
        assert "gap: 4px" in html
        assert "padding: 4px 8px" in html

    def test_centered_preset(self) -> None:
        """centered() centers items."""
        row = HTMLRow().centered()
        html = row.render()
        assert "justify-content: center" in html
        assert "align-items: center" in html

    def test_spaced_preset(self) -> None:
        """spaced() distributes items."""
        row = HTMLRow().spaced()
        html = row.render()
        assert "justify-content: space-between" in html

    def test_start_preset(self) -> None:
        """start() aligns to start."""
        row = HTMLRow().start()
        html = row.render()
        assert "justify-content: flex-start" in html

    def test_end_preset(self) -> None:
        """end() aligns to end."""
        row = HTMLRow().end()
        html = row.render()
        assert "justify-content: flex-end" in html


class TestHTMLRowChaining:
    """Test HTMLRow method chaining."""

    def test_chaining(self) -> None:
        """Methods can be chained."""
        row = HTMLRow().gap(10).align(AlignItems.CENTER).justify(JustifyContent.SPACE_BETWEEN)
        html = row.render()
        assert "gap: 10px" in html
        assert "align-items: center" in html
        assert "justify-content: space-between" in html

    def test_styled_returns_row(self) -> None:
        """styled() returns HTMLRow for chaining."""
        row = HTMLRow()
        result = row.styled(color="red")
        assert isinstance(result, HTMLRow)

    def test_add_class_returns_row(self) -> None:
        """add_class() returns HTMLRow for chaining."""
        row = HTMLRow()
        result = row.add_class("test")
        assert isinstance(result, HTMLRow)


# =============================================================================
# HTMLColumn Tests
# =============================================================================


class TestHTMLColumnBasics:
    """Test basic HTMLColumn functionality."""

    def test_default_styles(self) -> None:
        """HTMLColumn has flex column styles by default."""
        column = HTMLColumn()
        html = column.render()
        assert "display: flex" in html
        assert "flex-direction: column" in html

    def test_with_children(self) -> None:
        """HTMLColumn renders children."""
        column = HTMLColumn([HTMLString("A"), HTMLString("B")])
        html = column.render()
        assert "A" in html
        assert "B" in html


class TestHTMLColumnAlignment:
    """Test HTMLColumn alignment methods."""

    def test_align_with_enum(self) -> None:
        """align() accepts AlignItems enum."""
        column = HTMLColumn().align(AlignItems.CENTER)
        html = column.render()
        assert "align-items: center" in html

    def test_justify_with_enum(self) -> None:
        """justify() accepts JustifyContent enum."""
        column = HTMLColumn().justify(JustifyContent.SPACE_BETWEEN)
        html = column.render()
        assert "justify-content: space-between" in html


class TestHTMLColumnDirection:
    """Test HTMLColumn direction methods."""

    def test_reverse(self) -> None:
        """reverse() reverses column direction."""
        column = HTMLColumn().reverse()
        html = column.render()
        assert "flex-direction: column-reverse" in html


class TestHTMLColumnPresets:
    """Test HTMLColumn preset methods."""

    def test_stack_preset(self) -> None:
        """stack() applies stacked styling."""
        column = HTMLColumn().stack()
        html = column.render()
        assert "gap: 8px" in html

    def test_form_preset(self) -> None:
        """form() applies form styling."""
        column = HTMLColumn().form()
        html = column.render()
        assert "gap: 12px" in html
        assert "align-items: stretch" in html

    def test_centered_preset(self) -> None:
        """centered() centers items."""
        column = HTMLColumn().centered()
        html = column.render()
        assert "justify-content: center" in html
        assert "align-items: center" in html

    def test_stretch_preset(self) -> None:
        """stretch() stretches items."""
        column = HTMLColumn().stretch()
        html = column.render()
        assert "align-items: stretch" in html


class TestHTMLColumnChaining:
    """Test HTMLColumn method chaining."""

    def test_chaining(self) -> None:
        """Methods can be chained."""
        column = HTMLColumn().gap(16).align(AlignItems.CENTER).form()
        html = column.render()
        assert "align-items" in html

    def test_styled_returns_column(self) -> None:
        """styled() returns HTMLColumn for chaining."""
        column = HTMLColumn()
        result = column.styled(color="blue")
        assert isinstance(result, HTMLColumn)


# =============================================================================
# Nested Container Tests
# =============================================================================


class TestNestedContainers:
    """Test nesting containers inside each other."""

    def test_row_in_column(self) -> None:
        """Row can be nested in Column."""
        row = HTMLRow([HTMLString("A"), HTMLString("B")])
        column = HTMLColumn([HTMLString("Title"), row])
        html = column.render()
        assert "flex-direction: column" in html
        assert "flex-direction: row" in html

    def test_column_in_row(self) -> None:
        """Column can be nested in Row."""
        column = HTMLColumn([HTMLString("1"), HTMLString("2")])
        row = HTMLRow([column, HTMLString("Right")])
        html = row.render()
        assert "flex-direction: row" in html
        assert "flex-direction: column" in html

    def test_deeply_nested(self) -> None:
        """Deep nesting works correctly."""
        inner = HTMLRow([HTMLString("A"), HTMLString("B")])
        middle = HTMLColumn([HTMLString("Header"), inner])
        outer = HTMLRow([middle, HTMLString("Side")])
        html = outer.render()
        assert "A" in html
        assert "B" in html
        assert "Header" in html
        assert "Side" in html


# =============================================================================
# Integration with HTMLString Tests
# =============================================================================


class TestContainerWithStyledContent:
    """Test containers with styled HTMLString content."""

    def test_styled_strings_in_row(self) -> None:
        """Styled HTMLStrings render correctly in Row."""
        row = HTMLRow([
            HTMLString("Bold").bold(),
            HTMLString("Red").styled(color="red"),
        ])
        html = row.render()
        assert "font-weight: bold" in html
        assert "color: red" in html

    def test_styled_strings_in_column(self) -> None:
        """Styled HTMLStrings render correctly in Column."""
        column = HTMLColumn([
            HTMLString("Title").bold(),
            HTMLString("Subtitle").styled(color="gray"),
        ])
        html = column.render()
        assert "font-weight: bold" in html
        assert "color: gray" in html


# =============================================================================
# HTMLCard Tests
# =============================================================================


class TestHTMLCardBasics:
    """Test basic HTMLCard functionality."""

    def test_empty_card(self) -> None:
        """Empty card renders with default styles."""
        card = HTMLCard()
        html = card.render()
        assert "<div" in html
        assert "background-color: white" in html
        assert "padding: 16px" in html

    def test_card_with_children(self) -> None:
        """Card renders children."""
        card = HTMLCard([HTMLString("Content")])
        html = card.render()
        assert "Content" in html

    def test_card_with_title(self) -> None:
        """Card renders title."""
        card = HTMLCard(title="My Title", children=[HTMLString("Body")])
        html = card.render()
        assert "My Title" in html
        assert "Body" in html
        assert "font-weight: bold" in html

    def test_card_title_escapes_html(self) -> None:
        """Card title is HTML-escaped."""
        card = HTMLCard(title="<script>bad</script>")
        html = card.render()
        assert "&lt;script&gt;" in html

    def test_set_title(self) -> None:
        """set_title() changes the title."""
        card = HTMLCard()
        card.set_title("New Title")
        html = card.render()
        assert "New Title" in html

    def test_title_property(self) -> None:
        """title property returns current title."""
        card = HTMLCard(title="Test")
        assert card.title == "Test"


class TestHTMLCardShadow:
    """Test HTMLCard shadow methods."""

    def test_shadow_default(self) -> None:
        """shadow() adds default shadow."""
        card = HTMLCard().shadow()
        html = card.render()
        assert "box-shadow:" in html

    def test_shadow_with_size(self) -> None:
        """shadow() accepts ShadowSize enum."""
        card = HTMLCard().shadow(ShadowSize.LG)
        html = card.render()
        assert "box-shadow:" in html
        assert "10px 15px" in html

    def test_no_shadow(self) -> None:
        """no_shadow() removes shadow."""
        card = HTMLCard().shadow().no_shadow()
        html = card.render()
        assert "box-shadow: none" in html


class TestHTMLCardRounded:
    """Test HTMLCard border radius methods."""

    def test_rounded_default(self) -> None:
        """rounded() sets default border radius."""
        card = HTMLCard().rounded()
        html = card.render()
        assert "border-radius:" in html

    def test_rounded_with_size(self) -> None:
        """rounded() accepts RadiusSize enum."""
        card = HTMLCard().rounded(RadiusSize.LG)
        html = card.render()
        assert "border-radius: 8px" in html

    def test_no_rounded(self) -> None:
        """no_rounded() removes border radius."""
        card = HTMLCard().no_rounded()
        html = card.render()
        assert "border-radius: 0" in html


class TestHTMLCardBorder:
    """Test HTMLCard border methods."""

    def test_bordered(self) -> None:
        """bordered() adds a border."""
        card = HTMLCard().bordered()
        html = card.render()
        assert "border:" in html
        assert "solid" in html

    def test_bordered_with_color(self) -> None:
        """bordered() accepts color."""
        card = HTMLCard().bordered("red")
        html = card.render()
        assert "border:" in html
        assert "red" in html

    def test_no_border(self) -> None:
        """no_border() removes border."""
        card = HTMLCard().bordered().no_border()
        html = card.render()
        assert "border:" not in html


class TestHTMLCardPresets:
    """Test HTMLCard preset methods."""

    def test_default_preset(self) -> None:
        """default() applies light styling."""
        card = HTMLCard().default()
        html = card.render()
        assert "border:" in html
        assert "box-shadow:" in html

    def test_elevated_preset(self) -> None:
        """elevated() applies prominent shadow."""
        card = HTMLCard().elevated()
        html = card.render()
        assert "box-shadow:" in html
        assert "10px 15px" in html  # LG shadow

    def test_outlined_preset(self) -> None:
        """outlined() applies border only."""
        card = HTMLCard().outlined()
        html = card.render()
        assert "border:" in html
        assert "box-shadow: none" in html

    def test_flat_preset(self) -> None:
        """flat() removes border and shadow."""
        card = HTMLCard().flat()
        html = card.render()
        assert "box-shadow: none" in html

    def test_filled_preset(self) -> None:
        """filled() applies background color."""
        card = HTMLCard().filled("#f0f0f0")
        html = card.render()
        assert "background-color: #f0f0f0" in html


class TestHTMLCardChaining:
    """Test HTMLCard method chaining."""

    def test_chaining(self) -> None:
        """Methods can be chained."""
        card = HTMLCard().shadow().rounded().bordered()
        html = card.render()
        assert "box-shadow:" in html
        assert "border-radius:" in html
        assert "border:" in html

    def test_styled_returns_card(self) -> None:
        """styled() returns HTMLCard."""
        card = HTMLCard()
        result = card.styled(color="red")
        assert isinstance(result, HTMLCard)


# =============================================================================
# HTMLDivider Tests
# =============================================================================


class TestHTMLDividerBasics:
    """Test basic HTMLDivider functionality."""

    def test_simple_divider(self) -> None:
        """Simple divider renders as hr."""
        divider = HTMLDivider()
        html = divider.render()
        assert "<hr" in html
        assert "border-top:" in html

    def test_divider_with_label(self) -> None:
        """Divider with label renders text."""
        divider = HTMLDivider("OR")
        html = divider.render()
        assert "OR" in html
        assert "display: flex" in html

    def test_label_escapes_html(self) -> None:
        """Label is HTML-escaped."""
        divider = HTMLDivider("<script>bad</script>")
        html = divider.render()
        assert "&lt;script&gt;" in html


class TestHTMLDividerOrientation:
    """Test HTMLDivider orientation methods."""

    def test_vertical(self) -> None:
        """vertical() creates vertical divider."""
        divider = HTMLDivider().vertical()
        html = divider.render()
        assert "border-left:" in html

    def test_horizontal(self) -> None:
        """horizontal() creates horizontal divider."""
        divider = HTMLDivider().vertical().horizontal()
        html = divider.render()
        assert "<hr" in html or "border-top:" in html


class TestHTMLDividerStyle:
    """Test HTMLDivider style methods."""

    def test_solid(self) -> None:
        """solid() sets solid style."""
        divider = HTMLDivider().solid()
        html = divider.render()
        assert "solid" in html

    def test_dashed(self) -> None:
        """dashed() sets dashed style."""
        divider = HTMLDivider().dashed()
        html = divider.render()
        assert "dashed" in html

    def test_dotted(self) -> None:
        """dotted() sets dotted style."""
        divider = HTMLDivider().dotted()
        html = divider.render()
        assert "dotted" in html

    def test_style_with_enum(self) -> None:
        """style() accepts DividerStyle enum."""
        divider = HTMLDivider().style(DividerStyle.DASHED)
        html = divider.render()
        assert "dashed" in html


class TestHTMLDividerStyling:
    """Test HTMLDivider color and sizing."""

    def test_color(self) -> None:
        """color() sets divider color."""
        divider = HTMLDivider().color("red")
        html = divider.render()
        assert "red" in html

    def test_thickness(self) -> None:
        """thickness() sets divider width."""
        divider = HTMLDivider().thickness(3)
        html = divider.render()
        assert "3px" in html

    def test_margin(self) -> None:
        """margin() sets margin."""
        divider = HTMLDivider().margin("20px 0")
        html = divider.render()
        assert "20px 0" in html


class TestHTMLDividerPresets:
    """Test HTMLDivider preset methods."""

    def test_subtle(self) -> None:
        """subtle() applies light color."""
        divider = HTMLDivider().subtle()
        html = divider.render()
        assert "#f3f4f6" in html

    def test_bold(self) -> None:
        """bold() applies dark, thick style."""
        divider = HTMLDivider().bold()
        html = divider.render()
        assert "#374151" in html
        assert "2px" in html


# =============================================================================
# HTMLSpacer Tests
# =============================================================================


class TestHTMLSpacerBasics:
    """Test basic HTMLSpacer functionality."""

    def test_empty_spacer(self) -> None:
        """Empty spacer renders as div."""
        spacer = HTMLSpacer()
        html = spacer.render()
        assert "<div" in html

    def test_spacer_with_height(self) -> None:
        """Spacer with height."""
        spacer = HTMLSpacer().height(20)
        html = spacer.render()
        assert "height: 20px" in html

    def test_spacer_with_width(self) -> None:
        """Spacer with width."""
        spacer = HTMLSpacer().width(50)
        html = spacer.render()
        assert "width: 50px" in html


class TestHTMLSpacerSize:
    """Test HTMLSpacer size methods."""

    def test_size(self) -> None:
        """size() sets both width and height."""
        spacer = HTMLSpacer().size(100, 50)
        html = spacer.render()
        assert "width: 100px" in html
        assert "height: 50px" in html

    def test_height_with_size_object(self) -> None:
        """height() accepts Size object."""
        spacer = HTMLSpacer().height(Size.rem(2))
        html = spacer.render()
        assert "height: 2rem" in html


class TestHTMLSpacerFlex:
    """Test HTMLSpacer flex methods."""

    def test_flex(self) -> None:
        """flex() sets flex property."""
        spacer = HTMLSpacer().flex()
        html = spacer.render()
        assert "flex: 1" in html

    def test_flex_with_value(self) -> None:
        """flex() accepts grow value."""
        spacer = HTMLSpacer().flex(2)
        html = spacer.render()
        assert "flex: 2" in html

    def test_grow(self) -> None:
        """grow() sets flex-grow."""
        spacer = HTMLSpacer().grow(3)
        html = spacer.render()
        assert "flex-grow: 3" in html

    def test_shrink(self) -> None:
        """shrink() sets flex-shrink."""
        spacer = HTMLSpacer().shrink(0)
        html = spacer.render()
        assert "flex-shrink: 0" in html


class TestHTMLSpacerPresets:
    """Test HTMLSpacer preset methods."""

    def test_xs(self) -> None:
        """xs() creates 4px spacer."""
        spacer = HTMLSpacer().xs()
        html = spacer.render()
        assert "4px" in html

    def test_sm(self) -> None:
        """sm() creates 8px spacer."""
        spacer = HTMLSpacer().sm()
        html = spacer.render()
        assert "8px" in html

    def test_md(self) -> None:
        """md() creates 16px spacer."""
        spacer = HTMLSpacer().md()
        html = spacer.render()
        assert "16px" in html

    def test_lg(self) -> None:
        """lg() creates 24px spacer."""
        spacer = HTMLSpacer().lg()
        html = spacer.render()
        assert "24px" in html

    def test_xl(self) -> None:
        """xl() creates 32px spacer."""
        spacer = HTMLSpacer().xl()
        html = spacer.render()
        assert "32px" in html


# =============================================================================
# Integration Tests with New Containers
# =============================================================================


class TestContainerIntegration:
    """Test integration of Card, Divider, Spacer with Row/Column."""

    def test_card_in_row(self) -> None:
        """Card can be placed in a Row."""
        card = HTMLCard([HTMLString("Content")])
        row = HTMLRow([card, HTMLString("Side")])
        html = row.render()
        assert "Content" in html
        assert "Side" in html
        assert "background-color: white" in html

    def test_divider_in_row(self) -> None:
        """Vertical divider works in a Row."""
        divider = HTMLDivider().vertical()
        row = HTMLRow([HTMLString("Left"), divider, HTMLString("Right")])
        html = row.render()
        assert "Left" in html
        assert "Right" in html
        assert "border-left:" in html

    def test_spacer_in_row(self) -> None:
        """Flex spacer works in a Row."""
        spacer = HTMLSpacer().flex()
        row = HTMLRow([HTMLString("Left"), spacer, HTMLString("Right")])
        html = row.render()
        assert "flex: 1" in html

    def test_divider_in_column(self) -> None:
        """Horizontal divider works in a Column."""
        divider = HTMLDivider()
        column = HTMLColumn([HTMLString("Above"), divider, HTMLString("Below")])
        html = column.render()
        assert "Above" in html
        assert "Below" in html
        assert "<hr" in html

    def test_card_with_row_inside(self) -> None:
        """Row can be nested inside Card."""
        row = HTMLRow([HTMLString("A"), HTMLString("B")])
        card = HTMLCard(title="Header", children=[row])
        html = card.render()
        assert "Header" in html
        assert "flex-direction: row" in html
