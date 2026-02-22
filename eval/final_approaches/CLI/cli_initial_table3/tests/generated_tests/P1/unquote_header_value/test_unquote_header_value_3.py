from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_chars():
    """Test unquoting of escaped characters."""
    # Input has quotes around it. Inside, \" should become " and \\ should become \
    # Raw string r'"test \"quoted\" \\ backslash"' means the string contains:
    # "test \"quoted\" \\ backslash"
    # Expected result: test "quoted" \ backslash
    assert unquote_header_value(r'"test \"quoted\" \\ backslash"') == r'test "quoted" \ backslash'
