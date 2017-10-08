thief = mapper.load(data, Thief)  # use default schema
thief = mapper.load(data, private_thief_schema)  # explict schema, needs {schema: class}


class ObjectField(Field):
    def dump(self, obj):
        self._schema.dump(obj)

    def load(self, data):
        self._schema.load(data)


class PolymorphicObjectField(Field):
    def dump(self, obj):
        schema = self._schemas[type(obj)]
        schema.dump(obj)

