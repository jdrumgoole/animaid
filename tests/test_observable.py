"""Tests for observable HTML objects with pypubsub."""

import time

from pubsub import pub

from animaid import HTMLDict, HTMLList, HTMLSet


class TestHTMLListObservable:
    """Test HTMLList publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLList should have a unique _obs_id."""
        html_list = HTMLList([1, 2, 3])
        assert hasattr(html_list, "_obs_id")
        assert html_list._obs_id is not None

    def test_append_publishes(self) -> None:
        """Append should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.append(4)
            assert len(received) == 1
            assert received[0] == html_list._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_extend_publishes(self) -> None:
        """Extend should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.extend([4, 5])
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_setitem_publishes(self) -> None:
        """Setting item should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_list = HTMLList([1, 2, 3])
            html_list[0] = 100
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_pop_publishes(self) -> None:
        """Pop should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.pop()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_list = HTMLList([1, 2, 3])
            html_list.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_in_place_styling_returns_self(self) -> None:
        """In-place styling should return self (same object)."""
        html_list = HTMLList([1, 2, 3])
        styled = html_list.pills()
        assert styled is html_list


class TestHTMLDictObservable:
    """Test HTMLDict publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLDict should have a unique _obs_id."""
        html_dict = HTMLDict({"a": 1})
        assert hasattr(html_dict, "_obs_id")
        assert html_dict._obs_id is not None

    def test_setitem_publishes(self) -> None:
        """Setting item should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict["b"] = 2
            assert len(received) == 1
            assert received[0] == html_dict._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_update_publishes(self) -> None:
        """Update should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict.update({"b": 2, "c": 3})
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_pop_publishes(self) -> None:
        """Pop should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_dict = HTMLDict({"a": 1, "b": 2})
            html_dict.pop("a")
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_dict = HTMLDict({"a": 1})
            html_dict.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_in_place_styling_returns_self(self) -> None:
        """In-place styling should return self (same object)."""
        html_dict = HTMLDict({"a": 1})
        styled = html_dict.card()
        assert styled is html_dict


class TestHTMLSetObservable:
    """Test HTMLSet publishes changes via pypubsub."""

    def test_has_obs_id(self) -> None:
        """HTMLSet should have a unique _obs_id."""
        html_set = HTMLSet({1, 2, 3})
        assert hasattr(html_set, "_obs_id")
        assert html_set._obs_id is not None

    def test_add_publishes(self) -> None:
        """Add should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.add(4)
            assert len(received) == 1
            assert received[0] == html_set._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_discard_publishes(self) -> None:
        """Discard should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.discard(1)
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_update_publishes(self) -> None:
        """Update should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.update({4, 5})
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_clear_publishes(self) -> None:
        """Clear should publish change notification."""
        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            html_set = HTMLSet({1, 2, 3})
            html_set.clear()
            assert len(received) == 1
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_in_place_styling_returns_self(self) -> None:
        """In-place styling should return self (same object)."""
        html_set = HTMLSet({1, 2, 3})
        styled = html_set.pills()
        assert styled is html_set


