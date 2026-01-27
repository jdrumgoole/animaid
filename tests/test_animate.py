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
        assert item_id == "string_1"
        assert anim.get(item_id) is not None

    def test_add_item_with_custom_id(self) -> None:
        """Add should accept custom ID."""
        anim = Animate()
        item_id = anim.add(HTMLString("Hello"), id="custom_id")
        assert item_id == "custom_id"
        assert anim.get("custom_id") is not None

    def test_add_multiple_items(self) -> None:
        """Add should generate sequential IDs per type."""
        anim = Animate()
        id1 = anim.add(HTMLString("First"))
        id2 = anim.add(HTMLString("Second"))
        id3 = anim.add(HTMLString("Third"))
        assert id1 == "string_1"
        assert id2 == "string_2"
        assert id3 == "string_3"

    def test_add_mixed_types(self) -> None:
        """Add should generate type-specific IDs."""
        from animaid import HTMLList, HTMLDict, HTMLInt

        anim = Animate()
        str_id = anim.add(HTMLString("Hello"))
        list_id = anim.add(HTMLList([1, 2, 3]))
        dict_id = anim.add(HTMLDict({"a": 1}))
        int_id = anim.add(HTMLInt(42))
        str_id2 = anim.add(HTMLString("World"))

        assert str_id == "string_1"
        assert list_id == "list_1"
        assert dict_id == "dict_1"
        assert int_id == "int_1"
        assert str_id2 == "string_2"

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

    def test_clear_all_items(self) -> None:
        """clear_all should remove all items."""
        anim = Animate()
        anim.add(HTMLString("First"))
        anim.add(HTMLString("Second"))
        anim.add(HTMLString("Third"))
        assert len(anim.items()) == 3
        anim.clear_all()
        assert len(anim.items()) == 0

    def test_clear_single_item(self) -> None:
        """clear(id) should remove a single item by ID."""
        anim = Animate()
        id1 = anim.add(HTMLString("First"))
        id2 = anim.add(HTMLString("Second"))
        assert len(anim.items()) == 2
        result = anim.clear(id1)
        assert result is True
        assert len(anim.items()) == 1
        assert anim.get(id1) is None
        assert anim.get(id2) is not None

    def test_clear_nonexistent_item(self) -> None:
        """clear(id) should return False for nonexistent ID."""
        anim = Animate()
        result = anim.clear("nonexistent")
        assert result is False

    def test_add_stores_anim_id_on_object(self) -> None:
        """add() should store the animate ID on the object."""
        anim = Animate()
        item = HTMLString("Hello")
        item_id = anim.add(item)
        assert hasattr(item, '_anim_id')
        assert item._anim_id == item_id

    def test_remove_by_object(self) -> None:
        """remove() should accept an object and remove it."""
        anim = Animate()
        item1 = HTMLString("First")
        item2 = HTMLString("Second")
        anim.add(item1)
        anim.add(item2)
        assert len(anim.items()) == 2
        result = anim.remove(item1)
        assert result is True
        assert len(anim.items()) == 1
        assert item1._anim_id is None  # Should be cleared

    def test_clear_by_object(self) -> None:
        """clear() should accept an object and remove it."""
        anim = Animate()
        item = HTMLString("Hello")
        anim.add(item)
        result = anim.clear(item)
        assert result is True
        assert len(anim.items()) == 0

    def test_remove_object_not_added(self) -> None:
        """remove() should return False for object not added."""
        anim = Animate()
        item = HTMLString("Not added")
        result = anim.remove(item)
        assert result is False

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
        assert state[0]["id"] == "string_1"
        assert "font-weight: bold" in state[0]["html"]
        assert state[1]["id"] == "string_2"
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
