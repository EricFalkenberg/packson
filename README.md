
## Packson

An alternative to Jackson Databind for Python 3

### Installation
```
pip install packson
```

### Usage
```python
import json
from packson.datatypes import packson_object, PacksonField

@packson_object
class ASimplePacksonObject(object):
    field1 = PacksonField(type=int)

@packson_object
class AComplexPacksonObject(object):
    field1 = PacksonField(type=int)
    field2 = PacksonField(type=str)
    field3 = PacksonField(type=ASimplePacksonObject)

@packson_object
class AnIterableObject(object):
    iterable_field = PacksonField(type=list, boxed_type=ASimplePacksonObject)

# automatically bind json to packson objects
obj = AComplexPacksonObject.from_json(
    json.dumps(
        {
            'field1': 3,
            'field2': 'hello',
            'field3': {
                'field1': 4
            }
        }
    )
)
print(obj.field1)        # prints 3
print(obj.field2)        # prints 'hello'
print(obj.field3.field1) # prints 4

# also works with dictionaries
obj = AnIterableObject.from_dict(
    {
        'iterable_field': [
            {
                'a': 1
            },
            {
                'a': 2
            },
            {
                'a': 3
            }
        ]   
    }
)
print([i.a for i in obj.iterable_field]) # prints [1, 2, 3]
```
