from requests.utils import unquote_header_value

def test_unquote_header_value_basic():
    """Test basic unquoting of a string."""
    assert unquote_header_value('"test"') == 'test'
