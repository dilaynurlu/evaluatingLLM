from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """Test a string that is not quoted remains unchanged."""
    assert unquote_header_value('test') == 'test'
