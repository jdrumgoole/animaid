"""Tests for Window and WindowConfig classes."""

import pytest

from animaid import App, Window, WindowConfig


class TestWindowConfig:
    """Test WindowConfig initialization and presets."""

    def test_default_values(self) -> None:
        """WindowConfig should have sensible defaults."""
        config = WindowConfig()
        assert config.title == "AnimAID"
        assert config.width is None
        assert config.height is None
        assert config.theme == "light"
        assert config.background_color == "#fafafa"
        assert config.favicon is None

    def test_custom_values(self) -> None:
        """WindowConfig should accept custom values."""
        config = WindowConfig(
            title="Custom",
            width=800,
            height=600,
            theme="dark",
            background_color="#1a1a2e",
            favicon="/icon.png",
        )
        assert config.title == "Custom"
        assert config.width == 800
        assert config.height == 600
        assert config.theme == "dark"
        assert config.background_color == "#1a1a2e"
        assert config.favicon == "/icon.png"

    def test_compact_preset(self) -> None:
        """Compact preset should create 600x400 window."""
        config = WindowConfig.compact()
        assert config.width == 600
        assert config.height == 400
        assert config.title == "AnimAID"

    def test_compact_preset_custom_title(self) -> None:
        """Compact preset should accept custom title."""
        config = WindowConfig.compact(title="My Tool")
        assert config.width == 600
        assert config.height == 400
        assert config.title == "My Tool"

    def test_standard_preset(self) -> None:
        """Standard preset should create 1024x768 window."""
        config = WindowConfig.standard()
        assert config.width == 1024
        assert config.height == 768
        assert config.title == "AnimAID"

    def test_wide_preset(self) -> None:
        """Wide preset should create 1280x720 window."""
        config = WindowConfig.wide()
        assert config.width == 1280
        assert config.height == 720
        assert config.title == "AnimAID"

    def test_dark_preset(self) -> None:
        """Dark preset should set dark theme."""
        config = WindowConfig.dark()
        assert config.theme == "dark"
        assert config.background_color == "#1a1a2e"


class TestWindow:
    """Test Window runtime control."""

    def test_window_initial_values(self) -> None:
        """Window should reflect initial config values."""
        app = App(title="Test", theme="dark")
        assert app.window.title == "Test"
        assert app.window.theme == "dark"

    def test_window_with_config(self) -> None:
        """Window should accept WindowConfig."""
        config = WindowConfig.compact(title="Compact App")
        app = App(window=config)
        assert app.window.title == "Compact App"
        assert app.window.width == 600
        assert app.window.height == 400

    def test_set_title(self) -> None:
        """set_title should update title and return self."""
        app = App(title="Original")
        result = app.window.set_title("Updated")
        assert app.window.title == "Updated"
        assert result is app.window  # Returns self for chaining

    def test_set_theme_valid(self) -> None:
        """set_theme should update theme for valid values."""
        app = App()
        app.window.set_theme("dark")
        assert app.window.theme == "dark"
        app.window.set_theme("light")
        assert app.window.theme == "light"
        app.window.set_theme("auto")
        assert app.window.theme == "auto"

    def test_set_theme_invalid(self) -> None:
        """set_theme should raise ValueError for invalid theme."""
        app = App()
        with pytest.raises(ValueError, match="Invalid theme"):
            app.window.set_theme("invalid")

    def test_dark_preset_method(self) -> None:
        """dark() should set theme to dark."""
        app = App()
        result = app.window.dark()
        assert app.window.theme == "dark"
        assert result is app.window

    def test_light_preset_method(self) -> None:
        """light() should set theme to light."""
        app = App(theme="dark")
        result = app.window.light()
        assert app.window.theme == "light"
        assert result is app.window

    def test_resize(self) -> None:
        """resize should update width and height."""
        app = App()
        result = app.window.resize(1280, 720)
        assert app.window.width == 1280
        assert app.window.height == 720
        assert result is app.window

    def test_set_background(self) -> None:
        """set_background should update background color."""
        app = App()
        result = app.window.set_background("#000000")
        assert app.window.background_color == "#000000"
        assert result is app.window

    def test_set_favicon(self) -> None:
        """set_favicon should store favicon URL."""
        app = App()
        app.window.set_favicon("/static/icon.png")
        config = app.window.get_config()
        assert config["favicon"] == "/static/icon.png"

    def test_get_config(self) -> None:
        """get_config should return current window state."""
        app = App(title="Test", theme="dark")
        app.window.resize(800, 600)
        config = app.window.get_config()
        assert config["title"] == "Test"
        assert config["theme"] == "dark"
        assert config["width"] == 800
        assert config["height"] == 600

    def test_on_resize_callback(self) -> None:
        """on_resize should register callback."""
        app = App()
        called_with: list[tuple[int, int]] = []

        def callback(w: int, h: int) -> None:
            called_with.append((w, h))

        app.window.on_resize(callback)

        # Simulate resize event
        app.window.handle_window_event("resize", {"width": 1024, "height": 768})
        assert called_with == [(1024, 768)]
        assert app.window.width == 1024
        assert app.window.height == 768

    def test_on_close_callback(self) -> None:
        """on_close should register callback."""
        app = App()
        close_called = []

        def callback() -> None:
            close_called.append(True)

        app.window.on_close(callback)

        # Simulate close event
        app.window.handle_window_event("close", {})
        assert close_called == [True]

    def test_method_chaining(self) -> None:
        """Window methods should support chaining."""
        app = App()
        app.window.set_title("Chained").dark().resize(800, 600)
        assert app.window.title == "Chained"
        assert app.window.theme == "dark"
        assert app.window.width == 800


class TestAppClass:
    """Test App class (renamed from Animate)."""

    def test_app_initialization(self) -> None:
        """App should initialize with default values."""
        app = App()
        assert app.port == 8200
        assert app.title == "AnimAID"
        assert app.is_running is False
        assert app.window is not None

    def test_app_custom_values(self) -> None:
        """App should accept custom port and title."""
        app = App(port=8250, title="Custom Title")
        assert app.port == 8250
        assert app.title == "Custom Title"

    def test_app_with_theme(self) -> None:
        """App should accept theme parameter."""
        app = App(theme="dark")
        assert app.window.theme == "dark"

    def test_app_with_size(self) -> None:
        """App should accept width and height parameters."""
        app = App(width=800, height=600)
        assert app.window.width == 800
        assert app.window.height == 600

    def test_app_with_window_config(self) -> None:
        """App should accept WindowConfig."""
        config = WindowConfig.dark(title="Dark App")
        app = App(window=config)
        assert app.title == "Dark App"
        assert app.window.theme == "dark"

    def test_app_url_property(self) -> None:
        """URL property should return correct server URL."""
        app = App(port=8300)
        assert app.url == "http://127.0.0.1:8300"


