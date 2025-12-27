from requests.utils import unquote_header_value

def test_unquote_header_value_empty_string():
    """
    Test that an empty string is returned as-is (handling None or empty logic safely).
    """
    # Note: The function implementation checks `if value and ...`
    # so an empty string (falsy) returns immediately.
    header = ""
    expected = ""
    result = unquote_header_value(header)
    assert result == expected