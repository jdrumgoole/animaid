"""Animate - Tkinter-like interactive GUI environment using HTML."""

from __future__ import annotations

import asyncio
import threading
import time
import uuid
import webbrowser
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from animaid.html_object import HTMLObject


class Animate:
    """A Tkinter-like interactive GUI environment using HTML.

    The browser becomes the display surface, and AnimAID objects become
    widgets that can be added, updated, and removed programmatically
    with real-time visual feedback.

    Examples:
        >>> from animaid import Animate, HTMLString
        >>> anim = Animate()
        >>> anim.run()  # Starts server, opens browser
        >>> anim.add(HTMLString("Hello").bold)
        'item_0'
        >>> anim.add(HTMLString("World").italic)
        'item_1'
        >>> anim.stop()

        # Context manager support
        >>> with Animate() as anim:
        ...     anim.add(HTMLString("Temporary display"))
        # Server stops when context exits
    """

    def __init__(
        self,
        port: int = 8200,
        title: str = "AnimAID",
        auto_open: bool = True,
    ) -> None:
        """Initialize the Animate environment.

        Args:
            port: Port number for the server (default: 8200).
            title: Title displayed in the browser window.
            auto_open: Whether to automatically open browser on run().
        """
        self._port = port
        self._title = title
        self._auto_open = auto_open
        self._items: list[tuple[str, Any]] = []  # (id, item) pairs
        self._connections: set[Any] = set()  # WebSocket connections
        self._server_thread: threading.Thread | None = None
        self._server: Any = None
        self._lock = threading.Lock()
        self._next_id = 0
        self._running = False
        self._shutdown_event: asyncio.Event | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    def run(self) -> "Animate":
        """Start the server in a background thread and open the browser.

        Returns:
            Self for method chaining.
        """
        if self._running:
            return self

        from animaid.animate_server import create_animate_app

        app = create_animate_app(self)

        def server_thread() -> None:
            import uvicorn

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            self._shutdown_event = asyncio.Event()

            config = uvicorn.Config(
                app,
                host="127.0.0.1",
                port=self._port,
                log_level="warning",
            )
            server = uvicorn.Server(config)
            self._server = server

            loop.run_until_complete(server.serve())

        self._server_thread = threading.Thread(target=server_thread, daemon=True)
        self._server_thread.start()
        self._running = True

        # Wait for server to be ready
        time.sleep(0.5)

        # Open browser if requested
        if self._auto_open:
            webbrowser.open(self.url)

        return self

    def stop(self) -> None:
        """Stop the server."""
        if not self._running:
            return

        self._running = False

        if self._server is not None:
            self._server.should_exit = True

        # Give the server a moment to shut down
        if self._server_thread is not None:
            self._server_thread.join(timeout=2.0)

        self._server = None
        self._server_thread = None

    def add(self, item: "HTMLObject | str", id: str | None = None) -> str:
        """Add an item to the display.

        Args:
            item: An HTMLObject or string to display.
            id: Optional custom ID for the item. Auto-generated if not provided.

        Returns:
            The ID of the added item.
        """
        if id is None:
            id = self._generate_id()

        with self._lock:
            self._items.append((id, item))

        self._broadcast_add(id, item)
        return id

    def update(self, id: str, item: "HTMLObject | str") -> bool:
        """Update an existing item by ID.

        Args:
            id: The ID of the item to update.
            item: The new content to display.

        Returns:
            True if the item was found and updated, False otherwise.
        """
        with self._lock:
            for i, (item_id, _) in enumerate(self._items):
                if item_id == id:
                    self._items[i] = (id, item)
                    self._broadcast_update(id, item)
                    return True
        return False

    def remove(self, id: str) -> bool:
        """Remove an item by ID.

        Args:
            id: The ID of the item to remove.

        Returns:
            True if the item was found and removed, False otherwise.
        """
        with self._lock:
            for i, (item_id, _) in enumerate(self._items):
                if item_id == id:
                    self._items.pop(i)
                    self._broadcast_remove(id)
                    return True
        return False

    def clear(self) -> None:
        """Remove all items from the display."""
        with self._lock:
            self._items.clear()

        self._broadcast_clear()

    def get(self, id: str) -> "HTMLObject | str | None":
        """Get an item by ID.

        Args:
            id: The ID of the item to retrieve.

        Returns:
            The item if found, None otherwise.
        """
        with self._lock:
            for item_id, item in self._items:
                if item_id == id:
                    return item
        return None

    def items(self) -> list[tuple[str, Any]]:
        """Get a copy of all items.

        Returns:
            A list of (id, item) tuples.
        """
        with self._lock:
            return list(self._items)

    @property
    def url(self) -> str:
        """Get the server URL."""
        return f"http://127.0.0.1:{self._port}"

    @property
    def is_running(self) -> bool:
        """Check if the server is running."""
        return self._running

    @property
    def title(self) -> str:
        """Get the display title."""
        return self._title

    @property
    def port(self) -> int:
        """Get the server port."""
        return self._port

    def _generate_id(self) -> str:
        """Generate a unique ID for an item."""
        with self._lock:
            id = f"item_{self._next_id}"
            self._next_id += 1
            return id

    def _render_item(self, item: "HTMLObject | str") -> str:
        """Render an item to HTML string."""
        if hasattr(item, "render"):
            return item.render()
        return str(item)

    def _broadcast_add(self, id: str, item: "HTMLObject | str") -> None:
        """Broadcast an add message to all connected clients."""
        html = self._render_item(item)
        self._broadcast({"type": "add", "id": id, "html": html})

    def _broadcast_update(self, id: str, item: "HTMLObject | str") -> None:
        """Broadcast an update message to all connected clients."""
        html = self._render_item(item)
        self._broadcast({"type": "update", "id": id, "html": html})

    def _broadcast_remove(self, id: str) -> None:
        """Broadcast a remove message to all connected clients."""
        self._broadcast({"type": "remove", "id": id})

    def _broadcast_clear(self) -> None:
        """Broadcast a clear message to all connected clients."""
        self._broadcast({"type": "clear"})

    def _broadcast(self, message: dict[str, Any]) -> None:
        """Broadcast a message to all connected WebSocket clients."""
        import json

        if not self._connections:
            return

        data = json.dumps(message)
        dead_connections = set()

        for ws in list(self._connections):
            try:
                if self._loop is not None:
                    asyncio.run_coroutine_threadsafe(
                        ws.send_text(data), self._loop
                    )
            except Exception:
                dead_connections.add(ws)

        # Clean up dead connections
        self._connections -= dead_connections

    def get_full_state(self) -> list[dict[str, str]]:
        """Get the full state as a list of rendered items.

        Returns:
            A list of {"id": ..., "html": ...} dicts.
        """
        with self._lock:
            return [
                {"id": id, "html": self._render_item(item)}
                for id, item in self._items
            ]

    def __enter__(self) -> "Animate":
        """Enter context manager - start the server."""
        return self.run()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit context manager - stop the server."""
        self.stop()
