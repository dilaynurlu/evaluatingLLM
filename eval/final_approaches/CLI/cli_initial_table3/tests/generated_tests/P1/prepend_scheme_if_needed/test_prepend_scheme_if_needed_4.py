from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative():
    # //example.com -> http://example.com ?
    # Let's check what `parse_url('//example.com')` does.
    # It probably sees 'http' as scheme if none? No.
    # If url is '//example.com', scheme is None.
    # So it should become 'http://example.com'.
    
    url = "//example.com"
    new_scheme = "http"
    expected = "http://example.com"
    assert prepend_scheme_if_needed(url, new_scheme) == expected
    
    # //example.com/foo
    url2 = "//example.com/foo"
    expected2 = "http://example.com/foo"
    assert prepend_scheme_if_needed(url2, new_scheme) == expected2
