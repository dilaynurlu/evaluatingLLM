from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitivity():
    """
    Test that parameter keys are normalized to lowercase, 
    while parameter values preserve their case.
    """
    header = "application/x-www-form-urlencoded; CharSet=UTF-8; Foo=Bar"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/x-www-form-urlencoded"
    
    assert "charset" in params
    assert params["charset"] == "UTF-8"
    assert "foo" in params
    assert params["foo"] == "Bar"