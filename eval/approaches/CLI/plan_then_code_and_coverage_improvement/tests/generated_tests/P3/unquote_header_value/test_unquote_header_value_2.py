from requests.utils import unquote_header_value

def test_unquote_header_value_2():
    # Unquoted
    val = "foo"
    assert unquote_header_value(val) == "foo"