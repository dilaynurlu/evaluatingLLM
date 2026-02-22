from requests.utils import select_proxy

def test_select_proxy_5():
    # mailto:user@example.com -> scheme=mailto, path=user@example.com, hostname=None
    url = "mailto:user@example.com"
    proxies = {"mailto": "http://mail.proxy"}
    assert select_proxy(url, proxies) == "http://mail.proxy"
