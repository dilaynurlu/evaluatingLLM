from requests.utils import _parse_content_type_header

def test_parse_content_type_single_quoted_parameter():
    header = "application/atom+xml; type='entry'"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/atom+xml"
    assert params == {"type": "entry"}