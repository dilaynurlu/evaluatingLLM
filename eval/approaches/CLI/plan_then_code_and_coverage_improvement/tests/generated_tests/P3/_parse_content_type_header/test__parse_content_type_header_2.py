from requests.utils import _parse_content_type_header

def test__parse_content_type_header_2():
    # With parameters
    ct, params = _parse_content_type_header("text/html; charset=utf-8; foo=bar")
    assert ct == "text/html"
    assert params["charset"] == "utf-8"
    assert params["foo"] == "bar"