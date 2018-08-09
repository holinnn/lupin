from lupin.processors import upper


class TestUpper(object):
    def test_does_nothing_if_none(self):
        assert upper(None) is None

    def test_upper_string(self):
        assert upper("HeLLo") == "HELLO"
