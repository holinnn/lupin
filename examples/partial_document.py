from lupin import Mapper, Schema, fields as f
from models import Artist

mapper = Mapper()
artist_schema = Schema({
    "name": f.String(),
    "birthDate": f.DateTime(binding="birth_date", format="%Y-%m-%d")
}, name="artist")

mapper.register(Artist, artist_schema)

data = {
    "name": "Leonardo da Vinci"
}

artist = mapper.load(data, "artist", allow_partial=True)
assert artist.name == "Leonardo da Vinci"
assert not hasattr(artist, "birth_date")
