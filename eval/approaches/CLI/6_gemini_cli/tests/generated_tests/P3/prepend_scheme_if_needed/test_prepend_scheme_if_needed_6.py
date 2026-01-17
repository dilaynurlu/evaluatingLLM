from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_path():
    url = "example.com/foo/bar"
    new_scheme = "http"
    assert prepend_scheme_if_needed(url, new_scheme) == "http://example.com/foo/bar"
