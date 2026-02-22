from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_scheme():
    """
    Test that scheme is not prepended if already present.
    """
    url = "https://example.com/foo"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == url
