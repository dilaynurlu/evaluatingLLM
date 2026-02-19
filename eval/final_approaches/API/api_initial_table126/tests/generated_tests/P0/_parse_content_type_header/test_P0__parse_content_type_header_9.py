from requests.utils import _parse_content_type_header

def test_parse_content_type_case_sensitivity():
    # Tests that keys are lowercased but values preserve case
    header = "TEXT/html; CHARSET=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    # Note: The implementation does not force lowercase on content_type, only on parameter keys
    assert content_type == "TEXT/html"
    assert params == {"charset": "UTF-8"}