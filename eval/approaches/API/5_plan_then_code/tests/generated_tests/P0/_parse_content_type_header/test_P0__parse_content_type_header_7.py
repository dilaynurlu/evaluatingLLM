from requests.utils import _parse_content_type_header

def test_parse_content_type_equals_in_value():
    """Test that parameter values can contain equals signs."""
    # The function splits only on the first '=' found in the parameter token
    header = "application/x-www-form-urlencoded; key=val=ue"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/x-www-form-urlencoded"
    assert params == {"key": "val=ue"}