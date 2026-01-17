from requests.utils import select_proxy

def test_select_proxy_https_scheme():
    url = "https://example.com"
    proxies = {"https": "secure_proxy"}
    assert select_proxy(url, proxies) == "secure_proxy"
