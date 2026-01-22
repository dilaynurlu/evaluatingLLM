from requests.utils import _parse_content_type_header

def test__parse_content_type_header_4():
    # Case insensitivity for keys, but value preservation?
    # Code: params_dict[key.lower()] = value
    ct, params = _parse_content_type_header("text/plain; CHARSET=UTF-8")
    assert ct == "text/plain"
    assert "charset" in params
    assert params["charset"] == "UTF-8"
