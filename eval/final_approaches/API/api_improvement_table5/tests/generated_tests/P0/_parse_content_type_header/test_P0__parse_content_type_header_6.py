from requests.utils import _parse_content_type_header

def test_content_type_case_sensitivity():
    # Scenario: Parameter keys should be lowercased; values and content-type case should be preserved
    header = "Audio/MPEG; RATE=128k"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "Audio/MPEG"
    assert params == {"rate": "128k"}