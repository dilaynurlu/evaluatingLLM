import pytest
from requests.utils import select_proxy

def test_select_proxy_3():
    proxies = {
        "all": "http://allproxy.com",
        "all://example.com": "http://specific.com"
    }
    url = "http://example.com"
    # Specific host match should win over generic "all"
    assert select_proxy(url, proxies) == "http://specific.com"
    
    url2 = "http://other.com"
    assert select_proxy(url2, proxies) == "http://allproxy.com"
