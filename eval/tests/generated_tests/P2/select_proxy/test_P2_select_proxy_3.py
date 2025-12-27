import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_priority():
    """
    Test that 'all://hostname' takes precedence over the generic 'all' key,
    when scheme specific proxies are missing or do not match.
    
    In this case, the scheme 'ftp' is not present in proxies, so it 
    skips the first two priority checks and should hit 'all://hostname'.
    """
    url = "ftp://files.example.org/pub"
    proxies = {
        "all://files.example.org": "socks5://specific-host.local:1080",
        "all": "socks5://generic.local:1080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "socks5://specific-host.local:1080"