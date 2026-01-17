from requests.utils import unquote_header_value

def test_unquote_header_empty():
    assert unquote_header_value("") == ""
    assert unquote_header_value('""') == ""
