from requests.utils import select_proxy

def test_select_proxy_8():
    # Test URL with no hostname (e.g. file://)
    url = "file:///etc/hosts"
    proxies = {"file": "p1", "all": "p2"}
    # Code: if urlparts.hostname is None: return proxies.get(urlparts.scheme, proxies.get("all"))
    assert select_proxy(url, proxies) == "p1"
