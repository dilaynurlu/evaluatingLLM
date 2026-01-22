from requests.utils import _parse_content_type_header

def test__parse_content_type_header_7():
    # Parameter without equals
    ct, params = _parse_content_type_header("text/html; foo")
    # Code: index_of_equals = param.find("=")
    # if -1: key=param, value=True
    assert ct == "text/html"
    assert params["foo"] is True
