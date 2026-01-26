from requests.utils import select_proxy

def test_select_proxy_all_scheme_host_match():
    """
    Test that select_proxy prioritizes 'all://<hostname>' when specific scheme
    keys are missing, but before the generic 'all' key.
    """
    url = "ftp://example.com/resource"
    proxies = {
        "all://example.com": "http://10.10.1.3:8080",
        "all": "http://10.10.1.4:8080",
    }
    
    # Expect match on 'all://example.com'
    assert select_proxy(url, proxies) == "http://10.10.1.3:8080"