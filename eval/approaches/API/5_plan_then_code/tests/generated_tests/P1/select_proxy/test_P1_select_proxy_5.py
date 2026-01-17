from requests.utils import select_proxy

def test_select_proxy_all_generic_match():
    """
    Test that select_proxy matches 'all' when no other specific keys match.
    """
    proxies = {
        "all": "socks5://proxy.global"
    }
    url = "https://random-site.com/resource"
    
    # Expect the generic 'all' match
    assert select_proxy(url, proxies) == "socks5://proxy.global"