import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    proxies = {
        "file": "http://file.proxy",
        "all": "http://fallback.proxy"
    }
    url = "file:///etc/passwd" # hostname is None for file://
    proxy = select_proxy(url, proxies)
    # logic: proxies.get(scheme, proxies.get("all"))
    assert proxy == "http://file.proxy"
