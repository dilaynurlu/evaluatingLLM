from requests.utils import unquote_header_value

def test_unquote_header_quotes_in_middle():
    assert unquote_header_value('va"lue') == 'va"lue'
