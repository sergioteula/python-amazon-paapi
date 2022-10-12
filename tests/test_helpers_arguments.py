import unittest

from amazon_paapi.errors import AsinNotFound, InvalidArgument
from amazon_paapi.helpers.arguments import (
    check_browse_nodes_args,
    check_search_mandatory_args,
    check_search_pagination_args,
    check_variations_args,
    get_items_ids,
)


class TestHelpersArguments(unittest.TestCase):
    def setUp(self):
        self.amazon_urls = [
            "https://www.amazon.es/gp/product/B07PHPXHQS",
            "https://www.amazon.es/test-name/dp/B08TJRVWV1/?test",
        ]
        self.invalid_url = "https://www.amazon.es/earlyaccess"

    def tearDown(self):
        del self.amazon_urls
        del self.invalid_url

    def test_get_item_id_from_url(self):
        result = get_items_ids(self.amazon_urls[0])
        self.assertEqual(["B07PHPXHQS"], result)

    def test_get_item_id_from_several_urls(self):
        result = get_items_ids(self.amazon_urls)
        self.assertEqual(["B07PHPXHQS", "B08TJRVWV1"], result)

    def test_get_item_id_for_invalid_url(self):
        with self.assertRaises(AsinNotFound):
            get_items_ids(self.invalid_url)

    def test_get_item_id_from_several_urls_with_invalid_url(self):
        self.amazon_urls.insert(1, self.invalid_url)
        with self.assertRaises(AsinNotFound):
            get_items_ids(self.amazon_urls)

    def test_get_item_id_from_asin(self):
        result = get_items_ids("B01N5IB20Q")
        self.assertEqual(["B01N5IB20Q"], result)

    def test_get_items_ids_from_string_of_asins(self):
        result = get_items_ids("B01N5IB20Q,B01N5IB20Q,B01N5IB20Q")
        self.assertEqual(["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"], result)

    def test_get_items_ids_from_list_of_asins(self):
        result = get_items_ids(["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"])
        self.assertEqual(["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"], result)

    def test_get_items_ids_invalid_argument(self):
        with self.assertRaises(InvalidArgument):
            get_items_ids(34)

    def test_check_search_mandatory_args_correct(self):
        check_search_mandatory_args(actor="John Doe")

    def test_check_search_mandatory_args_raises_exception(self):
        with self.assertRaises(InvalidArgument):
            check_search_mandatory_args()

    def test_check_search_pagination_args_correct(self):
        check_search_pagination_args(item_count=1, item_page=10)

    def test_check_search_pagination_args_if_not_integers(self):
        with self.assertRaises(InvalidArgument):
            check_search_pagination_args(item_count=True, item_page="test")

    def test_check_search_pagination_args_if_not_between_1_10(self):
        with self.assertRaises(InvalidArgument):
            check_search_pagination_args(item_count=0, item_page=11)

    def test_check_check_variations_args_correct(self):
        check_variations_args(variation_count=1, variation_page=10)

    def test_check_check_variations_args_if_not_integers(self):
        with self.assertRaises(InvalidArgument):
            check_variations_args(variation_count=True, variation_page="test")

    def test_check_check_variations_args_if_not_between_1_10(self):
        with self.assertRaises(InvalidArgument):
            check_variations_args(variation_count=0, variation_page=11)

    def test_check_browse_nodes_args_correct(self):
        check_browse_nodes_args(browse_node_ids=["1"])

    def test_check_browse_nodes_args_if_not_list(self):
        with self.assertRaises(InvalidArgument):
            check_browse_nodes_args(browse_node_ids=1)
