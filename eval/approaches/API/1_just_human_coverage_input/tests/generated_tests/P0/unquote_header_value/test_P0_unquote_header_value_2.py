from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quote():
    # Test that escaped quotes are correctly unescaped
    # Input represents: "foo\"bar" -> content inside is foo"bar
    value = r'"foo\"bar"'
    expected = 'foo"bar'
    assert unquote_header_value(value) == expected