"""Tests for observable HTML objects with pypubsub."""

import time

import pytest
from pubsub import pub

from animaid import HTMLList, HTMLDict, HTMLSet


class TestHTMLListObservable:
    """Test HTMLList publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLList should have a unique _obs_id."""
        html_list = HTMLList([1, 2, 3])
        assert hasattr(html_list, '_obs_id')
        assert html_list._obs_id is not None

    def test_append_publishes(self) -> None:
        """Append should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.append(4)
            assert len(received) == 1
            assert received[0] == html_list._obs_id
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_extend_publishes(self) -> None:
        """Extend should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.extend([4, 5])
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_setitem_publishes(self) -> None:
        """Setting item should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_list = HTMLList([1, 2, 3])
            html_list[0] = 100
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_pop_publishes(self) -> None:
        """Pop should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.pop()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_styled_copy_preserves_obs_id(self) -> None:
        """Styled copies should preserve _obs_id for reactive updates."""
        html_list = HTMLList([1, 2, 3])
        styled = html_list.pills
        assert styled._obs_id == html_list._obs_id


class TestHTMLDictObservable:
    """Test HTMLDict publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLDict should have a unique _obs_id."""
        html_dict = HTMLDict({"a": 1})
        assert hasattr(html_dict, '_obs_id')
        assert html_dict._obs_id is not None

    def test_setitem_publishes(self) -> None:
        """Setting item should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict["b"] = 2
            assert len(received) == 1
            assert received[0] == html_dict._obs_id
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_update_publishes(self) -> None:
        """Update should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict.update({"b": 2, "c": 3})
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_pop_publishes(self) -> None:
        """Pop should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_dict = HTMLDict({"a": 1, "b": 2})
            html_dict.pop("a")
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_styled_copy_preserves_obs_id(self) -> None:
        """Styled copies should preserve _obs_id for reactive updates."""
        html_dict = HTMLDict({"a": 1})
        styled = html_dict.card
        assert styled._obs_id == html_dict._obs_id


class TestHTMLSetObservable:
    """Test HTMLSet publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLSet should have a unique _obs_id."""
        html_set = HTMLSet({1, 2, 3})
        assert hasattr(html_set, '_obs_id')
        assert html_set._obs_id is not None

    def test_add_publishes(self) -> None:
        """Add should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.add(4)
            assert len(received) == 1
            assert received[0] == html_set._obs_id
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_discard_publishes(self) -> None:
        """Discard should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.discard(1)
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_update_publishes(self) -> None:
        """Update should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.update({4, 5})
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, 'animaid.changed')
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, 'animaid.changed')

    def test_styled_copy_preserves_obs_id(self) -> None:
        """Styled copies should preserve _obs_id for reactive updates."""
        html_set = HTMLSet({1, 2, 3})
        styled = html_set.pills
        assert styled._obs_id == html_set._obs_id


class TestAnimateWithObservable:
    """Test Animate auto-updates when observable items change."""

    def test_animate_tracks_obs_id(self) -> None:
        """Animate should track obs_id when adding observable items."""
        from animaid import Animate

        anim = Animate(port=8290, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = anim.add(html_list)

            assert html_list._obs_id in anim._obs_id_to_item_id
            assert anim._obs_id_to_item_id[html_list._obs_id] == item_id
        finally:
            anim.stop()

    def test_animate_updates_on_list_change(self) -> None:
        """Animate should update browser when list changes."""
        from animaid import Animate

        anim = Animate(port=8291, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            anim.add(html_list)

            # Verify initial state
            state = anim.get_full_state()
            assert "1" in state[0]["html"]
            assert "4" not in state[0]["html"]

            # Mutate the list
            html_list.append(4)

            # Small delay for pubsub message to propagate
            time.sleep(0.1)

            # Verify updated state
            state = anim.get_full_state()
            assert "4" in state[0]["html"]
        finally:
            anim.stop()

    def test_animate_updates_on_dict_change(self) -> None:
        """Animate should update browser when dict changes."""
        from animaid import Animate

        anim = Animate(port=8292, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_dict = HTMLDict({"score": 0})
            anim.add(html_dict)

            # Verify initial state
            state = anim.get_full_state()
            assert "0" in state[0]["html"]

            # Mutate the dict
            html_dict["score"] = 100

            time.sleep(0.1)

            # Verify updated state
            state = anim.get_full_state()
            assert "100" in state[0]["html"]
        finally:
            anim.stop()

    def test_animate_updates_on_set_change(self) -> None:
        """Animate should update browser when set changes."""
        from animaid import Animate

        anim = Animate(port=8293, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_set = HTMLSet({1, 2, 3})
            anim.add(html_set)

            # Mutate the set
            html_set.add(99)

            time.sleep(0.1)

            # Verify updated state
            state = anim.get_full_state()
            assert "99" in state[0]["html"]
        finally:
            anim.stop()

    def test_animate_cleans_up_obs_id_on_remove(self) -> None:
        """Animate should clean up obs_id mapping when item is removed."""
        from animaid import Animate

        anim = Animate(port=8294, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = anim.add(html_list)

            assert html_list._obs_id in anim._obs_id_to_item_id

            anim.remove(item_id)

            assert html_list._obs_id not in anim._obs_id_to_item_id
        finally:
            anim.stop()

    def test_animate_cleans_up_obs_id_on_clear_all(self) -> None:
        """Animate should clean up all obs_id mappings when clear_all is called."""
        from animaid import Animate

        anim = Animate(port=8295, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            html_dict = HTMLDict({"a": 1})
            anim.add(html_list)
            anim.add(html_dict)

            assert len(anim._obs_id_to_item_id) == 2

            anim.clear_all()

            assert len(anim._obs_id_to_item_id) == 0
        finally:
            anim.stop()

    def test_refresh_method(self) -> None:
        """Refresh should re-render and broadcast a single item."""
        from animaid import Animate

        anim = Animate(port=8296, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = anim.add(html_list)

            # Manually modify without triggering notify
            list.append(html_list, 4)  # Bypass our override

            # State should not yet reflect change
            state = anim.get_full_state()
            # Note: state will actually reflect it since get_full_state re-renders

            # Call refresh
            result = anim.refresh(item_id)
            assert result is True

            # Refresh on non-existent ID
            result = anim.refresh("nonexistent")
            assert result is False
        finally:
            anim.stop()

    def test_refresh_all_method(self) -> None:
        """Refresh_all should re-render all items."""
        from animaid import Animate

        anim = Animate(port=8297, auto_open=False)
        anim.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            html_dict = HTMLDict({"a": 1})
            anim.add(html_list)
            anim.add(html_dict)

            # This should not raise
            anim.refresh_all()
        finally:
            anim.stop()
