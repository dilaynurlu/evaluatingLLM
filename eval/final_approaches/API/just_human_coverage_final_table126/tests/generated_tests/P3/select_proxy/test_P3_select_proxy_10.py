from requests.utils import select_proxy

def test_select_proxy_mismatch_scheme():
    url = "http://example.com"
    proxies = {
        "https": "http://proxy.secure.com",
        "ftp": "http://proxy.ftp.com"
    }
    
    result = select_proxy(url, proxies)
    assert result is None, \
        f"Expected None when no proxy key matches the URL scheme or host. Got: {result}"