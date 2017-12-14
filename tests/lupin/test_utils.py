import pytest
from lupin.utils import get_mapping
from lupin.errors import MissingMapping
from tests.fixtures import Painting, Jewel


class OilPainting(Painting):
    pass


class TestGetPolymorphicMapping(object):
    def test_raise_error_if_no_mapping_found(self, mona_lisa):
        with pytest.raises(MissingMapping):
            get_mapping({}, mona_lisa)

    def test_returns_mapping_of_object(self, mona_lisa, painting_mapping, jewel_mapping):
        mapping = get_mapping({Jewel: jewel_mapping, Painting: painting_mapping},
                              mona_lisa)
        assert mapping == painting_mapping

    def test_returns_mapping_of_parent_class_if(self, painting_mapping, jewel_mapping):
        painting = OilPainting(None, None)
        mapping = get_mapping({Jewel: jewel_mapping, Painting: painting_mapping},
                              painting)
        assert mapping == painting_mapping
