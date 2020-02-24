
## Packson

An alternative to Jackson Databind for Python 3

### Usage
```python

@packson_object
class AJsonRequest(object):
    field1 = PacksonField(attribute_type=int)
    field2 = PacksonField(attribute_type=str)
    field3 = PacksonField(attribute_type=AnotherPacksonObject)

@packson_object
class AnotherPacksonObject(object):
    field1 = PacksonField(attribute_type=int)


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
print(obj.data.field1.value())
```
