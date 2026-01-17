from requests.utils import select_proxy

def test_select_proxy_url_case_normalization():
    """
    Test that select_proxy normalizes the URL hostname to lowercase before lookup.
    """
    proxies = {
        "http://example.com": "http://proxy.match"
    }
    # URL has uppercase hostname
    url = "http://EXAMPLE.COM/path"
    
    # urlparse lowercases the hostname, so the key generated is "http://example.com", which matches.
    assert select_proxy(url, proxies) == "http://proxy.match"