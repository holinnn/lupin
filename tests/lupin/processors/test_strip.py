from lupin.processors import strip


class TestStrip(object):
    def test_does_nothing_if_none(self):
        assert strip(None) is None

    def test_strip_string(self):
        assert strip(" hello ") == "hello"
