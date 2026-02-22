from requests.utils import unquote_header_value

def test_unquote_header_value_escaped():
    """
    Test unquoting a value with escaped characters.
    """
    value = r'"foo\\bar\"baz"'
    result = unquote_header_value(value)
    
    # "foo\\bar\"baz" -> foo\bar"baz
    assert result == 'foo\\bar"baz'

