from requests.utils import unquote_header_value

def test_unquote_header_value_3():
    # Filename handling (escaped quotes)
    val = '"foo\"bar"'
    # "foo"bar" -> foo"bar
    assert unquote_header_value(val) == 'foo"bar'

