from requests.utils import _parse_content_type_header

def test__parse_content_type_header_6():
    # Parameter with empty value?
    ct, params = _parse_content_type_header("text/html; charset=")
    assert ct == "text/html"
    # charset= means value is empty string? Or ignored?
    # Code: if param: ...
    # if "charset=" is split by "=", key="charset", value=""
    # value is stripped of quotes/spaces.
    assert params.get("charset") == ""
