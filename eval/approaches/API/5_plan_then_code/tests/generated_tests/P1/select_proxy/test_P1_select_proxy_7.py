from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test proxy selection for URLs without a hostname (e.g. mailto:).
    It should attempt to look up the scheme in the proxies dictionary.
    """
    proxies = {
        "mailto": "http://mail.proxy.server"
    }
    url = "mailto:user@example.com"
    
    # urlparse("mailto:...") results in hostname=None. 
    # select_proxy should return proxies.get(scheme).
    assert select_proxy(url, proxies) == "http://mail.proxy.server"