from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_host_path_and_query():
    """
    Test prepending a scheme to a URL string that contains a host, path, and query parameters
    but no scheme.
    """
    url = "www.search-engine.com/search/results?q=python+requests&page=1"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://www.search-engine.com/search/results?q=python+requests&page=1"