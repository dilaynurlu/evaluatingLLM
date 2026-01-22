from requests.utils import select_proxy

def test_select_proxy_url_with_auth():
    # URL containing username and password
    url = "http://user:pass@example.com/resource"
    proxies = {
        "http://example.com": "http://proxy.auth.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.auth.com", \
        f"Expected credentials to be stripped from URL before proxy lookup. Got: {result}"