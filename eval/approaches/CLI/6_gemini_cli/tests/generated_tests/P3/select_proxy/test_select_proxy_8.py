from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    url = "file:///tmp/test"
    proxies = {"all": "proxy"}
    # If hostname is None, uses scheme or all.
    # scheme is file.
    assert select_proxy(url, proxies) == "proxy"
