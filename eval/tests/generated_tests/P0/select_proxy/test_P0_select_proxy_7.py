from requests.utils import select_proxy

def test_select_proxy_hostname_none_all_match():
    """
    Test scenarios where urlparse yields no hostname (e.g. mailto), 
    and proxies contains only 'all' fallback.
    """
    url = "mailto:user@example.com"
    proxies = {
        "all": "http://all_proxy",
    }
    # Should match 'all' when scheme is missing and hostname is None
    assert select_proxy(url, proxies) == "http://all_proxy"