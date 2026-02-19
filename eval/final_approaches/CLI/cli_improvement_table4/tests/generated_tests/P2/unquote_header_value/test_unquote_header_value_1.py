from requests.utils import unquote_header_value

def test_unquote_header_value_simple():
    value = '"foo"'
    assert unquote_header_value(value) == "foo"
