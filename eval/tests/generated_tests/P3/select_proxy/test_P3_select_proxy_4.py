import pytest
from requests.utils import select_proxy

def test_select_proxy_idn_fallback():
    """
    Refined test for 'all fallback match' covering International Domain Names (IDN).
    Ensures that URLs with non-ASCII characters do not cause errors and 
    correctly fall back to 'all' if no specific IDN key is found.
    """
    # URL with IDN characters (bücher.com)
    url = "http://\u0062\u00fc\u0063\u0068\u0065\u0072.com/path"
    
    proxies = {
        "all": "http://proxy.fallback:8080",
        "ftp": "http://proxy.ftp:8080"
    }
    
    # Should handle encoding/decoding safely and use the fallback
    result = select_proxy(url, proxies)
    assert result == "http://proxy.fallback:8080"