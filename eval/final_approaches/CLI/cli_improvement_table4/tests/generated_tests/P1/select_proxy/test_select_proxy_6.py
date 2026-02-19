import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    """Test selecting proxy for URL without hostname."""
    url = "file:///etc/hosts"
    proxies = {
        "file": "file_proxy",
        "all": "all_proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "file_proxy"
