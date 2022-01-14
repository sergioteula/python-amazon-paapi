import unittest

from amazon_paapi.errors import AsinNotFoundException
from amazon_paapi.tools import get_asin


class TestTools(unittest.TestCase):
    def test_get_asin(self):
        self.assertEqual(get_asin("B01N5IB20Q"), "B01N5IB20Q")
        self.assertEqual(
            get_asin("https://www.amazon.es/gp/product/B07PHPXHQS"), "B07PHPXHQS"
        )
        self.assertEqual(
            get_asin(
                "https://www.amazon.es/gp/product/B07PHPXHQS?pf_rd_r3FXDZDV1W6KY83KEE2Z"
                "4&pf_rd_p=c6fa5af0-ec7c-40de-8332-fd1421de4244&pd_rd_r=58786171-de0f-4"
                "fe1-a2df-ee335d6715ee&pd_rd_w=KND7A&pd_rd_wg=kIr5z&ref_=pd_gw_unk"
            ),
            "B07PHPXHQS",
        )
        self.assertEqual(get_asin("https://www.amazon.es/dp/B07PKW4CKF"), "B07PKW4CKF")
        self.assertEqual(
            get_asin(
                "https://www.amazon.es/dp/B07PKW4CKF?_encoding=UTF8&ref_=pocs_dp_m_sp_m"
                "ulti_c_more_nooffers_B08D1G2XVX"
            ),
            "B07PKW4CKF",
        )

    def test_asin_not_found(self):
        with self.assertRaises(AsinNotFoundException):
            get_asin("https://www.amazon.es/gp/")

        with self.assertRaises(AsinNotFoundException):
            get_asin("this is not even a URL")
