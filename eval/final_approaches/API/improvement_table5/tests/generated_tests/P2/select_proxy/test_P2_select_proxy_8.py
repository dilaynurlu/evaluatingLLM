import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all():
    """
    Test the lowest priority match: all.
    It should be used when no other keys match.
    """
    url = "http://example.com/resource"
    proxies = {
        "all": "http://all.proxy",
        "https": "http://secure.proxy"  # Irrelevant scheme
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://all.proxy"