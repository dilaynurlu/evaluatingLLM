from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_6():
    # Test URL starting with whitespace
    # urlparse might handle this, or it might be treated as part of path?
    url = " example.com/foo"
    new = prepend_scheme_if_needed(url, "http")
    # ' example.com/foo' has no scheme.
    # prepend http -> 'http:// example.com/foo' ?
    # Let's see behavior.
    assert new == "http:// example.com/foo"
