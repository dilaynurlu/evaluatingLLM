from requests.utils import _parse_content_type_header

def test_parse_content_type_multiple_parameters():
    header = "multipart/form-data; boundary=ExampleBoundary; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params["boundary"] == "ExampleBoundary"
    assert params["charset"] == "utf-8"
    assert len(params) == 2