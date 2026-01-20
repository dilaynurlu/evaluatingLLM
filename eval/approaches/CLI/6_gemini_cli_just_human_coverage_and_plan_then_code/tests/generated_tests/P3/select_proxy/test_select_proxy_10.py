from requests.utils import select_proxy

def test_select_proxy_mixed_case_url():
    # URL scheme/host are normalized by urlparse usually.
    url = "HTTP://Example.COM"
    proxies = {"http": "proxy"}
    assert select_proxy(url, proxies) == "proxy"
