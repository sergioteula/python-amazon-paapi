from amazon_paapi.exceptions import AsinNotFoundException
from amazon_paapi.tools import get_asin
import pytest


def test_get_asin():
    assert get_asin('B01N5IB20Q') == 'B01N5IB20Q'
    assert get_asin('https://www.amazon.es/gp/product/B07PHPXHQS') == 'B07PHPXHQS'
    assert get_asin('https://www.amazon.es/gp/product/B07PHPXHQS?pf_rd_r=3FXDZDV1W6KY83KEE2Z4&pf_rd_p=c6fa5af0-ec7c-40de-8332-fd1421de4244&pd_rd_r=58786171-de0f-4fe1-a2df-ee335d6715ee&pd_rd_w=KND7A&pd_rd_wg=kIr5z&ref_=pd_gw_unk') == 'B07PHPXHQS'
    assert get_asin('https://www.amazon.es/dp/B07PKW4CKF') == 'B07PKW4CKF'
    assert get_asin('https://www.amazon.es/dp/B07PKW4CKF?_encoding=UTF8&ref_=pocs_dp_m_sp_multi_c_more_nooffers_B08D1G2XVX') == 'B07PKW4CKF'

    with pytest.raises(AsinNotFoundException):
        get_asin('https://www.amazon.es/gp/')
    with pytest.raises(AsinNotFoundException):
        get_asin('this is not even a URL')
