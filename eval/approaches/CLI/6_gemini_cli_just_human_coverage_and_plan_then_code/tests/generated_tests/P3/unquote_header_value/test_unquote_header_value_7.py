from requests.utils import unquote_header_value

def test_unquote_header_incomplete_quotes():
    assert unquote_header_value('"value') == '"value'
    assert unquote_header_value('value"') == 'value"'
