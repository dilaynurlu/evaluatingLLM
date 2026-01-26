from requests.utils import _parse_content_type_header

def test_content_type_mixed_flags_and_values():
    # Scenario: A mix of key-value parameters and flag parameters in the same header
    header = "application/pdf; secure; version=1.7"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/pdf"
    assert params == {"secure": True, "version": "1.7"}