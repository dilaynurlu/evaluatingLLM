from requests.utils import unquote_header_value

def test_unquote_header_value_quoted():
    """
    Test unquoting a quoted value.
    """
    value = '"foo"'
    result = unquote_header_value(value)
    assert result == "foo"
