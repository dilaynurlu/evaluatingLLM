from requests.utils import unquote_header_value

def test_unquote_basic_string():
    """Test unquoting a simple string surrounded by double quotes."""
    input_val = '"simple_value"'
    # Should strip quotes
    assert unquote_header_value(input_val) == "simple_value"