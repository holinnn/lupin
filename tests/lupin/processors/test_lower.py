from lupin.processors import lower


class TestLower(object):
    def test_does_nothing_if_none(self):
        assert lower(None) is None

    def test_lower_string(self):
        assert lower("HeLLo") == "hello"
