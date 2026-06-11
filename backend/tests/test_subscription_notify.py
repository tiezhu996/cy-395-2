from app.services.subscription_service import should_notify


class FakeSubscription:
    def __init__(self, direction: str, target_rate: float):
        self.direction = direction
        self.target_rate = target_rate


class TestShouldNotifyBoth:
    def test_both_above_target(self):
        sub = FakeSubscription("both", 7.20)
        assert should_notify(sub, 7.30) is True

    def test_both_at_target(self):
        sub = FakeSubscription("both", 7.20)
        assert should_notify(sub, 7.20) is True

    def test_both_below_target(self):
        sub = FakeSubscription("both", 7.20)
        assert should_notify(sub, 7.10) is False

    def test_both_none_direction_defaults_to_both(self):
        sub = FakeSubscription(None, 7.20)
        assert should_notify(sub, 7.30) is True
        assert should_notify(sub, 7.10) is False


class TestShouldNotifyUp:
    def test_up_above_target(self):
        sub = FakeSubscription("up", 7.20)
        assert should_notify(sub, 7.30) is True

    def test_up_at_target(self):
        sub = FakeSubscription("up", 7.20)
        assert should_notify(sub, 7.20) is True

    def test_up_below_target_not_triggered(self):
        sub = FakeSubscription("up", 7.20)
        assert should_notify(sub, 7.10) is False

    def test_up_large_drop_not_triggered(self):
        sub = FakeSubscription("up", 7.20)
        assert should_notify(sub, 6.00) is False


class TestShouldNotifyDown:
    def test_down_below_target(self):
        sub = FakeSubscription("down", 7.20)
        assert should_notify(sub, 7.10) is True

    def test_down_at_target(self):
        sub = FakeSubscription("down", 7.20)
        assert should_notify(sub, 7.20) is True

    def test_down_above_target_not_triggered(self):
        sub = FakeSubscription("down", 7.20)
        assert should_notify(sub, 7.30) is False

    def test_down_large_rise_not_triggered(self):
        sub = FakeSubscription("down", 7.20)
        assert should_notify(sub, 8.00) is False


class TestShouldNotifyDirectionalDifference:
    def test_same_rate_different_direction(self):
        sub_up = FakeSubscription("up", 7.20)
        sub_down = FakeSubscription("down", 7.20)
        sub_both = FakeSubscription("both", 7.20)

        assert should_notify(sub_up, 7.30) is True
        assert should_notify(sub_down, 7.30) is False
        assert should_notify(sub_both, 7.30) is True

        assert should_notify(sub_up, 7.10) is False
        assert should_notify(sub_down, 7.10) is True
        assert should_notify(sub_both, 7.10) is False
