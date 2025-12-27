import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_host_match():
    """
    Refined test for 'all host match' covering IPv6 literals.
    Ensures that URLs containing IPv6 addresses (with brackets) are correctly 
    parsed and matched against their corresponding proxy keys.
    """
    # URL using an IPv6 literal
    url = "http://[::1]:8080/some/path"
    
    proxies = {
        # Specific match for the IPv6 host
        "all://[::1]": "http://proxy.ipv6-specific:8080",
        "all": "http://proxy.fallback:8080",
        "https": "http://proxy.other:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.ipv6-specific:8080"


'''
Asertion failed:

 result = select_proxy(url, proxies)
>       assert result == "http://proxy.ipv6-specific:8080"
E       AssertionError: assert 'http://proxy.fallback:8080' == 'http://proxy...specific:8080'
E         
E         - http://proxy.ipv6-specific:8080
E         + http://proxy.fallback:8080

eval/tests/generated_tests/P3/select_proxy/test_P3_select_proxy_3.py:21: AssertionError

'''