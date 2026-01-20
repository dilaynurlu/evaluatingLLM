import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    proxies = {"file": "http://proxy"}
    url = "file:///etc/hosts"
    # urlparse("file:///etc/hosts").hostname is None (usually, or empty)
    # logic: if hostname is None: return proxies.get(scheme, proxies.get('all'))
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy"
