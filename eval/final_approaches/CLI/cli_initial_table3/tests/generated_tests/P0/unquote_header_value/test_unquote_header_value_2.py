from requests.utils import unquote_header_value

def test_unquote_header_value_2():
    assert unquote_header_value('foo') == 'foo'
