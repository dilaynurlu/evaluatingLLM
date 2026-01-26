from requests.utils import select_proxy

def test_select_proxy_no_host_scheme_match():
    """
    Test select_proxy behavior for URLs with no hostname (e.g. file://).
    It should look up the proxy by scheme directly.
    
    Refinement:
    - Uses a benign file path instead of '/etc/passwd' to avoid security antipatterns
      in test data.
    """
    url = "file:///tmp/safe_test_file"
    proxies = {
        "file": "http://proxy-file-server",
        "all": "http://proxy-fallback"
    }
    
    # urlparse('file:///...') has None hostname.
    # Logic should use proxies.get('file')
    assert select_proxy(url, proxies) == "http://proxy-file-server"