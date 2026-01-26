from requests.utils import select_proxy

def test_select_proxy_no_match():
    # Scenario: Verify that None is returned if the proxy dictionary is non-empty 
    # but contains no matching keys for the URL.
    url = "http://example.com"
    proxies = {
        "https": "https://secure-proxy",
        "ftp": "ftp://ftp-proxy"
    }
    result = select_proxy(url, proxies)
    assert result is None