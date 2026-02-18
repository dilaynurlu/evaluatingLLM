from requests.utils import unquote_header_value

def test_unquote_header_value_4():
    val = '"back\\slash"'
    assert unquote_header_value(val) == "back\slash"
