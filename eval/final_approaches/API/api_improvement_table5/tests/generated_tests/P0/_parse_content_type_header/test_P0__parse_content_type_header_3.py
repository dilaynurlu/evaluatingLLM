from requests.utils import _parse_content_type_header

def test_content_type_params_flags_no_equals():
    header = "text/plain; foo; bar"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {"foo": True, "bar": True}