from datetime import datetime
from lupin import Mapper, Schema, fields as f
from models import Artist, Diamond, Painting, Thief

leonardo = Artist(name="Leonardo da Vinci", birth_date=datetime(1452, 4, 15))
mona_lisa = Painting(name="Mona Lisa", author=leonardo)
arsene = Thief(name="Arsène Lupin", stolen_items=[mona_lisa])


mapper = Mapper()
artist_schema = Schema({
    "name": f.String(),
    "birthDate": f.DateTime(binding="birth_date", format="%Y-%m-%d")
}, name="artist")

diamond_schema = Schema({
    "carat": f.Field(),
    "type": f.Constant("diamond")  # this will be used to know which mapping to used while loading JSON
}, name="diamond")

painting_schema = Schema({
    "name": f.String(),
    "type": f.Constant("painting"),
    "author": f.Object(artist_schema)
}, name="painting")

# Use `PolymorphicList` for `stolen_items`
thief_schema = Schema({
    "name": f.String(),
    "stolenItems": f.PolymorphicList(on="type",  # JSON key to lookup for the polymorphic type
                                     binding="stolen_items",
                                     schemas={
                                         "painting": painting_schema,  # if `type == "painting"` then use painting_schema
                                         "diamond": diamond_schema  # if `type == "diamond"` then use diamond_schema
                                     })
}, name="thief")


mapper.register(Artist, artist_schema)
mapper.register(Diamond, diamond_schema)
mapper.register(Painting, painting_schema)
mapper.register(Thief, thief_schema)


diamond = Diamond(carat=20)
arsene.stolen_items.append(diamond)

# Dump object
data = mapper.dump(arsene)
assert data == {
    "name": "Arsène Lupin",
    "stolenItems": [
        {
            "name": "Mona Lisa",
            "type": "painting",
            "author": {
                "name": "Leonardo da Vinci",
                "birthDate": "1452-04-15"
            }
        },
        {
            "carat": 20,
            "type": "diamond"
        }
    ]
}

# Load data
thief = mapper.load(data, "thief")
assert isinstance(thief.stolen_items[0], Painting)
assert isinstance(thief.stolen_items[1], Diamond)
