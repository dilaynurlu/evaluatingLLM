import pytest
from requests.utils import unquote_header_value

@pytest.mark.parametrize("input_val", [
    'my-value',
    "'my-value'",       # Single quotes should NOT be treated as delimiters
    "'quoted'",
    'key="value"'       # String containing quotes but not wrapped in them
])
def test_unquote_header_value_no_unquoting(input_val):
    """
    Test that strings not enclosed in double quotes are returned as-is.
    
    Addresses critique:
    - Single Quotes: Verifies strict adherence to RFC (only double quotes are delimiters).
    """
    assert unquote_header_value(input_val) == input_val