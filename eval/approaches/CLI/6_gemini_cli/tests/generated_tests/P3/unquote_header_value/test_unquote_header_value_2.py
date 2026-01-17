from requests.utils import unquote_header_value

def test_unquote_header_no_quotes():
    assert unquote_header_value("value") == "value"
