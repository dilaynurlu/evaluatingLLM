from requests.utils import select_proxy

def test_select_proxy_2():
    url = "http://example.com"
    proxies = {
        "http": "http://generic.com",
        "http://example.com": "http://specific.com"
    }
    assert select_proxy(url, proxies) == "http://specific.com"
