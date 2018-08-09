from lupin.processors import null_processor


class TestNullProcessor(object):
    def test_returns_value(self):
        assert null_processor(1) == 1
