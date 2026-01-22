from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_values():
    """
    Test that single and double quotes around parameter values are stripped correctly.
    """
    header = "multipart/form-data; boundary=\"boundary_string\"; param='single_quoted'"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {
        "boundary": "boundary_string",
        "param": "single_quoted"
    }