# coding: utf-8

from __future__ import absolute_import

"""
 Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License").
 You may not use this file except in compliance with the License.
 A copy of the License is located at

     http://www.apache.org/licenses/LICENSE-2.0

 or in the "license" file accompanying this file. This file is distributed
 on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied. See the License for the specific language governing
 permissions and limitations under the License.
"""

"""
    ProductAdvertisingAPI

    https://webservices.amazon.com/paapi5/documentation/index.html  # noqa: E501
"""

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ..api_client import ApiClient


class DefaultApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self,
                access_key=None,
                secret_key=None,
                host=None,
                region=None,
                api_client=None):
        if not host:
            host = "webservices.amazon.com"
        if not region:
            region = "us-east-1"
        if api_client is None:
            api_client = ApiClient(access_key = access_key,
                                   secret_key = secret_key,
                                   host = host,
                                   region = region)
        self.api_client = api_client

    def get_browse_nodes(self, get_browse_nodes_request, **kwargs):  # noqa: E501
        """get_browse_nodes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_browse_nodes(get_browse_nodes_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetBrowseNodesRequest get_browse_nodes_request: GetBrowseNodesRequest (required)
        :return: GetBrowseNodesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_browse_nodes_with_http_info(get_browse_nodes_request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_browse_nodes_with_http_info(get_browse_nodes_request, **kwargs)  # noqa: E501
            return data

    def get_browse_nodes_with_http_info(self, get_browse_nodes_request, **kwargs):  # noqa: E501
        """get_browse_nodes  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_browse_nodes_with_http_info(get_browse_nodes_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetBrowseNodesRequest get_browse_nodes_request: GetBrowseNodesRequest (required)
        :return: GetBrowseNodesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['get_browse_nodes_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_browse_nodes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'get_browse_nodes_request' is set
        if ('get_browse_nodes_request' not in params or
                params['get_browse_nodes_request'] is None):
            raise ValueError("Missing the required parameter `get_browse_nodes_request` when calling `get_browse_nodes`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'get_browse_nodes_request' in params:
            body_params = params['get_browse_nodes_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/paapi5/getbrowsenodes', 'POST', 'GetBrowseNodes',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetBrowseNodesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_items(self, get_items_request, **kwargs):  # noqa: E501
        """get_items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_items(get_items_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetItemsRequest get_items_request: GetItemsRequest (required)
        :return: GetItemsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_items_with_http_info(get_items_request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_items_with_http_info(get_items_request, **kwargs)  # noqa: E501
            return data

    def get_items_with_http_info(self, get_items_request, **kwargs):  # noqa: E501
        """get_items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_items_with_http_info(get_items_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetItemsRequest get_items_request: GetItemsRequest (required)
        :return: GetItemsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['get_items_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_items" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'get_items_request' is set
        if ('get_items_request' not in params or
                params['get_items_request'] is None):
            raise ValueError("Missing the required parameter `get_items_request` when calling `get_items`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'get_items_request' in params:
            body_params = params['get_items_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/paapi5/getitems', 'POST', 'GetItems',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetItemsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_variations(self, get_variations_request, **kwargs):  # noqa: E501
        """get_variations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_variations(get_variations_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetVariationsRequest get_variations_request: GetVariationsRequest (required)
        :return: GetVariationsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_variations_with_http_info(get_variations_request, **kwargs)  # noqa: E501
        else:
            (data) = self.get_variations_with_http_info(get_variations_request, **kwargs)  # noqa: E501
            return data

    def get_variations_with_http_info(self, get_variations_request, **kwargs):  # noqa: E501
        """get_variations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_variations_with_http_info(get_variations_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetVariationsRequest get_variations_request: GetVariationsRequest (required)
        :return: GetVariationsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['get_variations_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_variations" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'get_variations_request' is set
        if ('get_variations_request' not in params or
                params['get_variations_request'] is None):
            raise ValueError("Missing the required parameter `get_variations_request` when calling `get_variations`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'get_variations_request' in params:
            body_params = params['get_variations_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/paapi5/getvariations', 'POST', 'GetVariations',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetVariationsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def search_items(self, search_items_request, **kwargs):  # noqa: E501
        """search_items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_items(search_items_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SearchItemsRequest search_items_request: SearchItemsRequest (required)
        :return: SearchItemsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.search_items_with_http_info(search_items_request, **kwargs)  # noqa: E501
        else:
            (data) = self.search_items_with_http_info(search_items_request, **kwargs)  # noqa: E501
            return data

    def search_items_with_http_info(self, search_items_request, **kwargs):  # noqa: E501
        """search_items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_items_with_http_info(search_items_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SearchItemsRequest search_items_request: SearchItemsRequest (required)
        :return: SearchItemsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['search_items_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_items" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'search_items_request' is set
        if ('search_items_request' not in params or
                params['search_items_request'] is None):
            raise ValueError("Missing the required parameter `search_items_request` when calling `search_items`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'search_items_request' in params:
            body_params = params['search_items_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/paapi5/searchitems', 'POST', 'SearchItems',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SearchItemsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)