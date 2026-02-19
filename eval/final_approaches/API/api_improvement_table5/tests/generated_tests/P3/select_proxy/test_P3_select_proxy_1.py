from requests.utils import select_proxy

def test_select_proxy_exact_match():
    """
    Test that select_proxy prioritizes the exact <scheme>://<hostname> match
    over other less specific keys.
    
    Refinement:
    - Includes authentication credentials and specific port in URL to verify
      that select_proxy correctly extracts the hostname for the key lookup.
    - Uses mixed-case hostname to ensure case-insensitive matching.
    """
    # URL contains user:pass, mixed-case host, and explicit port.
    # The proxy lookup should normalize this to scheme='http', host='example.com'
    url = "http://user:pass@Example.com:8080/resource"
    
    proxies = {
        "http://example.com": "http://10.10.1.1:8080",  # Exact match (normalized)
        "http": "http://10.10.1.2:8080",
        "all://example.com": "http://10.10.1.3:8080",
        "all": "http://10.10.1.4:8080",
    }
    
    # Expect the most specific match: scheme + hostname, ignoring auth/port
    assert select_proxy(url, proxies) == "http://10.10.1.1:8080"