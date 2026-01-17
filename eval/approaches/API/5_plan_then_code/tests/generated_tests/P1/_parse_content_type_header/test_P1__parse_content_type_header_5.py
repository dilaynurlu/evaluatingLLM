from requests.utils import _parse_content_type_header

def test_parse_content_type_case_sensitivity():
    """Test that parameter keys are normalized to lowercase while values preserve their case."""
    header = "text/html; CharSet=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "UTF-8"}