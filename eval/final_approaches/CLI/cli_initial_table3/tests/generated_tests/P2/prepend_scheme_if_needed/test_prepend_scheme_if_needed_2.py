from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_without_scheme():
    """
    Test that scheme is prepended if missing.
    """
    url = "example.com/foo"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == "http://example.com/foo"
