from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitivity():
    """Test that parameter keys are case-insensitive (lowercased), but values preserve case."""
    header = "TEXT/HTML; CharSet=UTF-8; Version=1.0"
    content_type, params = _parse_content_type_header(header)
    
    # content_type is NOT lowercased by this function, only stripped
    assert content_type == "TEXT/HTML"
    # Keys are lowercased, values are not
    assert params == {
        "charset": "UTF-8",
        "version": "1.0"
    }