from requests.utils import _parse_content_type_header

def test__parse_content_type_header_case_insensitivity():
    """
    Test that parameter keys are lower-cased but values are not.
    """
    header = "application/json; CharSet=UTF-8; VERSION=1.0"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params["charset"] == "UTF-8"
    assert params["version"] == "1.0"
