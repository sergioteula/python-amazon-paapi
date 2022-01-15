import unittest

from amazon_paapi.helpers.generators import get_list_chunks


class TestHelpersGenerators(unittest.TestCase):
    def test_get_list_chunks(self):
        mocked_iterable = get_list_chunks(list(range(15)), 10)
        chunk = next(mocked_iterable)
        self.assertEqual(len(chunk), 10)
        chunk = next(mocked_iterable)
        self.assertEqual(len(chunk), 5)

        mocked_iterable = get_list_chunks(list(range(5)), 10)
        chunk = next(mocked_iterable)
        self.assertEqual(len(chunk), 5)
