from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_host():
    """
    Test prepending a scheme to a simple hostname.
    """
    url = "example.com"
    new_scheme = "http"
    expected = "http://example.com"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected