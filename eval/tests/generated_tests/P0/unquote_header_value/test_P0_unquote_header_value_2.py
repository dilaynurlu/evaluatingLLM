from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """
    Test that a string without surrounding double quotes is returned unchanged.
    """
    header = 'simple_value'
    expected = 'simple_value'
    result = unquote_header_value(header)
    assert result == expected