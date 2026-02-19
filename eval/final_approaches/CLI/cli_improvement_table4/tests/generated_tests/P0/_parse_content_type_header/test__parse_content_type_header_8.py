from requests.utils import _parse_content_type_header

def test_parse_content_type_header_8():
    # Test invalid parameters (no equals sign)
    header = "text/html; invalid-param; charset=utf-8"
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params["charset"] == "utf-8"
    # invalid-param is skipped or treated as key with value True?
    # Code:
    # key, value = param, True
    # index_of_equals = param.find("=")
    # if index_of_equals != -1: ... else ...
    # params_dict[key.lower()] = value
    assert params["invalid-param"] is True
