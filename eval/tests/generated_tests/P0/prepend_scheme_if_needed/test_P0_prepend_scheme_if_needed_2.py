from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing():
    """
    Test that an existing scheme in the URL is preserved and not overwritten
    by the new_scheme argument.
    """
    url = "https://example.com"
    new_scheme = "http"
    expected = "https://example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected