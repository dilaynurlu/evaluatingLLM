from requests.utils import unquote_header_value

def test_unquote_header_value_3():
    val = '"quoted\"quote"'
    assert unquote_header_value(val) == 'quoted"quote'
