from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_2():
    # Has scheme
    url = "https://example.com/path"
    new = prepend_scheme_if_needed(url, "http")
    assert new == "https://example.com/path"