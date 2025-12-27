from requests.utils import unquote_header_value

def test_unquote_header_value_basic():
    """
    Test that a simple string wrapped in double quotes is correctly unquoted.
    """
    header = '"simple_value"'
    expected = "simple_value"
    result = unquote_header_value(header)
    assert result == expected