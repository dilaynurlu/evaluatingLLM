import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_extra_whitespace():
    """
    Test parsing headers with irregular whitespace around delimiters.
    Refined to test various whitespace characters (tabs).
    """
    header = "  application/javascript  ;  version =  1.5  "
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/javascript"
    assert params == {'version': '1.5'}

    # Refinement: Tabs and mixed whitespace
    header_tabs = "\tapplication/json\t;\tcharset\t=\tutf-8\t"
    ct, p_tabs = _parse_content_type_header(header_tabs)
    assert ct == "application/json"
    assert p_tabs == {'charset': 'utf-8'}