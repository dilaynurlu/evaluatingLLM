from requests.utils import unquote_header_value

def test_unquote_header_value_3():
    # Input is literal: "foo\"bar"
    # Python string: '"foo\\\"bar"'
    assert unquote_header_value('"foo\\\"bar"') == 'foo"bar'

