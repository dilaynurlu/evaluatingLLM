from requests.utils import _parse_content_type_header

def test_parse_content_type_boolean_parameter():
    # Tests a parameter with no equals sign (flag-style)
    header = "text/html; secure"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {"secure": True}