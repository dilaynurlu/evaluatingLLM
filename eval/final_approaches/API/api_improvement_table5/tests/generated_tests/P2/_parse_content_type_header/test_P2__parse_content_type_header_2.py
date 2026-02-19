from requests.utils import _parse_content_type_header

def test_parse_content_type_simple_no_params():
    """
    Test a simple content type header with no parameters.
    Verifies that the function handles strings without semicolons correctly,
    returning an empty dictionary for parameters.
    """
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params == {}