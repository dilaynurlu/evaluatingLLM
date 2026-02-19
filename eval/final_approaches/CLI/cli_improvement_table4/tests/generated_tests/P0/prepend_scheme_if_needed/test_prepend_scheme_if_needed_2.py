from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_2():
    url = "https://example.com/path"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "https://example.com/path"
