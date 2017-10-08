from tests.fixtures import Thief


class TestLoad(object):
    def test_returns_a_thief(self, thief_schema, thief_data):
        thief = thief_schema.load(Thief, thief_data)
        assert isinstance(thief, Thief)
        assert thief.last_name == "Lupin"
        assert thief.first_name == "Arsène"


class TestDump(object):
    def test_returns_a_dictionary(self, thief_schema, thief, thief_data):
        data = thief_schema.dump(thief)
        assert data == thief_data
