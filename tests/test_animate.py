"""Tests for Animate class."""

import time
import urllib.request
import urllib.error

import pytest

from animaid import Animate, HTMLString


class TestAnimateBasics:
    """Test basic Animate functionality."""

    def test_initialization(self) -> None:
        """Animate should initialize with default values."""
        anim = Animate()
        assert anim.port == 8200
        assert anim.title == "AnimAID"
        assert anim.is_running is False

    def test_initialization_custom_values(self) -> None:
        """Animate should accept custom port and title."""
        anim = Animate(port=8250, title="Custom Title")
        assert anim.port == 8250
        assert anim.title == "Custom Title"

    def test_url_property(self) -> None:
        """URL property should return correct server URL."""
        anim = Animate(port=8300)
        assert anim.url == "http://127.0.0.1:8300"


class TestAnimateItemManagement:
    """Test item add/update/remove/clear methods."""

    def test_add_item(self) -> None:
        """Add should return ID and store item."""
        anim = Animate()
        item_id = anim.add(HTMLString("Hello"))
        assert item_id == "item_0"
        assert anim.get(item_id) is not None

    def test_add_item_with_custom_id(self) -> None:
        """Add should accept custom ID."""
        anim = Animate()
        item_id = anim.add(HTMLString("Hello"), id="custom_id")
        assert item_id == "custom_id"
        assert anim.get("custom_id") is not None

    def test_add_multiple_items(self) -> None:
        """Add should generate sequential IDs."""
        anim = Animate()
        id1 = anim.add(HTMLString("First"))
        id2 = anim.add(HTMLString("Second"))
        id3 = anim.add(HTMLString("Third"))
        assert id1 == "item_0"
        assert id2 == "item_1"
        assert id3 == "item_2"

    def test_add_string_item(self) -> None:
        """Add should accept plain strings."""
        anim = Animate()
        item_id = anim.add("Plain text")
        assert anim.get(item_id) == "Plain text"

    def test_update_item(self) -> None:
        """Update should change item content."""
        anim = Animate()
        item_id = anim.add(HTMLString("Original"))
        result = anim.update(item_id, HTMLString("Updated"))
        assert result is True
        item = anim.get(item_id)
        assert item is not None
        assert str(item) == "Updated"

    def test_update_nonexistent_item(self) -> None:
        """Update should return False for nonexistent ID."""
        anim = Animate()
        result = anim.update("nonexistent", HTMLString("Updated"))
        assert result is False

    def test_remove_item(self) -> None:
        """Remove should delete item."""
        anim = Animate()
        item_id = anim.add(HTMLString("To remove"))
        assert anim.get(item_id) is not None
        result = anim.remove(item_id)
        assert result is True
        assert anim.get(item_id) is None

    def test_remove_nonexistent_item(self) -> None:
        """Remove should return False for nonexistent ID."""
        anim = Animate()
        result = anim.remove("nonexistent")
        assert result is False

    def test_clear_items(self) -> None:
        """Clear should remove all items."""
        anim = Animate()
        anim.add(HTMLString("First"))
        anim.add(HTMLString("Second"))
        anim.add(HTMLString("Third"))
        assert len(anim.items()) == 3
        anim.clear()
        assert len(anim.items()) == 0

    def test_get_item(self) -> None:
        """Get should return item by ID."""
        anim = Animate()
        item = HTMLString("Hello")
        item_id = anim.add(item)
        retrieved = anim.get(item_id)
        assert retrieved is item

    def test_get_nonexistent_item(self) -> None:
        """Get should return None for nonexistent ID."""
        anim = Animate()
        assert anim.get("nonexistent") is None

    def test_items_returns_copy(self) -> None:
        """Items should return a copy of the items list."""
        anim = Animate()
        anim.add(HTMLString("First"))
        anim.add(HTMLString("Second"))
        items = anim.items()
        assert len(items) == 2
        items.clear()  # Modify the returned list
        assert len(anim.items()) == 2  # Original should be unchanged


class TestAnimateFullState:
    """Test full state rendering."""

    def test_get_full_state_empty(self) -> None:
        """Get full state should return empty list when no items."""
        anim = Animate()
        state = anim.get_full_state()
        assert state == []

    def test_get_full_state_with_items(self) -> None:
        """Get full state should return rendered items."""
        anim = Animate()
        anim.add(HTMLString("Hello").bold)
        anim.add(HTMLString("World").italic)
        state = anim.get_full_state()
        assert len(state) == 2
        assert state[0]["id"] == "item_0"
        assert "font-weight: bold" in state[0]["html"]
        assert state[1]["id"] == "item_1"
        assert "font-style: italic" in state[1]["html"]

    def test_get_full_state_plain_string(self) -> None:
        """Get full state should render plain strings."""
        anim = Animate()
        anim.add("Plain text")
        state = anim.get_full_state()
        assert len(state) == 1
        assert state[0]["html"] == "Plain text"


class TestAnimateContextManager:
    """Test context manager functionality."""

    def test_context_manager_enters(self) -> None:
        """Context manager should return Animate instance."""
        with Animate(port=8251, auto_open=False) as anim:
            assert isinstance(anim, Animate)
            assert anim.is_running is True

    def test_context_manager_stops_on_exit(self) -> None:
        """Context manager should stop server on exit."""
        anim_ref = None
        with Animate(port=8252, auto_open=False) as anim:
            anim_ref = anim
            assert anim.is_running is True
        # Give it a moment to stop
        time.sleep(0.5)
        assert anim_ref is not None
        assert anim_ref.is_running is False


class TestAnimateServer:
    """Test server functionality (integration tests)."""

    def test_server_starts_and_stops(self) -> None:
        """Server should start and stop correctly."""
        anim = Animate(port=8253, auto_open=False)
        assert anim.is_running is False

        anim.run()
        assert anim.is_running is True

        # Wait for server to be ready
        time.sleep(0.5)

        # Verify server responds
        with urllib.request.urlopen(anim.url, timeout=5) as response:
            assert response.status == 200
            content = response.read().decode("utf-8")
            assert "AnimAID" in content

        anim.stop()
        # Give it a moment to shut down
        time.sleep(0.5)
        assert anim.is_running is False

    def test_run_returns_self(self) -> None:
        """Run should return self for method chaining."""
        anim = Animate(port=8254, auto_open=False)
        result = anim.run()
        assert result is anim
        anim.stop()

    def test_double_run_is_safe(self) -> None:
        """Calling run twice should be safe."""
        anim = Animate(port=8255, auto_open=False)
        anim.run()
        result = anim.run()  # Second call should not fail
        assert result is anim
        anim.stop()

    def test_stop_when_not_running_is_safe(self) -> None:
        """Calling stop when not running should be safe."""
        anim = Animate()
        anim.stop()  # Should not raise
        anim.stop()  # Should not raise

    def test_server_serves_html_page(self) -> None:
        """Server should serve HTML page with title."""
        anim = Animate(port=8256, title="Test Title", auto_open=False)
        anim.run()
        time.sleep(0.5)

        with urllib.request.urlopen(anim.url, timeout=5) as response:
            assert response.status == 200
            content = response.read().decode("utf-8")
            assert "Test Title" in content
            assert "WebSocket" in content

        anim.stop()
