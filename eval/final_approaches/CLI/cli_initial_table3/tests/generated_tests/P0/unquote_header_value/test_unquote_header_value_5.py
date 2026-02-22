from requests.utils import unquote_header_value

def test_unquote_header_value_5():
    # Input: "\\server\share" (quoted)
    # is_filename=False
    # Should unescape backslashes: \\ -> \
    assert unquote_header_value(r'"\\server\\share"', is_filename=False) == r'\server\share'