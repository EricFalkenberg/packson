import unittest
import json
from datatypes import PacksonField, packson_object


class PacksonObjectTests(unittest.TestCase):

    def test_simple_object_from_json(self):
        res = SimpleObject.from_json(
            json.dumps(
                {
                    'a': 3
                }
            )
        )
        self.assertIsInstance(res, SimpleObject)
        self.assertEqual(res.a, 3)

    def test_complex_object_from_json(self):
        res = ComplexObject.from_json(
            json.dumps(
                {
                    'b': {
                        'a': 3
                    }
                }
            )
        )
        self.assertIsInstance(res, ComplexObject)
        self.assertIsInstance(res.b, SimpleObject)
        self.assertEqual(res.b.a, 3)

    def test_iterable_object_from_json(self):
        res = IterObject.from_json(
            json.dumps(
                {
                    'iterable': [
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
        )
        self.assertIsInstance(res, IterObject)
        self.assertIsInstance(res.iterable, list)
        for idx, element in enumerate(res.iterable):
            self.assertIsInstance(element, SimpleObject)
            self.assertIsInstance(element.a, int)
            self.assertEqual(idx+1, element.a)

    def test_simple_iterable_from_dict(self):
        obj = SimpleIterObject.from_dict(
            {
                'iterable': [1, 2, 3]
            }
        )
        self.assertEqual('[1, 2, 3]', str(obj.iterable))

    def test_simple_object_from_json_bad_type(self):
        with self.assertRaises(TypeError):
            SimpleObject.from_json(
                json.dumps(
                    {
                        'a': 'a_string'
                    }
                )
            )


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
class IterObject:
    iterable = PacksonField(type=list, boxed_type=SimpleObject)

@packson_object
class SimpleIterObject:
    iterable = PacksonField(type=list, boxed_type=int)


if __name__ == '__main__':
    unittest.main()