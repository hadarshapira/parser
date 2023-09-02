class Field:

    def __init__(self, name: str, field_type: str, length: int, mandatory: bool, **kwargs):
        self.name = name
        self.field_type = field_type
        self.length = length
        self.mandatory = mandatory
        for key, value in kwargs.items():
            setattr(self, key, value)
