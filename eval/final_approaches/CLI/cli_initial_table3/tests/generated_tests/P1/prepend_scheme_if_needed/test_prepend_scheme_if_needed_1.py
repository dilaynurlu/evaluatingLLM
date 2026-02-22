from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic():
    url = "example.com"
    new_scheme = "http"
    expected = "http://example.com"
    assert prepend_scheme_if_needed(url, new_scheme) == expected
    
    url2 = "example.com/foo"
    expected2 = "http://example.com/foo"
    assert prepend_scheme_if_needed(url2, new_scheme) == expected2
