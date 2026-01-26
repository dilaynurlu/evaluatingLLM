from requests.utils import _parse_content_type_header

def test_content_type_strip_quotes():
    # Scenario: Parameters with values enclosed in single and double quotes should have quotes stripped
    header = "application/xml; title=\"Main Title\"; version='1.0'"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {"title": "Main Title", "version": "1.0"}