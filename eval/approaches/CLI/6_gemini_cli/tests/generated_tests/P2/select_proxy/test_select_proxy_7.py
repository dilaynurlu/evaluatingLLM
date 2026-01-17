import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_case_insensitive():
    proxies = {"http": "http://proxy"}
    url = "HTTP://example.com"
    # urlparse likely lowercases scheme? Yes.
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy"
