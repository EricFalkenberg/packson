
## Packson
Easily bind json and dictionaries to python class instances 

### Justification 
Binding json and dictionaries to python class instances allows you to statically define what your data should look
like and provides a single interface for checking that all information in your data is typed and initialized correctly.

### Installation
```
pip install packson
```

### Examples 
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

# bind json data to AComplexPacksonObject 
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

# bind dictionary to AnIterableObject 
obj = AnIterableObject.from_dict(
    {
        'iterable_field': [
            {
                'field1': 1
            },
            {
                'field1': 2
            },
            {
                'field1': 3
            }
        ]   
    }
)
print([i.field1 for i in obj.iterable_field]) # prints [1, 2, 3]

# dump json data from AnIterableObject instance
print(obj.to_json()) 

# dump dictionary data from AnIterableObject instance
print(obj.to_dict()) 
```

