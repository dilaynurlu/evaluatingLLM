from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_4():
    # Ensure scheme is not replaced even if new_scheme is different
    url = "ftp://example.com/file"
    new = prepend_scheme_if_needed(url, "http")
    assert new == "ftp://example.com/file"
