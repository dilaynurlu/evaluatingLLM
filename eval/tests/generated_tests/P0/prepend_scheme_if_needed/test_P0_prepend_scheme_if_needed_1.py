from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_no_scheme():
    """
    Test that a new scheme is successfully prepended to a URL that lacks one.
    """
    url = "google.com"
    new_scheme = "http"
    expected = "http://google.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected