from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_value_parameter():
    # Tests a parameter with an equals sign but no value
    header = "text/html; foo="
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {"foo": ""}