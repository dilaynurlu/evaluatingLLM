from requests.utils import unquote_header_value

def test_unquote_single_quotes():
    """Test that single quotes are not treated as quote delimiters by this function."""
    input_val = "'single_quoted'"
    # The function only checks for value[0] == value[-1] == '"'
    assert unquote_header_value(input_val) == "'single_quoted'"