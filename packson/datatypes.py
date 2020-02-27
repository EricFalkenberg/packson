import json
from functools import WRAPPER_ASSIGNMENTS
import copy

PRIMITIVE_TYPES = [
    dict,
    list,
    str,
    int,
    float,
    bytes,
    tuple,
    list,
    set
]

ITERABLE_TYPES = [
    list,
    tuple,
    set
]


def packson_object(cls):

    class PacksonData(object):

        __json_data = {}

        def __init__(self, *args):
            self.__wrapper = cls(*args)
            for attr in WRAPPER_ASSIGNMENTS:
                if attr != '__annotations__':
                    setattr(self, attr, getattr(self.__wrapper.__class__, attr))
            self.__post_init__()

        def __post_init__(self):
            instance_attributes = super(PacksonData, self).__getattribute__('_PacksonData__wrapper') \
                .__class__ \
                .__dict__ \
                .items()
            for key, val in instance_attributes:
                if not key.startswith("__"):
                    self.__setattr__(key, val)

        def set_packson_field(self, key, val):
            attribute = copy.deepcopy(super(PacksonData, self).__getattribute__(key))
            if attribute.is_complex():
                val = attribute.type.from_dict(val)
            if attribute.is_iterable():
                new_val = []
                for element in val:
                    new_element = PacksonField(type=attribute.boxed_type, default=element)
                    if new_element.is_complex():
                        new_val += [new_element.type.from_dict(new_element.value)]
                    else:
                        new_val += [new_element]
                val = new_val
            if not isinstance(val, attribute.type):
                raise TypeError(f'value provided for {key} does not match field type {attribute.type}')
            attribute.set_value(val)
            self.__setattr__(key, attribute)

        def __setattr__(self, key, value):
            if key in WRAPPER_ASSIGNMENTS or key == '_PacksonData__wrapper':
                pass
            elif value.is_complex() and not value.is_none():
                self.__json_data[key] = value.value.to_dict()
            else:
                self.__json_data[key] = value.value
            super(PacksonData, self).__setattr__(key, value)

        def __getattribute__(self, item):
            attribute = super(PacksonData, self).__getattribute__(item)
            if isinstance(attribute, PacksonField):
                if attribute.is_iterable():
                    return [i.value if isinstance(i, PacksonField) else i for i in attribute.value]
                return attribute.value
            else:
                return attribute

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
            return repr(self.__wrapper)

    return PacksonData


class PacksonField(object):

    def __init__(self, type=None, boxed_type=None, default=None):
        self.type = type
        self.boxed_type = boxed_type
        self.value = default

    def set_value(self, value):
        self.value = value

    def is_complex(self):
        return not any([ty == self.type for ty in PRIMITIVE_TYPES])

    def is_iterable(self):
        return any([ty == self.type for ty in ITERABLE_TYPES])

    def is_none(self):
        return self.value is None


