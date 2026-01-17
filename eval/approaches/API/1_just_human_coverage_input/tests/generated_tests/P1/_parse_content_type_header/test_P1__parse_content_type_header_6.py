from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitivity():
    """
    Test that parameter keys are case-insensitive (converted to lowercase),
    while parameter values preserve their case.
    """
    header = "text/html; CharSet=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Key 'CharSet' should become 'charset', value 'UTF-8' should remain 'UTF-8'
    assert params == {"charset": "UTF-8"}