from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_3():
    # Test with different scheme existing
    url = "ftp://example.com/file"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "ftp://example.com/file"
