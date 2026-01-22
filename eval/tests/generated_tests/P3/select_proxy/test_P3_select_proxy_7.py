from requests.utils import select_proxy

def test_select_proxy_no_hostname_all():
    url = "file:///etc/passwd"
    proxies = {
        "http": "http://proxy.http.com",
        "all": "http://proxy.global.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.global.com", \
        f"Expected fallback to 'all' when hostname is missing and scheme doesn't match. Got: {result}"