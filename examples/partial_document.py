from lupin import Mapper, Schema, fields as f
from models import Artist

mapper = Mapper()

mapping = mapper.register(Artist, Schema({
    "name": f.String(),
    "birthDate": f.DateTime(binding="birth_date", format="%Y-%m-%d")
}))

data = {
    "name": "Leonardo da Vinci"
}

artist = mapper.load(data, mapping, allow_partial=True)
assert artist.name == "Leonardo da Vinci"
assert not hasattr(artist, "birth_date")
