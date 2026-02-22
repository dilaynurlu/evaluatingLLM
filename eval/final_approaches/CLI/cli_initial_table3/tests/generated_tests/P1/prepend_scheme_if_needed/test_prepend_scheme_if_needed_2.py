from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_existing():
    url = "https://example.com"
    new_scheme = "http"
    expected = "https://example.com"
    assert prepend_scheme_if_needed(url, new_scheme) == expected
    
    url2 = "ftp://example.com"
    new_scheme2 = "http"
    expected2 = "ftp://example.com"
    assert prepend_scheme_if_needed(url2, new_scheme2) == expected2
