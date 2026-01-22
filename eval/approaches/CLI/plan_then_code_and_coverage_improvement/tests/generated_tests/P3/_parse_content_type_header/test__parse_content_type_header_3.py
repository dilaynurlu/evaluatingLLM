from requests.utils import _parse_content_type_header

def test__parse_content_type_header_3():
    # Quoted values
    ct, params = _parse_content_type_header('application/json; title="Parsing Content"')
    assert ct == "application/json"
    assert params["title"] == "Parsing Content"