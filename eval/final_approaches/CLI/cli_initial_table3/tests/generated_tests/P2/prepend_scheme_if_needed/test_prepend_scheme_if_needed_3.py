from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_double_slash():
    """
    Test prepending scheme to URL starting with //.
    """
    url = "//example.com/foo"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == "http://example.com/foo"
