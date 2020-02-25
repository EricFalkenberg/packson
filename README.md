
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
class AnotherPacksonObject(object):
    field1 = PacksonField(type=int)

@packson_object
class AJsonRequest(object):
    field1 = PacksonField(type=int)
    field2 = PacksonField(type=str)
    field3 = PacksonField(type=AnotherPacksonObject)


# automatically bind json to packson objects
obj = AJsonRequest.from_json(
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
print(obj.field1)
print(obj.field3.field1)
```
