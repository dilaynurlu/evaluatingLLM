from requests.utils import select_proxy

def test_select_proxy_all_host_match():
    url = "http://www.google.com/search"
    proxies = {
        "all://www.google.com": "http://proxy.google_all.com",
        "all": "http://proxy.fallback.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.google_all.com", \
        f"Expected 'all://hostname' match. Got: {result}"