from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitivity():
    """
    Test that parameter keys are normalized to lowercase, but parameter values preserve their case.
    """
    header = "application/xml; CharSet=UTF-8; VERSION=1.0"
    expected_content_type = "application/xml"
    expected_params = {
        "charset": "UTF-8",
        "version": "1.0"
    }
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params