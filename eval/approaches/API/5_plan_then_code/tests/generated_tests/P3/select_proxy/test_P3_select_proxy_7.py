import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_precedence():
    """
    Test that for URLs without a hostname, the scheme-specific proxy
    takes precedence over 'all'.
    
    Refinement: Uses mixed-case scheme in URL to verify case insensitivity.
    """
    url = "FILE:///etc/hosts"
    proxies = {
        "file": "specific_file_proxy",
        "all": "global_proxy"
    }
    
    assert select_proxy(url, proxies) == "specific_file_proxy"