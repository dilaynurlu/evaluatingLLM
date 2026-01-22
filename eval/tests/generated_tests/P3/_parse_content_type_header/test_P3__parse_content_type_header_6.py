import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_value_containing_equals():
    """
    Test parsing a parameter value that contains an equals sign.
    Refined to include a stress test with a larger header (DoS protection check).
    """
    header = "text/html; url=http://example.com/foo?bar=baz"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {'url': 'http://example.com/foo?bar=baz'}

    # Refinement: Large input (DoS)
    # Ensure linear processing time or at least no recursion depth errors.
    # We create a header with 1000 parameters.
    large_header = "text/plain; " + "; ".join([f"p{i}=v{i}" for i in range(1000)])
    ct, p_large = _parse_content_type_header(large_header)
    assert ct == "text/plain"
    assert len(p_large) == 1000
    assert p_large['p999'] == 'v999'