from requests.utils import unquote_header_value

def test_unquote_header_value_unquoted():
    value = "foo"
    assert unquote_header_value(value) == "foo"
