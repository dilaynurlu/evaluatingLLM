from requests.utils import select_proxy

def test_select_proxy_5():
    # No hostname (e.g. file://) -> should fallback to scheme or all
    proxies = {"file": "http://fileproxy", "all": "http://allproxy"}
    url = "file:///etc/hosts"
    assert select_proxy(url, proxies) == "http://fileproxy"
