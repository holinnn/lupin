from lupin import Mapper, Schema, fields as f, validators as v
from lupin.errors import InvalidDocument, InvalidLength
from models import Artist

mapper = Mapper()

artist_schema = Schema({
    "name": f.String(validators=v.Length(max=10)),
}, name="artist")

mapping = mapper.register(Artist, artist_schema)

data = {
    "name": "Leonardo da Vinci"
}

try:
    mapper.load(data, "artist", allow_partial=True)
except InvalidDocument as errors:
    error = errors[0]
    assert isinstance(error, InvalidLength)
    assert error.path == ["name"]
