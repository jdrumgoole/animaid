"""Tests for HTML input widgets."""

import threading
import time


class TestInputEvent:
    """Tests for InputEvent dataclass."""

    def test_basic_event(self) -> None:
        """Test creating a basic event."""
        from animaid import InputEvent

        event = InputEvent(id="button_1", event_type="click")
        assert event.id == "button_1"
        assert event.event_type == "click"
        assert event.value is None
        assert event.timestamp is None

    def test_event_with_value(self) -> None:
        """Test creating an event with a value."""
        from animaid import InputEvent

        event = InputEvent(id="text_1", event_type="change", value="hello")
        assert event.id == "text_1"
        assert event.event_type == "change"
        assert event.value == "hello"

    def test_event_with_timestamp(self) -> None:
        """Test creating an event with a timestamp."""
        from animaid import InputEvent

        event = InputEvent(
            id="slider_1", event_type="change", value=50, timestamp=1234567890.0
        )
        assert event.timestamp == 1234567890.0

    def test_event_repr(self) -> None:
        """Test event string representation."""
        from animaid import InputEvent

        event = InputEvent(id="btn", event_type="click")
        assert "btn" in repr(event)
        assert "click" in repr(event)

    def test_event_repr_with_value(self) -> None:
        """Test event repr includes value."""
        from animaid import InputEvent

        event = InputEvent(id="text", event_type="change", value="test")
        assert "test" in repr(event)


class TestHTMLButton:
    """Tests for HTMLButton widget."""

    def test_basic_button(self) -> None:
        """Test creating a basic button."""
        from animaid import HTMLButton

        button = HTMLButton("Click Me")
        assert button.label == "Click Me"
        html = button.render()
        assert "Click Me" in html
        assert "anim-button" in html

    def test_button_on_click(self) -> None:
        """Test setting on_click callback."""
        from animaid import HTMLButton

        callback_called = False

        def callback() -> None:
            nonlocal callback_called
            callback_called = True

        button = HTMLButton("Test").on_click(callback)
        assert button._on_click is callback

        # Simulate callback
        button._on_click()
        assert callback_called

    def test_button_primary_preset(self) -> None:
        """Test primary button style."""
        from animaid import HTMLButton

        button = HTMLButton("Submit").primary()
        html = button.render()
        assert "primary" in html

    def test_button_danger_preset(self) -> None:
        """Test danger button style."""
        from animaid import HTMLButton

        button = HTMLButton("Delete").danger()
        html = button.render()
        assert "danger" in html

    def test_button_success_preset(self) -> None:
        """Test success button style."""
        from animaid import HTMLButton

        button = HTMLButton("Save").success()
        html = button.render()
        assert "success" in html

    def test_button_warning_preset(self) -> None:
        """Test warning button style."""
        from animaid import HTMLButton

        button = HTMLButton("Caution").warning()
        html = button.render()
        assert "warning" in html

    def test_button_large(self) -> None:
        """Test large button style."""
        from animaid import HTMLButton

        button = HTMLButton("Big").large()
        html = button.render()
        assert "18px" in html

    def test_button_small(self) -> None:
        """Test small button style."""
        from animaid import HTMLButton

        button = HTMLButton("Tiny").small()
        html = button.render()
        assert "12px" in html

    def test_button_styled(self) -> None:
        """Test custom styling."""
        from animaid import HTMLButton

        button = HTMLButton("Custom").styled(font_size="20px", color="purple")
        html = button.render()
        assert "font-size: 20px" in html
        assert "color: purple" in html

    def test_button_add_class(self) -> None:
        """Test adding CSS classes."""
        from animaid import HTMLButton

        button = HTMLButton("Styled").add_class("my-class", "another")
        html = button.render()
        assert "my-class" in html
        assert "another" in html

    def test_button_chaining(self) -> None:
        """Test method chaining."""
        from animaid import HTMLButton

        button = HTMLButton("Chained").primary().large()
        html = button.render()
        assert "primary" in html
        assert "18px" in html

    def test_button_html_escaping(self) -> None:
        """Test HTML escaping in label."""
        from animaid import HTMLButton

        button = HTMLButton("<script>alert('xss')</script>")
        html = button.render()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_button_anim_id_in_render(self) -> None:
        """Test that anim_id appears in rendered HTML."""
        from animaid import HTMLButton

        button = HTMLButton("Test")
        button._anim_id = "button_1"
        html = button.render()
        assert 'data-anim-id="button_1"' in html

    def test_button_html_method(self) -> None:
        """Test __html__ method for Jinja2."""
        from animaid import HTMLButton

        button = HTMLButton("Jinja")
        assert button.__html__() == button.render()


