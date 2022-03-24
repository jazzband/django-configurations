import base64
from django.test import TestCase
from configurations.example_generators import gen_bytes, gen_random_string, gen_django_secret_key


class ExampleGeneratorsTestCase(TestCase):
    def test_generators_dont_raise_exceptions(self):
        for gen in [gen_bytes(64, "hex"), gen_bytes(64, "base64"), gen_bytes(64, "base64_urlsafe"),
                    gen_random_string(16, "ab"), gen_random_string(5),
                    gen_django_secret_key]:
            with self.subTest(gen.__name__):
                gen()

    # gen_django_secret_key() and gen_random_string() are not tested beyond the above general test case
    # because they are just wrappers around existing django utilities.
    # They are thus assumed to work.

    def test_gen_bytes(self):
        with self.subTest("base64"):
            result = gen_bytes(64, "base64")()
            b = base64.standard_b64decode(result.encode("ASCII"))
            self.assertEqual(len(b), 64)

        with self.subTest("base64_urlsafe"):
            result = gen_bytes(64, "base64_urlsafe")()
            b = base64.urlsafe_b64decode(result.encode("ASCII"))
            self.assertEqual(len(b), 64)

        with self.subTest("hex"):
            result = gen_bytes(64, "hex")()
            b = bytes.fromhex(result)
            self.assertEqual(len(b), 64)

        with self.subTest("invalid"):
            self.assertRaises(ValueError, gen_bytes, 64, "invalid")