class TestAppWithObservable:
    """Test App auto-updates when observable items change."""

    def test_app_tracks_obs_id(self) -> None:
        """App should track obs_id when adding observable items."""
        from animaid import App

        app = App(port=8290, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = app.add(html_list)

            assert html_list._obs_id in app._obs_id_to_item_id
            assert app._obs_id_to_item_id[html_list._obs_id] == item_id
        finally:
            app.stop()

    def test_app_updates_on_list_change(self) -> None:
        """App should update browser when list changes."""
        from animaid import App

        app = App(port=8291, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            app.add(html_list)

            # Verify initial state
            state = app.get_full_state()
            assert "1" in state[0]["html"]
            assert "4" not in state[0]["html"]

            # Mutate the list
            html_list.append(4)

            # Small delay for pubsub message to propagate
            time.sleep(0.1)

            # Verify updated state
            state = app.get_full_state()
            assert "4" in state[0]["html"]
        finally:
            app.stop()

    def test_app_updates_on_dict_change(self) -> None:
        """App should update browser when dict changes."""
        from animaid import App

        app = App(port=8292, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_dict = HTMLDict({"score": 0})
            app.add(html_dict)

            # Verify initial state
            state = app.get_full_state()
            assert "0" in state[0]["html"]

            # Mutate the dict
            html_dict["score"] = 100

            time.sleep(0.1)

            # Verify updated state
            state = app.get_full_state()
            assert "100" in state[0]["html"]
        finally:
            app.stop()

    def test_app_updates_on_set_change(self) -> None:
        """App should update browser when set changes."""
        from animaid import App

        app = App(port=8293, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_set = HTMLSet({1, 2, 3})
            app.add(html_set)

            # Mutate the set
            html_set.add(99)

            time.sleep(0.1)

            # Verify updated state
            state = app.get_full_state()
            assert "99" in state[0]["html"]
        finally:
            app.stop()

    def test_app_cleans_up_obs_id_on_remove(self) -> None:
        """App should clean up obs_id mapping when item is removed."""
        from animaid import App

        app = App(port=8294, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = app.add(html_list)

            assert html_list._obs_id in app._obs_id_to_item_id

            app.remove(item_id)

            assert html_list._obs_id not in app._obs_id_to_item_id
        finally:
            app.stop()

    def test_app_cleans_up_obs_id_on_clear_all(self) -> None:
        """App should clean up all obs_id mappings when clear_all is called."""
        from animaid import App

        app = App(port=8295, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            html_dict = HTMLDict({"a": 1})
            app.add(html_list)
            app.add(html_dict)

            assert len(app._obs_id_to_item_id) == 2

            app.clear_all()

            assert len(app._obs_id_to_item_id) == 0
        finally:
            app.stop()

    def test_refresh_method(self) -> None:
        """Refresh should re-render and broadcast a single item."""
        from animaid import App

        app = App(port=8296, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            item_id = app.add(html_list)

            # Manually modify without triggering notify
            list.append(html_list, 4)  # Bypass our override

            # State would not yet reflect change without re-render
            # Note: get_full_state re-renders, so we skip checking here

            # Call refresh
            result = app.refresh(item_id)
            assert result is True

            # Refresh on non-existent ID
            result = app.refresh("nonexistent")
            assert result is False
        finally:
            app.stop()

    def test_refresh_all_method(self) -> None:
        """Refresh_all should re-render all items."""
        from animaid import App

        app = App(port=8297, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            html_list = HTMLList([1, 2, 3])
            html_dict = HTMLDict({"a": 1})
            app.add(html_list)
            app.add(html_dict)

            # This should not raise
            app.refresh_all()
        finally:
            app.stop()


class TestImmutableTypesObservable:
    """Test observable mechanism for immutable types."""

    def test_html_string_has_obs_id(self) -> None:
        """HTMLString should have a unique _obs_id."""
        from animaid import HTMLString

        s = HTMLString("hello")
        assert hasattr(s, "_obs_id")
        assert s._obs_id is not None

    def test_html_string_styling_publishes(self) -> None:
        """HTMLString styling should publish change notification."""
        from animaid import HTMLString

        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            s = HTMLString("hello")
            s.bold()
            assert len(received) == 1
            assert received[0] == s._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_html_int_has_obs_id(self) -> None:
        """HTMLInt should have a unique _obs_id."""
        from animaid import HTMLInt

        n = HTMLInt(42)
        assert hasattr(n, "_obs_id")
        assert n._obs_id is not None

    def test_html_int_styling_publishes(self) -> None:
        """HTMLInt styling should publish change notification."""
        from animaid import HTMLInt

        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            n = HTMLInt(42)
            n.red()
            assert len(received) == 1
            assert received[0] == n._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_html_float_has_obs_id(self) -> None:
        """HTMLFloat should have a unique _obs_id."""
        from animaid import HTMLFloat

        f = HTMLFloat(3.14)
        assert hasattr(f, "_obs_id")
        assert f._obs_id is not None

    def test_html_float_styling_publishes(self) -> None:
        """HTMLFloat styling should publish change notification."""
        from animaid import HTMLFloat

        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            f = HTMLFloat(3.14)
            f.bold()
            assert len(received) == 1
            assert received[0] == f._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_html_tuple_has_obs_id(self) -> None:
        """HTMLTuple should have a unique _obs_id."""
        from animaid import HTMLTuple

        t = HTMLTuple((1, 2, 3))
        assert hasattr(t, "_obs_id")
        assert t._obs_id is not None

    def test_html_tuple_styling_publishes(self) -> None:
        """HTMLTuple styling should publish change notification."""
        from animaid import HTMLTuple

        received: list[str] = []

        def listener(obs_id: str) -> None:
            received.append(obs_id)

        pub.subscribe(listener, "animaid.changed")
        try:
            t = HTMLTuple((1, 2, 3))
            t.pills()
            assert len(received) == 1
            assert received[0] == t._obs_id
        finally:
            pub.unsubscribe(listener, "animaid.changed")

    def test_app_updates_on_string_styling(self) -> None:
        """App should update browser when HTMLString is styled."""
        from animaid import App, HTMLString

        app = App(port=8298, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            s = HTMLString("hello")
            app.add(s)

            # Verify initial state
            state = app.get_full_state()
            assert "font-weight: bold" not in state[0]["html"]

            # Style the string
            s.bold()

            time.sleep(0.1)

            # Verify updated state
            state = app.get_full_state()
            assert "font-weight: bold" in state[0]["html"]
        finally:
            app.stop()

    def test_app_updates_on_int_styling(self) -> None:
        """App should update browser when HTMLInt is styled."""
        from animaid import App, HTMLInt

        app = App(port=8299, auto_open=False)
        app.run()
        time.sleep(0.5)

        try:
            n = HTMLInt(42)
            app.add(n)

            # Verify initial state
            state = app.get_full_state()
            assert "color: red" not in state[0]["html"]

            # Style the int
            n.red()

            time.sleep(0.1)

            # Verify updated state
            state = app.get_full_state()
            assert "color: red" in state[0]["html"]
        finally:
            app.stop()
