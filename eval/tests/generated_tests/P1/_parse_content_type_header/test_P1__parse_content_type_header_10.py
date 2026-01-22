from requests.utils import _parse_content_type_header

def test_parse_content_type_stripping_quotes_and_spaces():
    # Single quotes and surrounding spaces should be stripped from keys/values
    # Note: items_to_strip = "\"' " which includes space, single quote, double quote
    header = "application/javascript; ' version ' = ' 1.0 '"
    result = _parse_content_type_header(header)
    assert result == ("application/javascript", {"version": "1.0"})