from interfaces.local import LocalInterface


class TestLocalInterface:

    def setup(self):
        self.li = LocalInterface()

    def test_token_loading(self):
        assert 1_000_000 <= self.li.load_token(1234) <= 9_999_999
