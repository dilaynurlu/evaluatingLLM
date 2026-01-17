from requests.utils import select_proxy

def test_select_proxy_all_host_match():
    """
    Test that select_proxy matches 'all://hostname' when specific scheme matches are missing.
    """
    proxies = {
        "all://example.com": "http://proxy.specific.com",
        "all": "http://proxy.generic.com"
    }
    url = "ftp://example.com/resource"
    
    # Expect the all://hostname match
    assert select_proxy(url, proxies) == "http://proxy.specific.com"