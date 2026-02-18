from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitive_keys():
    header = "text/html; CharSet=UTF-8"
    # Keys are lowercased, values are preserved (but stripped)
    expected = ("text/html", {"charset": "UTF-8"})
    assert _parse_content_type_header(header) == expected
