from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitive_keys():
    """
    Test that parameter keys are case-insensitive and converted to lowercase.
    """
    header = "text/html; CharSet=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    # Key should be lowercased, value preserves case
    assert params == {'charset': 'UTF-8'}