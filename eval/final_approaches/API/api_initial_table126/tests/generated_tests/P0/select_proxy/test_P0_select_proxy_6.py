from requests.utils import select_proxy

def test_select_proxy_hostname_none_scheme_match():
    """
    Test scenarios where urlparse yields no hostname (e.g. mailto), 
    and proxies contains the scheme key.
    """
    url = "mailto:user@example.com"
    # urlparse("mailto:...") typically results in hostname being None
    proxies = {
        "mailto": "http://mail_proxy",
        "all": "http://all_proxy",
    }
    # Should match scheme 'mailto' directly when hostname is None
    assert select_proxy(url, proxies) == "http://mail_proxy"