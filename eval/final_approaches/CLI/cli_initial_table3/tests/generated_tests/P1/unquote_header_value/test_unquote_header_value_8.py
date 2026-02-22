from requests.utils import unquote_header_value

def test_unquote_header_value_mixed_quotes():
    """Test strings with mismatched quotes."""
    assert unquote_header_value('"test') == '"test'
    assert unquote_header_value('test"') == 'test"'
