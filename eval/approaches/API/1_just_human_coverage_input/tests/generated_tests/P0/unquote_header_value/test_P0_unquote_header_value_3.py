from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    # Test that double backslashes are unescaped to single backslashes
    # Input represents: "foo\\bar" -> content inside is foo\bar
    value = r'"foo\\bar"'
    expected = r'foo\bar'
    assert unquote_header_value(value) == expected