from requests.utils import unquote_header_value

def test_unquote_header_simple():
    assert unquote_header_value('"value"') == "value"
