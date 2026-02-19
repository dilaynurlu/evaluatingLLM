from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslashes():
    """
    Test that escaped backslashes are unescaped in a quoted string.
    Includes checks for trailing escaped backslashes and long strings (DoS prevention).
    """
    # Standard: "foo\\bar" -> "foo\bar"
    header_value = r'"foo\\bar"'
    result = unquote_header_value(header_value)
    assert result == r"foo\bar"

    # Trailing escape: "ending\\" -> "ending\"
    # Input has escaped backslash right before the closing quote.
    header_value_trailing = r'"ending\\"'
    result_trailing = unquote_header_value(header_value_trailing)
    assert result_trailing == r"ending\"

    # Performance/DoS check: Long string with many escapes
    long_header = r'"' + (r'\\' * 5000) + r'"'
    result_long = unquote_header_value(long_header)
    assert result_long == '\\' * 5000