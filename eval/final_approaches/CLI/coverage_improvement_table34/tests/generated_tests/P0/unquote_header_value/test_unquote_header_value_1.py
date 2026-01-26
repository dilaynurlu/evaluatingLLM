from requests.utils import unquote_header_value

def test_unquote_header_value_1():
    val = "simple"
    assert unquote_header_value(val) == "simple"
