import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_with_charset():
    """
    Test parsing a content type header that includes a charset parameter.
    Refined to test duplicate parameter keys (HTTP Parameter Pollution).
    """
    # Standard case
    header = "text/html; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {'charset': 'utf-8'}

    # Refinement: Duplicate keys. 
    # Logic usually overwrites previous keys. Verifying 'last-wins' behavior.
    header_dupe = "text/html; charset=utf-8; charset=iso-8859-1"
    content_type_d, params_d = _parse_content_type_header(header_dupe)
    assert content_type_d == "text/html"
    assert params_d == {'charset': 'iso-8859-1'}