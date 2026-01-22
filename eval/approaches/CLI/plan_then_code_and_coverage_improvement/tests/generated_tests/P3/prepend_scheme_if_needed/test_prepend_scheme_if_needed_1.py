from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_1():
    # No scheme
    url = "example.com/path"
    new = prepend_scheme_if_needed(url, "http")
    assert new == "http://example.com/path"