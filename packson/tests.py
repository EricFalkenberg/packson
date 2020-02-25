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


if __name__ == '__main__':
    unittest.main()