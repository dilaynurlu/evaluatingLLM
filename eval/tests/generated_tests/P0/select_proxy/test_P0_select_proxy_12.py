import pytest
from requests.utils import select_proxy

def test_select_proxy_empty_dict():
    """
    Test that select_proxy returns None when an empty dictionary is passed.
    """
    url = "http://www.example.com"
    proxies = {}
    
    result = select_proxy(url, proxies)
    assert result is None