from requests.utils import _parse_content_type_header

def test_parse_content_type_header_4():
    header = 'text/html; charset="utf-8"; title="Foo Bar"'
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params["charset"] == "utf-8"
    assert params["title"] == "Foo Bar"
