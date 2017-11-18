"""Models used in examples"""


class Artist(object):
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date


class Diamond(object):
    def __init__(self, carat):
        self.carat = carat


class Thief(object):
    def __init__(self, name, stolen_items):
        self.name = name
        self.stolen_items = stolen_items


class Painting(object):
    def __init__(self, name, author):
        self.name = name
        self.author = author
