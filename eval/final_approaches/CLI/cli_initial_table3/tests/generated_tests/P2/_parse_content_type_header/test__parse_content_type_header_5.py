from requests.utils import _parse_content_type_header

def test__parse_content_type_header_no_equals():
    """
    Test parsing where a parameter has no value.
    """
    header = "text/plain; no-value-param; other=value"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params["no-value-param"] is True
    assert params["other"] == "value"
