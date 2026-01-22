from requests.utils import unquote_header_value

def test_unquote_header_value_1():
    # Quoted
    val = '"foo"'
    assert unquote_header_value(val) == "foo"