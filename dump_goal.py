class Schema(object):
    pass
StringField = IntField = ObjectField = Schema

class Thief(object):
    def __init__(self, name, stolen_items):
        self.name = name
        self.stolen_items = stolen_items

class Artist(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class Painting(object):
    def __init__(self, name, author):
        self.name = name
        self.author = author

class Diamond(object):
    def __init__(self, carat, color):
        self.carat = carat
        self.color = color

diamond_schema = Schema({
    "carat": IntField(),
    "color": StringField(),
    "type": StringField(default="diamond")
})


artist_schema = Schema({
    "firstName": StringField(binding="first_name"),
    "lastName": StringField(binding="last_name")
})

painting_schema = Schema({
    "name": StringField(),
    "author": ObjectField(artist_schema),
    "type": StringField(default="type")
})

class ThiefSchema(Schema):
    created_at = DatetimeField(key="createdAt")
    full_name = DynamicField(lambda self, obj: self.

    def dump(self, obj):
        super().dump(obj)

thief_schema = Schema({
    "name": StringField(),
    "age": StaticField(value="42"),
    "full_name": DynamicField()
    "stolenItems": PolymorphicListField(binding="stolen_items",
                                        on="type",
                                        schemas={
                                            "diamond": diamond_schema,
                                            "painting": painting_schema
                                        })
})

public_thief_schema = Schema({
    "name": StringField(),
})


thief = Thief("Arsène Lupin", [])

schema = mapper.schema(Thief, {
                        },
                        default=True)
mapper.register(Thief, thief_schema, default=True)
mapper.register(Thief, public_thief_schema)
mapper.dump(thief) # a besoin de {class: [schema1, schema2]}


# un schema vers plusieurs classes ?   => un schema ne peut charger qu'une seule classe
# une classe vers plusieurs schemas ?  => oui donc une classe a plusieurs vue JSON
