from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quotes():
    """
    Test that escaped double quotes within the string are correctly unescaped.
    Replaces the ambiguous single-char test case.
    """
    # Case 1: Internal escaped quote "foo\"bar" -> foo"bar
    header_value = r'"foo\"bar"'
    result = unquote_header_value(header_value)
    assert result == 'foo"bar'

    # Case 2: Escaped quote at the end "quote\"" -> quote"
    # This ensures the parser doesn't mistake the escaped quote for the closing quote.
    header_value_end = r'"quote\""'
    result_end = unquote_header_value(header_value_end)
    assert result_end == 'quote"'