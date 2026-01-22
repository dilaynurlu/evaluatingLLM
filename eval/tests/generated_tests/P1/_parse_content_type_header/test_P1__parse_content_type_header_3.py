from requests.utils import _parse_content_type_header

def test_parse_content_type_with_quoted_parameter():
    # Quotes should be stripped from the value
    header = 'application/atom+xml; type="entry"'
    result = _parse_content_type_header(header)
    assert result == ("application/atom+xml", {"type": "entry"})