class TestHTMLTextInput:
    """Tests for HTMLTextInput widget."""

    def test_basic_text_input(self) -> None:
        """Test creating a basic text input."""
        from animaid import HTMLTextInput

        text = HTMLTextInput()
        html = text.render()
        assert 'type="text"' in html
        assert "anim-text-input" in html

    def test_text_input_with_value(self) -> None:
        """Test text input with initial value."""
        from animaid import HTMLTextInput

        text = HTMLTextInput(value="Hello")
        assert text.value == "Hello"
        html = text.render()
        assert 'value="Hello"' in html

    def test_text_input_with_placeholder(self) -> None:
        """Test text input with placeholder."""
        from animaid import HTMLTextInput

        text = HTMLTextInput(placeholder="Enter text...")
        assert text.placeholder == "Enter text..."
        html = text.render()
        assert 'placeholder="Enter text..."' in html

    def test_text_input_value_property(self) -> None:
        """Test value property getter and setter."""
        from animaid import HTMLTextInput

        text = HTMLTextInput(value="Initial")
        assert text.value == "Initial"
        text.value = "Changed"
        assert text.value == "Changed"

    def test_text_input_thread_safe_value(self) -> None:
        """Test thread-safe value access."""
        from animaid import HTMLTextInput

        text = HTMLTextInput(value="test")
        results: list[str] = []

        def reader() -> None:
            for _ in range(100):
                results.append(text.value)
                time.sleep(0.001)

        def writer() -> None:
            for i in range(100):
                text.value = f"value_{i}"
                time.sleep(0.001)

        t1 = threading.Thread(target=reader)
        t2 = threading.Thread(target=writer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Should not raise any errors
        assert len(results) == 100

    def test_text_input_on_change(self) -> None:
        """Test on_change callback."""
        from animaid import HTMLTextInput

        received: list[str] = []

        def callback(value: str) -> None:
            received.append(value)

        text = HTMLTextInput().on_change(callback)
        text._on_change("hello")
        assert received == ["hello"]

    def test_text_input_on_submit(self) -> None:
        """Test on_submit callback."""
        from animaid import HTMLTextInput

        received: list[str] = []

        def callback(value: str) -> None:
            received.append(value)

        text = HTMLTextInput().on_submit(callback)
        text._on_submit("submitted")
        assert received == ["submitted"]

    def test_text_input_wide(self) -> None:
        """Test wide preset."""
        from animaid import HTMLTextInput

        text = HTMLTextInput().wide()
        html = text.render()
        assert "width: 100%" in html

    def test_text_input_large(self) -> None:
        """Test large preset."""
        from animaid import HTMLTextInput

        text = HTMLTextInput().large()
        html = text.render()
        assert "18px" in html

    def test_text_input_small(self) -> None:
        """Test small preset."""
        from animaid import HTMLTextInput

        text = HTMLTextInput().small()
        html = text.render()
        assert "12px" in html

    def test_text_input_html_escaping(self) -> None:
        """Test HTML escaping."""
        from animaid import HTMLTextInput

        text = HTMLTextInput(value='<script>"test"</script>')
        html = text.render()
        assert "<script>" not in html


class TestHTMLCheckbox:
    """Tests for HTMLCheckbox widget."""

    def test_basic_checkbox(self) -> None:
        """Test creating a basic checkbox."""
        from animaid import HTMLCheckbox

        checkbox = HTMLCheckbox("Accept terms")
        assert checkbox.label == "Accept terms"
        assert checkbox.checked is False
        html = checkbox.render()
        assert "Accept terms" in html
        assert "anim-checkbox" in html

    def test_checkbox_checked(self) -> None:
        """Test checkbox with checked=True."""
        from animaid import HTMLCheckbox

        checkbox = HTMLCheckbox("Enabled", checked=True)
        assert checkbox.checked is True
        html = checkbox.render()
        assert "checked" in html

    def test_checkbox_value_property(self) -> None:
        """Test value property (alias for checked)."""
        from animaid import HTMLCheckbox

        checkbox = HTMLCheckbox("Test", checked=False)
        assert checkbox.value is False
        checkbox.value = True
        assert checkbox.checked is True
        assert checkbox.value is True

    def test_checkbox_on_change(self) -> None:
        """Test on_change callback."""
        from animaid import HTMLCheckbox

        received: list[bool] = []

        def callback(checked: bool) -> None:
            received.append(checked)

        checkbox = HTMLCheckbox("Test").on_change(callback)
        checkbox._on_change(True)
        assert received == [True]

    def test_checkbox_large(self) -> None:
        """Test large preset."""
        from animaid import HTMLCheckbox

        checkbox = HTMLCheckbox("Big").large()
        html = checkbox.render()
        assert "18px" in html

    def test_checkbox_small(self) -> None:
        """Test small preset."""
        from animaid import HTMLCheckbox

        checkbox = HTMLCheckbox("Small").small()
        html = checkbox.render()
        assert "12px" in html


class TestHTMLSlider:
    """Tests for HTMLSlider widget."""

    def test_basic_slider(self) -> None:
        """Test creating a basic slider."""
        from animaid import HTMLSlider

        slider = HTMLSlider()
        assert slider.min == 0
        assert slider.max == 100
        assert slider.value == 0
        assert slider.step == 1
        html = slider.render()
        assert 'type="range"' in html
        assert "anim-slider" in html

    def test_slider_custom_range(self) -> None:
        """Test slider with custom range."""
        from animaid import HTMLSlider

        slider = HTMLSlider(min=10, max=50, value=30)
        assert slider.min == 10
        assert slider.max == 50
        assert slider.value == 30
        html = slider.render()
        assert 'min="10"' in html
        assert 'max="50"' in html
        assert 'value="30"' in html

    def test_slider_step(self) -> None:
        """Test slider with custom step."""
        from animaid import HTMLSlider

        slider = HTMLSlider(min=0, max=1, step=0.1)
        assert slider.step == 0.1
        html = slider.render()
        assert 'step="0.1"' in html

    def test_slider_value_property(self) -> None:
        """Test value property."""
        from animaid import HTMLSlider

        slider = HTMLSlider(value=50)
        assert slider.value == 50
        slider.value = 75
        assert slider.value == 75

    def test_slider_on_change(self) -> None:
        """Test on_change callback."""
        from animaid import HTMLSlider

        received: list[float] = []

        def callback(value: float) -> None:
            received.append(value)

        slider = HTMLSlider().on_change(callback)
        slider._on_change(42.5)
        assert received == [42.5]

    def test_slider_wide(self) -> None:
        """Test wide preset."""
        from animaid import HTMLSlider

        slider = HTMLSlider().wide()
        html = slider.render()
        assert "width: 100%" in html

    def test_slider_thin(self) -> None:
        """Test thin preset."""
        from animaid import HTMLSlider

        slider = HTMLSlider().thin()
        html = slider.render()
        assert "height: 4px" in html

    def test_slider_thick(self) -> None:
        """Test thick preset."""
        from animaid import HTMLSlider

        slider = HTMLSlider().thick()
        html = slider.render()
        assert "height: 10px" in html


class TestHTMLSelect:
    """Tests for HTMLSelect widget."""

    def test_basic_select(self) -> None:
        """Test creating a basic select."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["A", "B", "C"])
        assert select.options == ["A", "B", "C"]
        assert select.value == "A"  # First option by default
        html = select.render()
        assert "anim-select" in html
        assert "<option" in html

    def test_select_with_value(self) -> None:
        """Test select with initial value."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["Red", "Green", "Blue"], value="Green")
        assert select.value == "Green"
        html = select.render()
        assert 'value="Green" selected' in html

    def test_select_value_property(self) -> None:
        """Test value property."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["X", "Y", "Z"])
        assert select.value == "X"
        select.value = "Y"
        assert select.value == "Y"

    def test_select_on_change(self) -> None:
        """Test on_change callback."""
        from animaid import HTMLSelect

        received: list[str] = []

        def callback(value: str) -> None:
            received.append(value)

        select = HTMLSelect(options=["A", "B"]).on_change(callback)
        select._on_change("B")
        assert received == ["B"]

    def test_select_wide(self) -> None:
        """Test wide preset."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["A"]).wide()
        html = select.render()
        assert "width: 100%" in html

    def test_select_large(self) -> None:
        """Test large preset."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["A"]).large()
        html = select.render()
        assert "18px" in html

    def test_select_html_escaping(self) -> None:
        """Test HTML escaping in options."""
        from animaid import HTMLSelect

        select = HTMLSelect(options=["<script>", "Normal"])
        html = select.render()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html


class TestAppEventHandling:
    """Tests for App event handling."""

    def test_event_queue_exists(self) -> None:
        """Test that App has event queue."""
        from animaid import App

        app = App(auto_open=False)
        assert hasattr(app, "_event_queue")

    def test_wait_for_event_timeout(self) -> None:
        """Test wait_for_event with timeout."""
        from animaid import App

        app = App(auto_open=False)
        event = app.wait_for_event(timeout=0.01)
        assert event is None

    def test_get_events_empty(self) -> None:
        """Test get_events when queue is empty."""
        from animaid import App

        app = App(auto_open=False)
        events = app.get_events()
        assert events == []

    def test_handle_input_event_click(self) -> None:
        """Test handling a click event."""
        from animaid import App, HTMLButton

        app = App(auto_open=False)
        button = HTMLButton("Test")
        app.add(button, id="btn_1")

        clicked = False

        def on_click() -> None:
            nonlocal clicked
            clicked = True

        button._on_click = on_click

        # Simulate event from browser
        app.handle_input_event({"id": "btn_1", "event": "click"})

        assert clicked
        events = app.get_events()
        assert len(events) == 1
        assert events[0].id == "btn_1"
        assert events[0].event_type == "click"

    def test_handle_input_event_change(self) -> None:
        """Test handling a change event."""
        from animaid import App, HTMLTextInput

        app = App(auto_open=False)
        text = HTMLTextInput(value="initial")
        app.add(text, id="text_1")

        received = []

        def on_change(value: str) -> None:
            received.append(value)

        text._on_change = on_change

        # Simulate event from browser
        app.handle_input_event({"id": "text_1", "event": "change", "value": "new"})

        assert text.value == "new"
        assert received == ["new"]
        events = app.get_events()
        assert len(events) == 1
        assert events[0].value == "new"

    def test_handle_input_event_submit(self) -> None:
        """Test handling a submit event."""
        from animaid import App, HTMLTextInput

        app = App(auto_open=False)
        text = HTMLTextInput(value="test")
        app.add(text, id="text_1")

        submitted = []

        def on_submit(value: str) -> None:
            submitted.append(value)

        text._on_submit = on_submit

        # Simulate event from browser
        app.handle_input_event({"id": "text_1", "event": "submit", "value": "test"})

        assert submitted == ["test"]


class TestShortAliases:
    """Tests for short alias imports."""

    def test_button_alias(self) -> None:
        """Test Button alias."""
        from animaid import Button, HTMLButton

        assert Button is HTMLButton

    def test_text_input_alias(self) -> None:
        """Test TextInput alias."""
        from animaid import HTMLTextInput, TextInput

        assert TextInput is HTMLTextInput

    def test_checkbox_alias(self) -> None:
        """Test Checkbox alias."""
        from animaid import Checkbox, HTMLCheckbox

        assert Checkbox is HTMLCheckbox

    def test_slider_alias(self) -> None:
        """Test Slider alias."""
        from animaid import HTMLSlider, Slider

        assert Slider is HTMLSlider

    def test_select_alias(self) -> None:
        """Test Select alias."""
        from animaid import HTMLSelect, Select

        assert Select is HTMLSelect
