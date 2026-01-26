from requests.utils import _parse_content_type_header

def test_content_type_empty_param_value():
    # Scenario: Parameter key present with equals sign but no value
    header = "text/csv; header="
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/csv"
    assert params == {"header": ""}