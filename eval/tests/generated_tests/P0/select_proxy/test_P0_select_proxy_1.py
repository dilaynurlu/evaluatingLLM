import pytest
from requests.utils import select_proxy

def test_select_proxy_none_argument():
    """
    Test that select_proxy returns None when the proxies argument is explicitly None.
    The function should handle None by defaulting to an empty dict internally.
    """
    url = "http://www.example.com"
    # Passing None as proxies
    result = select_proxy(url, None)
    assert result is None