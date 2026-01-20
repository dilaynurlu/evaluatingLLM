from requests.utils import unquote_header_value

def test_unquote_header_none():
    assert unquote_header_value(None) is None
