from requests.utils import select_proxy

def test_select_proxy_no_match():
    """
    Test that None is returned when no keys in the proxies dictionary match the URL.
    """
    url = "http://example.com"
    proxies = {
        "https": "http://secure_proxy",
        "ftp": "http://ftp_proxy"
    }
    assert select_proxy(url, proxies) is None