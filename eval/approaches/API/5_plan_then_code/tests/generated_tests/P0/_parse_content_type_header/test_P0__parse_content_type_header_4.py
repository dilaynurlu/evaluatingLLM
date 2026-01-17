from requests.utils import _parse_content_type_header

def test_parse_content_type_flags():
    """Test parameters without values (no equals sign) are treated as boolean flags."""
    header = "multipart/form-data; boundary=----------123; immutable"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {
        "boundary": "----------123",
        "immutable": True
    }