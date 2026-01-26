from requests.utils import select_proxy

def test_select_proxy_all_fallback():
    url = "ftp://ftp.example.com/file"
    proxies = {
        "http": "http://proxy.http.com",
        "all": "http://proxy.global.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.global.com", \
        f"Expected fallback to 'all' proxy when scheme does not match. Got: {result}"