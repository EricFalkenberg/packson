import unittest
import json
from os import listdir
from os.path import splitext
from packson.datatypes import PacksonField, packson_object

RESOURCE_FILES = {}
for file in listdir('resources/'):
    with open(f'resources/{file}') as f:
        RESOURCE_FILES[splitext(file)[0]] = f.read()


class PacksonObjectTests(unittest.TestCase):

    def test_simple_object_from_json(self):
        res = SimpleObject.from_json(RESOURCE_FILES['simple_object'])
        self.assertIsInstance(res, SimpleObject)
        self.assertEqual(res.a, 3)

    def test_complex_object_from_json(self):
        res = ComplexObject.from_json(RESOURCE_FILES['complex_object'])
        self.assertIsInstance(res, ComplexObject)
        self.assertIsInstance(res.b, SimpleObject)
        self.assertEqual(res.b.a, 3)

    def test_iterable_object_from_json(self):
        res = ComplexIterObject.from_json(
            RESOURCE_FILES['complex_iter_object'])
        self.assertIsInstance(res, ComplexIterObject)
        self.assertIsInstance(res.iterable, list)
        for idx, element in enumerate(res.iterable):
            self.assertIsInstance(element, SimpleObject)
            self.assertIsInstance(element.a, int)
            self.assertEqual(idx + 1, element.a)

    def test_simple_iterable_from_dict(self):
        obj = SimpleIterObject.from_dict(
            json.loads(RESOURCE_FILES['simple_iter_object']))
        self.assertEqual('[1, 2, 3]', str(obj.iterable))

    def test_multiple_complex_object_from_dict(self):
        obj = MultiFieldComplexObject.from_dict(
            json.loads(RESOURCE_FILES['multi_field_complex_object']))
        self.assertIsInstance(obj, MultiFieldComplexObject)
        self.assertIsInstance(obj.a, SimpleObject)
        self.assertIsInstance(obj.a.a, int)
        self.assertEqual(obj.a.a, 1)
        self.assertIsInstance(obj.b, SimpleObject)
        self.assertIsInstance(obj.b.a, int)
        self.assertEqual(obj.b.a, 2)
        self.assertIsInstance(obj.c, SimpleObject)
        self.assertIsInstance(obj.c.a, int)
        self.assertEqual(obj.c.a, 3)

    def test_simple_object_from_create(self):
        res = SimpleObject.create(
            a=3
        )
        self.assertIsInstance(res, SimpleObject)
        self.assertIsInstance(res.a, int)
        self.assertEqual(res.a, 3)
        self.assertEqual(res.to_json(), json.dumps(
            {
                'a': 3
            }
        ))

    def test_complex_object_from_create(self):
        res = ComplexObject.create(
            b=SimpleObject.create(
                a=3
            )
        )
        self.assertIsInstance(res, ComplexObject)
        self.assertIsInstance(res.b, SimpleObject)
        self.assertIsInstance(res.b.a, int)
        self.assertEqual(res.b.a, 3)
        self.assertEqual(res.to_json(), json.dumps(
            {
                'b': {
                    'a': 3
                }
            }
        ))

    def test_complex_iter_object_from_file(self):
        res = ComplexIterObject.from_file('resources/from_file.json')
        self.assertIsInstance(res, ComplexIterObject)
        self.assertIsInstance(res.iterable, list)
        for idx, element in enumerate(res.iterable):
            self.assertIsInstance(element, SimpleObject)
            self.assertIsInstance(element.a, int)
            self.assertEqual(idx + 1, element.a)

    def test_from_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            ComplexIterObject.from_file(
                'resources/a_file_that_definitely_doesnt_exist.json')

    def test_simple_object_from_json_bad_type(self):
        with self.assertRaises(TypeError):
            SimpleObject.from_json(
                json.dumps(
                    {
                        'a': 'a_string'
                    }
                )
            )

    def test_non_serializable_json(self):
        def non_serializable(x): return x if x else 0
        NonSerializable.create(
            field1=non_serializable
        ).to_json()

    def test_simple_object_from_json_bad_key(self):
        with self.assertRaises(AttributeError):
            SimpleObject.from_json(
                json.dumps(
                    {
                        'b': 3
                    }
                )
            )

    def test_simple_object_from_dict_missing_key(self):
        res = SimpleObject.from_dict({})
        self.assertIs(res.a, None)


class PacksonFieldTests(unittest.TestCase):

    def test_int_packson_field(self):
        int_field = PacksonField(type=int, default=0)
        self.assertEqual(int_field.value, 0)
        self.assertEqual(int_field.type, int)
        self.assertFalse(int_field.is_complex())
        self.assertFalse(int_field.is_none())


@packson_object
class SimpleObject:
    a = PacksonField(type=int)


@packson_object
class ComplexObject:
    b = PacksonField(type=SimpleObject)


@packson_object
class MultiFieldComplexObject:
    a = PacksonField(type=SimpleObject)
    b = PacksonField(type=SimpleObject)
    c = PacksonField(type=SimpleObject)


@packson_object
class ComplexIterObject:
    iterable = PacksonField(type=list, boxed_type=SimpleObject)


@packson_object
class SimpleIterObject:
    iterable = PacksonField(type=list, boxed_type=int)


@packson_object
class NonSerializable:
    field1 = PacksonField(type=type(lambda x: 0))


if __name__ == '__main__':
    unittest.main()
