
import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_order():
    # Order: scheme://host, scheme, all://host, all
    url = "http://example.com"
    proxies = {
        "all": "http://proxy4.com",
        "all://example.com": "http://proxy3.com",
        "http": "http://proxy2.com",
        "http://example.com": "http://proxy1.com"
    }
    assert select_proxy(url, proxies) == "http://proxy1.com"
    
    del proxies["http://example.com"]
    assert select_proxy(url, proxies) == "http://proxy2.com"
    
    del proxies["http"]
    assert select_proxy(url, proxies) == "http://proxy3.com"
    
    del proxies["all://example.com"]
    assert select_proxy(url, proxies) == "http://proxy4.com"
