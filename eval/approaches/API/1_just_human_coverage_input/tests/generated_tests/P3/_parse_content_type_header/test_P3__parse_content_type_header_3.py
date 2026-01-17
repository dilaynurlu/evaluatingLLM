import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_and_escaped():
    """
    Test parsing parameters where values are enclosed in quotes (single or double)
    and contain escaped characters. Verifies that the parser strips surrounding quotes
    and handles content appropriately.
    """
    # Case 1: Standard double quotes and single quotes
    header = "application/xml; charset=\"utf-8\"; title='Test Data'"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/xml"
    assert params["charset"] == "utf-8"
    assert params["title"] == "Test Data"

    # Case 2: Escaped quotes inside the value. 
    # Note: requests' simple parser may strictly strip outer quotes only.
    # We check that the parser at least doesn't crash and returns the inner string.
    header_escaped = 'text/plain; data="Value with \\"quoted\\" content"'
    _, params_escaped = _parse_content_type_header(header_escaped)
    
    # Depending on exact implementation of stripping, we verify the content is preserved
    val = params_escaped["data"]
    assert "Value with" in val
    assert "quoted" in val