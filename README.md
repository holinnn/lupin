# lupin is a Python JSON object mapper

[![Build Status](https://travis-ci.org/holinnn/lupin.svg)](https://travis-ci.org/holinnn/lupin)

lupin is meant to help in serializing python objects to JSON and unserializing JSON data to python objects.


## Installation

```
pip install lupin
```

## Usage

lupin uses schemas to create a representation of a python object.

A schema is composed of fields which represents the way to load and dump an attribute of an object.

### Define schemas

```python
from datetime import datetime
from lupin import Mapper, Schema, fields as f


# 1) Define your models
class Thief(object):
    def __init__(self, name, stolen_items):
        self.name = name
        self.stolen_items = stolen_items


class Painting(object):
    def __init__(self, name, author):
        self.name = name
        self.author = author


class Artist(object):
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date


# 2) Create schemas
artist_schema = Schema({
    "name": f.String(),
    "birthDate": f.DateTime(binding="birth_date", format="%Y-%m-%d")
}, name="artist")

painting_schema = Schema({
    "name": f.String(),
    "author": f.Object(artist_schema)
}, name="painting")

thief_schema = Schema({
    "name": f.String(),
    "stolenItems": f.List(painting_schema, binding="stolen_items")
}, name="thief")

# 3) Create a mapper and register a schema for each of your models you want to map to JSON objects
mapper = Mapper()

mapper.register(Artist, artist_schema)
mapper.register(Painting, painting_schema)
mapper.register(Thief, thief_schema)


# 4) Create some sample data
leonardo = Artist(name="Leonardo da Vinci", birth_date=datetime(1452, 4, 15))
mona_lisa = Painting(name="Mona Lisa", author=leonardo)
arsene = Thief(name="Arsène Lupin", stolen_items=[mona_lisa])
```

### Dump objects

```python
# use mapper to dump python objects
assert mapper.dump(leonardo) == {
    "name": "Leonardo da Vinci",
    "birthDate": "1452-04-15"
}

assert mapper.dump(mona_lisa) == {
    "name": "Mona Lisa",
    "author": {
        "name": "Leonardo da Vinci",
        "birthDate": "1452-04-15"
    }
}

assert mapper.dump(arsene) == {
    "name": "Arsène Lupin",
    "stolenItems": [
        {
            "name": "Mona Lisa",
            "author": {
                "name": "Leonardo da Vinci",
                "birthDate": "1452-04-15"
            }
        }
    ]
}
```

### Load objects

```python
# use mapper to load JSON data
data = {
    "name": "Mona Lisa",
    "author": {
        "name": "Leonardo da Vinci",
        "birthDate": "1452-04-15"
    }
}
painting = mapper.load(data, "painting")  # "painting" is the name of the schame you want to use
artist = painting.author

assert isinstance(painting, Painting)
assert painting.name == "Mona Lisa"

assert isinstance(artist, Artist)
assert artist.name == "Leonardo da Vinci"
assert artist.birth_date == datetime(1452, 4, 15)
```

### Polymorphic lists

Sometimes a list can contain multiple type of objects. In such cases you will have to use a `PolymorphicList`, you will also need to add
a key in the items schema to store the type of the object (you can use a `Constant` field).

Say that our thief has level up and has stolen a diamond.

```python
class Diamond(object):
    def __init__(self, carat):
        self.carat = carat


mapper = Mapper()

# Register a schema for diamonds
diamond_schema = Schema({
    "carat": f.Field(),
    "type": f.Constant("diamond")  # this will be used to know which schema to used while loading JSON
}, name="diamond")
mapper.register(Diamond, diamond_schema)

# Change our painting schema in order to include a `type` field
painting_schema = Schema({
    "name": f.String(),
    "type": f.Constant("painting"),
    "author": f.Object(artist_schema)
}, name="painting")
mapper.register(Painting, painting_schema)

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
```

### Validation

Lupin provides a set of builtin validators, you can find them in the [lupin/validators](https://github.com/holinnn/lupin/tree/develop/lupin/validators) folder.

While creating your schemas you can assign validators to the fields. Before loading a document lupin will validate
its format. If one field is invalid, an `InvalidDocument` is raised with all the error detected in the data.

Example :

```python
from lupin import Mapper, Schema, fields as f, validators as v
from lupin.errors import InvalidDocument, InvalidLength
from models import Artist

mapper = Mapper()

artist_schema = Schema({
    "name": f.String(validators=v.Length(max=10)),
}, name="artist")
mapper.register(Artist, artist_schema)

data = {
    "name": "Leonardo da Vinci"
}

try:
    mapper.load(data, artist_schema, allow_partial=True)
except InvalidDocument as errors:
    error = errors[0]
    assert isinstance(error, InvalidLength)
    assert error.path == ["name"]
```

Current validators are :
- `DateTimeFormat` (validate that value is a valid datetime format)
- `Equal` (validate that value is equal to a predefined one)
- `In` (validate that a value is contained in a set of value)
- `Length` (validate the length of a value)
- `Match` (validate the format of a value with a regex)
- `Type` (validate the type of a value, this validator is already included in all fields to match the field type)
- `URL` (validate an URL string format)
- `IsNone` (validate that value is None)
- `Between` (validate that value belongs to a range)


#### Combination

You can build validators combinations using the `&` and `|` operator.

Example :

```python
from lupin import validators as v
from lupin.errors import ValidationError

validators = v.Equal("Lupin") | v.Equal("Andrésy")
# validators passes only if value is "Lupin" or "Andrésy"

validators("Lupin", [])

try:
    validators("Holmes", [])
except ValidationError:
    print("Validation error")
```
