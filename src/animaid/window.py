"""Window configuration and runtime control for AnimAID applications."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from animaid.animate import App


@dataclass
class WindowConfig:
    """Configuration for window initialization.

    Use this to configure the initial state of the browser window
    when creating an App.

    Examples:
        >>> from animaid import App, WindowConfig
        >>> # Use a preset for quick setup
        >>> config = WindowConfig.compact(title="My Tool")
        >>> with App(window=config) as app:
        ...     app.add(HTMLString("Hello"))

        >>> # Or configure manually
        >>> config = WindowConfig(
        ...     title="Dashboard",
        ...     width=1280,
        ...     height=720,
        ...     theme="dark"
        ... )
    """

    title: str = "AnimAID"
    width: int | None = None  # None = browser default
    height: int | None = None  # None = browser default
    theme: str = "light"  # "light", "dark", "auto"
    background_color: str = "#fafafa"
    favicon: str | None = None

    @classmethod
    def compact(cls, title: str = "AnimAID") -> WindowConfig:
        """Create a compact window configuration (600x400).

        Args:
            title: The window title.

        Returns:
            A WindowConfig for a small, compact window.
        """
        return cls(title=title, width=600, height=400)

    @classmethod
    def standard(cls, title: str = "AnimAID") -> WindowConfig:
        """Create a standard window configuration (1024x768).

        Args:
            title: The window title.

        Returns:
            A WindowConfig for a standard-sized window.
        """
        return cls(title=title, width=1024, height=768)

    @classmethod
    def wide(cls, title: str = "AnimAID") -> WindowConfig:
        """Create a wide window configuration (1280x720).

        Args:
            title: The window title.

        Returns:
            A WindowConfig for a wide (16:9) window.
        """
        return cls(title=title, width=1280, height=720)

    @classmethod
    def dark(cls, title: str = "AnimAID") -> WindowConfig:
        """Create a dark-themed window configuration.

        Args:
            title: The window title.

        Returns:
            A WindowConfig with dark theme.
        """
        return cls(title=title, theme="dark", background_color="#1a1a2e")


class Window:
    """Runtime window control for AnimAID applications.

    Access this via the `app.window` property. Provides methods to
    dynamically control the browser window appearance and behavior.

    Examples:
        >>> with App() as app:
        ...     app.window.dark()           # Switch to dark theme
        ...     app.window.set_title("Processing...")
        ...     app.window.resize(1280, 720)
    """

    def __init__(self, app: App, config: WindowConfig) -> None:
        """Initialize the Window with configuration.

        Args:
            app: The parent App instance.
            config: Initial window configuration.
        """
        self._app = app
        self._title = config.title
        self._width = config.width
        self._height = config.height
        self._theme = config.theme
        self._background_color = config.background_color
        self._favicon = config.favicon
        self._on_resize_callback: Callable[[int, int], None] | None = None
        self._on_close_callback: Callable[[], None] | None = None

    # Read-only properties
    @property
    def title(self) -> str:
        """Get the current window title."""
        return self._title

    @property
    def width(self) -> int | None:
        """Get the current window width (None if browser default)."""
        return self._width

    @property
    def height(self) -> int | None:
        """Get the current window height (None if browser default)."""
        return self._height

    @property
    def theme(self) -> str:
        """Get the current theme ('light', 'dark', or 'auto')."""
        return self._theme

    @property
    def background_color(self) -> str:
        """Get the current background color."""
        return self._background_color

    # Mutators (broadcast to browser)
    def set_title(self, title: str) -> Window:
        """Set the window title.

        Updates the browser tab title in real-time.

        Args:
            title: The new window title.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.set_title("Processing... 50%")
        """
        self._title = title
        self._broadcast_window_change("title", title)
        return self

    def resize(self, width: int, height: int) -> Window:
        """Resize the browser window.

        Note: Some browsers may restrict window resizing for security.

        Args:
            width: The new width in pixels.
            height: The new height in pixels.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.resize(1280, 720)
        """
        self._width = width
        self._height = height
        self._broadcast_window_change("resize", {"width": width, "height": height})
        return self

    def set_theme(self, theme: str) -> Window:
        """Set the color theme.

        Args:
            theme: The theme to use ('light', 'dark', or 'auto').

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.set_theme("dark")
        """
        if theme not in ("light", "dark", "auto"):
            raise ValueError(f"Invalid theme: {theme}. Must be 'light', 'dark', or 'auto'.")
        self._theme = theme
        self._broadcast_window_change("theme", theme)
        return self

    def set_background(self, color: str) -> Window:
        """Set the page background color.

        Args:
            color: CSS color value (e.g., '#ffffff', 'rgb(0,0,0)', 'white').

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.set_background("#1a1a2e")
        """
        self._background_color = color
        self._broadcast_window_change("background", color)
        return self

    def set_favicon(self, url: str) -> Window:
        """Set the page favicon.

        Args:
            url: URL to the favicon image.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.set_favicon("/static/icon.png")
        """
        self._favicon = url
        self._broadcast_window_change("favicon", url)
        return self

    # Preset methods
    def dark(self) -> Window:
        """Switch to dark theme.

        Convenience method equivalent to `set_theme("dark")`.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.dark()
        """
        return self.set_theme("dark")

    def light(self) -> Window:
        """Switch to light theme.

        Convenience method equivalent to `set_theme("light")`.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.light()
        """
        return self.set_theme("light")

    def fullscreen(self) -> Window:
        """Request fullscreen mode.

        Note: Browsers may require user interaction before allowing fullscreen.

        Returns:
            Self for method chaining.

        Examples:
            >>> app.window.fullscreen()
        """
        self._broadcast_window_change("fullscreen", True)
        return self

    # Event callbacks
    def on_resize(self, callback: Callable[[int, int], None]) -> Window:
        """Register a callback for window resize events.

        Args:
            callback: Function that receives (width, height) when window resizes.

        Returns:
            Self for method chaining.

        Examples:
            >>> def handle_resize(width, height):
            ...     print(f"Window resized to {width}x{height}")
            >>> app.window.on_resize(handle_resize)
        """
        self._on_resize_callback = callback
        return self

    def on_close(self, callback: Callable[[], None]) -> Window:
        """Register a callback for window close events.

        Args:
            callback: Function called when the window is about to close.

        Returns:
            Self for method chaining.

        Examples:
            >>> def handle_close():
            ...     print("Window closing!")
            >>> app.window.on_close(handle_close)
        """
        self._on_close_callback = callback
        return self

    def handle_window_event(self, event: str, data: dict[str, Any]) -> None:
        """Handle a window event from the browser.

        This is called internally by the server.

        Args:
            event: The event type ('resize', 'close').
            data: Event-specific data.
        """
        if event == "resize":
            width = data.get("width", 0)
            height = data.get("height", 0)
            self._width = width
            self._height = height
            if self._on_resize_callback:
                self._on_resize_callback(width, height)
        elif event == "close":
            if self._on_close_callback:
                self._on_close_callback()

    def _broadcast_window_change(self, property_name: str, value: Any) -> None:
        """Broadcast a window property change to all connected clients.

        Args:
            property_name: The property that changed.
            value: The new value.
        """
        self._app._broadcast({"type": "window", "property": property_name, "value": value})

    def get_config(self) -> dict[str, Any]:
        """Get the current window configuration as a dictionary.

        Used by the server to send initial configuration to clients.

        Returns:
            Dictionary with current window settings.
        """
        return {
            "title": self._title,
            "width": self._width,
            "height": self._height,
            "theme": self._theme,
            "background_color": self._background_color,
            "favicon": self._favicon,
        }
