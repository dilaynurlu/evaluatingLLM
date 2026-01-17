import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_file_scheme():
    """
    Test select_proxy behavior for URLs without a hostname (e.g. file://).
    
    For a 'file://' URL, the hostname is None. The function should check for the scheme ('file')
    directly in the proxies dictionary.
    """
    url = "file:///etc/hosts"
    proxies = {
        "file": "http://proxy.for.file",
        "all": "http://proxy.generic",
    }
    
    result = select_proxy(url, proxies)
    
    # It should match 'file' scheme preference over 'all'
    assert result == "http://proxy.for.file"