from requests.utils import select_proxy

def test_select_proxy_input_none():
    url = "http://example.com"
    assert select_proxy(url, None) is None
