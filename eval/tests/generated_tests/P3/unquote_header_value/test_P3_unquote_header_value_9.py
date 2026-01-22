from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    """Test that strings with mismatched or partial quotes are returned as-is."""
    # Case 1: Start quote only
    val1 = '"foo'
    assert unquote_header_value(val1) == '"foo'
    
    # Case 2: End quote only
    val2 = 'foo"'
    assert unquote_header_value(val2) == 'foo"'

    # Case 3: Quote in the middle
    val3 = 'foo"bar'
    assert unquote_header_value(val3) == 'foo"bar'

    # Case 4: Mismatched structure "foo
    val4 = '"foo'
    assert unquote_header_value(val4) == '"foo'