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


# 2) create a mapper
mapper = Mapper()

# 3) register a schema for each of your models you want to map to JSON objects
artist_mapping = mapper.register(Artist, Schema({
    "name": f.String(),
    "birthDate": f.Datetime(binding="birth_date", format="%Y-%m-%d")
}))

painting_mapping = mapper.register(Painting, Schema({
    "name": f.String(),
    "author": f.Object(artist_mapping)
}))

mapper.register(Thief, Schema({
    "name": f.String(),
    "stolenItems": f.List(painting_mapping, binding="stolen_items")
}))


# 4) create some sample data
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
painting = mapper.load(data, painting_mapping)
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
diamond_mapping = mapper.register(Diamond, Schema({
    "carat": f.Field(),
    "type": f.Constant("diamond")  # this will be used to know which mapping to used while loading JSON
}))

# Change our painting schema in order to include a `type` field
painting_mapping = mapper.register(Painting, Schema({
    "name": f.String(),
    "type": f.Constant("painting"),
    "author": f.Object(artist_mapping)
}))

# Use `PolymorphicList` for `stolen_items`
thief_mapping = mapper.register(Thief, Schema({
    "name": f.String(),
    "stolenItems": f.PolymorphicList(on="type",  # JSON key to lookup for the polymorphic type
                                     binding="stolen_items",
                                     mappings={
                                         "painting": painting_mapping,  # if `type == "painting"` then use painting_mapping
                                         "diamond": diamond_mapping  # if `type == "diamond"` then use diamond_mapping
                                     })
}))


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
thief = mapper.load(data, thief_mapping)
assert isinstance(thief.stolen_items[0], Painting)
assert isinstance(thief.stolen_items[1], Diamond)
```
