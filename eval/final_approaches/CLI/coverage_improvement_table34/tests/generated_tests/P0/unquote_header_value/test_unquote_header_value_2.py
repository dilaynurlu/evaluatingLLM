from requests.utils import unquote_header_value

def test_unquote_header_value_2():
    val = '"quoted"'
    assert unquote_header_value(val) == "quoted"
