import unittest
from unittest.mock import Mock, patch

from amazon_paapi.errors.exceptions import MalformedRequest
from amazon_paapi.helpers import requests


class TestRequests(unittest.TestCase):
    @patch.object(requests, "GetItemsRequest")
    def test_get_items_request(self, mock_get_items_request):
        mock_get_items_request.return_value = "foo"
        result = requests.get_items_request(Mock(), ["test"])

        self.assertEqual("foo", result)

    @patch.object(requests, "GetItemsRequest")
    def test_get_items_request_error(self, mock_get_items_request):
        mock_get_items_request.side_effect = TypeError()

        with self.assertRaises(MalformedRequest):
            requests.get_items_request(Mock(), ["test"])

    @patch.object(requests, "SearchItemsRequest")
    def test_search_items_request(self, mock_search_items_request):
        mock_search_items_request.return_value = "foo"
        result = requests.get_search_items_request(Mock())

        self.assertEqual("foo", result)

    @patch.object(requests, "SearchItemsRequest")
    def test_search_items_request_error(self, mock_search_items_request):
        mock_search_items_request.side_effect = TypeError()

        with self.assertRaises(MalformedRequest):
            requests.get_search_items_request(Mock())

    @patch.object(requests, "GetVariationsRequest")
    def test_variations_request(self, mock_variations_request):
        mock_variations_request.return_value = "foo"
        result = requests.get_variations_request(Mock())

        self.assertEqual("foo", result)

    @patch.object(requests, "GetVariationsRequest")
    def test_variations_request_error(self, mock_variations_request):
        mock_variations_request.side_effect = TypeError()

        with self.assertRaises(MalformedRequest):
            requests.get_variations_request(Mock())

    @patch.object(requests, "GetBrowseNodesRequest")
    def test_browse_nodes_request(self, mock_browse_nodes_request):
        mock_browse_nodes_request.return_value = "foo"
        result = requests.get_browse_nodes_request(Mock())

        self.assertEqual("foo", result)

    @patch.object(requests, "GetBrowseNodesRequest")
    def test_browse_nodes_request_error(self, mock_browse_nodes_request):
        mock_browse_nodes_request.side_effect = TypeError()

        with self.assertRaises(MalformedRequest):
            requests.get_browse_nodes_request(Mock())

    def test_get_items_response(self):
        amazon_api = Mock()
        api_result = Mock()
        api_result.items_result.items = "foo"
        amazon_api.api.get_items.return_value = api_result
        response = requests.get_items_response(amazon_api, Mock())

        self.assertEqual("foo", response)

    def test_search_items_response(self):
        amazon_api = Mock()
        api_result = Mock(search_result="foo")
        amazon_api.api.search_items.return_value = api_result
        response = requests.get_search_items_response(amazon_api, Mock())

        self.assertEqual("foo", response)

    def test_get_variations_response(self):
        amazon_api = Mock()
        api_result = Mock(variations_result="foo")
        amazon_api.api.get_variations.return_value = api_result
        response = requests.get_variations_response(amazon_api, Mock())

        self.assertEqual("foo", response)

    def test_get_browse_nodes_response(self):
        amazon_api = Mock()
        api_result = Mock()
        api_result.browse_nodes_result.browse_nodes = "foo"
        amazon_api.api.get_browse_nodes.return_value = api_result
        response = requests.get_browse_nodes_response(amazon_api, Mock())

        self.assertEqual("foo", response)
