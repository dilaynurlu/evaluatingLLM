from requests.utils import unquote_header_value

def test_unquote_header_value_4():
    # Input: "\\server\share" (quoted)
    # is_filename=True
    # Should NOT unescape backslashes if it starts with \\
    assert unquote_header_value(r'"\\server\share"', is_filename=True) == r'\\server\share'