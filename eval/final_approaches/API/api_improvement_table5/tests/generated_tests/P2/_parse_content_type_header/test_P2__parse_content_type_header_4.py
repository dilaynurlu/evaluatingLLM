from requests.utils import _parse_content_type_header

def test_parse_content_type_boolean_parameters():
    """
    Test parameters that do not contain an equals sign.
    These should be parsed as keys with the boolean value True.
    """
    header = "text/plain; is_secure; check_feature"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {
        "is_secure": True,
        "check_feature": True
    }