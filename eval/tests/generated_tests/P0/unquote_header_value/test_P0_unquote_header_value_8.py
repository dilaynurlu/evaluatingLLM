from requests.utils import unquote_header_value

def test_unquote_header_value_single_quotes():
    """
    Test that strings wrapped in single quotes are NOT unquoted by this function,
    as it specifically targets double quotes used in HTTP headers.
    """
    header = "'value'"
    expected = "'value'"
    result = unquote_header_value(header)
    assert result == expected