import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_case_and_port_handling():
    """
    Refined test for 'exact host match' covering:
    1. Precedence: 'scheme://host' > 'scheme' > 'all://host' > 'all'.
    2. Case Sensitivity: Ensures keys match even if URL has mixed case.
    3. Port Handling: Ensures host key matches URL even if URL specifies a port.
    """
    # URL has mixed case scheme/host and a specific port
    url = "HTTP://Example.COM:1234/some/path"
    
    # Keys are standard lowercase
    proxies = {
        "http://example.com": "http://proxy.specific-host:8080",
        "http": "http://proxy.general-scheme:8080",
        "all://example.com": "http://proxy.all-scheme-host:8080",
        "all": "http://proxy.fallback:8080",
    }
    
    # The selector should normalize the URL's scheme/host and ignore the port 
    # for the key lookup (or handle it gracefully), matching the specific host key.
    result = select_proxy(url, proxies)
    assert result == "http://proxy.specific-host:8080"