import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_values():
    """
    Test that quotes (double quotes) are stripped from parameter values.
    Refined to test that internal quotes or escaped characters are preserved
    relative to the stripping logic (naive stripping only removes outer quotes).
    """
    # Naive parser strips outer quotes but preserves internal escaped quotes
    header = 'application/xml; title="foo\\"bar"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {"title": 'foo\\"bar'}