from requests.utils import unquote_header_value

def test_unquote_header_value_basic_stripping():
    """
    Test that a simple quoted string has its surrounding quotes stripped correctly.
    """
    value = '"simple-value"'
    result = unquote_header_value(value)
    assert result == 'simple-value'