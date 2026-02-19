from requests.utils import select_proxy

def test_select_proxy_all_match():
    """
    Test that select_proxy falls back to the 'all' key when no other specific
    keys (scheme or host based) are present in the proxies dictionary.
    """
    url = "https://example.com/resource"
    proxies = {
        "all": "http://10.10.1.4:8080",
        "other": "http://10.10.1.9:8080"
    }
    
    # Expect fallback to 'all'
    assert select_proxy(url, proxies) == "http://10.10.1.4:8080"