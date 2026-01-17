from requests.utils import unquote_header_value

def test_unquote_header_escaped_backslash():
    assert unquote_header_value("""val\\ue""") == 'val\\ue'
