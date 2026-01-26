from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    # urlparse("http:foo") -> scheme='http', path='foo', hostname=None
    url = "http:foo"
    proxies = {"http": "p1", "all": "p2"}
    assert select_proxy(url, proxies) == "p1"
    
    proxies = {"all": "p2"}
    assert select_proxy(url, proxies) == "p2"
