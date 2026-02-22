from requests.utils import unquote_header_value

def test_unquote_header_value_1():
    assert unquote_header_value('"foo"') == 'foo'
