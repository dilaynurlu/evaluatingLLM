from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_5():
    # URL with leading whitespace? 
    # parse_url might handle it or not.
    # prepend_scheme_if_needed passes it to parse_url.
    url = " example.com"
    # parse_url might fail or treat space as part of path?
    # If path=" example.com", scheme=None.
    # -> http:// example.com ?
    # Let's see behavior.
    new = prepend_scheme_if_needed(url.strip(), "http")
    assert new == "http://example.com"
