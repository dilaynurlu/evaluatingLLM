from requests.utils import _parse_content_type_header

def test_parse_content_type_header_7():
    # Test parameters with whitespace
    header = "text/html ; charset = utf-8 ; foo = bar "
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params["charset"] == "utf-8"
    assert params["foo"] == "bar"
