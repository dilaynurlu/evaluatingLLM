from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted():
    header = "text/html; title=\"Hello World\"; author='Me'"
    # Code strips " ' and space from value
    expected = ("text/html", {"title": "Hello World", "author": "Me"})
    assert _parse_content_type_header(header) == expected

