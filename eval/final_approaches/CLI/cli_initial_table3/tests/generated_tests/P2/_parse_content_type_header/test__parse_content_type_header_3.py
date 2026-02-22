from requests.utils import _parse_content_type_header

def test__parse_content_type_header_quoted_and_spaces():
    """
    Test parsing content-type with quoted values and extra spaces.
    """
    header = ' multipart/form-data ; boundary="foo bar" ; charset = "utf-8" '
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "foo bar", "charset": "utf-8"}
