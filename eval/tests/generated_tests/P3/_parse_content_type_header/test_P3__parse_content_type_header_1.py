from requests.utils import _parse_content_type_header

def test_parse_content_type_header_simple_no_params():
    # Refined: Covers simple valid type and empty input robustness
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/json"
    assert params == {}

    # Test empty string input handling (Critique: Empty Inputs)
    content_type_empty, params_empty = _parse_content_type_header("")
    # Implementation dependent: usually returns empty string and empty dict
    assert content_type_empty == ""
    assert params_empty == {}