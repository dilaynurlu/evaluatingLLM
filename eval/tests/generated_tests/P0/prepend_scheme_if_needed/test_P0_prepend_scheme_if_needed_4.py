from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_path_query_fragment():
    """
    Test prepending a scheme to a complex schemeless URL containing path, query, and fragment.
    """
    url = "example.com/path/to/resource?query=1#fragment"
    new_scheme = "http"
    expected = "http://example.com/path/to/resource?query=1#fragment"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected