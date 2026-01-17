from requests.utils import unquote_header_value

def test_unquote_header_value_partial_quotes():
    # Test that mismatched or partial quotes are not stripped
    value = '"start_only'
    assert unquote_header_value(value) == value