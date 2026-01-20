from requests.utils import unquote_header_value

def test_unquote_header_escaped_quote():
    assert unquote_header_value('"val\"ue"') == 'val"ue'
