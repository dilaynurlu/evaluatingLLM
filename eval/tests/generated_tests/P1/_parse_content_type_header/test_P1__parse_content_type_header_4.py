from requests.utils import _parse_content_type_header

def test_parse_content_type_standalone_parameter():
    # Parameter without equals sign becomes True
    header = "text/html; prevent-caching"
    result = _parse_content_type_header(header)
    assert result == ("text/html", {"prevent-caching": True})