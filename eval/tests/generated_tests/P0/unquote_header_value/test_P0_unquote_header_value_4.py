from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """
    Test that escaped backslashes within the string are correctly unescaped.
    """
    # Input represents: "foo\\bar"
    # Expected represents: foo\bar
    header = r'"foo\\bar"'
    expected = r'foo\bar'
    result = unquote_header_value(header)
    assert result == expected