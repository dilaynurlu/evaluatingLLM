from requests.utils import _parse_content_type_header

def test_parse_content_type_irregular_semicolons_and_whitespace():
    """
    Test robustness against extra semicolons (empty tokens) and irregular whitespace.
    """
    header = " image/png ;  ; key = value ;;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "image/png"
    assert params == {"key": "value"}