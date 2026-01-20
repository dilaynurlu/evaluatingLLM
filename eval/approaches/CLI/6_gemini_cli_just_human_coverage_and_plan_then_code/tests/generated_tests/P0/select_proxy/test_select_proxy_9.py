
import pytest
from requests.utils import select_proxy

def test_select_proxy_empty_url():
    url = ""
    proxies = {"all": "http://proxy.com"}
    # urlparse("") -> scheme='' hostname=None
    # proxies.get('') -> None, proxies.get('all') -> proxy.com
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
