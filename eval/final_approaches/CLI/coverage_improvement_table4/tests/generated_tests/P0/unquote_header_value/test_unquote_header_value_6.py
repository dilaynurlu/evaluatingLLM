from requests.utils import unquote_header_value

def test_unquote_header_value_6():
    # Test string with no quotes
    val = "noquotes"
    assert unquote_header_value(val) == "noquotes"
