from requests.utils import unquote_header_value

def test_unquote_header_value_empty():
    assert unquote_header_value(None) is None
    assert unquote_header_value("") == ""
