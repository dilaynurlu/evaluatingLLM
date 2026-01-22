import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_simple_no_params():
    """
    Test parsing a simple content type header with no parameters.
    Refined to include trailing delimiters which technically imply missing segments.
    """
    header = "application/json"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/json"
    assert params == {}

    # Refinement: Trailing semicolon behavior (empty segment at end)
    header_trailing = "application/json;"
    content_type_t, params_t = _parse_content_type_header(header_trailing)
    assert content_type_t == "application/json"
    assert params_t == {}