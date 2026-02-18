from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_4():
    # Test with authentication but no scheme
    # We use // to ensure urlparse treats it as netloc-relative, not scheme 'user'
    url = "//user:pass@example.com/path"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://user:pass@example.com/path"
