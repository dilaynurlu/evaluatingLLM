from requests.utils import _parse_content_type_header

def test__parse_content_type_header_empty_params():
    """
    Test parsing with empty parameter sections (multiple semicolons).
    """
    header = "text/plain; ; charset=utf-8;;"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params["charset"] == "utf-8"
