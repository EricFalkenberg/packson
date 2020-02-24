import json
from functools import WRAPPER_ASSIGNMENTS

PRIMITIVE_TYPES = [
    dict,
    list,
    str,
    int,
    float
]


def packson_object(cls):

    class PacksonData(object):

        __json_data = {}

        def __init__(self, *args):
            super(PacksonData, self).__setattr__('data', cls(*args))
            for attr in WRAPPER_ASSIGNMENTS:
                if attr != '__annotations__':
                    setattr(self, attr, getattr(self.data.__class__, attr))
            self.__post_init__()

        def __post_init__(self):
            instance_attributes = super(PacksonData, self).__getattribute__('data') \
                .__class__ \
                .__dict__ \
                .items()
            for key, val in instance_attributes:
                if not key.startswith("__"):
                    self.__setattr__(key, val)

        def set_packson_field(self, key, val):
            attribute = self.data.__getattribute__(key)
            if attribute.is_complex():
                val = attribute.type().from_dict(val)
            if not isinstance(val, attribute.type()):
                raise TypeError(f'{key} input {val} does not match field type {attribute.type()}')
            attribute.set_value(val)
            self.__setattr__(key, attribute)

        def __setattr__(self, key, value):
            data = super(PacksonData, self).__getattribute__('data')
            if key in WRAPPER_ASSIGNMENTS:
                pass
            elif value.is_complex() and not value.is_none():
                self.__json_data[key] = value.value().to_dict()
            else:
                self.__json_data[key] = value.value()
            setattr(data, key, value)

        def to_json(self):
            return json.dumps(self.to_dict())

        def to_dict(self):
            return self.__json_data

        @classmethod
        def from_json(cls, input_json):
            input_parsed = json.loads(input_json)
            return cls.from_dict(input_parsed)

        @classmethod
        def from_dict(cls, input_dict):
            o = cls()
            for key, val in input_dict.items():
                o.set_packson_field(key, val)
            return o

        def __repr__(self):
            return repr(self.data)

    return PacksonData


class PacksonField(object):

    def __init__(self, attribute_type=None, default=None):
        self.attribute_type = attribute_type
        self.attribute_value = default

    def type(self):
        return self.attribute_type

    def value(self):
        return self.attribute_value

    def set_value(self, attribute_value):
        self.attribute_value = attribute_value

    def is_complex(self):
        return not any([ty == self.type() for ty in PRIMITIVE_TYPES])

    def is_none(self):
        return self.value() is None


