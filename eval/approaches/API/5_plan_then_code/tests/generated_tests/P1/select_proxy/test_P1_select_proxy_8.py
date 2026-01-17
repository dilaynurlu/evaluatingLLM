from requests.utils import select_proxy

def test_select_proxy_no_hostname_all_match():
    """
    Test proxy selection for URLs without a hostname when the scheme is not in proxies.
    It should fallback to the "all" key.
    """
    proxies = {
        "all": "http://fallback.proxy"
    }
    url = "custom-scheme:opaque-data"
    
    # urlparse("custom-scheme:...") results in hostname=None.
    # scheme "custom-scheme" is not in proxies, so it should return proxies.get("all").
    assert select_proxy(url, proxies) == "http://fallback.proxy"