import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_host_port():
    """
    Test prepending scheme to a host:port string.
    urllib3's parser typically handles 'host:port' correctly (identifying port)
    and leaves scheme as None. The function should prepend the scheme.
    """
    url = "localhost:8080"
    new_scheme = "http"
    
    expected = "http://localhost:8080"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected