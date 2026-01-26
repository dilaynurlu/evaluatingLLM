from requests.utils import _parse_content_type_header

def test_parse_content_type_case_sensitivity():
    # Keys should be lowercased, but content-type and values should preserve case
    header = "TEXT/HTML; CharSet=UTF-8"
    result = _parse_content_type_header(header)
    assert result == ("TEXT/HTML", {"charset": "UTF-8"})