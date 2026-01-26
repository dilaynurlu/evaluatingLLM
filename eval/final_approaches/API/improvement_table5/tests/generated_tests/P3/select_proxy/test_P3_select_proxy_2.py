from requests.utils import select_proxy

def test_select_proxy_scheme_match():
    """
    Test that select_proxy prioritizes the <scheme> match when the exact
    <scheme>://<hostname> key is missing, but before 'all' variants.
    
    Refinement:
    - Uses uppercase scheme in URL (HTTP) to verify case-insensitive scheme lookup.
    """
    url = "HTTP://example.com/resource"
    proxies = {
        "http": "http://10.10.1.2:8080",  # Lowercase key should match 'HTTP' URL
        "all://example.com": "http://10.10.1.3:8080",
        "all": "http://10.10.1.4:8080",
    }
    
    # Expect match on scheme 'http'
    assert select_proxy(url, proxies) == "http://10.10.1.2:8080"