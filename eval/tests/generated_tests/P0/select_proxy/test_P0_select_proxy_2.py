import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_scheme_host_match():
    """
    Test selecting a proxy defined specifically for 'scheme://hostname'.
    This corresponds to the first key checked in the priority list.
    """
    url = "http://www.example.com/resource"
    proxies = {
        "http://www.example.com": "http://specific-proxy.com:8080",
        "http": "http://general-proxy.com:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://specific-proxy.com:8080"