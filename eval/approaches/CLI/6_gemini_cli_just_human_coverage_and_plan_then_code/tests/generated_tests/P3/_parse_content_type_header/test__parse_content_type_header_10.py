from requests.utils import _parse_content_type_header

def test_parse_content_type_mixed_quotes_spacing():
    header = " application/json ;  version = \" 1.0 \" ; format=compact "
    ct, params = _parse_content_type_header(header)
    assert ct == "application/json"
    assert params == {"version": "1.0", "format": "compact"}

