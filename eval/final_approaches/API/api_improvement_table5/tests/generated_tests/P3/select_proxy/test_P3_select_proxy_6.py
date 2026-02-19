from requests.utils import select_proxy

def test_select_proxy_no_host_all_match():
    """
    Test select_proxy behavior for URLs with no hostname when the specific scheme
    is missing from proxies. It should fall back to 'all'.
    
    Refinement:
    - Uses a benign file path instead of '/etc/passwd' to avoid security antipatterns
      in test data.
    """
    url = "file:///tmp/safe_test_file"
    proxies = {
        "http": "http://proxy-http",
        "all": "http://proxy-fallback"
    }
    
    # Scheme is 'file', which is missing. Fallback to 'all'.
    assert select_proxy(url, proxies) == "http://proxy-fallback"